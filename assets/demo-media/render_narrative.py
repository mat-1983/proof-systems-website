#!/usr/bin/env python3
"""Composite composition-aware stage callouts onto the four denser demo films.

The public masters for Applications Ledger, LedgerLink, Cashflow and
Management Accounts are rebuilt from the preserved AGE-600 sources in
``source/``. SiteLog, BudgetFlow, CPR and Probables are not re-encoded.

Usage:
    python3 assets/demo-media/render_narrative.py preview
    python3 assets/demo-media/render_narrative.py render
    python3 assets/demo-media/render_narrative.py review
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
SOURCE_DIR = ROOT / "source"
REVIEW_DIR = REPO / "docs" / "age-601-film-review"
FONT_PATH = Path("/System/Library/Fonts/HelveticaNeue.ttc")

WIDTH = 1280
HEIGHT = 720
FILL = (18, 16, 14, 236)
BORDER = (216, 144, 66, 255)
KICKER_COLOUR = (216, 144, 66, 255)
LINE_COLOUR = (247, 241, 232, 255)
RADIUS = 16
PAD_X = 28
PAD_TOP = 18
PAD_BOTTOM = 20
KICKER_SIZE = 13
LINE_SIZE = 26
TRACKING = 2.2

STANDARD_Y = 588
ABOVE_TABS_Y = 546
LEFT_X = 32


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    kicker: str
    line: str
    placement: str = "standard"


@dataclass(frozen=True)
class Film:
    slug: str
    cues: tuple[Cue, ...]


FILMS: tuple[Film, ...] = (
    Film(
        "applications-ledger",
        (
            Cue(4.20, 7.40, "LIVE CONTRACTS", "Status and a route into each ledger"),
            Cue(8.20, 13.80, "CONTRACT LEDGER", "Application, certification, payment and retention"),
            Cue(108.80, 113.80, "FINANCE VIEW", "Attention queue for cash and retention"),
            Cue(119.50, 123.80, "FORECAST HYGIENE", "Missing or stale forecasts"),
        ),
    ),
    Film(
        "ledgerlink",
        (
            Cue(47.20, 51.50, "OVERHEAD ACTUALS", "Period transaction listing", "above_tabs"),
            Cue(69.05, 70.80, "RETENTION BY PROJECT", "Held and released from the same extract", "above_tabs"),
        ),
    ),
    Film(
        "cashflow",
        (
            Cue(8.20, 18.40, "COMMERCIAL FINANCE", "Short-term and long-term cashflow"),
            Cue(27.00, 34.00, "SHORT-TERM", "Funding events and daily cash", "above_tabs"),
            Cue(38.40, 48.00, "COST-VALUE", "Project schedule feeding the longer view", "above_tabs"),
        ),
    ),
    Film(
        "management-accounts",
        (
            Cue(6.40, 10.80, "MONTHLY PACK", "Open the reporting workbook"),
            Cue(14.60, 18.20, "PROFIT AND LOSS", "Current year, budget and forecast", "above_tabs"),
            Cue(22.60, 33.80, "LIVE PROJECTS", "Turnover and gross margin by region", "above_tabs"),
        ),
    ),
)


def fail(message: str) -> None:
    print(f"FAIL {message}", file=sys.stderr)
    raise SystemExit(1)


def font(size: int, index: int) -> ImageFont.FreeTypeFont:
    if not FONT_PATH.is_file():
        fail(f"missing system font {FONT_PATH}")
    return ImageFont.truetype(str(FONT_PATH), size=size, index=index)


def tracked_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, tracking: float) -> float:
    if not text:
        return 0.0
    width = 0.0
    for index, char in enumerate(text):
        width += draw.textlength(char, font=face)
        if index < len(text) - 1:
            width += tracking
    return width


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: float,
) -> None:
    x, y = xy
    for index, char in enumerate(text):
        draw.text((x, y), char, font=face, fill=fill)
        x += draw.textlength(char, font=face)
        if index < len(text) - 1:
            x += tracking


def cue_y(placement: str) -> int:
    if placement == "above_tabs":
        return ABOVE_TABS_Y
    if placement == "standard":
        return STANDARD_Y
    fail(f"unknown placement {placement}")
    return STANDARD_Y


def render_overlay(cue: Cue) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    kicker_face = font(KICKER_SIZE, 10)
    line_face = font(LINE_SIZE, 0)
    kicker = cue.kicker.upper()
    kicker_w = tracked_width(draw, kicker, kicker_face, TRACKING)
    line_w = draw.textlength(cue.line, font=line_face)
    inner_w = max(kicker_w, line_w)
    box_w = int(inner_w + PAD_X * 2)
    box_h = PAD_TOP + KICKER_SIZE + 10 + LINE_SIZE + PAD_BOTTOM
    x = LEFT_X
    y = cue_y(cue.placement)
    if x + box_w > WIDTH - 24:
        fail(f"callout too wide for {cue.kicker}: {box_w}px")
    if y + box_h > HEIGHT - 20:
        fail(f"callout too tall for {cue.kicker}")
    draw.rounded_rectangle(
        (x, y, x + box_w, y + box_h),
        radius=RADIUS,
        fill=FILL,
        outline=BORDER,
        width=1,
    )
    draw_tracked(draw, (x + PAD_X, y + PAD_TOP), kicker, kicker_face, KICKER_COLOUR, TRACKING)
    draw.text((x + PAD_X, y + PAD_TOP + KICKER_SIZE + 10), cue.line, font=line_face, fill=LINE_COLOUR)
    return image


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_path(slug: str) -> Path:
    path = SOURCE_DIR / f"{slug}-demo.mp4"
    if not path.is_file():
        fail(f"missing preserved source {path.relative_to(REPO)}")
    return path


def public_path(slug: str) -> Path:
    return ROOT / f"{slug}-demo.mp4"


def ffmpeg_bin() -> str:
    binary = shutil.which("ffmpeg")
    if not binary:
        fail("ffmpeg is not available")
    return binary


def ffprobe_bin() -> str:
    binary = shutil.which("ffprobe")
    if not binary:
        fail("ffprobe is not available")
    return binary


def extract_frame(video: Path, time_s: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg_bin(),
        "-y",
        "-ss",
        f"{time_s:.3f}",
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-q:v",
        "3",
        str(dest),
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def composite_preview(slug: str, cue: Cue, dest: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        frame_path = Path(tmp) / "frame.jpg"
        extract_frame(source_path(slug), (cue.start + cue.end) / 2, frame_path)
        base = Image.open(frame_path).convert("RGBA")
        if base.size != (WIDTH, HEIGHT):
            fail(f"{slug} frame size {base.size} != {WIDTH}x{HEIGHT}")
        overlay = render_overlay(cue)
        composed = Image.alpha_composite(base, overlay).convert("RGB")
        dest.parent.mkdir(parents=True, exist_ok=True)
        composed.save(dest, quality=90, optimize=True)


def preview(films: tuple[Film, ...] = FILMS) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for film in films:
        for index, cue in enumerate(film.cues, start=1):
            name = f"{film.slug}-callout-{index:02d}.jpg"
            dest = REVIEW_DIR / name
            composite_preview(film.slug, cue, dest)
            print(f"wrote {dest.relative_to(REPO)}")


def render_film(film: Film) -> None:
    source = source_path(film.slug)
    dest = public_path(film.slug)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        overlay_paths: list[Path] = []
        for index, cue in enumerate(film.cues, start=1):
            overlay = render_overlay(cue)
            path = tmp_path / f"{index:02d}.png"
            overlay.save(path)
            overlay_paths.append(path)
        command = [ffmpeg_bin(), "-y", "-i", str(source)]
        for path in overlay_paths:
            command.extend(["-i", str(path)])
        filters: list[str] = []
        last = "0:v"
        for index, cue in enumerate(film.cues, start=1):
            label = f"v{index}"
            filters.append(
                f"[{last}][{index}:v] overlay=0:0:format=auto:"
                f"enable='between(t,{cue.start:.3f},{cue.end:.3f})'[{label}]"
            )
            last = label
        command.extend(
            [
                "-filter_complex",
                ";".join(filters),
                "-map",
                f"[{last}]",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-profile:v",
                "high",
                "-level",
                "4.0",
                "-crf",
                "16",
                "-preset",
                "slow",
                "-movflags",
                "+faststart",
                "-fflags",
                "+bitexact",
                "-flags",
                "+bitexact",
                "-map_metadata",
                "-1",
                str(tmp_path / "out.mp4"),
            ]
        )
        subprocess.run(command, check=True)
        shutil.move(str(tmp_path / "out.mp4"), dest)
    print(f"rendered {dest.relative_to(REPO)} sha256={sha256_file(dest)}")


def render(films: tuple[Film, ...] = FILMS) -> None:
    for film in films:
        render_film(film)


def review_frames(films: tuple[Film, ...] = FILMS) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    preserved = (
        ("sitelog", (0.5, 8.0, 18.0, 32.0, 45.0, 54.0, 60.0, 70.0, 80.0)),
        ("budgetflow", (0.5, 8.0, 18.0, 32.0, 47.0, 55.0, 70.0, 100.0, 120.0)),
        ("cpr", (0.5, 6.0, 12.0, 16.0)),
        ("probables", (0.5, 12.0, 20.0, 30.0, 45.0, 55.0)),
    )
    for slug, times in preserved:
        video = public_path(slug)
        if not video.is_file():
            fail(f"missing {video.relative_to(REPO)}")
        for index, time_s in enumerate(times, start=1):
            dest = REVIEW_DIR / f"{slug}-stage-{index:02d}.jpg"
            extract_frame(video, time_s, dest)
            print(f"wrote {dest.relative_to(REPO)}")
    for film in films:
        video = public_path(film.slug)
        extract_frame(video, 0.5, REVIEW_DIR / f"{film.slug}-stage-title.jpg")
        for index, cue in enumerate(film.cues, start=1):
            dest = REVIEW_DIR / f"{film.slug}-callout-{index:02d}.jpg"
            extract_frame(video, (cue.start + cue.end) / 2, dest)
            print(f"wrote {dest.relative_to(REPO)}")
        # Mid-stage frames without a callout, to show the interface is clear.
        clear_times = {
            "applications-ledger": (28.0, 50.0, 70.0, 90.0, 104.0, 125.0),
            "ledgerlink": (8.0, 16.0, 32.0, 71.0, 90.0),
            "cashflow": (12.0, 62.0, 75.0),
            "management-accounts": (12.0, 42.0, 50.0),
        }
        for index, time_s in enumerate(clear_times[film.slug], start=1):
            dest = REVIEW_DIR / f"{film.slug}-clear-{index:02d}.jpg"
            extract_frame(video, time_s, dest)
            print(f"wrote {dest.relative_to(REPO)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preview", "render", "review"))
    parser.add_argument("--slug", action="append", dest="slugs", help="Limit to one or more film slugs")
    args = parser.parse_args()
    selected = tuple(film for film in FILMS if not args.slugs or film.slug in args.slugs)
    if args.slugs and len(selected) != len(set(args.slugs)):
        fail(f"unknown slug in {args.slugs}")
    if args.command == "preview":
        preview(selected)
    elif args.command == "render":
        render(selected)
    else:
        review_frames(selected)
    return 0


if __name__ == "__main__":
    sys.exit(main())
