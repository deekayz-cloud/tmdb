"""Combines the color-variant JSON manifests into one Overflight-compatible endpoint.

Overflight only accepts a single URL per source and expects the image field
named "url_img", not "url_1080p". Mirrors the existing PHP nachbau's
all_color.php.
"""
import json
import os

OUTPUT_ROOT = os.getenv("OUTPUT_ROOT", "docs")

source_files = [
    os.path.join(OUTPUT_ROOT, "tmdb_movies_color.json"),
    os.path.join(OUTPUT_ROOT, "tmdb_tv_color.json"),
]

seen_urls = set()
combined = []

for source_file in source_files:
    if not os.path.isfile(source_file):
        continue
    with open(source_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        url = item.pop("url_1080p", None)
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        item["url_img"] = url
        combined.append(item)

with open(os.path.join(OUTPUT_ROOT, "tmdb_all.json"), "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f"Combined manifest written: {len(combined)} items")
