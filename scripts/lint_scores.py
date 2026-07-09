#!/usr/bin/env python3

import argparse
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

SCORES_DIR = Path("scores")
TUNES_DIR = Path("content") / "songs"

COPYRIGHT_LINE = "U.S. public domain - freedjazz.org"
MAJ_7_SYMBOL = "^"

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--write", action="store_true")
args = parser.parse_args()

for tune in os.listdir(SCORES_DIR):
    changed = False

    score_dir = SCORES_DIR / tune
    mscx_path = score_dir / f"{tune}.mscx"

    tune_index_path = TUNES_DIR / tune / "index.md"

    try:
        with open(tune_index_path) as tune_index:
            metadata = next(yaml.load_all(tune_index, Loader=yaml.FullLoader))
    except FileNotFoundError:
        print(f"{tune}: no index.md")
        continue

    tree = ET.parse(mscx_path)
    root = tree.getroot()

    title = root.find("./Score/metaTag[@name='workTitle']")
    if title.text != metadata["title"]:
        print(f"{tune}: title '{title.text}' != '{metadata["title"]}'")
        if args.write:
            title.text = metadata["title"]
            changed = True

    # TODO lint composer and lyricist

    subtitle = root.find("./Score/metaTag[@name='subtitle']")
    if (subtitle is not None) and subtitle.text == "Subtitle":
        print(f"{tune}: subtitle is '{subtitle.text}'")
        if args.write:
            subtitle.text = ""
            changed = True

    cw = root.find("./Score/metaTag[@name='copyright']")
    if cw.text != COPYRIGHT_LINE:
        print(f"{tune}: wrong copyright line")
        if args.write:
            cw.text = COPYRIGHT_LINE
            changed = True

    # Normalize major seventh symbols
    # Different versions of .mscx have this in different places
    harmonies = list(root.findall("./Score/Staff/Measure/voice/Harmony/harmonyInfo/name"))
    harmonies += list(root.findall("./Score/Staff/Measure/voice/Harmony/name"))
    for harmony in harmonies:
        if harmony.text in ["^", "^7", "maj7"] and harmony.text != MAJ_7_SYMBOL:
            print(f"{tune}:  major seventh needs normalization")
            if args.write:
                harmony.text = MAJ_7_SYMBOL
                changed = True

    if args.write and changed:
        tree.write(mscx_path)
