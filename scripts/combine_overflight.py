"""Combines the plain/color JSON manifests into Overflight-compatible endpoints.

Overflight only accepts a single URL per source and expects the image field
named "url_img", not "url_1080p". Mirrors the existing PHP nachbau's
all_color.php (shuffle(), field rename, dedup by URL).
"""
import json
import os
import random

OUTPUT_ROOT = os.getenv("OUTPUT_ROOT", "docs")


def combine(source_names, output_name):
    seen_urls = set()
    combined = []

    for source_name in source_names:
        source_file = os.path.join(OUTPUT_ROOT, source_name)
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

    random.shuffle(combined)

    with open(os.path.join(OUTPUT_ROOT, output_name), "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"{output_name}: {len(combined)} items")


combine(["tmdb_movies_color.json", "tmdb_tv_color.json"], "tmdb_all.json")
combine(["tmdb_movies.json", "tmdb_tv.json"], "tmdb_all_plain.json")
