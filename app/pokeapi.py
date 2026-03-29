import asyncio
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import POKEAPI_BASE
from app.models import Pokemon, PokemonType


# PokéAPI type names → German translations
TYPE_TRANSLATIONS = {
    "normal": "Normal",
    "fire": "Feuer",
    "water": "Wasser",
    "electric": "Elektro",
    "grass": "Pflanze",
    "ice": "Eis",
    "fighting": "Kampf",
    "poison": "Gift",
    "ground": "Boden",
    "flying": "Flug",
    "psychic": "Psycho",
    "bug": "Käfer",
    "rock": "Gestein",
    "ghost": "Geist",
    "dragon": "Drache",
    "dark": "Unlicht",
    "steel": "Stahl",
    "fairy": "Fee",
}

COLOR_TRANSLATIONS = {
    "black": "Schwarz",
    "blue": "Blau",
    "brown": "Braun",
    "gray": "Grau",
    "green": "Grün",
    "pink": "Rosa",
    "purple": "Lila",
    "red": "Rot",
    "white": "Weiß",
    "yellow": "Gelb",
}


async def fetch_generation_pokemon(client: httpx.AsyncClient, gen: int) -> list[dict]:
    """Fetch all Pokémon IDs belonging to a generation."""
    resp = await client.get(f"{POKEAPI_BASE}/generation/{gen}", timeout=30)
    resp.raise_for_status()
    data = resp.json()
    species_list = data["pokemon_species"]
    return [{"name": s["name"], "url": s["url"]} for s in species_list]


async def fetch_species(client: httpx.AsyncClient, species_name: str) -> dict | None:
    """Fetch species data including German name, color, generation, evolution chain."""
    try:
        resp = await client.get(f"{POKEAPI_BASE}/pokemon-species/{species_name}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return None


async def fetch_pokemon(client: httpx.AsyncClient, pokemon_id: int) -> dict | None:
    """Fetch Pokémon data (types, height, weight, sprites)."""
    try:
        resp = await client.get(f"{POKEAPI_BASE}/pokemon/{pokemon_id}", timeout=30)
        resp.raise_for_status()
        return resp.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return None


async def fetch_evolution_chain(client: httpx.AsyncClient, url: str) -> dict | None:
    """Fetch evolution chain data."""
    try:
        resp = await client.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except (httpx.HTTPStatusError, httpx.RequestError):
        return None


def extract_german_name(species_data: dict) -> str:
    for name_entry in species_data.get("names", []):
        if name_entry["language"]["name"] == "de":
            return name_entry["name"]
    return species_data["name"].capitalize()


def parse_evolution_chain(chain: dict) -> dict[str, int | None]:
    """Parse evolution chain into a mapping of species_name → evolves_from species_name."""
    result = {}

    def walk(node, parent_name=None):
        species_name = node["species"]["name"]
        result[species_name] = parent_name
        for evo in node.get("evolves_to", []):
            walk(evo, species_name)

    walk(chain["chain"])
    return result


async def seed_generation(session: AsyncSession, gen: int, progress_callback=None):
    """Fetch and store all Pokémon for a given generation."""
    async with httpx.AsyncClient() as client:
        species_list = await fetch_generation_pokemon(client, gen)
        total = len(species_list)

        # Collect all evolution chain URLs and species data first
        evolution_map = {}  # species_name → evolves_from_species_name
        semaphore = asyncio.Semaphore(5)  # rate limit

        async def process_pokemon(species_info, index):
            async with semaphore:
                species_name = species_info["name"]
                species_data = await fetch_species(client, species_name)
                if not species_data:
                    return

                pokemon_id = species_data["id"]
                pokemon_data = await fetch_pokemon(client, pokemon_id)
                if not pokemon_data:
                    return

                # Get evolution chain
                evo_url = species_data.get("evolution_chain", {}).get("url")
                if evo_url and evo_url not in evolution_map:
                    evo_data = await fetch_evolution_chain(client, evo_url)
                    if evo_data:
                        chain_map = parse_evolution_chain(evo_data)
                        evolution_map.update(chain_map)

                german_name = extract_german_name(species_data)
                color = species_data["color"]["name"]
                height = pokemon_data["height"] / 10  # decimetres → meters
                weight = pokemon_data["weight"] / 10  # hectograms → kg
                types = [t["type"]["name"] for t in pokemon_data["types"]]

                artwork_url = (
                    pokemon_data.get("sprites", {})
                    .get("other", {})
                    .get("official-artwork", {})
                    .get("front_default", "")
                )
                sprite_url = pokemon_data.get("sprites", {}).get("front_default", "")

                pokemon = Pokemon(
                    id=pokemon_id,
                    name=species_name,
                    german_name=german_name,
                    color=color,
                    height=height,
                    weight=weight,
                    generation=gen,
                    sprite_url=sprite_url or "",
                    artwork_url=artwork_url or "",
                )
                for type_name in types:
                    pokemon.types.append(PokemonType(type_name=type_name))

                session.add(pokemon)

                if progress_callback:
                    progress_callback(index + 1, total, german_name)

        tasks = [process_pokemon(s, i) for i, s in enumerate(species_list)]
        await asyncio.gather(*tasks)

        # Now update evolves_from_id based on evolution chains
        await session.flush()
        for species_name, from_name in evolution_map.items():
            if from_name is None:
                continue
            # Find both Pokémon in current session
            from sqlalchemy import select
            result = await session.execute(
                select(Pokemon).where(Pokemon.name == species_name)
            )
            poke = result.scalar_one_or_none()
            result2 = await session.execute(
                select(Pokemon).where(Pokemon.name == from_name)
            )
            from_poke = result2.scalar_one_or_none()
            if poke and from_poke:
                poke.evolves_from_id = from_poke.id

        await session.commit()
