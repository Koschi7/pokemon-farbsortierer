import asyncio
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import init_db, get_session, async_session
from app.models import Pokemon, PokemonType, Favorite, Setting
from app.config import get_default_generations
from app.pokeapi import COLOR_TRANSLATIONS, TYPE_TRANSLATIONS, seed_generation
from app.tts import generate_audio, generate_size_audio, PRONUNCIATION

# In-memory seed status tracking
_seed_status: dict = {
    "running": False,
    "done": False,
    "error": "",       # error message if failed
    "phase": "",       # "start", "seed" or "audio"
    "current": 0,
    "total": 0,
    "detail": "",      # e.g. Pokemon name or generation
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/sw.js")
async def service_worker():
    return FileResponse("app/static/sw.js", media_type="application/javascript")


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
    q: str = "",
    session: AsyncSession = Depends(get_session),
):
    generations = await get_active_generations(session)
    query = (
        select(Pokemon)
        .options(selectinload(Pokemon.types))
        .where(Pokemon.generation.in_(generations))
    )

    if filter == "favorites":
        fav_ids = (await session.execute(select(Favorite.pokemon_id))).scalars().all()
        if not fav_ids:
            return HTMLResponse('<p class="hint">Noch keine Favoriten!</p>')
        query = query.where(Pokemon.id.in_(fav_ids))
    elif filter == "search":
        if not q.strip():
            return HTMLResponse('<p class="hint">Tippe einen Namen ein!</p>')
        search_term = f"%{q.strip()}%"
        query = query.where(Pokemon.german_name.ilike(search_term))
    elif filter == "color" and value:
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

    # Check if favorited
    fav = await session.execute(select(Favorite).where(Favorite.pokemon_id == pokemon_id))
    is_favorite = fav.scalar_one_or_none() is not None

    return templates.TemplateResponse("partials/detail.html", {
        "request": request,
        "pokemon": pokemon,
        "evolutions": evolutions,
        "type_translations": TYPE_TRANSLATIONS,
        "is_favorite": is_favorite,
    })


@app.post("/pokemon/{pokemon_id}/favorite", response_class=HTMLResponse)
async def toggle_favorite(
    request: Request,
    pokemon_id: int,
    session: AsyncSession = Depends(get_session),
):
    fav = await session.execute(select(Favorite).where(Favorite.pokemon_id == pokemon_id))
    existing = fav.scalar_one_or_none()
    if existing:
        await session.delete(existing)
        is_favorite = False
    else:
        session.add(Favorite(pokemon_id=pokemon_id))
        is_favorite = True
    await session.commit()

    heart = "❤️" if is_favorite else "🤍"
    return HTMLResponse(
        f'<button class="fav-btn {"fav-active" if is_favorite else ""}" '
        f'hx-post="/pokemon/{pokemon_id}/favorite" hx-swap="outerHTML">'
        f'{heart}</button>'
    )


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

    logger.info("Background seed started for generations: %s", generations)
    try:
        async with async_session() as session:
            for gen in generations:
                logger.info("Seeding generation %d", gen)
                _seed_status.update(phase="seed", detail=f"Generation {gen}")

                pokemon_ids = (await session.execute(
                    select(Pokemon.id).where(Pokemon.generation == gen)
                )).scalars().all()

                if pokemon_ids:
                    await session.execute(
                        delete(PokemonType).where(PokemonType.pokemon_id.in_(pokemon_ids))
                    )
                    await session.execute(delete(Pokemon).where(Pokemon.generation == gen))
                await session.commit()

                def on_progress(current, total, name):
                    _seed_status.update(current=current, total=total, detail=name)

                await seed_generation(session, gen, progress_callback=on_progress)

            # Generate audio
            logger.info("Generating audio for %d generations", len(generations))
            _seed_status.update(phase="audio", current=0, total=0, detail="")
            result = await session.execute(select(Pokemon).order_by(Pokemon.id))
            all_pokemon = result.scalars().all()
            total = len(all_pokemon)
            _seed_status["total"] = total
            for i, poke in enumerate(all_pokemon):
                _seed_status.update(current=i + 1, detail=poke.german_name)
                force = poke.german_name in PRONUNCIATION
                await generate_audio(poke.german_name, poke.id, force=force)
                await generate_size_audio(poke.size_description_spoken, poke.id, force=True)

        logger.info("Background seed completed successfully")
        _seed_status.update(running=False, done=True, error="")
    except Exception as e:
        logger.error("Background seed failed: %s", e, exc_info=True)
        _seed_status.update(running=False, done=False, error=str(e))


@app.post("/settings/seed", response_class=HTMLResponse)
async def reseed_data(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    generations = await get_active_generations(session)

    # Prevent double-start
    if _seed_status["running"]:
        if request.headers.get("HX-Request"):
            return HTMLResponse(_render_seed_status())
        return RedirectResponse(url="/settings", status_code=303)

    # Set status before creating the task so the response sees it immediately
    _seed_status.update(running=True, done=False, error="", phase="start", current=0, total=0, detail="")
    asyncio.create_task(_reseed_in_background(generations))

    # If called via HTMX, return the polling banner directly
    if request.headers.get("HX-Request"):
        return HTMLResponse(_render_seed_status())
    return RedirectResponse(url="/settings", status_code=303)


def _render_seed_status() -> str:
    if _seed_status["running"]:
        phase = _seed_status["phase"]
        current = _seed_status["current"]
        total = _seed_status["total"]
        detail = _seed_status["detail"]

        if phase == "start":
            pct = 0
            label = "Starte…"
        elif phase == "seed":
            pct = round(current / total * 100) if total > 0 else 0
            label = f"Pokémon laden: {current}/{total} — {detail}"
        else:
            pct = round(current / total * 100) if total > 0 else 0
            label = f"Audio generieren: {current}/{total} — {detail}"

        return (
            '<div id="seed-status" class="seed-banner running" '
            'hx-get="/settings/seed-status" hx-trigger="every 1s" hx-swap="outerHTML">'
            f'<div class="seed-label">{label}</div>'
            f'<div class="seed-progress-bar"><div class="seed-progress-fill" style="width:{pct}%"></div></div>'
            '</div>'
            '<button id="seed-btn" class="settings-btn seed-btn" disabled hx-swap-oob="true">'
            'Daten werden geladen…</button>'
        )

    if _seed_status["error"]:
        error = _seed_status["error"]
        _seed_status["error"] = ""
        return (
            '<div id="seed-status" class="seed-banner error">'
            f'Fehler beim Laden: {error}</div>'
            '<button id="seed-btn" class="settings-btn seed-btn" hx-swap-oob="true">'
            'Erneut versuchen</button>'
        )

    if _seed_status["done"]:
        _seed_status["done"] = False
        return (
            '<div id="seed-status" class="seed-banner done">'
            '✅ Fertig! Alle Daten und Audiodateien wurden generiert.</div>'
            '<button id="seed-btn" class="settings-btn seed-btn" hx-swap-oob="true">'
            'Daten neu laden</button>'
        )

    return '<div id="seed-status"></div>'


@app.get("/settings/seed-status", response_class=HTMLResponse)
async def seed_status(request: Request):
    return HTMLResponse(_render_seed_status())
