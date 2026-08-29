#!/usr/bin/env python3
"""Deterministic checks for AGE-600 routes, copy, form and safety."""

from __future__ import annotations

import html.parser
import os
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
PUBLIC_HTML = sorted(path for path in ROOT.rglob("*.html") if ".git" not in path.parts)

STORY_SLUGS = [
    "sitelog",
    "budgetflow",
    "applications-ledger",
    "cpr",
    "probables",
    "ledgerlink",
    "cashflow",
    "management-accounts",
]

FULL_FILMS = [f"assets/demo-media/{slug}-demo.mp4" for slug in STORY_SLUGS]
TEASERS = [
    "assets/demo-media/sitelog-teaser.mp4",
    "assets/demo-media/budgetflow-teaser.mp4",
    "assets/demo-media/ledgerlink-teaser.mp4",
]

HOMEPAGE_REQUIRED = [
    "Operational systems for owner-led SMEs",
    "Systems built around how your business really works.",
    "Discuss a workflow",
    "See selected systems",
    "01 / THE GAP",
    "02 / CAPABILITY",
    "03 / PROOF",
    "04 / APPROACH",
    "05 / OPERATOR FIRST",
    "06 / START",
    "Synthetic demonstration",
    "These films use synthetic Northstar data to demonstrate systems and workflows I have designed",
    "Explore SiteLog",
    "Explore BudgetFlow",
    "See the finance workflow",
    "View all systems",
    "I started with the operation, not the technology.",
    "What important work should be easier to run?",
    "You no longer have to choose between a spreadsheet and software built for somebody else's business.",
    "Buy the commodity foundation",
    "AI does not process the company accounting data",
    "mobile-first web application",
    "Selected Systems",
    "Ask about team training",
    "https://www.linkedin.com/in/mat-glendenning",
]

PUBLIC_REJECTED = [
    "Pantera",
    "Pete Mills",
    "Xonetic",
    "youtube",
    "YouTube",
    "founding cohort",
    "founding-diagnostic",
    "four founding",
    "Four founding",
    "four places",
    "free founding",
    "Apply for a founding",
    "founding diagnostic",
    "£350",
    "decision_role",
    "desired_outcome",
    "hours_per_week",
    "application-received",
    "CLIENT PERSPECTIVE",
    "05 / CLIENT",
    "Contract Performance Reporting",
    "Avenir Next",
    "fonts.googleapis",
    "fonts.gstatic",
]

FORM_REQUIRED = [
    'name="proof-systems-qualifier"',
    'data-netlify="true"',
    'netlify-honeypot="bot-field"',
    'name="bot-field"',
    'name="route_key" value="general-enquiry"',
    'name="route_label" value="Discuss a workflow"',
    'name="lead_state" value="enquiry-received"',
    'name="page_source" value="workflow.html"',
    'name="submitted_at"',
    'name="name"',
    'name="email"',
    'name="company"',
    'name="workflow_help"',
    'name="contact_consent"',
    "Send enquiry",
    "Tell me about one workflow that should work better.",
]

VISIBLE_FIELDS = {"name", "email", "company", "workflow_help", "contact_consent"}
REMOVED_FIELDS = {"decision_role", "desired_outcome", "hours_per_week"}


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.videos: list[dict] = []
        self.refs: list[tuple[str, str]] = []
        self._current_video: dict | None = None
        self.script_srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: (value or "") for key, value in attrs}
        element_id = attr.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            self.ids.add(element_id)
        if tag == "a" and attr.get("href"):
            self.hrefs.append(attr["href"])
            self.refs.append(("href", attr["href"]))
        if tag == "img" and attr.get("src"):
            self.refs.append(("img", attr["src"]))
        if tag == "link" and attr.get("href"):
            self.refs.append(("link", attr["href"]))
        if tag == "script" and attr.get("src"):
            self.script_srcs.append(attr["src"])
            self.refs.append(("script", attr["src"]))
        if tag == "source" and attr.get("src"):
            self.refs.append(("source", attr["src"]))
        if tag == "track" and attr.get("src"):
            self.refs.append(("track", attr["src"]))
        if tag == "video":
            video = {"attrs": attr, "sources": [], "tracks": []}
            self.videos.append(video)
            self._current_video = video
            if attr.get("poster"):
                self.refs.append(("poster", attr["poster"]))
            if attr.get("src"):
                self.refs.append(("video", attr["src"]))
        if tag == "source" and self._current_video is not None:
            self._current_video["sources"].append(attr)
        if tag == "track" and self._current_video is not None:
            self._current_video["tracks"].append(attr)
        if tag not in {"meta", "link", "img", "br", "input", "hr", "source", "track"}:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "video":
            self._current_video = None
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()


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


def is_local_ref(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme in {"mailto", "https", "http"}:
        return False
    if value.startswith("#"):
        return False
    return True


def visible_text(raw: str) -> str:
    visible = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    visible = re.sub(r"<style[\s\S]*?</style>", " ", visible, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = visible.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", visible)


def parse_page(path: pathlib.Path) -> tuple[str, PageParser]:
    raw = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    return raw, parser


def check_routes(failures: list[str]) -> None:
    required = [
        "index.html",
        "workflow.html",
        "privacy.html",
        "checkout.html",
        "video-series.html",
        "work/index.html",
        "assets/css/site.css",
        "assets/js/site.js",
        "assets/js/form.js",
        "assets/img/social.jpg",
        "favicon.svg",
        "_redirects",
        "training.html",
        "assets/fonts/InterVariable.woff2",
        "assets/fonts/LICENSE.txt",
        "assets/brand/logo-light.svg",
        "assets/brand/icon-light.svg",
        "assets/brand/favicon.svg",
    ]
    for rel in required:
        if not exact_case_file(ROOT, rel):
            fail(f"missing required path: {rel}", failures)
    for slug in STORY_SLUGS:
        rel = f"work/{slug}.html"
        if not exact_case_file(ROOT, rel):
            fail(f"missing story route: {rel}", failures)


def check_homepage(failures: list[str]) -> None:
    path = ROOT / "index.html"
    raw, parser = parse_page(path)
    if parser.stack:
        fail(f"index.html unclosed tags: {parser.stack}", failures)
    if parser.errors:
        failures.extend(f"index.html: {item}" for item in parser.errors)
    compact = visible_text(raw)
    for phrase in HOMEPAGE_REQUIRED:
        if phrase not in compact and phrase not in raw:
            fail(f"homepage missing required phrase: {phrase}", failures)
    if "CLIENT PERSPECTIVE" in raw or "05 / CLIENT" in raw:
        fail("homepage must omit the unapproved client-perspective chapter", failures)
    if re.search(r"<img[^>]+(portrait|headshot)", raw, re.I):
        fail("homepage must not include a portrait", failures)
    for film in FULL_FILMS:
        if film in raw:
            fail(f"homepage must not embed full film {film}", failures)
    for teaser in TEASERS:
        if f'data-teaser-src="{teaser}"' not in raw:
            fail(f"homepage missing poster-first teaser {teaser}", failures)
    if parser.videos:
        fail("homepage must not contain a video element; teasers are JS-injected", failures)
    if 'href="workflow.html"' not in raw:
        fail("homepage missing enquiry CTA", failures)
    for slug in ("sitelog", "budgetflow"):
        if f"work/{slug}.html" not in raw:
            fail(f"homepage missing story link for {slug}", failures)
    if "assets/js/site.js" not in raw:
        fail("homepage must use shared site.js", failures)


def check_form(failures: list[str]) -> None:
    path = ROOT / "workflow.html"
    raw, parser = parse_page(path)
    if parser.stack:
        fail(f"workflow.html unclosed tags: {parser.stack}", failures)
    for phrase in FORM_REQUIRED:
        if phrase not in raw:
            fail(f"workflow.html missing {phrase}", failures)
    for field in REMOVED_FIELDS:
        if f'name="{field}"' in raw:
            fail(f"workflow.html still exposes removed field {field}", failures)
    names = re.findall(r'<input[^>]*name="([^"]+)"|<textarea[^>]*name="([^"]+)"', raw)
    visible = set()
    for a, b in names:
        name = a or b
        if name in {"form-name", "bot-field", "route_key", "route_label", "lead_state", "page_source", "submitted_at", "interest_source"}:
            continue
        visible.add(name)
    if visible != VISIBLE_FIELDS:
        fail(f"visible fields {sorted(visible)} != {sorted(VISIBLE_FIELDS)}", failures)
    if "method=\"POST\"" not in raw and "method='POST'" not in raw:
        fail("enquiry form must POST", failures)
    if 'name="interest_source"' not in raw:
        fail("enquiry form missing hidden interest_source", failures)
    js = (ROOT / "assets/js/form.js").read_text(encoding="utf-8")
    if "preventDefault" not in js:
        fail("form.js must keep the success state on the enquiry page", failures)
    if "file:" not in js:
        fail("form.js must intercept local submissions", failures)
    if "ai-team-training" not in js or "replaceState" not in js:
        fail("form.js must capture ai-team-training interest and strip it from the URL", failures)


def check_stories(failures: list[str]) -> None:
    work_index = (ROOT / "work/index.html").read_text(encoding="utf-8")
    for slug in STORY_SLUGS:
        rel = f"{slug}.html"
        if rel not in work_index:
            fail(f"work index missing {rel}", failures)
        path = ROOT / "work" / rel
        raw, parser = parse_page(path)
        if parser.stack:
            fail(f"{path.name} unclosed tags: {parser.stack}", failures)
        if "Synthetic demonstration" not in raw:
            fail(f"{path.name} missing Synthetic demonstration label", failures)
        if "Discuss a workflow" not in raw:
            fail(f"{path.name} missing enquiry action", failures)
        if len(parser.videos) != 1:
            fail(f"{path.name} expected one film, got {len(parser.videos)}", failures)
            continue
        video = parser.videos[0]
        attrs = video["attrs"]
        if "controls" not in attrs:
            fail(f"{path.name}: film missing controls", failures)
        if "autoplay" in attrs or "loop" in attrs:
            fail(f"{path.name}: film must not autoplay or loop", failures)
        if attrs.get("preload") not in {"none", "metadata"}:
            fail(f"{path.name}: unexpected preload {attrs.get('preload')!r}", failures)
        sources = video["sources"]
        expected_src = f"../assets/demo-media/{slug}-demo.mp4"
        if not sources or sources[0].get("src") != expected_src:
            fail(f"{path.name}: unexpected source {sources}", failures)
        tracks = video["tracks"]
        if not tracks or tracks[0].get("kind") != "captions":
            fail(f"{path.name}: missing captions track", failures)
        if f"../assets/demo-media/{slug}-demo.vtt" not in raw:
            fail(f"{path.name}: missing VTT path", failures)
        if f"../assets/demo-media/{slug}-poster.jpg" not in raw:
            fail(f"{path.name}: missing poster", failures)
        if "What this film shows" not in raw:
            fail(f"{path.name}: missing accessible summary", failures)
        if "Back to Selected Systems" not in raw:
            fail(f"{path.name} missing Back to Selected Systems", failures)
        if "Suggested next:" not in raw:
            fail(f"{path.name} missing suggested next route", failures)
        if slug == "ledgerlink":
            if "connection to accounts software" not in raw:
                fail("LedgerLink story missing 'connection to accounts software'", failures)
            if "connection to a workbook" in raw.lower():
                fail("LedgerLink story must not say connection to a workbook", failures)
            if "AI does not process the company accounting data" not in raw:
                fail("LedgerLink story missing no-AI accounting statement", failures)
        if slug == "cpr":
            if "Central Project Register" not in raw:
                fail("CPR story must use Central Project Register", failures)
            if "database and API" not in raw:
                fail("CPR story must explain the database/API service", failures)


def check_redirects(failures: list[str]) -> None:
    checkout = (ROOT / "checkout.html").read_text(encoding="utf-8")
    video = (ROOT / "video-series.html").read_text(encoding="utf-8")
    redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
    if 'name="robots" content="noindex"' not in checkout:
        fail("checkout.html must be noindex", failures)
    if "workflow.html" not in checkout:
        fail("checkout.html must point at the enquiry form", failures)
    if 'name="robots" content="noindex"' not in video:
        fail("video-series.html must be noindex", failures)
    if "index.html" not in video:
        fail("video-series.html must point at the homepage", failures)
    if "/checkout" not in redirects or "/workflow.html" not in redirects:
        fail("_redirects missing checkout to enquiry mapping", failures)
    if "/video-series" not in redirects:
        fail("_redirects missing video-series mapping", failures)


def check_public_copy(failures: list[str]) -> None:
    for path in PUBLIC_HTML:
        raw = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for phrase in PUBLIC_REJECTED:
            if phrase in raw:
                fail(f"{rel} contains rejected wording: {phrase}", failures)
        if path.name.endswith(".html"):
            parser = PageParser()
            parser.feed(raw)
            parser.close()
            if parser.stack:
                fail(f"{rel} unclosed tags: {parser.stack}", failures)
            for kind, value in parser.refs:
                if not is_local_ref(value):
                    if value.startswith("http://"):
                        fail(f"{rel}: insecure URL {value}", failures)
                    continue
                rel_path = urllib.parse.urlparse(value).path
                if rel_path.endswith("/"):
                    rel_path = rel_path + "index.html"
                resolved = (path.parent / rel_path).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    fail(f"{rel}: local ref escapes root {value}", failures)
                    continue
                if not resolved.is_file():
                    fail(f"{rel}: broken {kind} {value}", failures)


def check_mobile_header(failures: list[str]) -> None:
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    if "max-width: 100%" not in css.split(".nav-inner {", 1)[-1].split("}", 1)[0]:
        fail("nav-inner must cap at the viewport width", failures)
    mobile = css.split("@media (max-width: 760px)", 1)
    if len(mobile) != 2:
        fail("missing 760px header breakpoint", failures)
        return
    block = mobile[1].split("@media", 1)[0]
    if "width: 100%" not in block or "padding-inline: 16px" not in block:
        fail("mobile nav-inner must use full viewport width with 16px inset padding", failures)
    if "gap: 0.4rem" not in block:
        fail("mobile header gap must fit brand, enquiry CTA and Menu inside 390px", failures)
    if ".nav-cta" not in block or ".nav-toggle" not in block:
        fail("mobile header must keep the enquiry CTA and Menu control", failures)
    if "overflow-x" in block:
        fail("mobile header must fit without using overflow-x as the fix", failures)
    narrow = css.split("@media (max-width: 359px)", 1)
    if len(narrow) != 2:
        fail("missing 359px header reflow breakpoint for 320px viewports", failures)
        return
    narrow_block = narrow[1].split("@media", 1)[0]
    if "flex-wrap: wrap" not in narrow_block:
        fail("320px header must wrap rather than overflow", failures)
    if "flex: 1 0 100%" not in narrow_block or ".nav-cta" not in narrow_block:
        fail("320px header must keep Discuss a workflow on its own reachable row", failures)
    if ".nav-toggle" not in narrow_block or "order: 1" not in narrow_block:
        fail("320px header must keep Menu visible on the first row", failures)
    if "overflow-x" in narrow_block:
        fail("320px header must fit without using overflow-x as the fix", failures)
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    if ".nav-open:focus-visible ~ .nav-toggle" not in css:
        fail("mobile Menu must show a visible focus ring when the checkbox is :focus-visible", failures)
    if "outline: 2px solid var(--focus)" not in css.split(".nav-open:focus-visible ~ .nav-toggle", 1)[-1][:280]:
        fail("mobile Menu focus ring must use the visible focus outline", failures)


REQUIRED_MAP_RELS = [
    ("cpr", "sitelog", "project-identity"),
    ("cpr", "budgetflow", "project-identity"),
    ("cpr", "applications-ledger", "project-identity"),
    ("cpr", "probables", "project-identity"),
    ("sitelog", "budgetflow", "weekly-labour-cost"),
    ("budgetflow", "accounts-software", "payment-export"),
    ("accounts-software", "ledgerlink", "accounts-extraction"),
    ("ledgerlink", "local-processing", "checked-local-processing"),
    ("local-processing", "cashflow", "checked-local-processing"),
    ("local-processing", "management-accounts", "checked-local-processing"),
]


def diagram_rels(raw: str) -> set[tuple[str, str, str]]:
    found: set[tuple[str, str, str]] = set()
    for match in re.finditer(
        r'data-from="([^"]+)"[^>]*data-to="([^"]+)"[^>]*data-rel="([^"]+)"|'
        r'data-from="([^"]+)"[^>]*data-rel="([^"]+)"[^>]*data-to="([^"]+)"|'
        r'data-to="([^"]+)"[^>]*data-from="([^"]+)"[^>]*data-rel="([^"]+)"',
        raw,
    ):
        groups = [g for g in match.groups() if g]
        if len(groups) == 3:
            if match.group(1):
                found.add((match.group(1), match.group(2), match.group(3)))
            elif match.group(4):
                found.add((match.group(4), match.group(6), match.group(5)))
            else:
                found.add((match.group(8), match.group(7), match.group(9)))
    return found


def check_architecture(failures: list[str]) -> None:
    expected = set(REQUIRED_MAP_RELS)
    for rel in ("index.html", "work/index.html"):
        raw = (ROOT / rel).read_text(encoding="utf-8")
        found = diagram_rels(raw)
        missing = expected - found
        if missing:
            fail(f"{rel} missing diagram relationships: {sorted(missing)}", failures)
        if ("budgetflow", "ledgerlink", "payment-export") in found:
            fail(f"{rel} still sends BudgetFlow payment export to LedgerLink", failures)
        if 'class="map-wide"' not in raw or 'class="map-tall"' not in raw:
            fail(f"{rel} must keep wide and tall architecture diagrams", failures)
        if "Project identity" not in raw or "Finance" not in raw:
            fail(f"{rel} must distinguish identity from finance grouping", failures)
        if 'class="map-identity-bus"' not in raw:
            fail(f"{rel} tall map must use a non-crossing identity bus", failures)
        if 'data-route="gutter"' not in raw:
            fail(f"{rel} must route lower identity links in the side gutter", failures)
        css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        label_rule = css.split(".map-label {", 1)[-1].split("}", 1)[0]
        if "var(--amber)" not in label_rule or "var(--amber-deep)" in label_rule:
            fail("map labels must use --amber at 4.5:1 rather than --amber-deep", failures)
        if "font-size: 12px" not in label_rule:
            fail("map labels must be 12px so they remain readable when scaled", failures)
        map_rule = css.split(".system-map {", 1)[-1].split("}", 1)[0]
        if "margin-inline: 0" not in map_rule:
            fail("system-map must reset user-agent figure horizontal margins", failures)
        if ".map-tall .map-title { font-size: 15px; }" not in css:
            fail("tall map titles must enlarge at the mobile breakpoint", failures)
        mobile_css = css.split("@media (max-width: 760px)", 1)[-1].split("@media", 1)[0]
        if ".system-map { padding: 0.5rem; }" not in mobile_css:
            fail("narrow maps must reduce figure padding so the SVG uses wrap width", failures)
        tall = raw.split('<svg class="map-tall"', 1)[-1].split("</svg>", 1)[0]
        if ">Applications Ledger<" in tall:
            fail(f"{rel} tall map must split Applications Ledger to fit the node", failures)
        if ">Applications<" not in tall or ">Ledger<" not in tall:
            fail(f"{rel} tall map must keep Applications and Ledger as split node text", failures)


def check_homepage_structure(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    opens = len(re.findall(r"<section\b", raw, flags=re.I))
    closes = len(re.findall(r"</section>", raw, flags=re.I))
    if opens != closes:
        fail(f"index.html section tags unbalanced: {opens} open, {closes} close", failures)
    markers = re.findall(r'class="marker">([^<]+)', raw)
    expected = [
        "Operational systems for owner-led SMEs",
        "01 / THE GAP",
        "01B / FIT",
        "02 / CAPABILITY",
        "03 / PROOF",
        "04 / APPROACH",
        "05 / OPERATOR FIRST",
        "06 / START",
    ]
    if markers != expected:
        fail(f"homepage marker sequence {markers} != {expected}", failures)
    if "06 / OPERATOR FIRST" in raw or "07 / START" in raw:
        fail("unpublished testimonial numbering remains on the homepage", failures)
    proof_end = raw.find('id="proof"')
    approach = raw.find('id="approach"')
    if proof_end != -1 and approach != -1:
        between = raw[proof_end:approach]
        if between.count("</section>") != 1:
            fail("Proof chapter must close with exactly one </section> before Approach", failures)


def check_round2(failures: list[str]) -> None:
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    if "Avenir Next" in css or "font-weight: 650" in css or "font-weight: 750" in css:
        fail("CSS still uses Avenir Next or faux 650/750 weights", failures)
    if '@font-face' not in css or "InterVariable.woff2" not in css or "font-display: swap" not in css:
        fail("Inter Variable must be self-hosted with font-display swap", failures)
    font = ROOT / "assets/fonts/InterVariable.woff2"
    import hashlib
    digest = hashlib.sha256(font.read_bytes()).hexdigest()
    if digest != "693b77d4f32ee9b8bfc995589b5fad5e99adf2832738661f5402f9978429a8e3":
        fail(f"InterVariable.woff2 hash mismatch: {digest}", failures)
    licence = hashlib.sha256((ROOT / "assets/fonts/LICENSE.txt").read_bytes()).hexdigest()
    if licence != "262481e844521b326f5ecd053e59b98c8b2da78c8ee1bdbb6e8174305e54935a":
        fail(f"Inter licence hash mismatch: {licence}", failures)
    training = (ROOT / "training.html").read_text(encoding="utf-8")
    if "Train your team to use AI on real workflows, not toy examples." not in training:
        fail("training page missing primary line", failures)
    if "Ask about team training" not in training:
        fail("training page missing training CTA", failures)
    if "workflow.html?interest=ai-team-training" not in training:
        fail("training CTA must reuse the general enquiry form with interest=ai-team-training", failures)
    if "half-day" not in training:
        fail("training page must describe the half-day workshop", failures)
    work_index = (ROOT / "work/index.html").read_text(encoding="utf-8")
    if "<title>Selected Systems | Proof Systems</title>" not in work_index:
        fail("Selected Systems public title is missing", failures)
    if ">Work<" in work_index:
        fail("Selected Systems index still uses Work as the public name", failures)
    for path in PUBLIC_HTML:
        raw = path.read_text(encoding="utf-8")
        if "fonts.googleapis" in raw or "fonts.gstatic" in raw:
            fail(f"{path.name} loads a remote font", failures)
        if "Contract Performance Reporting" in raw:
            fail(f"{path.name} still expands CPR incorrectly", failures)


def check() -> int:
    failures: list[str] = []
    check_routes(failures)
    check_homepage(failures)
    check_form(failures)
    check_stories(failures)
    check_redirects(failures)
    check_public_copy(failures)
    check_mobile_header(failures)
    check_architecture(failures)
    check_homepage_structure(failures)
    check_round2(failures)
    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS routes, eight stories, short enquiry form, omitted client chapter, "
        "poster-first homepage teasers and public-copy safety"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
