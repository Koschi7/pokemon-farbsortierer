import os
from dotenv import load_dotenv

load_dotenv("config.env")


def get_default_generations() -> list[int]:
    raw = os.getenv("GENERATIONS", "1")
    return [int(g.strip()) for g in raw.split(",") if g.strip().isdigit()]


DATABASE_URL = "sqlite+aiosqlite:///pokemon.db"
POKEAPI_BASE = "https://pokeapi.co/api/v2"
