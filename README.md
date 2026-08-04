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
2. `docs/` wird per GitHub Pages veröffentlicht (Actions-Deploy, kein Commit ins Git-History)

## Setup

1. Secret setzen (TMDB Read Access Token, nicht der v3 API Key):
   ```
   gh secret set TMDB_BEARER_TOKEN --repo deekayz-cloud/tmdb
   ```
2. Repo → Settings → Pages → Source: "GitHub Actions" (einmalig, siehe unten)
3. Workflow manuell anstoßen zum Testen: `gh workflow run generate.yml`

## Overflight-URLs (nach erstem erfolgreichen Run)

- `https://deekayz-cloud.github.io/tmdb/tmdb_movies.json`
- `https://deekayz-cloud.github.io/tmdb/tmdb_tv.json`
- `https://deekayz-cloud.github.io/tmdb/tmdb_movies_color.json`
- `https://deekayz-cloud.github.io/tmdb/tmdb_tv_color.json`

## Lokal testen

```
pip install -r requirements.txt
cp .env.example .env   # TMDB_BEARER_TOKEN eintragen
python scripts/tmdb_plain.py
python scripts/tmdb_color.py
```
