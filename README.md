# Pokemon Entdecker / Pokemon Explorer

A kid-friendly web app for discovering Pokemon — filter by **color**, **type**, or **name**. Built for children aged 3–5 with text-to-speech, kid-friendly size comparisons, and a colorful touch-optimized UI. Supports **German** and **English**.

> Eine kinderfreundliche Web-App zum Entdecken von Pokemon — filtern nach **Farbe**, **Typ** oder **Name**. Entwickelt fur Kinder im Alter von 3–5 Jahren mit Sprachausgabe, kindgerechten Grossenvergleichen und einem bunten, touch-optimierten Design. Unterstutzt **Deutsch** und **Englisch**.

**[Deutsch](#deutsch) | [English](#english)**

---

## Deutsch

### Features

- **Filtern** nach Farbe, Typ oder Name (Suchfunktion)
- **Favoriten** — Lieblings-Pokemon mit Herz markieren
- **Detailkarten** mit Artwork, Typ-Badges, kindgerechtem Grossenvergleich und Entwicklungskette
- **Sprachausgabe** der Pokemon-Namen und Grossenvergleiche (Edge TTS, deutsche und englische Stimme)
- **Typ-Icons** im Scarlet/Violet-Stil ([partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons))
- **Zweisprachig** — Deutsch und Englisch umschaltbar in den Einstellungen
- **Offline-fahig** — Service Worker cached Assets, Bilder und Audio
- **PWA** — installierbar als App auf Android/iOS
- **Responsive Design** fur iPhone, iPad, Fire Tablet und Desktop
- **Eltern-Einstellungen** (versteckt hinter 3s Long-Press auf den Titel)
- **Generationsfilter** (1–9) uber Einstellungen
- **Fortschrittsbalken** beim Laden neuer Pokemon-Daten

### Voraussetzungen

- Python 3.10+
- Internetverbindung (nur fur das initiale Laden der Pokemon-Daten und TTS-Generierung)

### Installation

```bash
git clone https://github.com/Koschi7/pokemon-farbsortierer.git
cd pokemon-farbsortierer

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp config.env.example config.env
# In config.env die gewunschten Generationen eintragen (z.B. GENERATIONS=1,2)

# Pokemon-Daten laden + Sprachausgabe generieren (DE + EN)
python seed.py

# Optional: bestimmte Generationen
python seed.py --generations 1,2,3
```

### Starten

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Die App ist dann unter `http://localhost:8000` erreichbar.

### Bedienung

**Fur Kinder:**
- Farbe, Typ oder Suche auswahlen uber die Buttons im Header
- Pokemon antippen → Detailkarte mit Bild, Typ, Grosse und Entwicklung
- Name antippen → Name wird vorgelesen
- Grossenvergleich antippen → Grosse wird vorgelesen
- Herz antippen → als Favorit speichern

**Fur Eltern:**
- 3 Sekunden lang auf den Titel drucken → Einstellungen
- Generationen an-/abwahlen und Daten neu laden (mit Fortschrittsanzeige)
- Sprache zwischen Deutsch und Englisch umschalten
- Audio wird automatisch im Hintergrund fur beide Sprachen generiert

### Deployment (VPS)

```bash
sudo nano /etc/systemd/system/pokemon.service
```

```ini
[Unit]
Description=Pokemon Entdecker
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pokemon-farbsortierer
ExecStart=/var/www/pokemon-farbsortierer/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pokemon
sudo systemctl start pokemon
```

Dahinter einen Reverse-Proxy (z.B. Caddy oder nginx) fur HTTPS.

---

## English

### Features

- **Filter** by color, type, or name (search function)
- **Favorites** — save favorite Pokemon with a heart button
- **Detail cards** with artwork, type badges, kid-friendly size comparisons, and evolution chains
- **Text-to-speech** for Pokemon names and size descriptions (Edge TTS, German and English voices)
- **Type icons** in Scarlet/Violet style ([partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons))
- **Bilingual** — switch between German and English in settings
- **Offline support** — Service Worker caches assets, images, and audio
- **PWA** — installable as an app on Android/iOS
- **Responsive design** for iPhone, iPad, Fire Tablet, and desktop
- **Hidden parent settings** (3s long-press on the title)
- **Generation filter** (1–9) via settings
- **Progress bar** when loading new Pokemon data

### Requirements

- Python 3.10+
- Internet connection (only for initial data seeding and TTS generation)

### Installation

```bash
git clone https://github.com/Koschi7/pokemon-farbsortierer.git
cd pokemon-farbsortierer

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp config.env.example config.env
# Set desired generations in config.env (e.g. GENERATIONS=1,2)

# Seed Pokemon data + generate audio (DE + EN)
python seed.py

# Optional: specific generations
python seed.py --generations 1,2,3
```

### Run

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

App will be available at `http://localhost:8000`.

### Usage

**For kids:**
- Pick a color, type, or use the search in the header
- Tap a Pokemon → detail card with artwork, type, size comparison, and evolutions
- Tap the name → name is read aloud
- Tap the size description → size is read aloud
- Tap the heart → save as favorite

**For parents:**
- Long-press (3s) on the title → settings page
- Toggle generations and re-seed data (with progress bar)
- Switch language between German and English
- Audio is automatically generated in the background for both languages

### Deployment (VPS)

```bash
sudo nano /etc/systemd/system/pokemon.service
```

```ini
[Unit]
Description=Pokemon Entdecker
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pokemon-farbsortierer
ExecStart=/var/www/pokemon-farbsortierer/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pokemon
sudo systemctl start pokemon
```

Use a reverse proxy (e.g. Caddy or nginx) in front for HTTPS.

### Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** Jinja2 + HTMX
- **Database:** SQLite (local PokeAPI cache)
- **TTS:** Edge TTS (German + English voices, pre-generated MP3s)
- **Type Icons:** [partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons) (MIT)
- **Data:** [PokeAPI](https://pokeapi.co)
- **Offline:** Service Worker + PWA manifest

---

### Keywords

`pokemon`, `kids app`, `kinder app`, `pokedex`, `pokemon explorer`, `pokemon color`, `pokemon type filter`, `text-to-speech`, `tts`, `edge-tts`, `fastapi`, `htmx`, `jinja2`, `sqlite`, `pwa`, `offline`, `bilingual`, `german`, `english`, `pokemon for kids`, `pokemon entdecker`, `pokemon farbsortierer`, `kid-friendly`, `kindgerecht`, `pokeapi`

---

Built with [Claude Code](https://claude.ai/claude-code)

Type icons by [partywhale](https://github.com/partywhale/pokemon-type-icons) under MIT license. Pokemon data from [PokeAPI](https://pokeapi.co).
