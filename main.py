#!/usr/bin/env python3
"""Entry point: copy the pre-rendered poster to the output directory.

Standard library only. The poster itself is drawn by compose_poster.py
during development; this program just copies the bundled entry.png so
the sandboxed run is deterministic and needs no fonts or network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
