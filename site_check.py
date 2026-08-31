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
    "View SiteLog",
    "View BudgetFlow",
    "View finance workflow",
    "View all selected systems",
    "Demo videos: bespoke systems built to solve painful workflows.",
    "I started with the operation, not the technology.",
    "What important work should be easier to run?",
    "The software is there. The flow between it is not.",
    "Buy the foundation. Build only what makes the business yours.",
    "Use established software where it fits. Add a focused bespoke layer where it does not.",
    "Bespoke fixes the manual work that off-the-shelf software leaves behind.",
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
    "Mobile-first weekly site record bespoke to business function.",
    "Admin Ready Invoices &amp; Exports",
    "Turn weekly labour costs into visible budget decisions.",
    "Weekly labour allocation",
    "Budget Control",
    "Accounts Software Exports",
    "Data extracts directly from accounts systems ready for integration to bespoke systems",
    "Keep the useful tools. Add a bespoke layer that connects accounts or ERP software, spreadsheets and operational workflows.",
    "Proof Systems builds around what already works.",
    "Fix the workflow first. Then make it intelligent.",
    "Disconnected work",
    "Connected system",
    "Reliable data",
    "Controlled automation",
    "Capable team",
    "View selected systems",
    "Helping owner-led businesses replace fragile spreadsheets, disconnected tools and repetitive work with practical software integrated with existing technology, controlled AI automation and training their teams can use.",
    "Operational systems for owner-led SMEs.",
    "Selected Systems",
    "Ask about team training",
    "Ask about AI team training",
    "https://www.linkedin.com/in/mathew-glendenning-90670649/",
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
    "I help owner-led businesses replace fragile spreadsheets",
    "View all systems",
    "mobile-first web application",
    "With an ERP or accounts foundation, operational software sits above it",
    "With ERP",
    "Without ERP",
    "Not every gap needs a build. The right fit comes first.",
    "Improve the operation, not just the interface.",
    "Working systems make the difference visible.",
    "These films use synthetic Northstar data to demonstrate systems and workflows I have designed",
    "Explore SiteLog",
    "See the finance workflow",
    "Operator-led. Built around the real workflow. Technology used where it earns its place.",
    "Make the correct weekly record the easiest one to create.",
    "Move from accounts data to decisions without rebuilding the story by hand.",
    "Mobile-first weekly site records, invoices and admin-ready exports.",
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
    if "began as independent bespoke systems" not in raw:
        fail("connected workflow must keep the approved independent-then-integrated meaning", failures)
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
        "sha256": "42582734d95b1a51cac3c9cb61360aa10c695c5d21d7b83c897967815f63cfc2",
        "max_bytes": 500000,
        "width": 1672,
        "height": 840,
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
    if "homepage-stack-no-erp.webp" not in raw:
        fail("homepage missing the approved no-ERP stack artwork", failures)
    if 'id="stack-erp"' in raw or "With ERP" in raw:
        fail("homepage must not render the With ERP / Without ERP switch", failures)
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
    if ".iso-amber { stroke: var(--amber);" not in css or ".iso-blue { stroke: var(--blue);" not in css:
        fail("shared amber/blue connection stroke language is missing", failures)
    if "waiting" not in raw.lower():
        fail("Gap scene must keep waiting and late-report cues", failures)
    if "too-late" not in raw.lower() and "too late" not in raw.lower():
        fail("Gap scene must keep the too-late cue", failures)
    if "re-entered" not in raw.lower():
        fail("Gap scene must keep the re-entered cue", failures)
    if "bespoke layer" not in raw.lower():
        fail("Fit scene missing bespoke-layer composition", failures)
    if "Understand" not in raw or "Choose" not in raw or "Prove" not in raw or "Extend" not in raw:
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
        if "width" in meta or "height" in meta:
            width, height = webp_dimensions(path)
            if width != meta.get("width", width) or height != meta.get("height", height):
                fail(f"{rel} dimensions {width}x{height} != {meta.get('width')}x{meta.get('height')}", failures)
    if 'src="../assets/img/age-600/selected-systems-connected-demo.webp"' not in work:
        fail("Selected Systems missing connected approved visual", failures)
    if 'loading="lazy"' not in work or 'decoding="async"' not in work:
        fail("connected approved visual must use lazy loading and async decoding", failures)
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


CAPABILITY_COPY = [
    "02 / CAPABILITY",
    "Fix the workflow first. Then make it intelligent.",
    "Disconnected work",
    "People, spreadsheets and offline documents hold different parts of the process.",
    "Connected system",
    "A fitted operational system connects the work, people and controls.",
    "Reliable data",
    "The working process creates a connected, usable flow of structured data.",
    "Controlled automation",
    "AI Automation comes after the workflow works. Repetitive tasks can then be automated safely.",
    "Capable team",
    "Role-specific training helps people apply AI safely and usefully to the work they already do.",
    "Discuss a workflow",
    "View selected systems",
    "Ask about AI team training",
]

GENERAL_SYSTEMS_LABELS = {
    "Selected Systems",
    "See selected systems",
    "View all selected systems",
    "View selected systems",
    "Back to Selected Systems",
}

HOMEPAGE_RASTERS = (
    "homepage-stack-erp.webp",
    "homepage-stack-no-erp.webp",
    "01-the-gap.webp",
    "01b-fit.webp",
    "04-approach.webp",
)


def check_round4(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    work = (ROOT / "work/index.html").read_text(encoding="utf-8")

    if 'class="proposition-lead"' not in raw or 'class="proposition-support"' not in raw:
        fail("homepage missing proposition lead/support hierarchy", failures)
    if "Operational systems for owner-led SMEs." not in raw:
        fail("proposition lead copy is not the approved sentence", failures)
    lead_rule = css.split(".proposition-lead {", 1)[-1].split("}", 1)[0] if ".proposition-lead {" in css else ""
    support_rule = css.split(".proposition-support {", 1)[-1].split("}", 1)[0] if ".proposition-support {" in css else ""
    if "clamp(2.15rem" not in lead_rule:
        fail("proposition lead must be materially larger than the previous marker treatment", failures)
    if "clamp(1.18rem" not in support_rule:
        fail("proposition support must be larger than the previous lede treatment", failures)
    if "max-width: none" not in lead_rule:
        fail("proposition lead must use the available composition width", failures)

    if "h2 { font-size: clamp(1.8rem, 4vw, 2.8rem); max-width: 22ch;" not in css:
        fail("global h2 measure must stay 22ch", failures)
    for selector in ("#gap h2", "#economics h2", "#approach h2", "#proof h2", "#capability h2"):
        if selector not in css:
            fail(f"{selector} must use a scoped width override", failures)

    cap = re.search(r'<section class="chapter" id="capability"[^>]*>([\s\S]*?)</section>', raw)
    if not cap:
        fail("homepage missing Capability section", failures)
    else:
        body = cap.group(1)
        for phrase in CAPABILITY_COPY:
            if phrase not in body:
                fail(f"Capability copy missing {phrase!r}", failures)
        if 'class="capability-grid"' in body or 'class="cap-visual"' in body:
            fail("Capability must not keep the three-card layout", failures)
        if 'class="capability-stages"' not in body or 'class="capability-svg"' not in body:
            fail("Capability must use a scroll-revealed graphical workflow", failures)
        if body.count("<li") < 5:
            fail("Capability must expose five sequential stages", failures)
        if 'href="work/index.html#individual-systems">View selected systems</a>' not in body:
            fail("Capability View selected systems must target the individual-systems index", failures)
        if 'data-cap-step="6"' not in raw:
            fail("Capability no-JavaScript default must be the complete final workflow", failures)

    if "desktop-hide-copy" in raw:
        fail("Gap, Fit and Approach copy must stay live HTML, not visually clipped", failures)
    if 'data-scene="gap"' not in raw or 'data-scene="fit"' not in raw or 'data-scene="approach"' not in raw:
        fail("Gap, Fit and Approach must be staged semantic scenes", failures)
    if raw.count('data-chapter-reveal') < 1:
        fail("homepage must mark the stack chapter for progressive reveal", failures)
    if ".scene-erp" in css:
        erp_rule = css.split(".scene-erp,", 1)[-1].split("}", 1)[0]
        if "var(--raised)" in erp_rule or "border-radius: 22px" in erp_rule:
            fail("ERP/no-ERP scenes must not sit in a raised rectangular frame", failures)
    if "html.js .approved-scene-ltr img" not in css or "clip-path: inset(0 100% 0 0)" not in css:
        fail("desktop progressive reveal must clip the approved rasters, not redraw them", failures)
    if "html.js .approved-scene-up img" not in css:
        fail("ERP/no-ERP reveal must uncover the foundation before the fitted layer", failures)
    reduced = css.split("@media (prefers-reduced-motion: reduce)", 1)[-1]
    if "html.js .approved-scene img" not in reduced or "clip-path: inset(0) !important" not in reduced:
        fail("reduced-motion must show the complete approved artwork", failures)
    if "IntersectionObserver" not in js or "data-reveal" not in js:
        fail("chapter reveal must use IntersectionObserver or equivalent on normal scroll", failures)
    if "preventDefault" in js and "wheel" in js:
        fail("progressive reveal must not hijack scroll", failures)
    if "WebGL" in raw or "webgl" in js:
        fail("homepage must not add WebGL", failures)

    if 'class="stack-explain"' not in raw:
        fail("stack explanation must sit outside the scene", failures)
    if "homepage-stack-erp.webp" in raw:
        fail("homepage must not render the ERP stack artwork", failures)

    proof = raw[raw.find('id="proof"'):raw.find('id="approach"')]
    if "View SiteLog" not in proof or "View BudgetFlow" not in proof:
        fail("Proof must keep SiteLog and BudgetFlow view actions", failures)
    if proof.find("View all selected systems") < proof.find('class="proof-grid"'):
        fail("View all selected systems must sit beneath the three-card grid", failures)
    if 'class="button button-systems"' not in proof:
        fail("all-systems action must be a prominent button, not a card-link", failures)
    if 'href="work/index.html#individual-systems">View all selected systems</a>' not in proof:
        fail("Proof all-systems button must target the individual-systems index", failures)
    if "View all systems" in proof:
        fail("finance card must not keep a general View all systems link", failures)
    if 'href="work/index.html#finance">View finance workflow</a>' not in proof:
        fail("finance-specific Proof action must remain finance-specific", failures)
    if 'class="proof-label"' in proof:
        fail("homepage Proof cards must not show Synthetic demonstration labels", failures)

    if 'id="individual-systems"' not in work:
        fail("Selected Systems must expose id=individual-systems for hash selection", failures)
    if 'hash === "#finance" || hash === "#individual-systems"' not in js and 'hash === "#individual-systems"' not in js:
        fail("site.js must select the individual view for #individual-systems", failures)
    if "pageshow" not in js:
        fail("individual-systems hash must be re-applied after the connected view was previously selected", failures)
    if "#individual-systems:target" not in css:
        fail("no-JavaScript arrival at #individual-systems must still reveal the individual index", failures)
    if "#connected-workflow:target" not in css:
        fail("no-JavaScript arrival at #connected-workflow must still reveal the connected view", failures)
    if "popstate" not in js:
        fail("Selected Systems must keep browser back/forward in sync with the view", failures)
    if 'href="work/index.html#connected-workflow">Selected Systems' in raw:
        fail("general Selected Systems actions must not default to the connected view", failures)

    for path in PUBLIC_HTML:
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        for match in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', html):
            href, label = match.group(1), match.group(2).strip()
            if label not in GENERAL_SYSTEMS_LABELS:
                continue
            if "#individual-systems" not in href:
                fail(f"{rel}: {label!r} must use explicit #individual-systems, got {href}", failures)
            if href.endswith("work/") or href.endswith("../work/"):
                fail(f"{rel}: {label!r} still uses a directory URL without the individual hash", failures)
            if "#connected-workflow" in href:
                fail(f"{rel}: general {label!r} must not open the connected view", failures)


def check_approved_artwork(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    required_src = [
        'src="assets/img/age-600/homepage-stack-no-erp.webp"',
    ]
    for src in required_src:
        if src not in raw:
            fail(f"homepage must visibly reference {src}", failures)
        if raw.count(src) != 1:
            fail(f"homepage should declare {src} once as the primary visual", failures)
    for retired in (
        'src="assets/img/age-600/01-the-gap.webp"',
        'src="assets/img/age-600/01b-fit.webp"',
        'src="assets/img/age-600/04-approach.webp"',
    ):
        if retired in raw:
            fail(f"homepage must not keep {retired} as the primary chapter visual", failures)
    if "fit-visual" in raw or "gap-visual" in raw:
        fail("retired simplified SVG chapter drawings must not return as the primary homepage graphics", failures)
    if "<img" in raw:
        for match in re.finditer(
            r'<img\b[^>]*class="[^"]*approved-visual[^"]*"[^>]*>',
            raw,
        ):
            tag = match.group(0)
            if "01b-fit.webp" in tag:
                if 'width="1672"' not in tag or 'height="840"' not in tag:
                    fail(f"cropped Fit visual must declare 1672x840: {tag[:140]}", failures)
            elif 'width="1672"' not in tag or 'height="941"' not in tag:
                fail(f"approved homepage visual must declare source 1672x941: {tag[:120]}", failures)
            if 'loading="lazy"' not in tag or 'decoding="async"' not in tag:
                fail("approved homepage visuals must use lazy loading and async decoding", failures)
    if "clip-path: inset(0 100% 0 0)" not in css.split("html.js", 1)[-1]:
        fail("progressive movement must be scoped to JavaScript so no-JS shows the full artwork", failures)
    if ".approved-scene {" not in css:
        fail("approved scenes need a borderless full-bleed container", failures)
    scene_rule = css.split(".approved-scene {", 1)[-1].split("}", 1)[0]
    if "border: 0" not in scene_rule:
        fail("approved scenes must not sit in a card or outlined frame", failures)
    if "html.js .approved-scene img" not in css.split("@media (prefers-reduced-motion: reduce)", 1)[-1]:
        fail("reduced-motion must force the complete approved artwork", failures)
    if "Only the missing layer" not in raw:
        fail("Fit must keep the live HTML cue for the missing layer", failures)


def check_round5(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    work = (ROOT / "work/index.html").read_text(encoding="utf-8")
    if "Bespoke fixes the manual work that off-the-shelf software leaves behind." not in raw:
        fail("Fit close copy is not the approved sentence", failures)
    if "Proof Systems builds around what already works." not in raw:
        fail("stack supporting copy missing the approved closing line", failures)
    if "bindStickyScene" not in js:
        fail("site.js must drive the Capability sequence from normal scroll", failures)
    if "preventDefault" in js and "wheel" in js:
        fail("Capability sequence must not hijack scroll", failures)
    if "WebGL" in js or "webgl" in raw:
        fail("Capability must not use WebGL", failures)
    reduced = css.split("@media (prefers-reduced-motion: reduce)", 1)[-1]
    if "html.js .cap-stage" not in reduced or "opacity: 1 !important" not in reduced:
        fail("reduced-motion must expose the complete Capability workflow", failures)
    if 'class="button-amber"' not in css.split(".button-amber {", 1)[0] and ".button-amber {" not in css:
        fail("amber/orange action buttons are missing", failures)
    if "background: var(--amber)" not in css.split(".view-switch input:checked + label {", 1)[-1][:180]:
        fail("active Selected Systems control must be solid amber", failures)
    if "border: 1.5px solid var(--amber)" not in css.split(".view-switch label {", 1)[-1][:260]:
        fail("inactive Selected Systems control must use an amber border", failures)
    if work.count('class="button button-amber"') < 8:
        fail("each Selected Systems card must use a centred amber button", failures)
    if 'class="card-link" href="sitelog.html">Explore SiteLog' in work:
        fail("Selected Systems must not keep ordinary Explore text links", failures)
    if 'id="view-connected"' not in work or 'id="view-individual"' not in work:
        fail("Selected Systems must keep accessible view radios", failures)
    if "html:not(.js) #individual-systems:target" not in css:
        fail(
            "no-JavaScript :target fallback must be scoped so it cannot "
            "override the checked radio after history.pushState",
            failures,
        )
    if re.search(r"(?m)^#individual-systems:target", css):
        fail("unscoped #individual-systems:target would keep the individual view visible after Connected is checked", failures)
    if "html:not(.js) .wrap:has(#connected-workflow:target)" not in css:
        fail("no-JavaScript #connected-workflow hash must still select the connected view", failures)


def webp_dimensions(path: pathlib.Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[12:16] == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if data[12:16] == b"VP8 ":
        width = int.from_bytes(data[26:28], "little") & 0x3FFF
        height = int.from_bytes(data[28:30], "little") & 0x3FFF
        return width, height
    raise ValueError(f"unrecognised WebP layout in {path}")


def desktop_cap_step(progress: float) -> int:
    import math

    return min(6, 1 + math.floor(progress * 6))


def check_round6(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    work = (ROOT / "work/index.html").read_text(encoding="utf-8")
    if "practical software integrated with existing technology" not in raw:
        fail("proposition support must include integrated with existing technology", failures)
    if "Operator-led" in raw and "Built around the real workflow" in raw:
        fail("homepage still contains the deleted quiet line", failures)
    desktop = css.split("@media (min-width: 981px)", 1)[-1].split("@media", 1)[0]
    if ".proposition-support" not in desktop or "#start .lede" not in desktop or ".stack-explain" not in desktop:
        fail("desktop wrap must drop half-width caps on proposition, stack copy and Start lede", failures)
    if "max-width: none" not in desktop:
        fail("desktop copy must use the full wrap width", failures)
    if "text-align: center" in desktop.split(".proposition-support", 1)[-1][:120]:
        fail("desktop proposition copy must stay left aligned", failures)
    proof = raw[raw.find('id="proof"'):raw.find('id="approach"')]
    if 'class="proof-label"' in proof:
        fail("homepage Proof cards must not show Synthetic demonstration labels", failures)
    if 'class="proof-label"' in work:
        fail("Selected Systems index must not show card-level Synthetic demonstration labels", failures)
    for slug in STORY_SLUGS:
        story = (ROOT / "work" / f"{slug}.html").read_text(encoding="utf-8")
        if "Synthetic demonstration" not in story:
            fail(f"{slug} story must keep synthetic provenance", failures)
    for phrase in (
        "Frontline capture",
        "Project control",
        "Finance and reporting",
        "Mobile-first weekly site record bespoke to business function.",
        "Admin Ready Invoices &amp; Exports",
        "Turn weekly labour costs into visible budget decisions.",
        "Weekly labour allocation",
        "Budget Control",
        "Accounts Software Exports",
        "Data extracts directly from accounts systems ready for integration to bespoke systems",
    ):
        if phrase not in proof:
            fail(f"Proof cards missing {phrase!r}", failures)
    if proof.count('class="proof-line"') < 6:
        fail("Proof supporting copy must be separate visible lines", failures)
    kicker = css.split(".proof-grid .kicker {", 1)[-1].split("}", 1)[0] if ".proof-grid .kicker {" in css else ""
    if "clamp(1rem" not in kicker:
        fail("homepage Proof kickers must be visibly larger than the default kicker", failures)
    if "Bespoke fixes the manual work that off-the-shelf software leaves behind." not in raw:
        fail("Fit close copy is not the approved sentence", failures)
    fit_path = ROOT / "assets/img/age-600/01b-fit.webp"
    fit_w, fit_h = webp_dimensions(fit_path)
    if (fit_w, fit_h) != (1672, 840):
        fail(f"Fit raster must be 1672x840 without stretch, found {fit_w}x{fit_h}", failures)
    if "Not every gap needs a build" in raw:
        fail("Fit caption copy must not remain in the homepage source", failures)
    cap = re.search(r'<svg class="capability-svg"[\s\S]*?</svg>', raw)
    if not cap:
        fail("Capability illustration is missing", failures)
        return
    svg = cap.group(0)
    if svg.count("<path class=\"cap-connector") != 4:
        fail("Capability must use four separate connector path segments", failures)
    connectors = re.findall(r'class="cap-connector cap-gated" data-cap-from="([2-5])"', svg)
    if connectors != ["2", "3", "4", "5"]:
        fail(f"Capability must have four independently gated connectors, found {connectors}", failures)
    icons = re.findall(r'class="cap-icon cap-gated" data-cap-from="([1-5])"', svg)
    if icons != ["1", "2", "3", "4", "5"]:
        fail(f"Capability must independently gate five relevant icons, found {icons}", failures)
    if "cap-spark" not in svg or "cap-check" not in svg:
        fail("Capability icons must include automation-control and team-learning cues", failures)
    if "visibility: hidden" not in css.split("html.js .cap-stage", 1)[-1][:180]:
        fail("future Capability captions must be fully hidden, not dimmed", failures)
    if re.search(r"\.cap-stage[^{]*\{[^}]*opacity:\s*0\.28", css):
        fail("Capability must not leave inactive stages visible as dimmed text", failures)
    if "Ask about AI team training" not in raw:
        fail("Capability action must be Ask about AI team training", failures)
    if "Math.min(steps, 1 + Math.floor(progress * steps))" not in js:
        fail("Capability desktop steps must use equal travel buckets", failures)
    if "400vh" not in css:
        fail("desktop Capability travel must be shorter than 480vh while remaining distinct", failures)
    if "560vh" in css:
        fail("desktop Capability travel must no longer use the longer 560vh interval", failures)
    expected_steps = {
        0.00: 1,
        0.16: 1,
        0.17: 2,
        0.33: 2,
        0.34: 3,
        0.49: 3,
        0.50: 4,
        0.66: 4,
        0.67: 5,
        0.83: 5,
        0.84: 6,
        1.00: 6,
    }
    for progress, want in expected_steps.items():
        got = desktop_cap_step(progress)
        if got != want:
            fail(f"Capability step at progress {progress} is {got}, expected {want}", failures)
    previous = 1
    for index in range(0, 101):
        current = desktop_cap_step(index / 100)
        if current < previous:
            fail("Capability desktop steps must stay coherent when scrolling forward", failures)
        previous = current
    previous = 6
    for index in range(100, -1, -1):
        current = desktop_cap_step(index / 100)
        if current > previous:
            fail("Capability desktop steps must stay coherent when scrolling back", failures)
        previous = current
    radio_block = css.split(".wrap:has(#view-connected:checked) .work-connected", 1)[-1][:80]
    if "display: block" not in radio_block:
        fail("JavaScript checked-radio state must show the connected view", failures)
    check_round6_review_corrections(css, js, failures)


def check_round6_review_corrections(css: str, js: str, failures: list[str]) -> None:
    for match in re.finditer(r"\.proof-line[^{]*\{([^}]*)\}", css):
        body = match.group(1)
        if re.search(r"color:\s*var\(--ink\)", body) or re.search(r"color:\s*#17120d", body, re.I):
            fail("Proof supporting lines must not use ink on the dark Proof cards", failures)
        colors = re.findall(r"color:\s*([^;]+)", body)
        for value in colors:
            token = value.strip().lower()
            if token in {"var(--cream)", "var(--text)", "#f3eee4", "#fffdf8", "#ffffff"}:
                continue
            fail(f"Proof supporting lines must use a light colour, found {value.strip()}", failures)
    if "var(--cream)" not in css.split(".proof-line {", 1)[-1].split("}", 1)[0]:
        fail("base .proof-line colour must be cream", failures)
    if "var(--raised)" not in css.split(".panel-cream .proof-grid .card {", 1)[-1].split("}", 1)[0]:
        fail("homepage Proof cards must keep the dark raised background", failures)

    hidden_sel = 'html.js #capability[data-capability]:not([data-cap-step="6"]) .capability-actions {'
    if hidden_sel not in css:
        fail("desktop JS must hide Capability actions until stage 6", failures)
    else:
        hidden = css.split(hidden_sel, 1)[-1].split("}", 1)[0]
        if "visibility: hidden" not in hidden:
            fail("Capability actions must be visibility:hidden before stage 6 so they leave keyboard focus and AT", failures)
        if "pointer-events: none" not in hidden:
            fail("Capability actions must ignore pointer input before stage 6", failures)
        if "opacity: 0" not in hidden:
            fail("Capability actions must be visually hidden before stage 6", failures)
        if "visibility: visible" in hidden:
            fail("pre-stage-6 Capability actions must not stay visibility:visible", failures)
    shown_sel = 'html.js #capability[data-capability][data-cap-step="6"] .capability-actions {'
    if shown_sel not in css:
        fail("stage 6 must explicitly expose Capability actions", failures)
    else:
        shown = css.split(shown_sel, 1)[-1].split("}", 1)[0]
        if "visibility: visible" not in shown:
            fail("stage 6 Capability actions must be visibility:visible", failures)
        if "pointer-events: auto" not in shown:
            fail("stage 6 Capability actions must be pointer-reachable", failures)
    if "syncCapabilityActions" not in js:
        fail("site.js must sync Capability action exposure with the current stage", failures)
    if 'setAttribute("inert"' not in js or 'setAttribute("aria-hidden"' not in js:
        fail("Capability actions must be inert and aria-hidden before stage 6", failures)
    if 'removeAttribute("inert")' not in js or 'removeAttribute("aria-hidden")' not in js:
        fail("Capability actions must drop inert/aria-hidden at stage 6", failures)
    if 'String(step) === "6"' not in js:
        fail("Capability action exposure must follow the stage-6 threshold", failures)
    reduced_exposes = False
    for block in css.split("@media (prefers-reduced-motion: reduce)")[1:]:
        body = block.split("@media", 1)[0]
        if ".capability-actions" not in body:
            continue
        rule = body.split(".capability-actions", 1)[-1][:240]
        if "visibility: visible !important" in rule and "pointer-events: auto" in rule:
            reduced_exposes = True
    if not reduced_exposes:
        fail("reduced-motion must expose Capability actions without waiting for animation", failures)


def check_round7(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    work = (ROOT / "work/index.html").read_text(encoding="utf-8")
    training = (ROOT / "training.html").read_text(encoding="utf-8")
    workflow = (ROOT / "workflow.html").read_text(encoding="utf-8")
    new_linkedin = "https://www.linkedin.com/in/mathew-glendenning-90670649/"
    old_linkedin = "https://www.linkedin.com/in/mat-glendenning"
    if "AI Automation comes after the workflow works. Repetitive tasks can then be automated safely." not in raw:
        fail("Controlled automation narrative must use the approved AI Automation sentence", failures)
    if raw.count("AI Automation comes after") < 1:
        fail("homepage should contain the AI Automation sentence", failures)
    if 'data-cap-step="6"' not in raw:
        fail("Capability no-JS default must be stage 6 so actions are present", failures)
    if "400vh" not in css.split("html.js #capability[data-capability]", 1)[-1][:80]:
        fail("desktop Capability min-height must be 400vh", failures)
    if "[data-cap-step=\"5\"] .cap-gated" not in css or "[data-cap-step=\"6\"] .cap-gated" not in css:
        fail("stage 5 and stage 6 must both show the five Capability icons", failures)
    if 'String(step) === "6"' not in js:
        fail("Capability actions must wait for stage 6", failures)
    if training.count("A remote or in-person half-day") != 2:
        fail("training page must use A remote or in-person half-day twice", failures)
    if "A remote half-day" in training:
        fail("training page still uses A remote half-day", failures)
    if "page-training" not in training or ".page-training h1" not in css or ".page-training .intro" not in css:
        fail("training heading and intro must use the full desktop wrap", failures)
    if "This connected workflow began as independent bespoke systems, built one at a time with a long-term approach that allowed them to form one fully integrated system." not in work:
        fail("Connected workflow disclosure is not the approved sentence", failures)
    if "synthetic Northstar business story" in work:
        fail("old Connected workflow disclosure remains", failures)
    if 'class="map-text"' in work:
        fail("connected-workflow map-text paragraph must be removed", failures)
    if "These are operator-built systems demonstrated with synthetic Northstar data" not in work:
        fail("Selected Systems must keep the page-level synthetic Northstar explanation", failures)
    if work.count('class="card-label">Outcome</p>') != 8:
        fail("each Selected Systems card must show Outcome as its own label", failures)
    if work.count('class="card-label">Evidence shown</p>') != 8:
        fail("each Selected Systems card must show Evidence shown as its own label", failures)
    if "<strong>Outcome." in work or "<strong>Evidence shown." in work:
        fail("Selected Systems cards must not keep Outcome/Evidence as inline strong prefixes", failures)
    sitelog = (ROOT / "work/sitelog.html").read_text(encoding="utf-8")
    if "Off-the-shelf options didn't fit how the business operated and became expensive through per-user charges." not in sitelog:
        fail("SiteLog problem copy is not the approved paragraph", failures)
    budgetflow = (ROOT / "work/budgetflow.html").read_text(encoding="utf-8")
    if "Off-the-shelf options require the business to change its operating approach to fit the software." not in budgetflow:
        fail("BudgetFlow problem copy is not the approved paragraph", failures)
    if 'href="applications-ledger.html">Suggested next: Applications Ledger</a>' not in budgetflow:
        fail("BudgetFlow suggested next must be Applications Ledger", failures)
    if "ledgerlink.html" in budgetflow[budgetflow.find("Suggested next"):budgetflow.find("Suggested next") + 180]:
        fail("BudgetFlow suggested next must not remain LedgerLink", failures)
    apps = (ROOT / "work/applications-ledger.html").read_text(encoding="utf-8")
    if "This makes it difficult to maintain business-wide visibility of late payments and outstanding actions." not in apps:
        fail("Applications Ledger problem copy is not the approved paragraph", failures)
    cashflow = (ROOT / "work/cashflow.html").read_text(encoding="utf-8")
    if "Cash views are often rebuilt manually in Excel from applications, bank files and project schedules that do not share a source." not in cashflow:
        fail("Cashflow problem copy is not the approved paragraph", failures)
    cpr = (ROOT / "work/cpr.html").read_text(encoding="utf-8")
    if "<h2>How it is used</h2>" not in cpr:
        fail("CPR heading must be How it is used", failures)
    if "Every bespoke system draws on one trusted source of project information." not in cpr:
        fail("CPR How it is used copy is not the approved paragraph", failures)
    if "<h2>Who uses it</h2>" in cpr:
        fail("CPR must not keep Who uses it", failures)
    join = css.split("@media (min-width: 761px)", 1)[-1].split("@media", 1)[0]
    for selector in (".chapter-hero", "#gap", "#economics", "#proof", "#approach", "#about"):
        if selector not in join:
            fail(f"desktop chapter-join rule missing {selector}", failures)
    if "padding-bottom: 0" not in join.split(".chapter-hero", 1)[-1][:80]:
        fail("proposition/stack must drop the empty bottom band into Gap", failures)
    if "padding-bottom: 0" not in join.split("#gap", 1)[-1][:220]:
        fail("Gap scene must not leave an empty cream band into Fit", failures)
    if "padding-bottom: 0" not in join.split("#economics", 1)[-1][:220] and "padding-bottom: 0" not in join.split("#gap,", 1)[-1][:280]:
        fail("Fit/Approach chapter joins must not leave empty outgoing bands", failures)
    if "padding-bottom: 0" not in join.split("#approach", 1)[-1][:220]:
        fail("Approach scene must not leave an empty band into Operator First", failures)
    if "page-enquiry" not in workflow or ".page-enquiry .page-main .wrap" not in css:
        fail("enquiry page must centre a bounded desktop column", failures)
    if "width: min(46rem" not in css.split(".page-enquiry .page-main .wrap", 1)[-1][:120]:
        fail("enquiry column must stay a readable centred measure, not viewport-edge", failures)
    if "#individual-systems" not in css or "#connected-workflow" not in css:
        fail("Selected Systems hash targets must be present in CSS", failures)
    margin_src = css
    if "scroll-margin-top" not in margin_src or "var(--nav-h)" not in margin_src.split("scroll-margin-top", 1)[-1][:80]:
        fail("Selected Systems anchors must offset hash scroll by --nav-h so cards clear the sticky nav", failures)
    for target in ("#individual-systems", "#connected-workflow", "#finance"):
        nearby = css.split(target, 1)
        if len(nearby) < 2 or "scroll-margin-top" not in nearby[-1][:280] and "scroll-margin-top" not in css[max(0, css.find(target) - 160):css.find(target) + 220]:
            fail(f"{target} must use scroll-margin-top so hash navigation clears the sticky nav", failures)
    for path in PUBLIC_HTML:
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if old_linkedin in html:
            fail(f"{rel} still uses the old LinkedIn destination", failures)
        if "LinkedIn" in html and new_linkedin not in html:
            fail(f"{rel} LinkedIn label is missing the approved profile URL", failures)
        if new_linkedin in html and 'rel="noopener noreferrer"' not in html:
            fail(f"{rel} LinkedIn link must keep external-link security attributes", failures)


def check_round8(failures: list[str]) -> None:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    if 'class="gap-scene"' not in raw or 'class="fit-scene"' not in raw or 'class="approach-journey"' not in raw:
        fail("homepage must use semantic Gap, Fit and Approach scenes", failures)
    if "Industry Specific Software" not in raw:
        fail("Fit scene missing Industry Specific Software", failures)
    if "Waiting · hidden" not in raw or "Too late" not in raw:
        fail("Gap captions must include Waiting · hidden and Too late", failures)
    if 'data-gap-step="4"' not in raw or 'data-fit-step="4"' not in raw or 'data-approach-step="5"' not in raw:
        fail("Gap, Fit and Approach no-JS defaults must be the complete final scenes", failures)
    if 'class="capability-journey"' not in raw:
        fail("Capability must include the vertical journey composition", failures)
    if "bindStickyScene" not in js:
        fail("site.js must stage Gap, Fit, Approach and Capability from natural scroll", failures)
    if "preventDefault" in js and "wheel" in js:
        fail("scene staging must not hijack scroll", failures)
    if "300vh" not in css or "360vh" not in css:
        fail("Gap/Fit/Approach travel must be short staged sticky heights", failures)
    if ".fit-transition" not in css or "stroke-width: 3" not in css.split(".fit-transition path", 1)[-1][:180]:
        fail("Fit connector must use a 3-unit amber stroke", failures)
    if ".fit-transition-vertical" not in css:
        fail("Fit narrow composition must use a vertical connecting arrow", failures)
    if ".approach-node-b" not in css or "top: -8%" not in css.split(".approach-node-b", 1)[-1][:120]:
        fail("Understand people node must sit separately above the magnifying glass", failures)
    if "fonts.googleapis" in raw or "data-lucide" in raw:
        fail("homepage scenes must not add remote icons or fonts", failures)
    if ".capability-journey { display: none; }" not in css:
        fail("wide Capability must keep the horizontal journey and hide the vertical one", failures)
    reduced = css.split("@media (prefers-reduced-motion: reduce)")[-1]
    if "[data-scene]" not in reduced or "min-height: 0" not in reduced:
        fail("reduced-motion must present the complete staged scenes", failures)
    check_narrow_gap_overflow(css, failures)


def narrow_gap_unclipped_right_edge(viewport: int) -> float:
    """Predicted document right edge of the rotated Gap connector if the scene does not clip.

    Vertical Gap uses `rotate(90deg) scaleX(1.47) scaleY(0.72)` on a 38rem-tall
    `.gap-links` box. CSS transforms apply right-to-left, so the axis-aligned
    width after rotation is `38rem * 0.72`. Independent review measured 379px,
    399px and 414px at 320/360/390; this geometry reproduces those figures.
    """
    scene_height = 38 * 16
    wrap = viewport - 32
    scene_width = min(wrap, 30 * 16)
    aabb_width = scene_height * 0.72
    pad = (viewport - scene_width) / 2
    return pad + scene_width / 2 + aabb_width / 2


def check_narrow_gap_overflow(css: str, failures: list[str]) -> None:
    measured = {320: 379, 360: 399, 390: 414}
    for viewport, observed in measured.items():
        predicted = narrow_gap_unclipped_right_edge(viewport)
        if abs(predicted - observed) > 1.5:
            fail(
                f"Gap connector geometry no longer matches the reviewed overflow "
                f"at {viewport}px (predicted {predicted:.1f}, reviewed {observed})",
                failures,
            )
        if predicted <= viewport:
            fail(
                f"narrow Gap connector at {viewport}px would no longer overflow without containment",
                failures,
            )
    for viewport in (500, 768, 1024, 1280, 1440):
        if narrow_gap_unclipped_right_edge(viewport) > viewport + 1:
            fail(
                f"Gap connector geometry now overflows at {viewport}px where review found none",
                failures,
            )
    narrow = css.split("@media (max-width: 900px)", 1)
    if len(narrow) < 2:
        fail("narrow Gap composition breakpoint is missing", failures)
        return
    block = narrow[-1].split("@media", 1)[0]
    scene_rule = block.split(".gap-scene {", 1)
    if len(scene_rule) < 2:
        fail("narrow Gap scene rule is missing", failures)
        return
    body = scene_rule[-1].split("}", 1)[0]
    if "overflow: hidden" not in body:
        fail(
            "narrow .gap-scene must clip the rotated .gap-links box so 320/360/390 "
            "viewports do not grow a horizontal scrollbar",
            failures,
        )
    if "rotate(90deg)" not in block or "scaleX(1.47)" not in block or "scaleY(0.72)" not in block:
        fail("narrow Gap must keep the approved rotated connector composition", failures)
    if "overflow-x: hidden" in body:
        fail("Gap overflow must be contained on the scene, not by hiding page overflow", failures)
    check_approach_stage_scope(css, failures)


def check_approach_stage_scope(css: str, failures: list[str]) -> None:
    for match in re.finditer(r"(?m)^\.approach-stage\s*\{([^}]*)\}", css):
        body = match.group(1)
        if "linear-gradient" in body or "#2a3038" in body:
            fail(
                "unscoped .approach-stage must not paint the legacy dark card behind journey titles",
                failures,
            )
    if re.search(r"(?m)^\.approach-stage span\s*\{", css):
        fail(
            "legacy .approach-stage span must be scoped so it cannot restyle journey SVG nodes",
            failures,
        )
    if re.search(r"(?m)^\.approach-stage strong\s*\{", css) or re.search(
        r"(?m)^\.approach-stage em\s*\{", css
    ):
        fail("legacy .approach-stage strong/em must be scoped to .approach-stages", failures)
    journey = css.split(".approach-journey .approach-stage {", 1)
    if len(journey) < 2:
        fail("Approach journey stage wrapper needs an explicit transparent reset", failures)
        return
    reset = journey[-1].split("}", 1)[0]
    if "background: none" not in reset and "background: transparent" not in reset:
        fail("Approach journey stage wrapper must be transparent on the sand section", failures)
    if "box-shadow: none" not in reset:
        fail("Approach journey stage wrapper must not keep the legacy drop shadow", failures)
    if "border: 0" not in reset and "border: none" not in reset:
        fail("Approach journey stage wrapper must be unframed", failures)
    meta = css.split(".approach-meta h3 {", 1)
    if len(meta) < 2 or "var(--ink)" not in meta[-1].split("}", 1)[0]:
        fail("Approach stage titles must use ink so they read on the sand background", failures)
    if ".approach-stages .approach-stage" not in css:
        fail("legacy Approach card styling must remain scoped to .approach-stages", failures)


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
    check_round4(failures)
    check_approved_artwork(failures)
    check_round5(failures)
    check_round6(failures)
    check_round7(failures)
    check_round8(failures)
    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS routes, eight stories, round-8 staged Gap/Fit/Capability/Approach scenes, "
        "round-7 training/work/stories/joins/enquiry/LinkedIn, enquiry form, "
        "omitted client chapter, poster-first teasers and public-copy safety"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
