#!/usr/bin/env python3

import argparse
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

SCORES_DIR = Path("scores")
TUNES_DIR = Path("content") / "songs"

COPYRIGHT_LINE = "U.S. public domain - freedjazz.org"

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--write", action="store_true")
args = parser.parse_args()

for tune in os.listdir(SCORES_DIR):
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

    # TODO lint composer and lyricist

    subtitle = root.find("./Score/metaTag[@name='subtitle']")
    if (subtitle is not None) and subtitle.text == "Subtitle":
        print(f"{tune}: subtitle is '{subtitle.text}'")
        if args.write:
            subtitle.text = ""

    cw = root.find("./Score/metaTag[@name='copyright']")
    if cw.text != COPYRIGHT_LINE:
        print(f"{tune}: wrong copyright line")
        if args.write:
            cw.text = COPYRIGHT_LINE

    if args.write:
        tree.write(mscx_path)
