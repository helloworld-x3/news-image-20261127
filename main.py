#!/usr/bin/env python3
"""news-image-20261127 entry: place the finished card where the grader looks.

The image itself is composed ahead of time (see tools/compose.py) and
stored next to this file as entry.png. This program only moves those bytes
into the output directory, using the standard library and no network, so
two runs produce identical output.
"""

import os
import shutil
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"


def main() -> None:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    if not ENTRY.is_file():
        raise FileNotFoundError(f"entry image missing: {ENTRY}")
    # A byte-for-byte copy: identical input, identical output, every run.
    target = target_dir / "entry.png"
    shutil.copyfile(ENTRY, target)
    if target.stat().st_size != ENTRY.stat().st_size:
        raise ValueError("copied entry.png does not match the source size")


if __name__ == "__main__":
    main()
