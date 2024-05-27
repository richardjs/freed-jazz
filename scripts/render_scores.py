#!/usr/bin/env python3

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SCORES_DIR = Path("scores")
SONGS_DIR = Path("content") / "songs"


KEYS = {
    "gb": -6,
    "db": -5,
    "ab": -4,
    "eb": -3,
    "bb": -2,
    "f": -1,
    "c": 0,
    "g": 1,
    "d": 2,
    "a": 3,
    "e": 4,
    "b": 5,
    "fs": 6,
    "cs": 7,
}


def transpose(mscx_path, to_key_num, output_file):
    tree = ET.parse(mscx_path)
    root = tree.getroot()

    key = root.find("./Score/Staff/Measure/voice/KeySig/concertKey")
    key_num = int(key.text)

    key_diff = key_num - to_key_num

    steps = key_diff * 7 % 12
    # if steps > 6:
    #    steps -= 11

    key.text = str(to_key_num)

    for note in root.findall("./Score/Staff/Measure/voice/Chord/Note"):
        pitch = note.find("pitch")
        pitch.text = str(int(pitch.text) - steps)

        # TODO We should be properly dealing with this
        # https://musescore.github.io/MuseScore_PluginAPI_Docs/plugins/html/tpc.html
        note.remove(note.find("tpc"))

    for harmony_root in root.findall("./Score/Staff/Measure/voice/Harmony/root"):
        harmony_root.text = str(int(harmony_root.text) - key_diff)

    for harmony_base in root.findall("./Score/Staff/Measure/voice/Harmony/base"):
        harmony_base.text = str(int(harmony_base.text) - key_diff)

    tree.write(output_file)


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

    for key, key_num in KEYS.items():
        output_paths += [
            song_dir / f"{song}_{key}.pdf",
            song_dir / f"{song}_{key}.svg",
        ]

    for output_path in output_paths:
        render_input_path = mscx_path

        # Grab key from the filename, if thee is one
        match = re.match(r"[^\.]+_([^\.]+)\.[^\.]+", str(output_path))
        if match:
            key = match.groups()[0]
            tmp_mscx = score_dir / "tmp.mscx"
            transpose(render_input_path, KEYS[key], tmp_mscx)
            render_input_path = tmp_mscx

        if output_path.suffix == ".svg":
            svg_page_path = Path(str(output_path).replace(".svg", "-1.svg"))
            if svg_page_path.exists() and svg_page_path.stat().st_mtime >= mscx_mtime:
                print(f"{svg_page_path} is up to date.")
                continue
        else:
            if output_path.exists() and output_path.stat().st_mtime >= mscx_mtime:
                print(f"{output_path} is up to date.")
                continue

        print(f"Rendering {output_path}...")
        os.system(f"mscore -o {output_path} {render_input_path}")

        if output_path == png_path:
            # mscore generates separate PNGs for each page; we only have
            # single-page sheets right now, so remove the page suffix
            os.system(f"mv { song_dir / '*-1.png' } { png_path }")

            # Trim PNG
            os.system(f"magick { png_path } -trim { png_path }")
