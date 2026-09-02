#!/usr/bin/env python3
"""Composite composition-aware stage callouts onto the four denser demo films.

Public masters for Applications Ledger, LedgerLink and Cashflow are
rebuilt into ``assets/demo-media/`` from the preserved AGE-600 sources in
``source/``. The withdrawn Management Accounts rendition is rebuilt into
``retained-withdrawn/management-accounts/``. SiteLog, BudgetFlow, CPR and
Probables are not re-encoded.

Callouts sit above the native player-control band. On the story page the
film is 46rem wide on desktop (828×466 at 18px root) and wrap-width on a
390px phone (342×192). A 54px native control bar then covers the bottom
83px (desktop) or 202px (phone) of the 720p master. No callout pixel may
sit at y>=500.

Usage from the repository root:
    python3 tools/demo-film-narrative/render_narrative.py preview
    python3 tools/demo-film-narrative/render_narrative.py render
    python3 tools/demo-film-narrative/render_narrative.py review
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

TOOL_ROOT = Path(__file__).resolve().parent
REPO = TOOL_ROOT.parent.parent
PUBLIC_MEDIA = REPO / "assets" / "demo-media"
SOURCE_DIR = TOOL_ROOT / "source"
REVIEW_DIR = TOOL_ROOT / "review"
RETAINED_MEDIA = TOOL_ROOT / "retained-withdrawn"
WITHDRAWN_SLUGS = frozenset({"management-accounts"})
FONT_PATH = Path("/System/Library/Fonts/HelveticaNeue.ttc")

WIDTH = 1280
HEIGHT = 720
FILL = (18, 16, 14, 236)
BORDER = (216, 144, 66, 255)
KICKER_COLOUR = (216, 144, 66, 255)
LINE_COLOUR = (247, 241, 232, 255)
RADIUS = 14
PAD_X = 24
PAD_TOP = 14
PAD_BOTTOM = 14
KICKER_SIZE = 12
LINE_SIZE = 22
KICKER_LINE_GAP = 8
TRACKING = 2.0
# Native controls at 390px cover ~202px of the 720p master. Keep callouts above.
CONTROL_CLEAR_Y = 500


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    kicker: str
    line: str
    x: int
    y: int


@dataclass(frozen=True)
class Film:
    slug: str
    cues: tuple[Cue, ...]


FILMS: tuple[Film, ...] = (
    Film(
        "applications-ledger",
        (
            Cue(4.20, 7.40, "LIVE CONTRACTS", "Status and a route into each ledger", 248, 430),
            Cue(8.20, 13.80, "CONTRACT LEDGER", "Application, certification, payment and retention", 24, 430),
            Cue(108.80, 113.80, "FINANCE VIEW", "Attention queue for cash and retention", 248, 380),
            Cue(119.50, 123.80, "FORECAST HYGIENE", "Missing or stale forecasts", 248, 280),
        ),
    ),
    Film(
        "ledgerlink",
        (
            Cue(47.20, 51.50, "OVERHEAD ACTUALS", "Period transaction listing", 900, 370),
            Cue(69.05, 70.80, "RETENTION BY PROJECT", "Held and released from the same extract", 40, 392),
        ),
    ),
    Film(
        "cashflow",
        (
            Cue(8.20, 18.40, "COMMERCIAL FINANCE", "Short-term and long-term cashflow", 40, 430),
            Cue(27.00, 34.00, "SHORT-TERM", "Funding events and daily cash", 40, 400),
            Cue(38.40, 48.00, "COST-VALUE", "Project schedule feeding the longer view", 40, 128),
        ),
    ),
    Film(
        "management-accounts",
        (
            Cue(6.40, 10.80, "MONTHLY PACK", "Open the reporting workbook", 700, 400),
            Cue(14.60, 18.20, "PROFIT AND LOSS", "Current year, budget and forecast", 40, 132),
            Cue(22.60, 33.80, "LIVE PROJECTS", "Turnover and gross margin by region", 40, 400),
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


def box_size(cue: Cue) -> tuple[int, int]:
    probe = ImageDraw.Draw(Image.new("RGBA", (WIDTH, HEIGHT)))
    kicker_face = font(KICKER_SIZE, 10)
    line_face = font(LINE_SIZE, 0)
    inner_w = max(
        tracked_width(probe, cue.kicker.upper(), kicker_face, TRACKING),
        probe.textlength(cue.line, font=line_face),
    )
    box_w = int(inner_w + PAD_X * 2)
    box_h = PAD_TOP + KICKER_SIZE + KICKER_LINE_GAP + LINE_SIZE + PAD_BOTTOM
    return box_w, box_h


def render_overlay(cue: Cue) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    kicker_face = font(KICKER_SIZE, 10)
    line_face = font(LINE_SIZE, 0)
    kicker = cue.kicker.upper()
    box_w, box_h = box_size(cue)
    x, y = cue.x, cue.y
    if x < 16 or y < 16:
        fail(f"callout too close to the edge for {cue.kicker}")
    if x + box_w > WIDTH - 16:
        fail(f"callout too wide for {cue.kicker}: {box_w}px at x={x}")
    if y + box_h > CONTROL_CLEAR_Y:
        fail(
            f"callout for {cue.kicker} occupies y={y}-{y + box_h}, "
            f"which enters the native-control band (y>={CONTROL_CLEAR_Y})"
        )
    draw.rounded_rectangle(
        (x, y, x + box_w, y + box_h),
        radius=RADIUS,
        fill=FILL,
        outline=BORDER,
        width=1,
    )
    draw_tracked(draw, (x + PAD_X, y + PAD_TOP), kicker, kicker_face, KICKER_COLOUR, TRACKING)
    draw.text(
        (x + PAD_X, y + PAD_TOP + KICKER_SIZE + KICKER_LINE_GAP),
        cue.line,
        font=line_face,
        fill=LINE_COLOUR,
    )
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
    return PUBLIC_MEDIA / f"{slug}-demo.mp4"


def film_path(slug: str) -> Path:
    if slug in WITHDRAWN_SLUGS:
        return RETAINED_MEDIA / slug / f"{slug}-demo.mp4"
    return public_path(slug)


def ffmpeg_bin() -> str:
    binary = shutil.which("ffmpeg")
    if not binary:
        fail("ffmpeg is not available")
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
            dest = REVIEW_DIR / f"{film.slug}-callout-{index:02d}.jpg"
            composite_preview(film.slug, cue, dest)
            print(f"wrote {dest.relative_to(REPO)}")


def render_film(film: Film) -> None:
    source = source_path(film.slug)
    dest = film_path(film.slug)
    dest.parent.mkdir(parents=True, exist_ok=True)
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
        video = film_path(film.slug)
        extract_frame(video, 0.5, REVIEW_DIR / f"{film.slug}-stage-title.jpg")
        for index, cue in enumerate(film.cues, start=1):
            dest = REVIEW_DIR / f"{film.slug}-callout-{index:02d}.jpg"
            extract_frame(video, (cue.start + cue.end) / 2, dest)
            print(f"wrote {dest.relative_to(REPO)}")
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
    control_proof(films)


# Story-page video sizes: 46rem at 18px root on desktop, wrap-width on a 390px phone.
DESKTOP_VIDEO = (828, 466)
PHONE_VIDEO = (342, 192)
CONTROL_BAR_PX = 48


def draw_native_controls(video: Image.Image, current_s: float, duration_s: float) -> Image.Image:
    """Paint a Chrome-sized native control overlay onto a displayed video frame."""
    width, height = video.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bar_top = height - CONTROL_BAR_PX
    fade = 10
    for index in range(fade):
        alpha = int(160 * ((index + 1) / fade))
        y = bar_top - fade + index
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    draw.rectangle((0, bar_top, width, height), fill=(20, 20, 20, 235))
    margin = 10
    rail_y = bar_top + 7
    draw.rounded_rectangle((margin, rail_y, width - margin, rail_y + 4), radius=2, fill=(180, 180, 180, 180))
    played = margin + int((width - margin * 2) * min(current_s / duration_s, 1.0))
    draw.rounded_rectangle((margin, rail_y, played, rail_y + 4), radius=2, fill=(255, 255, 255, 255))
    draw.ellipse((played - 5, rail_y - 3, played + 5, rail_y + 7), fill=(255, 255, 255, 255))
    icon_y = bar_top + 22
    # Play triangle
    draw.polygon([(14, icon_y), (14, icon_y + 16), (28, icon_y + 8)], fill=(255, 255, 255, 255))
    try:
        face = font(12 if width > 400 else 10, 0)
    except SystemExit:
        face = ImageFont.load_default()
    current = f"{int(current_s // 60)}:{int(current_s % 60):02d}"
    duration = f"{int(duration_s // 60)}:{int(duration_s % 60):02d}"
    draw.text((36, icon_y + 1), f"{current} / {duration}", font=face, fill=(255, 255, 255, 255))
    # Volume, captions, overflow, fullscreen on the right
    right = width - 14
    draw.rectangle((right - 14, icon_y + 2, right - 2, icon_y + 14), outline=(255, 255, 255, 255), width=1)
    draw.line([(right - 8, icon_y + 2), (right - 8, icon_y - 2)], fill=(255, 255, 255, 255))
    right -= 28
    draw.text((right - 18, icon_y), "CC", font=face, fill=(255, 255, 255, 230))
    right -= 36
    draw.polygon(
        [(right - 10, icon_y + 4), (right, icon_y + 8), (right - 10, icon_y + 12)],
        fill=(255, 255, 255, 230),
    )
    draw.polygon(
        [(right - 16, icon_y + 6), (right - 10, icon_y + 8), (right - 16, icon_y + 10)],
        fill=(255, 255, 255, 230),
    )
    composed = Image.alpha_composite(video.convert("RGBA"), overlay)
    return composed.convert("RGB")


def page_frame(video: Image.Image, viewport: tuple[int, int], title: str) -> Image.Image:
    """Place the displayed video on a story-page-sized dark canvas."""
    vw, vh = viewport
    page = Image.new("RGB", viewport, (10, 11, 13))
    draw = ImageDraw.Draw(page)
    try:
        kicker_face = font(11, 10)
        title_face = font(28 if vw > 800 else 22, 0)
        meta_face = font(12, 0)
    except SystemExit:
        kicker_face = title_face = meta_face = ImageFont.load_default()
    pad = 24 if vw > 800 else 24
    x = (vw - video.size[0]) // 2
    draw.text((x, 28), "SYNTHETIC DEMONSTRATION", font=kicker_face, fill=(216, 144, 66))
    draw.text((x, 48), title, font=title_face, fill=(243, 238, 228))
    draw.text((x, 84), "Synthetic demonstration  ·  native controls open", font=meta_face, fill=(170, 166, 158))
    page.paste(video, (x, 110))
    return page


def control_proof(films: tuple[Film, ...] = FILMS) -> None:
    durations = {
        "applications-ledger": 130.7,
        "ledgerlink": 109.3,
        "cashflow": 78.7,
        "management-accounts": 53.9,
    }
    titles = {
        "applications-ledger": "Applications Ledger",
        "ledgerlink": "LedgerLink",
        "cashflow": "Cashflow",
        "management-accounts": "Management Accounts",
    }
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for film in films:
            video = film_path(film.slug)
            for index, cue in enumerate(film.cues, start=1):
                time_s = (cue.start + cue.end) / 2
                raw = tmp_path / f"{film.slug}-{index}.jpg"
                extract_frame(video, time_s, raw)
                master = Image.open(raw).convert("RGB")
                if master.size != (WIDTH, HEIGHT):
                    fail(f"{film.slug} review frame {master.size}")
                for label, size in (("desktop", DESKTOP_VIDEO), ("phone", PHONE_VIDEO)):
                    scaled = master.resize(size, Image.Resampling.LANCZOS)
                    controlled = draw_native_controls(scaled, time_s, durations[film.slug])
                    viewport = (1440, 900) if label == "desktop" else (390, 844)
                    page = page_frame(controlled, viewport, titles[film.slug])
                    dest = REVIEW_DIR / f"{film.slug}-callout-{index:02d}-controls-{label}.jpg"
                    page.save(dest, quality=90, optimize=True)
                    print(f"wrote {dest.relative_to(REPO)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preview", "render", "review", "controls"))
    parser.add_argument("--slug", action="append", dest="slugs", help="Limit to one or more film slugs")
    args = parser.parse_args()
    selected = tuple(film for film in FILMS if not args.slugs or film.slug in args.slugs)
    if args.slugs and len(selected) != len(set(args.slugs)):
        fail(f"unknown slug in {args.slugs}")
    if args.command == "preview":
        preview(selected)
    elif args.command == "render":
        render(selected)
    elif args.command == "controls":
        control_proof(selected)
    else:
        review_frames(selected)
    return 0


if __name__ == "__main__":
    sys.exit(main())
