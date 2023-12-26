#!/usr/bin/env python3

import os
from pathlib import Path

SCORES_DIR = Path("scores")
SONGS_DIR = Path("content") / "songs"

for song in os.listdir(SCORES_DIR):
    score_dir = SCORES_DIR / song
    mscx_path = score_dir / f"{song}.mscx"

    mscx_mtime = mscx_path.stat().st_mtime

    song_dir = SONGS_DIR / song

    png_path = song_dir / f"{song}.png"
    output_paths = [
        song_dir / f"{song}.pdf",
        song_dir / f"{song}.mscz",
        song_dir / f"{song}.svg",
        png_path,
    ]

    for output_path in output_paths:
        if output_path.suffix == ".svg":
            svg_page_path = song_dir / f"{song}-1.svg"
            if svg_page_path.exists() and svg_page_path.stat().st_mtime >= mscx_mtime:
                print(f"{svg_page_path} is up to date.")
                continue
        else:
            if output_path.exists() and output_path.stat().st_mtime >= mscx_mtime:
                print(f"{output_path} is up to date.")
                continue

        print(f"Rendering {output_path}...")
        os.system(f"mscore -o {output_path} {mscx_path}")

        if output_path == png_path:
            # mscore generates separate PNGs for each page; we only have
            # single-page sheets right now, so remove the page suffix
            os.system(f"mv { song_dir / '*-1.png' } { png_path }")

            # Trim PNG
            os.system(f"magick { png_path } -trim { png_path }")
