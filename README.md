# Pokémon Entdecker

**[Deutsch](#deutsch) | [English](#english)**

---

## Deutsch

Eine kinderfreundliche Web-App zum Entdecken von Pokémon — sortiert nach **Farbe** und **Typ**. Entwickelt für Kinder im Alter von 3–5 Jahren.

### Features

- Pokémon nach Farbe oder Typ filtern
- Offizielle Typ-Icons im Scarlet/Violet-Stil ([partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons))
- Deutsche Namen und Typbezeichnungen
- Detailkarten mit Artwork, Typ, kindgerechtem Größenvergleich und Entwicklungskette
- Sprachausgabe der Pokémon-Namen und Größenvergleiche (Edge TTS, deutsche Stimme)
- Responsive Design für iPhone und iPad/Tablet
- Eltern-Einstellungen (versteckt hinter 3s Long-Press auf den Titel)
- Generationsfilter (1–9) über Einstellungen oder Konfigurationsdatei

### Voraussetzungen

- Python 3.10+
- Internetverbindung (nur für das initiale Laden der Pokémon-Daten und TTS-Generierung)

### Installation

```bash
git clone https://github.com/Koschi7/pokemon-farbsortierer.git
cd pokemon-farbsortierer

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp config.env.example config.env
# In config.env die gewünschten Generationen eintragen (z.B. GENERATIONS=1,2)

# Pokémon-Daten + Sprachausgabe generieren
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

**Für Kinder:**
- Farbe oder Typ auswählen über die Buttons
- Pokémon antippen → Detailkarte mit Bild, Typ, Größe und Entwicklung
- Name antippen → Name wird vorgelesen
- Größenvergleich antippen → Größe wird vorgelesen

**Für Eltern:**
- 3 Sekunden lang auf „Pokémon Entdecker" drücken → Einstellungen
- Generationen an-/abwählen und Daten neu laden

### Deployment (VPS)

```bash
# Beispiel: systemd Service
sudo nano /etc/systemd/system/pokemon.service
```

```ini
[Unit]
Description=Pokémon Entdecker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/pokemon-farbsortierer
ExecStart=/opt/pokemon-farbsortierer/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pokemon
sudo systemctl start pokemon
```

Dahinter einen Reverse-Proxy (z.B. Caddy oder nginx) für HTTPS.

---

## English

A kid-friendly web app for exploring Pokémon — sorted by **color** and **type**. Built for children aged 3–5.

### Features

- Filter Pokémon by color or type
- Official type icons in Scarlet/Violet style ([partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons))
- German names and type labels
- Detail cards with artwork, type, kid-friendly size comparisons, and evolution chains
- Text-to-speech for Pokémon names and size descriptions (Edge TTS, German voice)
- Responsive design for iPhone and iPad/tablet
- Hidden parent settings (3s long-press on the title)
- Generation filter (1–9) via settings or config file

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

# Seed Pokémon data + generate audio
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
- Pick a color or type using the filter buttons
- Tap a Pokémon → detail card with artwork, type, size comparison, and evolutions
- Tap the name → name is read aloud
- Tap the size description → size is read aloud

**For parents:**
- Long-press (3s) on "Pokémon Entdecker" title → settings page
- Toggle generations and re-seed data

### Deployment (VPS)

```bash
sudo nano /etc/systemd/system/pokemon.service
```

```ini
[Unit]
Description=Pokémon Entdecker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/pokemon-farbsortierer
ExecStart=/opt/pokemon-farbsortierer/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
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

- **Backend:** Python, FastAPI
- **Frontend:** Jinja2 + HTMX
- **Database:** SQLite (local PokéAPI cache)
- **TTS:** Edge TTS (German voice, pre-generated MP3s)
- **Type Icons:** [partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons) (MIT)
- **Data:** [PokéAPI](https://pokeapi.co)

---

Built with [Claude Code](https://claude.ai/claude-code)

Type icons by [partywhale](https://github.com/partywhale/pokemon-type-icons) under MIT license. Pokémon data from [PokéAPI](https://pokeapi.co).
