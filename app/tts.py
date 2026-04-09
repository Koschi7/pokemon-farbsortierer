import asyncio
import os
import edge_tts

from app.i18n import TTS_CONFIG

MAX_RETRIES = 3
RETRY_DELAY = 2.0
BETWEEN_DELAY = 0.3

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")

# Phonetic overrides so the German TTS doesn't fall into English pronunciation.
# Keys = official German name, values = how the TTS should say it.
PRONUNCIATION = {
    # Gen 1
    "Krabby": "Krabbi",
    "Kingler": "Kinglär",
    "Nidoran♀": "Nidoran Weiblich",
    "Nidoran♂": "Nidoran Männlich",
    "Nidoqueen": "Nidokwien",
    "Starmie": "Starmii",
    "Porygon": "Porigon",
    "Aerodactyl": "Ärodaktül",
    "Chaneira": "Schaneira",
    "Kicklee": "Kickleh",
    "Nockchan": "Nocktschan",
    "Mewtu": "Mjutu",
    # Gen 2
    "Hoothoot": "Hutu",
    "Ledyba": "Lediba",
    "Ledian": "Lediahn",
    "Lanturn": "Lantern",
    "Togetic": "Togetick",
    "Snubbull": "Snubbull",
    "Granbull": "Grannbull",
    "Octillery": "Oktilleri",
    "Porygon2": "Porigon Zwei",
    "Miltank": "Miltänk",
    "Suicune": "SSui-kune",
    "Pupitar": "Pupitar",
    # Gen 3
    "Wingull": "Wingall",
    "Pelipper": "Pelippär",
    "Ninjask": "Nindschask",
    "Wailmer": "Weilmär",
    "Wailord": "Weilord",
    "Spoink": "Schpoink",
    "Shuppet": "Schuppet",
    "Banette": "Banett",
    "Relicanth": "Relikant",
    "Regirock": "Redschi-Rock",
    "Regice": "Redschi-Eis",
    "Registeel": "Redschi-Stiel",
    "Kyogre": "Kiogre",
    "Groudon": "Groudon",
    "Rayquaza": "Räi-kwasa",
    "Jirachi": "Dschiraschi",
    "Deoxys": "Deoksis",
    # Gen 4
    "Shaymin": "Scheimin",
    "Shellos": "Schellos",
    "Chatot": "Tschatot",
    # Gen 5
    "Reshiram": "Reschiram",
    "Chandelure": "Schandelür",
    # Gen 6
    "Chespin": "Tschespin",
    "Vivillon": "Wiwijon",
    # Gen 7
    "Rowlet": "Raulett",
    "Wishiwashi": "Wischi-Waschi",
    # Gen 8
    "Grookey": "Gruhki",
    "Thwackey": "Twacki",
    "Rillaboom": "Rillabuhm",
    "Sobble": "Sobbel",
    "Drizzile": "Drisseil",
    "Inteleon": "Intellion",
    "Wooloo": "Wuhlu",
    "Dubwool": "Dabbwull",
    # Gen 9
    "Quaquaval": "Kwakwawal",
    "Shroodle": "Schruhdel",
    "Tinkaton": "Tinkaton",
}


def _audio_dir_for(lang: str) -> str:
    """Return audio directory for a language, e.g. static/audio/de/."""
    d = os.path.join(AUDIO_DIR, lang)
    os.makedirs(d, exist_ok=True)
    return d


async def _tts_with_retry(text: str, filepath: str, voice: str, rate: str, pitch: str):
    """Generate TTS audio with retry logic for rate limiting."""
    for attempt in range(MAX_RETRIES):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(filepath)
            await asyncio.sleep(BETWEEN_DELAY)
            return
        except Exception:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise


async def generate_audio(name: str, pokemon_id: int, lang: str = "de", force: bool = False) -> str:
    """Generate an MP3 file for a Pokemon name. Returns the relative path."""
    audio_dir = _audio_dir_for(lang)
    filename = f"{pokemon_id}.mp3"
    filepath = os.path.join(audio_dir, filename)

    if os.path.exists(filepath) and not force:
        return f"{lang}/{filename}"

    cfg = TTS_CONFIG.get(lang, TTS_CONFIG["de"])
    spoken = PRONUNCIATION.get(name, name) if lang == "de" else name
    await _tts_with_retry(spoken, filepath, cfg["voice"], cfg["rate"], cfg["pitch"])
    return f"{lang}/{filename}"


async def generate_size_audio(text: str, pokemon_id: int, lang: str = "de", force: bool = False) -> str:
    """Generate an MP3 file for a Pokemon's size description."""
    audio_dir = _audio_dir_for(lang)
    filename = f"size_{pokemon_id}.mp3"
    filepath = os.path.join(audio_dir, filename)

    if os.path.exists(filepath) and not force:
        return f"{lang}/{filename}"

    cfg = TTS_CONFIG.get(lang, TTS_CONFIG["de"])
    await _tts_with_retry(text, filepath, cfg["voice"], cfg["rate"], cfg["pitch"])
    return f"{lang}/{filename}"
