#!/usr/bin/env python3
"""Deterministic local checks for AGE-600 synthetic demonstration media."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
MEDIA = ROOT / "assets" / "demo-media"

FILMS = [
    {
        "slug": "sitelog",
        "source": "sitelog-demo.mp4",
        "poster": "sitelog-poster.jpg",
        "captions": "sitelog-demo.vtt",
        "sha256": "f91d00ff10fb5b5159ad8ffe3a2ea277f6d55da0dfe17b9492c6469a32eb0e51",
        "duration": 91.4,
        "preserve": True,
    },
    {
        "slug": "budgetflow",
        "source": "budgetflow-demo.mp4",
        "poster": "budgetflow-poster.jpg",
        "captions": "budgetflow-demo.vtt",
        "sha256": "dda5c8ac812c5dce7a33a0d3ec22296e552087ec38a8626bd79e00a9d485ed62",
        "duration": 126.9,
        "preserve": True,
    },
    {
        "slug": "ledgerlink",
        "source": "ledgerlink-demo.mp4",
        "poster": "ledgerlink-poster.jpg",
        "captions": "ledgerlink-demo.vtt",
        "sha256": "43ab2ade873b68ddde8b95fa528e944014d6de7ab7bffe70ca56eccc7c6089b7",
        "duration": 109.3,
        "master": "tools/demo-film-narrative/source/ledgerlink-demo.mp4",
        "master_sha256": "2123f74adf316d22b0efbaff6c7cfced227ba0c0850c58be572cb1c760c3db02",
    },
    {
        "slug": "cpr",
        "source": "cpr-demo.mp4",
        "poster": "cpr-poster.jpg",
        "captions": "cpr-demo.vtt",
        "sha256": "ca066cfd62834562bcc000cb501172047600a4356b68613ff13e97aec3f748af",
        "duration": 18.6,
    },
    {
        "slug": "applications-ledger",
        "source": "applications-ledger-demo.mp4",
        "poster": "applications-ledger-poster.jpg",
        "captions": "applications-ledger-demo.vtt",
        "sha256": "b6c31c1c92467a7dd6216e82e6d775536005abfedeca35e89fab83af02435848",
        "duration": 130.7,
        "master": "tools/demo-film-narrative/source/applications-ledger-demo.mp4",
        "master_sha256": "e63d2c36dca58e3f5b234e3c9ff9e8819d129edbd05c72bcecb2317a8035598a",
    },
    {
        "slug": "cashflow",
        "source": "cashflow-demo.mp4",
        "poster": "cashflow-poster.jpg",
        "captions": "cashflow-demo.vtt",
        "sha256": "d49f68443d16be845e194653c0393dc3b175aa41bd335e77cc4046ae213a7d61",
        "duration": 78.7,
        "master": "tools/demo-film-narrative/source/cashflow-demo.mp4",
        "master_sha256": "769e9b44cf7c97ec565c52938c1b194e14eed97e49d65bcdb8c34fedf11c109f",
    },
    {
        "slug": "probables",
        "source": "probables-demo.mp4",
        "poster": "probables-poster.jpg",
        "captions": "probables-demo.vtt",
        "sha256": "647300de26440d2afa33ae0b64a5e7ccd4a04a0909f72f906c5726a1377dfc63",
        "duration": 58.1,
    },
    {
        "slug": "management-accounts",
        "source": "management-accounts-demo.mp4",
        "poster": "management-accounts-poster.jpg",
        "captions": "management-accounts-demo.vtt",
        "sha256": "b68377a7019155b19adec19756534104fed9d8700a1b36ec1b48664bc7db9358",
        "duration": 53.9,
        "master": "tools/demo-film-narrative/source/management-accounts-demo.mp4",
        "master_sha256": "38bbe17c361e4252ed288f0df095236394cb9b4402b6c74941bd19ba1c67df9c",
    },
]

PRESERVED_POSTERS = {
    "sitelog-poster.jpg": "4022b4b2829dc32d004bfdd10c9dc0297fad5a353545832cc6dea5a1cf028a40",
    "budgetflow-poster.jpg": "1af478e41bf80428b75aa9fcda6b9c3b469ec997b8189875c863a19e4f513162",
}

TEASERS = [
    "sitelog-teaser.mp4",
    "budgetflow-teaser.mp4",
    "ledgerlink-teaser.mp4",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def exact_case_file(rel: str) -> bool:
    current = ROOT
    for part in pathlib.PurePosixPath(rel).parts:
        try:
            names = os.listdir(current)
        except FileNotFoundError:
            return False
        if part not in names:
            return False
        current = current / part
    return current.is_file()


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path: pathlib.Path) -> dict[str, str]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {}
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name,width,height",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1",
        str(path),
    ]
    output = subprocess.check_output(command, text=True)
    data: dict[str, str] = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key] = value
    return data


def has_audio(path: pathlib.Path) -> bool:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return False
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "csv=p=0",
        str(path),
    ]
    return bool(subprocess.check_output(command, text=True).strip())


def parse_vtt_timestamp(token: str) -> float:
    stamp = token.strip().split()[0]
    parts = stamp.split(":")
    if len(parts) == 2:
        hours = 0
        minutes, rest = parts
    elif len(parts) == 3:
        hours, minutes, rest = parts
    else:
        raise ValueError(f"unrecognised VTT timestamp {token!r}")
    seconds, millis = rest.split(".")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def vtt_cue_ends(text: str) -> list[tuple[float, float]]:
    cues: list[tuple[float, float]] = []
    for line in text.splitlines():
        if " --> " not in line:
            continue
        start_token, end_token = line.split(" --> ", 1)
        cues.append((parse_vtt_timestamp(start_token), parse_vtt_timestamp(end_token)))
    return cues


def check_vtt(path: pathlib.Path, duration: float, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("WEBVTT"):
        fail(f"{path.name} is not a WebVTT file", failures)
        return
    try:
        cues = vtt_cue_ends(text)
    except ValueError as exc:
        fail(f"{path.name}: {exc}", failures)
        return
    if not cues:
        fail(f"{path.name} has no timed cues", failures)
        return
    previous_end = 0.0
    for start, end in cues:
        if start < 0 or end <= start:
            fail(f"{path.name}: invalid cue {start:.3f} --> {end:.3f}", failures)
        if start + 0.001 < previous_end:
            fail(f"{path.name}: cues overlap or run backwards at {start:.3f}", failures)
        if end - duration > 0.2:
            fail(f"{path.name}: cue ends at {end:.3f}s beyond duration {duration:.3f}s", failures)
        previous_end = end
    if path.name == "ledgerlink-demo.vtt" and "connection to accounts software" not in text:
        fail("ledgerlink-demo.vtt must describe the connection to accounts software", failures)


def load_render_module():
    path = ROOT / "tools" / "demo-film-narrative" / "render_narrative.py"
    spec = importlib.util.spec_from_file_location("demo_film_narrative", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["demo_film_narrative"] = module
    spec.loader.exec_module(module)
    return module


def check_callout_clearance(failures: list[str]) -> None:
    module = load_render_module()
    if module is None:
        fail("unable to load tools/demo-film-narrative/render_narrative.py", failures)
        return
    for film in module.FILMS:
        for cue in film.cues:
            _box_w, box_h = module.box_size(cue)
            if cue.y + box_h > module.CONTROL_CLEAR_Y:
                fail(
                    f"{film.slug} {cue.kicker} occupies y={cue.y}-{cue.y + box_h}, "
                    f"enters native-control band y>={module.CONTROL_CLEAR_Y}",
                    failures,
                )


def check_publish_package(failures: list[str]) -> None:
    prepare = ROOT / "tools" / "prepare_publish.py"
    if not prepare.is_file():
        fail("missing tools/prepare_publish.py", failures)
        return
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "publish"
        try:
            subprocess.run(
                [sys.executable, str(prepare), "--out", str(out)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            fail("tools/prepare_publish.py failed", failures)
            return
        media = out / "assets" / "demo-media"
        for film in FILMS:
            for name in (film["source"], film["poster"], film["captions"]):
                if not (media / name).is_file():
                    fail(f"publish package missing assets/demo-media/{name}", failures)
        for teaser in TEASERS:
            if not (media / teaser).is_file():
                fail(f"publish package missing assets/demo-media/{teaser}", failures)
        forbidden = [
            out / "assets" / "demo-media" / "source",
            out / "assets" / "demo-media" / "render_narrative.py",
            out / "tools",
            out / "docs" / "age-601-film-review",
        ]
        for path in forbidden:
            if path.exists():
                fail(f"publish package must not contain {path.relative_to(out)}", failures)
        for slug in ("applications-ledger", "ledgerlink", "cashflow", "management-accounts"):
            if (media / "source" / f"{slug}-demo.mp4").exists():
                fail(f"publish package contains duplicate source master {slug}", failures)


def check() -> int:
    failures: list[str] = []
    if not MEDIA.is_dir():
        print("FAIL assets/demo-media is missing")
        return 1

    for film in FILMS:
        source_rel = f"assets/demo-media/{film['source']}"
        poster_rel = f"assets/demo-media/{film['poster']}"
        caption_rel = f"assets/demo-media/{film['captions']}"
        for rel in (source_rel, poster_rel, caption_rel):
            if not exact_case_file(rel):
                fail(f"missing media file with exact case: {rel}", failures)
        source = ROOT / source_rel
        duration = film["duration"]
        if source.is_file():
            digest = sha256_file(source)
            if digest != film["sha256"]:
                fail(f"{source_rel} hash mismatch: {digest}", failures)
            info = probe(source)
            if info:
                if info.get("codec_name") != "h264":
                    fail(f"{film['source']}: expected h264, got {info.get('codec_name')}", failures)
                if info.get("width") != "1280" or info.get("height") != "720":
                    fail(
                        f"{film['source']}: expected 1280x720, got {info.get('width')}x{info.get('height')}",
                        failures,
                    )
                try:
                    duration = float(info["duration"])
                except (KeyError, ValueError):
                    fail(f"{film['source']}: duration missing from probe", failures)
                else:
                    if abs(duration - film["duration"]) > 0.2:
                        fail(
                            f"{film['source']}: duration {duration:.3f}s != {film['duration']}",
                            failures,
                        )
                if has_audio(source):
                    fail(f"{film['source']}: public film must remain silent", failures)
            elif not shutil.which("ffprobe"):
                fail("ffprobe is not available to probe codec, dimensions and duration", failures)
        if film.get("master"):
            master_rel = film["master"]
            if not exact_case_file(master_rel):
                fail(f"missing preserved source master: {master_rel}", failures)
            else:
                master_digest = sha256_file(ROOT / master_rel)
                if master_digest != film["master_sha256"]:
                    fail(f"{master_rel} hash mismatch: {master_digest}", failures)
        poster = ROOT / poster_rel
        if poster.is_file() and film["poster"] in PRESERVED_POSTERS:
            digest = sha256_file(poster)
            if digest != PRESERVED_POSTERS[film["poster"]]:
                fail(f"{poster_rel} preserved poster hash mismatch: {digest}", failures)
        captions = ROOT / caption_rel
        if captions.is_file():
            check_vtt(captions, duration, failures)

    render_script = ROOT / "tools" / "demo-film-narrative" / "render_narrative.py"
    if not render_script.is_file():
        fail("missing tools/demo-film-narrative/render_narrative.py", failures)
    if (MEDIA / "render_narrative.py").exists():
        fail("render tooling must not live under assets/demo-media", failures)
    if (MEDIA / "source").exists():
        fail("preserved source masters must not live under assets/demo-media", failures)
    check_callout_clearance(failures)

    check_publish_package(failures)

    for teaser in TEASERS:
        rel = f"assets/demo-media/{teaser}"
        if not exact_case_file(rel):
            fail(f"missing teaser: {rel}", failures)
            continue
        info = probe(ROOT / rel)
        if info:
            if info.get("codec_name") != "h264":
                fail(f"{teaser}: expected h264", failures)
            try:
                duration = float(info["duration"])
            except (KeyError, ValueError):
                fail(f"{teaser}: duration missing", failures)
            else:
                if duration > 6.5:
                    fail(f"{teaser}: teaser too long ({duration:.3f}s)", failures)
        size = (ROOT / rel).stat().st_size
        if size > 400_000:
            fail(f"{teaser}: teaser larger than 400KB ({size})", failures)

    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS eight synthetic films, exact master hashes, preserved sources "
        "outside the public tree, posters, duration-bounded VTT files, "
        "short homepage teasers and publish-package exclusions"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
