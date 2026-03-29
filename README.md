# Pokémon Entdecker

Eine kinderfreundliche Web-App zum Entdecken von Pokémon — sortiert nach **Farbe** und **Typ**. Entwickelt für Kinder im Alter von 3–5 Jahren.

## Features

- Pokémon nach Farbe oder Typ filtern
- Deutsche Namen und Typbezeichnungen
- Detailkarten mit Artwork, Typ, Größenvergleich und Entwicklungskette
- Sprachausgabe der Pokémon-Namen (Text-to-Speech)
- Responsive Design für iPhone und iPad/Tablet
- Eltern-Einstellungen (versteckt hinter Long-Press auf den Titel)
- Generationsfilter über Einstellungen oder Konfigurationsdatei

## Voraussetzungen

- Python 3.10+
- Internetverbindung (nur für das initiale Laden der Pokémon-Daten)

## Installation

```bash
# Repository klonen
git clone https://github.com/DEIN-USERNAME/pokemon-farbsortierer.git
cd pokemon-farbsortierer

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Konfiguration anpassen
cp config.env.example config.env
# In config.env die gewünschten Generationen eintragen (z.B. GENERATIONS=1,2)

# Pokémon-Daten laden
python seed.py

# Optional: bestimmte Generationen laden
python seed.py --generations 1,2,3
```

## Starten

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Die App ist dann unter `http://localhost:8000` erreichbar.

## Bedienung

### Für Kinder
- **Farbe/Typ** auswählen über die bunten Buttons oben
- **Pokémon antippen** → Detailkarte mit Bild, Typ, Größe und Entwicklung
- **Name antippen** → Name wird vorgelesen

### Für Eltern
- **3 Sekunden lang auf "Pokémon Entdecker"** drücken → Einstellungen öffnen
- Generationen an-/abwählen
- Daten neu laden

## Deployment (VPS)

```bash
# App starten (im Hintergrund)
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Oder mit systemd Service
# Siehe unten für eine Beispiel-Konfiguration
```

### Beispiel systemd Service

```ini
[Unit]
Description=Pokémon Entdecker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/pokemon-farbsortierer
ExecStart=/opt/pokemon-farbsortierer/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Technologie

- **Backend:** Python, FastAPI
- **Frontend:** Jinja2 Templates, HTMX
- **Datenbank:** SQLite (lokaler Cache der PokéAPI-Daten)
- **Sprachausgabe:** Web Speech API (Browser)
- **Datenquelle:** [PokéAPI](https://pokeapi.co)
