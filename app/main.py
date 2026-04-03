import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import init_db, get_session
from app.models import Pokemon, PokemonType, Setting
from app.config import get_default_generations
from app.pokeapi import COLOR_TRANSLATIONS, TYPE_TRANSLATIONS, seed_generation
from app.tts import generate_audio, generate_size_audio, PRONUNCIATION

# In-memory seed status tracking
_seed_status: dict = {"running": False, "done": False}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


async def get_active_generations(session: AsyncSession) -> list[int]:
    result = await session.execute(select(Setting).where(Setting.key == "generations"))
    setting = result.scalar_one_or_none()
    if setting:
        return [int(g) for g in setting.value.split(",") if g.strip().isdigit()]
    return get_default_generations()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "colors": COLOR_TRANSLATIONS,
        "types": TYPE_TRANSLATIONS,
    })


@app.get("/pokemon", response_class=HTMLResponse)
async def pokemon_grid(
    request: Request,
    filter: str = "color",
    value: str = "",
    session: AsyncSession = Depends(get_session),
):
    generations = await get_active_generations(session)
    query = (
        select(Pokemon)
        .options(selectinload(Pokemon.types))
        .where(Pokemon.generation.in_(generations))
    )

    if filter == "color" and value:
        query = query.where(Pokemon.color == value)
    elif filter == "type" and value:
        query = query.where(
            Pokemon.id.in_(
                select(PokemonType.pokemon_id).where(PokemonType.type_name == value)
            )
        )

    query = query.order_by(Pokemon.id)
    result = await session.execute(query)
    pokemon_list = result.scalars().all()

    return templates.TemplateResponse("partials/grid.html", {
        "request": request,
        "pokemon_list": pokemon_list,
        "type_translations": TYPE_TRANSLATIONS,
    })


@app.get("/pokemon/{pokemon_id}", response_class=HTMLResponse)
async def pokemon_detail(
    request: Request,
    pokemon_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.id == pokemon_id)
    )
    pokemon = result.scalar_one_or_none()
    if not pokemon:
        return HTMLResponse("<p>Pokémon nicht gefunden</p>", status_code=404)

    generations = await get_active_generations(session)

    # Get evolution chain (only from active generations)
    evolutions = []

    # Find the base of the chain by walking up evolves_from
    base = pokemon
    while base.evolves_from_id:
        result = await session.execute(
            select(Pokemon).options(selectinload(Pokemon.types)).where(
                Pokemon.id == base.evolves_from_id,
                Pokemon.generation.in_(generations),
            )
        )
        parent = result.scalar_one_or_none()
        if parent:
            base = parent
        else:
            break

    # Now walk down the chain from base
    async def get_chain(poke):
        evolutions.append(poke)
        result = await session.execute(
            select(Pokemon)
            .options(selectinload(Pokemon.types))
            .where(
                Pokemon.evolves_from_id == poke.id,
                Pokemon.generation.in_(generations),
            )
            .order_by(Pokemon.id)
        )
        children = result.scalars().all()
        for child in children:
            await get_chain(child)

    await get_chain(base)

    return templates.TemplateResponse("partials/detail.html", {
        "request": request,
        "pokemon": pokemon,
        "evolutions": evolutions,
        "type_translations": TYPE_TRANSLATIONS,
    })


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    active_gens = await get_active_generations(session)
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "active_generations": active_gens,
        "all_generations": list(range(1, 10)),
    })


@app.post("/settings", response_class=HTMLResponse)
async def save_settings(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    form = await request.form()
    selected = [int(k.replace("gen_", "")) for k in form.keys() if k.startswith("gen_")]

    if not selected:
        selected = [1]

    gen_str = ",".join(str(g) for g in sorted(selected))

    result = await session.execute(select(Setting).where(Setting.key == "generations"))
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = gen_str
    else:
        session.add(Setting(key="generations", value=gen_str))
    await session.commit()

    return RedirectResponse(url="/settings", status_code=303)


async def _reseed_in_background(generations: list[int]):
    """Re-seed data and generate audio in the background with its own session."""
    from app.database import async_session

    _seed_status["running"] = True
    _seed_status["done"] = False
    try:
        async with async_session() as session:
            for gen in generations:
                pokemon_ids = (await session.execute(
                    select(Pokemon.id).where(Pokemon.generation == gen)
                )).scalars().all()

                if pokemon_ids:
                    await session.execute(
                        delete(PokemonType).where(PokemonType.pokemon_id.in_(pokemon_ids))
                    )
                    await session.execute(delete(Pokemon).where(Pokemon.generation == gen))
                await session.commit()

                await seed_generation(session, gen)

            # Generate audio
            result = await session.execute(select(Pokemon).order_by(Pokemon.id))
            all_pokemon = result.scalars().all()
            for poke in all_pokemon:
                force = poke.german_name in PRONUNCIATION
                await generate_audio(poke.german_name, poke.id, force=force)
                await generate_size_audio(poke.size_description_spoken, poke.id, force=True)
    finally:
        _seed_status["running"] = False
        _seed_status["done"] = True


@app.post("/settings/seed", response_class=HTMLResponse)
async def reseed_data(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    generations = await get_active_generations(session)

    # Run seeding + audio generation in background so the request returns immediately
    asyncio.create_task(_reseed_in_background(generations))

    # If called via HTMX, return the polling banner directly
    if request.headers.get("HX-Request"):
        return HTMLResponse(
            '<div id="seed-status" class="seed-banner running" '
            'hx-get="/settings/seed-status" hx-trigger="every 2s" hx-swap="outerHTML">'
            '⏳ Daten werden geladen…</div>'
        )
    return RedirectResponse(url="/settings", status_code=303)


@app.get("/settings/seed-status", response_class=HTMLResponse)
async def seed_status(request: Request):
    if _seed_status["running"]:
        return HTMLResponse(
            '<div id="seed-status" class="seed-banner running" '
            'hx-get="/settings/seed-status" hx-trigger="every 2s" hx-swap="outerHTML">'
            '⏳ Daten werden geladen…</div>'
        )
    if _seed_status["done"]:
        _seed_status["done"] = False
        return HTMLResponse(
            '<div id="seed-status" class="seed-banner done">'
            '✅ Fertig! Alle Daten und Audiodateien wurden generiert.</div>'
        )
    return HTMLResponse('<div id="seed-status"></div>')
