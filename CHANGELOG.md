# Changelog / Änderungsprotokoll

**[Deutsch](#deutsch) | [English](#english)**

---

## Deutsch

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
