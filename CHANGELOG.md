# Changelog / Änderungsprotokoll

**[Deutsch](#deutsch) | [English](#english)**

---

## Deutsch

### 2026-04-11

**Font Awesome Icons**
- Suche und Favoriten im Header als Icons (Lupe, Herz) statt Text — spart Platz auf kleinen Bildschirmen
- Favoriten-Herz auf Detailkarte nutzt Font Awesome statt Emoji fur konsistente Darstellung

### 2026-04-09

**Zweisprachigkeit (Deutsch + Englisch)**
- Sprache umschaltbar in den Einstellungen
- Alle UI-Texte, Pokemon-Namen, Typ-Labels und Grossenvergleiche in beiden Sprachen
- Sprachausgabe (TTS) wird fur beide Sprachen generiert
- Suche funktioniert in der aktiven Sprache

**Favoriten**
- Herz-Button auf der Detailkarte zum Markieren von Lieblings-Pokemon
- Neuer Favoriten-Tab im Header zeigt alle markierten Pokemon

**Suchfunktion**
- Neuer "Suche"-Modus im Header
- Pokemon nach Namen filtern mit Echtzeit-Ergebnissen (300ms Debounce)

**Offline & PWA**
- Service Worker cached CSS, JS, Icons, Audio und Pokemon-Bilder
- Web App Manifest fur Installation als App (Android/iOS)

**Verbesserungen**
- Seed-Button wird deaktiviert wahrend Daten geladen werden (kein Doppelklick)
- Fehlerbehandlung und Logging im Hintergrund-Task
- Datenbank-Indexes fur schnellere Filter-Abfragen
- Kompakteres Tablet-Layout fur Fire Tablet 8
- TTS Retry-Logik bei Rate-Limiting

### 2026-04-03

**Bugfixes & Verbesserungen**
- Daten neu laden läuft jetzt im Hintergrund — kein Timeout mehr auf der Einstellungsseite
- Fortschrittsbalken auf der Einstellungsseite: zeigt Phase (Pokémon laden / Audio generieren), aktuellen Stand und Abschluss
- Entwicklungsketten zeigen nur noch Pokémon aus aktiven Generationen

### 2026-03-29

**Automatische Sprachausgabe beim Neu-Laden**
- Sprachausgabe (Namen + Größenvergleiche) wird automatisch im Hintergrund generiert, wenn Eltern über die Einstellungen Daten neu laden
- Kein CLI-Zugriff mehr nötig für neue Generationen

**Größenvergleiche verbessert (Seed)**
- Größen-Audio wird jetzt immer neu generiert beim Seeden

### 2026-03-28

**TTS-Aussprache optimiert**
- Phonetische Korrekturen für deutsche Pokémon-Namen (Gen 1–9), z.B. „Krabby" → „Krabbi", „Mewtu" → „Mjutu"
- „Zentimeter" wird korrekt als „Tsentimeter" ausgesprochen
- „Papa" → „Pappa" (verhindert französische Betonung)
- Komma statt Punkt als Trenner zwischen Höhe und Vergleich

**Kindgerechte Größenvergleiche**
- 12 Größenkategorien mit Vergleichen wie „So groß wie ein Teddy!", „So groß wie du!", „So groß wie ein Haus!"
- Klickbare Größenbeschreibung mit Lautsprecher-Symbol
- Separate Display- und Sprachversionen (z.B. „1,7 m" vs. „1 Meter 70")

**Nidoran-Darstellung**
- ♀/♂-Symbole werden als „Weiblich"/„Männlich" angezeigt

**Kompaktes Mobile-Layout**
- Header und Filter-Buttons in einer kompakten, sticky Zeile
- Typ-Icons als horizontale Scroll-Leiste (nur Icons, ohne Text)
- Umschalter Farbe/Typ im Header

**Detailkarten-Fix**
- Kein Flackern mehr beim Öffnen der Detailkarte

**Typ-Icons**
- Scarlet/Violet-Style SVG-Icons von [partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons)

### 2026-03-27

**Erster Release**
- Pokémon-Daten von PokéAPI (Gen 1–9)
- Filter nach Farbe und Typ
- Detailkarten mit Artwork und Entwicklungskette
- Deutsche Sprachausgabe (Edge TTS)
- Eltern-Einstellungen mit Long-Press
- SQLite-Datenbank

---

## English

### 2026-04-11

**Font Awesome Icons**
- Search and favorites in header as icons (magnifying glass, heart) instead of text — saves space on small screens
- Favorite heart on detail card uses Font Awesome instead of emoji for consistent rendering

### 2026-04-09

**Bilingual support (German + English)**
- Language switchable in settings
- All UI text, Pokemon names, type labels, and size comparisons in both languages
- Text-to-speech (TTS) generated for both languages
- Search works in the active language

**Favorites**
- Heart button on detail card to mark favorite Pokemon
- New favorites tab in header shows all marked Pokemon

**Search**
- New "Search" mode in header
- Filter Pokemon by name with real-time results (300ms debounce)

**Offline & PWA**
- Service Worker caches CSS, JS, icons, audio, and Pokemon images
- Web App Manifest for installation as app (Android/iOS)

**Improvements**
- Seed button disabled while data is loading (prevents double-click)
- Error handling and logging in background task
- Database indexes for faster filter queries
- Compact tablet layout optimized for Fire Tablet 8
- TTS retry logic for rate limiting

### 2026-04-03

**Bugfixes & improvements**
- Re-seeding now runs in the background — no more timeout on the settings page
- Progress bar on settings page showing phase (loading Pokémon / generating audio), current progress, and completion
- Evolution chains only show Pokémon from active generations

### 2026-03-29

**Auto-generate audio on re-seed**
- TTS audio (names + size descriptions) is now automatically generated in the background when parents re-seed data via settings
- No CLI access needed for new generations

**Size audio always regenerated on seed**
- Size description audio is now force-regenerated during seeding

### 2026-03-28

**TTS pronunciation improvements**
- Phonetic overrides for German Pokémon names (Gen 1–9), e.g. "Krabby" → "Krabbi", "Mewtu" → "Mjutu"
- "Zentimeter" correctly pronounced as "Tsentimeter"
- "Papa" → "Pappa" (prevents French-sounding stress)
- Comma separator between height and comparison in spoken text

**Kid-friendly size comparisons**
- 12 size categories with comparisons like "As tall as a teddy!", "As tall as you!", "As tall as a house!"
- Clickable size description with speaker icon
- Separate display and spoken versions (e.g. "1,7 m" vs. "1 Meter 70")

**Nidoran display**
- ♀/♂ symbols shown as "Weiblich"/"Männlich"

**Compact mobile layout**
- Header and filter buttons in a compact sticky row
- Type icons as horizontal scroll bar (icons only, no text)
- Color/type mode toggle in header

**Detail card fix**
- No more flicker when opening detail cards

**Type icons**
- Scarlet/Violet-style SVG icons from [partywhale/pokemon-type-icons](https://github.com/partywhale/pokemon-type-icons)

### 2026-03-27

**Initial release**
- Pokémon data from PokéAPI (Gen 1–9)
- Filter by color and type
- Detail cards with artwork and evolution chains
- German text-to-speech (Edge TTS)
- Hidden parent settings via long-press
- SQLite database
