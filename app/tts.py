import os
import edge_tts

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
VOICE = "de-DE-ConradNeural"  # Natural-sounding German male voice

# Phonetic overrides so the German TTS doesn't fall into English pronunciation.
# Keys = official German name, values = how the TTS should say it.
PRONUNCIATION = {
    # Gen 1
    "Krabby": "Krabbi",
    "Kingler": "Kinglär",
    "Nidoqueen": "Nidokwien",
    "Starmie": "Starmii",
    "Porygon": "Porigon",
    "Aerodactyl": "Ärodaktül",
    "Chaneira": "Schaneira",
    "Kicklee": "Kickleh",
    "Nockchan": "Nocktschan",
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


async def generate_audio(name: str, pokemon_id: int, force: bool = False) -> str:
    """Generate an MP3 file for a Pokémon name. Returns the filename."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    filename = f"{pokemon_id}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    if os.path.exists(filepath) and not force:
        return filename

    spoken = PRONUNCIATION.get(name, name)
    communicate = edge_tts.Communicate(spoken, VOICE, rate="-10%", pitch="+5Hz")
    await communicate.save(filepath)
    return filename


async def generate_size_audio(text: str, pokemon_id: int, force: bool = False) -> str:
    """Generate an MP3 file for a Pokémon's size description."""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    filename = f"size_{pokemon_id}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    if os.path.exists(filepath) and not force:
        return filename

    communicate = edge_tts.Communicate(text, VOICE, rate="-10%", pitch="+5Hz")
    await communicate.save(filepath)
    return filename
