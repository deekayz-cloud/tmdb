# TMDB Backgrounds → Overflight JSON

Nachbau/Erweiterung von [adelatour11/androidtvbackground](https://github.com/adelatour11/androidtvbackground):
gleiche, unveränderte Pillow-Rendering-Logik (`scripts/tmdb_plain.py`, `scripts/tmdb_color.py`),
aber statt nur lokaler Bilddateien wird zusätzlich ein Overflight-kompatibles JSON-Manifest erzeugt
(`title`, `location`, `url_1080p`), damit Projectivy Launcher die Bilder per URL laden kann
(Projectivys Folder-Wallpaper-Quelle kann keine Netzwerk-URLs lesen, nur lokale Pfade).

Dient dem visuellen Vergleich mit dem eigenständigen PHP-Nachbau in `projectivy-tmdb-de`.

## Ablauf

GitHub Actions (`.github/workflows/generate.yml`) läuft alle 6h:
1. `scripts/tmdb_plain.py` und `scripts/tmdb_color.py` rendern Bilder + schreiben JSON nach `docs/`
2. `scripts/combine_overflight.py` fasst Movies+TV je Variante zu zwei
   Overflight-tauglichen Dateien zusammen (Feld `url_img` statt `url_1080p`, dedupliziert,
   Reihenfolge zufällig gemischt) — Overflight akzeptiert pro Quelle nur eine URL,
   analog zum `all_color.php` im PHP-Nachbau
3. `docs/` wird per GitHub Pages veröffentlicht (Actions-Deploy, kein Commit ins Git-History)

## Setup

1. Secret setzen (TMDB Read Access Token, nicht der v3 API Key):
   ```
   gh secret set TMDB_BEARER_TOKEN --repo deekayz-cloud/tmdb
   ```
2. Repo → Settings → Pages → Source: "GitHub Actions" (einmalig, siehe unten)
3. Workflow manuell anstoßen zum Testen: `gh workflow run generate.yml`

## Overflight-URLs (je eine pro Quelle)

Color-Backdrops (Movies+TV):
```
https://deekayz-cloud.github.io/tmdb/tmdb_all.json
```

Plain-Backdrops (Movies+TV):
```
https://deekayz-cloud.github.io/tmdb/tmdb_all_plain.json
```

Beide enthalten Movies+TV kombiniert, dedupliziert, zufällig gemischt, Feld `url_img`.
Die 4 Einzel-JSONs (`tmdb_movies.json`, `tmdb_tv.json`, `tmdb_movies_color.json`,
`tmdb_tv_color.json`) bleiben zusätzlich unter `docs/` erreichbar, sind aber nicht
Overflight-kompatibel (Feldname `url_1080p`, nicht kombiniert).

## Lokal testen

```
pip install -r requirements.txt
cp .env.example .env   # TMDB_BEARER_TOKEN eintragen
python scripts/tmdb_plain.py
python scripts/tmdb_color.py
python scripts/combine_overflight.py
```
