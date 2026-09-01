#!/usr/bin/env python3
"""Build a production-shaped publish package of the static website.

The live Netlify site currently publishes the repository root. Files under
``tools/`` and review-only evidence are therefore ordinary static paths if
that root is uploaded. This script copies only the public site into a
publish directory so source masters, render tooling and review frames are
absent from the deploy-ready output.

Usage from the repository root:
    python3 tools/prepare_publish.py
    python3 tools/prepare_publish.py --out /tmp/proof-publish
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "publish"

ROOT_FILES = (
    "_redirects",
    "favicon.svg",
    "checkout.html",
    "index.html",
    "privacy.html",
    "training.html",
    "video-series.html",
    "workflow.html",
)

ROOT_DIRS = (
    "assets",
    "work",
)

EXCLUDED_UNDER_ASSETS = (
    Path("assets/demo-media/source"),
    Path("assets/demo-media/render_narrative.py"),
)


def copy_public(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for name in ROOT_FILES:
        src = ROOT / name
        if not src.is_file():
            raise SystemExit(f"missing public file {name}")
        shutil.copy2(src, out / name)
    for name in ROOT_DIRS:
        src = ROOT / name
        if not src.is_dir():
            raise SystemExit(f"missing public directory {name}")
        shutil.copytree(src, out / name, dirs_exist_ok=True)
    for rel in EXCLUDED_UNDER_ASSETS:
        target = out / rel
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = args.out if args.out.is_absolute() else (Path.cwd() / args.out)
    copy_public(out)
    print(f"wrote publish package {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
