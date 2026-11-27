#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261127 (Python 3.13, stdlib only).

Copies the entry image beside this file to the output directory as
entry.png. The program runs with no network, so it only copies bytes it
already holds; running it twice writes the same bytes both times.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError(f"entry image missing: {src}")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
