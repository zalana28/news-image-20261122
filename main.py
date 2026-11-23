#!/usr/bin/env python3
"""Entrypoint: copy the pre-built poster to /output/entry.png.

Standard library only. No network, no randomness: two runs write the
same bytes, because entry.png is a fixed file in this repository.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
