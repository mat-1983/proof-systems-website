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
    "The software is there. The flow between it is not.",
    "With ERP",
    "Without ERP",
    "Buy the foundation. Build only what makes the business yours.",
    "Use established software where it fits. Add a focused bespoke layer where it does not.",
    "Not every gap needs a build. The right fit comes first.",
    "Start with one useful outcome. Prove it. Extend only when it earns the next step.",
    "Start where the need is clearest",
    "Unused features",
    "Process bends",
    "Only the missing layer",
    "Observe real workflow",
    "One useful outcome",
    "Initial build",
    "Future development",
    "Clear workflow",
    "Focused build",
    "Needs clarity",
    "Workflow diagnostic",
    "Team capability",
    "AI training",
    "AI does not process the company accounting data",
    "mobile-first web application",
    "Selected Systems",
    "Ask about team training",
    "https://www.linkedin.com/in/mat-glendenning",
]

HOMEPAGE_STALE = [
    "You no longer have to choose between a spreadsheet and software built for somebody else's business.",
    "Buy the commodity foundation",
    "One-person dependencies",
    "Hidden exceptions",
    "Reporting after the decision",
    "When the problem is clear",
    "When the first step works",
    "How the selected systems connect",
    "Re-entered information",
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
        "assets/img/age-600/homepage-stack-erp.webp",
        "assets/img/age-600/homepage-stack-no-erp.webp",
        "assets/img/age-600/01-the-gap.webp",
        "assets/img/age-600/01b-fit.webp",
        "assets/img/age-600/04-approach.webp",
        "assets/img/age-600/selected-systems-connected-demo.webp",
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
    for phrase in HOMEPAGE_STALE:
        if phrase in compact or phrase in raw:
            fail(f"homepage still contains stale copy: {phrase}", failures)
    if 'class="proof-grid"' not in raw:
        fail("homepage must restore the compact proof-grid", failures)
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
    ("sitelog", "budgetflow", "weekly-labour-cost"),
    ("cpr", "sitelog", "project-identity"),
    ("cpr", "ledgerlink", "project-identity"),
    ("cpr", "accounts-software", "project-identity"),
    ("ledgerlink", "sitelog", "ledger-connection"),
    ("ledgerlink", "budgetflow", "ledger-connection"),
    ("ledgerlink", "applications-ledger", "ledger-connection"),
    ("ledgerlink", "probables", "ledger-connection"),
    ("accounts-software", "ledgerlink", "accounts-two-way"),
    ("accounts-software", "local-processing", "checked-local-processing"),
    ("verified-inputs", "local-processing", "verified-inputs"),
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
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'data-from="cpr"' in homepage or 'class="map-wide"' in homepage:
        fail("homepage must not keep the selected-systems architecture map", failures)
    rel = "work/index.html"
    raw = (ROOT / rel).read_text(encoding="utf-8")
    found = diagram_rels(raw)
    missing = expected - found
    if missing:
        fail(f"{rel} missing diagram relationships: {sorted(missing)}", failures)
    if ("budgetflow", "ledgerlink", "payment-export") in found:
        fail(f"{rel} still sends BudgetFlow payment export to LedgerLink", failures)
    if ("cpr", "budgetflow", "project-identity") in found or ("cpr", "probables", "project-identity") in found:
        fail(f"{rel} must not invent extra CPR identity arrows", failures)
    if "map-wide" not in raw or "map-tall" not in raw:
        fail(f"{rel} must keep wide and tall connected diagrams", failures)
    if "Individual systems" not in raw or "Connected workflow" not in raw:
        fail("Selected Systems must expose Individual systems and Connected workflow views", failures)
    if "not the general Proof Systems offer" not in raw and "not the general offer" not in raw:
        fail("connected workflow must not be presented as the general offer", failures)
    if "weekly labour costs" not in raw.lower():
        fail("connected workflow missing weekly labour costs caption", failures)
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
    if "conn-amber" not in css or "conn-blue" not in css:
        fail("connected diagram must keep amber operational links distinct from blue finance paths", failures)
    tall_match = re.search(r"<svg[^>]*class=\"[^\"]*map-tall[^\"]*\"[\s\S]*?</svg>", raw)
    tall = tall_match.group(0) if tall_match else ""
    if not tall:
        fail(f"{rel} missing tall connected diagram", failures)
    if ">APPLICATIONS LEDGER<" in tall or ">Applications Ledger<" in tall:
        fail(f"{rel} tall map must split Applications Ledger to fit the node", failures)
    if ">APPLICATIONS<" not in tall or ">LEDGER<" not in tall:
        fail(f"{rel} tall map must keep Applications and Ledger as split node text", failures)
    if 'id="view-individual"' not in raw or 'id="view-connected"' not in raw:
        fail("Selected Systems missing accessible view radios", failures)
    if 'name="work-view"' not in raw:
        fail("Selected Systems view control must share a radiogroup name", failures)


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


DESIGN_REFS = {
    "homepage-stack-erp.png": "2e772a058e52a2d11a02190de0c3acd3752a9e59b2514b1f322960a6c6648216",
    "homepage-stack-no-erp.png": "665546ba0db36ab937b9ae2948f96a88edefd268c6c3e4ecaabac0464982ddbb",
    "selected-systems-connected-demo.png": "40ddf929a6147f8be0839679df4f10c12e04d38e772517ae541cdd174dc2b8c6",
    "01-the-gap.png": "9444732dcae5ca88912395e6256addb4b49e05490fb85ff8d56c0e1eb3365900",
    "01b-fit.png": "a78c4e805f3d5ed49ebe3b217174ba93e6f419cdcec591c6ec2f8ad9f4c47a9a",
    "04-approach.png": "141b64df1fe5b1bbca304ac54e7359d027aea533e031550a99cea9e9d6631b40",
}

PUBLIC_WEBPS = {
    "assets/img/age-600/homepage-stack-erp.webp": {
        "sha256": "78b1d07a363b49c994e33cc1763f42a9e6e4d3f04722ec2cb1e67841373be230",
        "max_bytes": 500000,
    },
    "assets/img/age-600/homepage-stack-no-erp.webp": {
        "sha256": "c4e45e6f5e0d2812a70b1ff7d10aef9d1f711eb1bd6bea7bab3c93c74d8beedd",
        "max_bytes": 500000,
    },
    "assets/img/age-600/01-the-gap.webp": {
        "sha256": "091990e87569fc38d4eaf26b18034dee5cb89035c4a5e1924313f2d8fb4096e0",
        "max_bytes": 500000,
    },
    "assets/img/age-600/01b-fit.webp": {
        "sha256": "77ece0c13101ed9fbfd95c424701fcd7061dae25fb1e1614f836d841a7ec2e6b",
        "max_bytes": 500000,
    },
    "assets/img/age-600/04-approach.webp": {
        "sha256": "4374c811d7dd31d9138f56efdc4a91d5483b75e117600357800fd1fe2ea5d686",
        "max_bytes": 500000,
    },
    "assets/img/age-600/selected-systems-connected-demo.webp": {
        "sha256": "0147e15be2fb8a040bdf18d040bf8f4904fc92039292c6d6f879744c2459c71b",
        "max_bytes": 500000,
    },
}


def check_round3(failures: list[str]) -> None:
    import hashlib

    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'data-opening' not in raw or 'class="opening-mark"' not in raw:
        fail("homepage missing opening node-mark sequence", failures)
    if 'class="opening-name"' not in raw or ">Proof Systems<" not in raw:
        fail("homepage must reveal the Proof Systems name after the mark", failures)
    if 'id="stack-erp"' not in raw or 'id="stack-no-erp"' not in raw:
        fail("homepage missing With ERP / Without ERP control", failures)
    if "Inbox" not in raw or "Spreadsheet" not in raw or "Approval" not in raw or "Report" not in raw:
        fail("Gap chapter missing the Inbox to Report workflow chain", failures)
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    about_rule = css.split("#about h2", 1)[-1].split("}", 1)[0]
    if "#about h2" not in css or "#start h2" not in css:
        fail("operator and enquiry headings must override the global h2 measure", failures)
    if "max-width: none" not in about_rule:
        fail("operator and enquiry headings must use the available composition width", failures)
    if "16.8em" in css or "14.5em" in css:
        fail("operator and enquiry headings must not use a narrow artificial measure", failures)
    if 'class="iso-top"' not in raw or 'class="iso-left"' not in raw or 'class="iso-right"' not in raw:
        fail("homepage scenes must use three-face isometric construction", failures)
    if ".iso-amber { stroke: var(--amber);" not in css or ".iso-blue { stroke: var(--blue);" not in css:
        fail("shared amber/blue connection stroke language is missing", failures)
    if "WAITING" not in raw or "TOO LATE" not in raw or "RE-ENTERED" not in raw:
        fail("Gap scene must show re-entry, waiting and late-report cues", failures)
    if "BROAD SOFTWARE" not in raw or "BESPOKE LAYER" not in raw:
        fail("Fit scene missing broad-software / bespoke-layer composition", failures)
    if "UNDERSTAND" not in raw or "CHOOSE" not in raw or "PROVE" not in raw or "EXTEND" not in raw:
        fail("Approach scene missing the four workstation stages", failures)
    if 'class="gap-key"' not in raw:
        fail("Gap scene must keep a readable HTML key for small viewports", failures)
    if "route-pad" not in raw:
        fail("Approach entry routes must remain dimensional pads, not empty text cards", failures)
    work = (ROOT / "work/index.html").read_text(encoding="utf-8")
    if 'class="slab"' not in work:
        fail("connected workflow must use dimensional slabs, not flat rectangles only", failures)
    if ".iso-svg" not in css or "max-width: 100%" not in css.split(".iso-svg {", 1)[-1].split("}", 1)[0]:
        fail("iso scenes must cap at the composition width", failures)
    if ".map-tall .conn-title { font-size: 15px; }" not in css:
        fail("tall connected labels must enlarge at the mobile breakpoint", failures)
    iso_block = css.split(".iso-frame,", 1)[-1].split(".iso-amber,", 1)[0] if ".iso-frame," in css else ""
    if "overflow-x" in iso_block:
        fail("dimensional scenes must not hide overflow with overflow-x", failures)
    if re.search(r"(?<!backdrop-)filter:\s*blur\(", css):
        fail("CSS must not use blur filters on type or copy", failures)
    if 'class="approved-visual"' not in raw or "scene-fallback" not in raw:
        fail("homepage must pair approved desktop visuals with native fallbacks", failures)
    if "desktop-hide-copy" not in raw:
        fail("Gap, Fit and Approach copy must remain in the DOM for assistive technology", failures)
    if "@media (min-width: 900px)" not in css:
        fail("approved visuals must switch at a 900px desktop breakpoint", failures)
    two_col = css.find("grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr)")
    gap_visual = css.rfind("#gap .approved-visual")
    if two_col == -1 or gap_visual == -1 or gap_visual < two_col:
        fail(
            "desktop Gap visual rule must follow the base two-column .gap-scene declaration "
            "so the approved image spans the wrap"
        )
    gap_visual_rule = css[gap_visual:gap_visual + 220]
    if "grid-column: 1 / -1" not in gap_visual_rule:
        fail("desktop Gap approved visual must span the full grid")
    if "width: 100%" not in gap_visual_rule:
        fail("desktop Gap approved visual must use the full wrap width")
    gap_scene_desktop = css.rfind("#gap .gap-scene")
    if gap_scene_desktop == -1 or gap_scene_desktop < two_col:
        fail("desktop #gap .gap-scene one-column rule must follow the base two-column declaration")
    if "minmax(0, 1fr)" not in css[gap_scene_desktop:gap_scene_desktop + 160]:
        fail("desktop #gap .gap-scene must be a single full-width column")
    if "clip: rect(0, 0, 0, 0)" not in css.split(".desktop-hide-copy {", 1)[-1][:280]:
        fail("desktop-hidden copy must use a visually-hidden clip, not display:none", failures)
    hide_rule = css.split(".desktop-hide-copy {", 1)[-1].split("}", 1)[0]
    if "display: none" in hide_rule or "display:none" in hide_rule:
        fail("desktop-hidden copy must not use display:none", failures)
    for rel, meta in PUBLIC_WEBPS.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing public derivative {rel}", failures)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != meta["sha256"]:
            fail(f"{rel} hash mismatch: {actual}", failures)
        if path.stat().st_size > meta["max_bytes"]:
            fail(f"{rel} exceeds {meta['max_bytes']} bytes", failures)
        if f'src="{rel}"' not in raw and f'src="../{rel}"' not in work:
            if rel.endswith("selected-systems-connected-demo.webp"):
                if f'src="../{rel}"' not in work:
                    fail("Selected Systems missing connected approved visual", failures)
            elif f'src="{rel}"' not in raw:
                fail(f"homepage missing approved visual {rel}", failures)
        snippet = raw if "selected-systems" not in rel else work
        if rel.split("/")[-1] not in snippet:
            fail(f"public page missing {rel}", failures)
        if 'width="1672"' not in snippet or 'height="941"' not in snippet:
            fail(f"{rel} must declare source pixel dimensions", failures)
        if 'loading="lazy"' not in snippet or 'decoding="async"' not in snippet:
            fail("approved visuals must use lazy loading and async decoding", failures)
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    if "updateOpening" not in js:
        fail("site.js must drive the opening sequence from natural scroll", failures)
    if "preventDefault" in js and "wheel" in js:
        fail("opening sequence must not hijack scroll", failures)
    for path in PUBLIC_HTML:
        html = path.read_text(encoding="utf-8")
        if "docs/design/age-600-round-3" in html or "generated_images" in html:
            fail(f"{path.relative_to(ROOT).as_posix()} must not serve design-review rasters", failures)
    ref_dir = ROOT / "docs" / "design" / "age-600-round-3"
    for name, digest in DESIGN_REFS.items():
        path = ref_dir / name
        if not path.is_file():
            fail(f"missing design reference {name}", failures)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            fail(f"{name} hash mismatch: {actual}", failures)


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
    check_round3(failures)
    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS routes, eight stories, round-3 homepage chapters, proof-grid, "
        "connected workflow view, enquiry form, omitted client chapter, "
        "poster-first teasers and public-copy safety"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
