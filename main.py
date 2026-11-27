#!/usr/bin/env python3
"""THE WORLD — 26 November 2026.

Runtime entrypoint: copies the pre-rendered front page (entry.png,
drawn at build time by draw.py) to the grader's output directory.

Deliberately stdlib-only. The grader's pinned Python 3.13 runtime has
no third-party imaging library and no system fonts, so nothing here
may import a third-party package: the front page is drawn once by the
developer (draw.py + the vendored DejaVu fonts in fonts/) and shipped
in this repository as entry.png. Every run therefore writes exactly
the same bytes.

Output contract: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png),
a whole PNG, exactly 1024x1024, at most 1 MiB. Any deviation fails
loudly with a non-zero exit code instead of writing a bad file.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Read the IHDR chunk; raise unless it is a whole PNG."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    # Validate the committed source first: a corrupt entry.png must
    # fail fast with a clear message instead of being copied and then
    # failing the post-copy check with a misleading error.
    src_sha = sha256_file(SOURCE)
    src_width, src_height = png_dimensions(SOURCE)
    if (src_width, src_height) != (1024, 1024):
        raise SystemExit(
            f"committed entry.png is {src_width}x{src_height}, not 1024x1024")
    src_size = os.path.getsize(SOURCE)
    if src_size > MAX_BYTES:
        raise SystemExit(
            f"committed entry.png is {src_size} bytes, over the 1 MiB limit")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_file(dest) != src_sha:
        raise SystemExit("entry.png differs from the committed file")
    width, height = png_dimensions(dest)
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, not 1024x1024")
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    print(f"wrote {dest} {size} bytes, {width}x{height} PNG, "
          f"sha256 {sha256_file(dest)[:16]}...")


if __name__ == "__main__":
    sys.exit(main())
