#!/usr/bin/env python3
"""Seed script: fetches Pokemon data from PokeAPI and stores it in SQLite."""

import asyncio
import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete, select

from app.config import DATABASE_URL, get_default_generations
from app.models import Base, Pokemon, PokemonType, Setting
from app.pokeapi import seed_generation
from app.tts import generate_audio, generate_size_audio, PRONUNCIATION
from app.i18n import get_size_description_spoken


async def main():
    generations = get_default_generations()
    if "--generations" in sys.argv:
        idx = sys.argv.index("--generations")
        if idx + 1 < len(sys.argv):
            generations = [int(g) for g in sys.argv[idx + 1].split(",")]

    print(f"Seeding generations: {generations}")

    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Clear existing data for these generations
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

        for gen in generations:
            print(f"\n--- Generation {gen} ---")

            def progress(current, total, name):
                print(f"  [{current}/{total}] {name}")

            await seed_generation(session, gen, progress_callback=progress)
            print(f"Generation {gen} done!")

        # Save generations setting
        result = await session.execute(select(Setting).where(Setting.key == "generations"))
        setting = result.scalar_one_or_none()
        gen_str = ",".join(str(g) for g in generations)
        if setting:
            setting.value = gen_str
        else:
            session.add(Setting(key="generations", value=gen_str))
        await session.commit()

    # Generate TTS audio files for both languages
    async with async_session() as session:
        result = await session.execute(select(Pokemon).order_by(Pokemon.id))
        all_pokemon = result.scalars().all()
        total = len(all_pokemon)

        for lang_code in ("de", "en"):
            print(f"\n--- Audio [{lang_code.upper()}] ---")
            for i, poke in enumerate(all_pokemon):
                name = poke.german_name if lang_code == "de" else poke.name.title()
                force = (lang_code == "de" and poke.german_name in PRONUNCIATION)
                await generate_audio(name, poke.id, lang=lang_code, force=force)
                spoken = get_size_description_spoken(poke.height, lang_code)
                await generate_size_audio(spoken, poke.id, lang=lang_code, force=True)
                hint = f" (-> {PRONUNCIATION[poke.german_name]})" if force else ""
                print(f"  [{i+1}/{total}] Audio: {name}{hint}")

    await engine.dispose()
    print("\nDone! Database and audio files have been created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
