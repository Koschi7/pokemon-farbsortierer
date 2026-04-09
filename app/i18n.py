"""Internationalization: UI strings, type/color labels per language."""

TRANSLATIONS = {
    "de": {
        # Header
        "app_title": "Pokemon Entdecker",
        "mode_color": "Farbe",
        "mode_type": "Typ",
        "mode_search": "Suche",
        # Hints
        "hint_default": "Wähle eine Farbe oder einen Typ!",
        "hint_search": "Tippe einen Namen ein!",
        "hint_no_favorites": "Noch keine Favoriten!",
        # Detail
        "evolution": "Entwicklung",
        "not_found": "Pokemon nicht gefunden",
        # Settings
        "settings_title": "Einstellungen",
        "settings_gen_title": "Generationen",
        "settings_gen_hint": "Wähle aus, welche Pokemon-Generationen angezeigt werden sollen.",
        "settings_save": "Speichern",
        "settings_seed_title": "Daten aktualisieren",
        "settings_seed_hint": "Lade die Pokemon-Daten für die ausgewählten Generationen neu von der PokeAPI.",
        "settings_seed_btn": "Daten neu laden",
        "settings_seed_loading": "Daten werden geladen…",
        "settings_seed_retry": "Erneut versuchen",
        "settings_lang_title": "Sprache / Language",
        "settings_back": "Zurück",
        # Seed status
        "seed_start": "Starte…",
        "seed_pokemon": "Pokemon laden",
        "seed_audio": "Audio generieren",
        "seed_done": "Fertig! Alle Daten und Audiodateien wurden generiert.",
        "seed_error": "Fehler beim Laden",
        # Types
        "types": {
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
        },
        # Colors
        "colors": {
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
        },
    },
    "en": {
        # Header
        "app_title": "Pokemon Explorer",
        "mode_color": "Color",
        "mode_type": "Type",
        "mode_search": "Search",
        # Hints
        "hint_default": "Pick a color or type!",
        "hint_search": "Type a name!",
        "hint_no_favorites": "No favorites yet!",
        # Detail
        "evolution": "Evolution",
        "not_found": "Pokemon not found",
        # Settings
        "settings_title": "Settings",
        "settings_gen_title": "Generations",
        "settings_gen_hint": "Choose which Pokemon generations to display.",
        "settings_save": "Save",
        "settings_seed_title": "Update Data",
        "settings_seed_hint": "Reload Pokemon data for selected generations from the PokeAPI.",
        "settings_seed_btn": "Reload Data",
        "settings_seed_loading": "Loading data…",
        "settings_seed_retry": "Try again",
        "settings_lang_title": "Sprache / Language",
        "settings_back": "Back",
        # Seed status
        "seed_start": "Starting…",
        "seed_pokemon": "Loading Pokemon",
        "seed_audio": "Generating audio",
        "seed_done": "Done! All data and audio files have been generated.",
        "seed_error": "Error loading data",
        # Types
        "types": {
            "normal": "Normal",
            "fire": "Fire",
            "water": "Water",
            "electric": "Electric",
            "grass": "Grass",
            "ice": "Ice",
            "fighting": "Fighting",
            "poison": "Poison",
            "ground": "Ground",
            "flying": "Flying",
            "psychic": "Psychic",
            "bug": "Bug",
            "rock": "Rock",
            "ghost": "Ghost",
            "dragon": "Dragon",
            "dark": "Dark",
            "steel": "Steel",
            "fairy": "Fairy",
        },
        # Colors
        "colors": {
            "black": "Black",
            "blue": "Blue",
            "brown": "Brown",
            "gray": "Gray",
            "green": "Green",
            "pink": "Pink",
            "purple": "Purple",
            "red": "Red",
            "white": "White",
            "yellow": "Yellow",
        },
    },
}


# Size descriptions per language
SIZE_BRACKETS = {
    "de": [
        (0.2, "{h} – Passt in deine Hand!"),
        (0.3, "{h} – So groß wie ein Lineal!"),
        (0.5, "{h} – So groß wie ein Teddy!"),
        (0.7, "{h} – So groß wie ein Kissen!"),
        (0.9, "{h} – So groß wie ein Bobbycar!"),
        (1.1, "{h} – So groß wie du!"),
        (1.3, "{h} – So groß wie ein Fahrrad!"),
        (1.6, "{h} – So groß wie ein Schneemann!"),
        (2.0, "{h} – So groß wie Mama oder Papa!"),
        (3.0, "{h} – So groß wie eine Zimmerdecke!"),
        (5.0, "{h} – So groß wie eine Giraffe!"),
        (999, "{h} – So groß wie ein Haus!"),
    ],
    "en": [
        (0.2, "{h} – Fits in your hand!"),
        (0.3, "{h} – As tall as a ruler!"),
        (0.5, "{h} – As tall as a teddy bear!"),
        (0.7, "{h} – As tall as a pillow!"),
        (0.9, "{h} – As tall as a scooter!"),
        (1.1, "{h} – As tall as you!"),
        (1.3, "{h} – As tall as a bicycle!"),
        (1.6, "{h} – As tall as a snowman!"),
        (2.0, "{h} – As tall as Mom or Dad!"),
        (3.0, "{h} – As tall as a ceiling!"),
        (5.0, "{h} – As tall as a giraffe!"),
        (999, "{h} – As tall as a house!"),
    ],
}

SIZE_BRACKETS_SPOKEN = {
    "de": [
        (0.2, "{h}, Passt in deine Hand!"),
        (0.3, "{h}, So groß wie ein Lineal!"),
        (0.5, "{h}, So groß wie ein Teddy!"),
        (0.7, "{h}, So groß wie ein Kissen!"),
        (0.9, "{h}, So groß wie ein Bobbycar!"),
        (1.1, "{h}, So groß wie du!"),
        (1.3, "{h}, So groß wie ein Fahrrad!"),
        (1.6, "{h}, So groß wie ein Schneemann!"),
        (2.0, "{h}, So groß wie Mama oder Pappa!"),
        (3.0, "{h}, So groß wie eine Zimmerdecke!"),
        (5.0, "{h}, So groß wie eine Giraffe!"),
        (999, "{h}, So groß wie ein Haus!"),
    ],
    "en": [
        (0.2, "{h}, Fits in your hand!"),
        (0.3, "{h}, As tall as a ruler!"),
        (0.5, "{h}, As tall as a teddy bear!"),
        (0.7, "{h}, As tall as a pillow!"),
        (0.9, "{h}, As tall as a scooter!"),
        (1.1, "{h}, As tall as you!"),
        (1.3, "{h}, As tall as a bicycle!"),
        (1.6, "{h}, As tall as a snowman!"),
        (2.0, "{h}, As tall as Mom or Dad!"),
        (3.0, "{h}, As tall as a ceiling!"),
        (5.0, "{h}, As tall as a giraffe!"),
        (999, "{h}, As tall as a house!"),
    ],
}

# TTS config per language
TTS_CONFIG = {
    "de": {
        "voice": "de-DE-ConradNeural",
        "rate": "-10%",
        "pitch": "+5Hz",
    },
    "en": {
        "voice": "en-US-GuyNeural",
        "rate": "-10%",
        "pitch": "+5Hz",
    },
}


def get_t(lang: str) -> dict:
    """Get translation dict for a language, fallback to German."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["de"])


def format_height_display(height: float, lang: str = "de") -> str:
    """Format height for display: '70 cm' or '1,7 m'."""
    if lang == "de":
        if height < 1.0:
            return f"{round(height * 100)} cm"
        return f"{height:.1f} m".replace(".", ",")
    else:
        # English: feet and inches or metric
        if height < 1.0:
            return f"{round(height * 100)} cm"
        return f"{height:.1f} m"


def format_height_spoken(height: float, lang: str = "de") -> str:
    """Format height for TTS."""
    if lang == "de":
        if height < 1.0:
            return f"{round(height * 100)} Tsentimeter"
        m = int(height)
        cm = round((height - m) * 100)
        if cm == 0:
            return f"{m} Meter"
        return f"{m} Meter {cm}"
    else:
        if height < 1.0:
            return f"{round(height * 100)} centimeters"
        m = int(height)
        cm = round((height - m) * 100)
        if cm == 0:
            return f"{m} meter"
        return f"{m} meter {cm}"


def get_size_description(height: float, lang: str = "de") -> str:
    """Get display size description for a height."""
    h_str = format_height_display(height, lang)
    for max_h, template in SIZE_BRACKETS.get(lang, SIZE_BRACKETS["de"]):
        if height <= max_h:
            return template.format(h=h_str)
    return h_str


def get_size_description_spoken(height: float, lang: str = "de") -> str:
    """Get spoken size description for TTS."""
    h_str = format_height_spoken(height, lang)
    for max_h, template in SIZE_BRACKETS_SPOKEN.get(lang, SIZE_BRACKETS_SPOKEN["de"]):
        if height <= max_h:
            return template.format(h=h_str)
    return h_str
