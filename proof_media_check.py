#!/usr/bin/env python3
"""Deterministic local checks for AGE-590 homepage proof media."""

from __future__ import annotations

import hashlib
import html.parser
import os
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
WORKFLOW = ROOT / "workflow.html"
HTML_FILES = sorted(ROOT.glob("*.html"))

EXPECTED_VIDEOS = [
    {
        "title": "SiteLog",
        "poster": "assets/demo-media/sitelog-poster.jpg",
        "source": "assets/demo-media/sitelog-demo.mp4",
        "captions": "assets/demo-media/sitelog-demo.vtt",
        "sha256": {
            "assets/demo-media/sitelog-demo.mp4": "f91d00ff10fb5b5159ad8ffe3a2ea277f6d55da0dfe17b9492c6469a32eb0e51",
            "assets/demo-media/sitelog-poster.jpg": "4022b4b2829dc32d004bfdd10c9dc0297fad5a353545832cc6dea5a1cf028a40",
        },
    },
    {
        "title": "BudgetFlow",
        "poster": "assets/demo-media/budgetflow-poster.jpg",
        "source": "assets/demo-media/budgetflow-demo.mp4",
        "captions": "assets/demo-media/budgetflow-demo.vtt",
        "sha256": {
            "assets/demo-media/budgetflow-demo.mp4": "dda5c8ac812c5dce7a33a0d3ec22296e552087ec38a8626bd79e00a9d485ed62",
            "assets/demo-media/budgetflow-poster.jpg": "1af478e41bf80428b75aa9fcda6b9c3b469ec997b8189875c863a19e4f513162",
        },
    },
]

REQUIRED_PHRASES = [
    "Synthetic demonstration",
    "These are synthetic demonstrations of operator-built systems",
    "Construction is the evidence context, not a limit on the workflows this diagnostic can review",
    "SiteLog supplies the recurring weekly records, and BudgetFlow controls their downstream allocation and processing",
    "Tradespeople enter current-week site records",
    "Administrators keep the project and user controls and export the week",
    "Managers allocate weekly costs against project budgets",
    "Quantity surveyors control variations, quotes and overspends",
    "Accounts produce the payment exports",
    "Apply for a founding diagnostic",
]

REJECTED_PHRASES = [
    "Workforce and labour control",
    "Document-processing workflow",
    "Production systems, not demonstrations",
    "£350",
    "Pantera",
    "Northstar",
    "youtube",
    "vimeo",
]


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.stack: list[str] = []
        self.videos: list[dict] = []
        self.script_tags = 0
        self.proof_h3: list[str] = []
        self.proof_labels: list[str] = []
        self.refs: list[tuple[str, str]] = []
        self._in_proof = False
        self._in_proof_card = False
        self._capture: str | None = None
        self._capture_buf: list[str] = []
        self._current_video: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: (value or "") for key, value in attrs}
        classes = attr.get("class", "").split()
        if tag == "div" and "proof" in classes:
            self._in_proof = True
        if tag == "article" and self._in_proof:
            self._in_proof_card = True
        if tag == "script":
            self.script_tags += 1
        if tag == "h3" and self._in_proof_card:
            self._start_capture("h3")
        if tag == "p" and self._in_proof_card and "proof-label" in classes:
            self._start_capture("label")
        if tag == "video":
            video = {
                "attrs": attr,
                "sources": [],
                "tracks": [],
                "in_proof": self._in_proof,
            }
            self.videos.append(video)
            self._current_video = video
            if attr.get("poster"):
                self.refs.append(("poster", attr["poster"]))
            if attr.get("src"):
                self.refs.append(("video", attr["src"]))
        if tag == "source" and self._current_video is not None:
            self._current_video["sources"].append(attr)
            if attr.get("src"):
                self.refs.append(("source", attr["src"]))
        if tag == "track" and self._current_video is not None:
            self._current_video["tracks"].append(attr)
            if attr.get("src"):
                self.refs.append(("track", attr["src"]))
        if tag == "a" and attr.get("href"):
            self.refs.append(("href", attr["href"]))
        if tag == "img" and attr.get("src"):
            self.refs.append(("img", attr["src"]))
        if tag == "link" and attr.get("href"):
            self.refs.append(("link", attr["href"]))
        if tag not in {"meta", "link", "img", "br", "input", "hr", "source", "track"}:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h3", "p"} and self._capture:
            text = "".join(self._capture_buf).strip()
            if self._capture == "h3":
                self.proof_h3.append(text)
            elif self._capture == "label":
                self.proof_labels.append(text)
            self._capture = None
            self._capture_buf = []
        if tag == "video":
            self._current_video = None
        if tag == "article" and self._in_proof_card:
            self._in_proof_card = False
        if tag == "div" and self._in_proof and not self._in_proof_card:
            self._in_proof = False
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._capture_buf.append(data)

    def _start_capture(self, kind: str) -> None:
        self._capture = kind
        self._capture_buf = []


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def exact_case_file(root: pathlib.Path, rel: str) -> bool:
    current = root
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


def is_local_ref(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme in {"mailto", "https", "http"}:
        return False
    if value.startswith("#"):
        return False
    return True


def check_broken_references(failures: list[str]) -> None:
    for html_path in HTML_FILES:
        raw = html_path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(raw)
        parser.close()
        for kind, value in parser.refs:
            if not is_local_ref(value):
                if value.startswith("http://"):
                    fail(f"{html_path.name}: insecure URL {value}", failures)
                continue
            rel = urllib.parse.urlparse(value).path
            if not exact_case_file(ROOT, rel):
                fail(f"{html_path.name}: broken {kind} {value}", failures)


def check() -> int:
    failures: list[str] = []
    if not INDEX.is_file():
        print("FAIL index.html is missing")
        return 1

    raw = INDEX.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    if parser.stack:
        fail(f"unclosed tags: {parser.stack}", failures)

    videos = parser.videos
    if len(videos) != 2:
        fail(f"expected exactly 2 videos, got {len(videos)}", failures)
    if any(not video["in_proof"] for video in videos):
        fail("every video must be inside the operational-proof grid", failures)
    if parser.proof_h3 != ["SiteLog", "BudgetFlow"]:
        fail(f"expected proof titles SiteLog and BudgetFlow, got {parser.proof_h3}", failures)
    if parser.proof_labels != ["Synthetic demonstration", "Synthetic demonstration"]:
        fail(f"expected synthetic-demonstration labels on both cards, got {parser.proof_labels}", failures)
    if parser.script_tags:
        fail("index.html must not introduce JavaScript", failures)

    for expected, video in zip(EXPECTED_VIDEOS, videos):
        attrs = video["attrs"]
        if "controls" not in attrs:
            fail(f"{expected['title']}: missing controls", failures)
        if "playsinline" not in attrs:
            fail(f"{expected['title']}: missing playsinline", failures)
        if attrs.get("preload") != "metadata":
            fail(f"{expected['title']}: preload must be metadata, got {attrs.get('preload')!r}", failures)
        if "autoplay" in attrs:
            fail(f"{expected['title']}: autoplay is present", failures)
        if "loop" in attrs:
            fail(f"{expected['title']}: loop is present", failures)
        if attrs.get("poster") != expected["poster"]:
            fail(f"{expected['title']}: unexpected poster {attrs.get('poster')!r}", failures)
        sources = video["sources"]
        if len(sources) != 1 or sources[0].get("src") != expected["source"]:
            fail(f"{expected['title']}: unexpected source {sources}", failures)
        tracks = video["tracks"]
        if len(tracks) != 1:
            fail(f"{expected['title']}: expected one caption track, got {len(tracks)}", failures)
        else:
            track = tracks[0]
            if track.get("kind") != "captions":
                fail(f"{expected['title']}: track kind must be captions", failures)
            if track.get("src") != expected["captions"]:
                fail(f"{expected['title']}: unexpected caption path {track.get('src')!r}", failures)
            if not track.get("label"):
                fail(f"{expected['title']}: caption track needs a label", failures)
        for rel, digest in expected["sha256"].items():
            path = ROOT / rel
            if not exact_case_file(ROOT, rel):
                fail(f"missing media file with exact case: {rel}", failures)
                continue
            actual = sha256_file(path)
            if actual != digest:
                fail(f"{rel} hash mismatch: {actual}", failures)
        if not exact_case_file(ROOT, expected["captions"]):
            fail(f"missing caption file with exact case: {expected['captions']}", failures)
        else:
            caption_text = (ROOT / expected["captions"]).read_text(encoding="utf-8")
            if not caption_text.startswith("WEBVTT"):
                fail(f"{expected['captions']} is not a WebVTT file", failures)

    if re.search(r"\bautoplay\b|\bloop\b", raw, re.I):
        fail("autoplay or loop wording is present in index.html", failures)
    if ".proof video{" not in raw or "width:100%" not in raw.split(".proof video{", 1)[-1].split("}", 1)[0]:
        fail("proof videos must be width 100% for mobile and desktop", failures)
    if "@media(max-width:760px){.grid,.systems,.proof,.fit{grid-template-columns:1fr}" not in raw:
        fail("mobile one-column proof layout is missing", failures)
    if re.search(r"@keyframes|animation:|transition:", raw, re.I):
        fail("proof page introduces animation or transition", failures)

    visible = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = visible.replace("&nbsp;", " ")
    visible_compact = re.sub(r"\s+", " ", visible)
    for phrase in REQUIRED_PHRASES:
        if phrase not in visible_compact:
            fail(f"missing required phrase: {phrase}", failures)
    for phrase in REJECTED_PHRASES:
        if phrase.lower() in visible_compact.lower() or phrase.lower() in raw.lower():
            fail(f"rejected wording still present: {phrase}", failures)

    cta_count = raw.count('href="workflow.html"')
    if cta_count < 3:
        fail(f"expected at least 3 workflow.html CTAs, got {cta_count}", failures)
    if 'href="privacy.html"' not in raw:
        fail("homepage privacy route is missing", failures)

    if not WORKFLOW.is_file():
        fail("workflow.html is missing", failures)
    else:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        if 'name="proof-systems-qualifier"' not in workflow:
            fail("Netlify form identity proof-systems-qualifier is missing", failures)
        if 'data-netlify="true"' not in workflow:
            fail("Netlify form marker is missing", failures)

    check_broken_references(failures)

    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS exactly two local proof videos, captions, posters, "
        "no autoplay/loop, founding CTA and form identity unchanged"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
