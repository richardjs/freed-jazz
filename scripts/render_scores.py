#!/usr/bin/env python3

import os
from pathlib import Path
import xml.etree.ElementTree as ET

SCORES_DIR = Path("scores")
SONGS_DIR = Path("content") / "songs"


KEYS = {
    -6: "Gb",
    -5: "Db",
    -4: "Ab",
    -3: "Eb",
    -2: "Bb",
    -1: "F",
    0: "C",
    1: "G",
    2: "D",
    3: "A",
    4: "E",
    5: "B",
    6: "F#",
    7: "C#",
}


def transpose(mscx_path, to_key_num):
    tree = ET.parse(mscx_path)
    root = tree.getroot()

    key_elem = root.find("./Score/Staff/Measure/voice/KeySig/concertKey")
    key_num = int(key_elem.text)

    key_elem.text = str(to_key_num)

    steps = (key_num - to_key_num) * 7 % 12
    if steps > 6:
        steps -= 11

    for note_elem in root.findall("./Score/Staff/Measure/voice/Chord/Note"):
        pitch_elem = note_elem.find("pitch")
        pitch_elem.text = str(int(pitch_elem.text) - steps)

        # TODO We probably should be properly dealing with this,
        # instead of just removing it.
        # https://musescore.github.io/MuseScore_PluginAPI_Docs/plugins/html/tpc.html
        note_elem.remove(note_elem.find("tpc"))

    # TODO Change chord symbols

    tree.write("/tmp/output.mscx")


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
