#!/usr/bin/env python3
"""Deterministic checks for the Proof Systems V2 site contract."""

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
    "sitelog", "budgetflow", "applications-ledger", "cpr", "probables",
    "ledgerlink", "cashflow", "management-accounts",
]
FILM_STORY_SLUGS = [slug for slug in STORY_SLUGS if slug != "management-accounts"]
TEASERS = ["sitelog", "budgetflow", "ledgerlink"]
WITHDRAWN_MEDIA_NAMES = (
    "management-accounts-demo.mp4",
    "management-accounts-poster.jpg",
    "management-accounts-demo.vtt",
)

PUBLIC_REJECTED = [
    "Pantera", "Pete Mills", "Xonetic", "founding cohort", "founding-diagnostic",
    "four founding", "Four founding", "four places", "free founding",
    "Apply for a founding", "founding diagnostic", "£350", "decision_role",
    "desired_outcome", "hours_per_week", "application-received",
    "CLIENT PERSPECTIVE", "Contract Performance Reporting", "Avenir Next",
    "fonts.googleapis", "fonts.gstatic",
]

FORM_REQUIRED = [
    'name="proof-systems-qualifier"', 'data-netlify="true"',
    'netlify-honeypot="bot-field"', 'name="bot-field"',
    'name="route_key" value="general-enquiry"',
    'name="route_label" value="Discuss a workflow"',
    'name="lead_state" value="enquiry-received"',
    'name="page_source" value="workflow.html"', 'name="submitted_at"',
    'name="name"', 'name="email"', 'name="company"',
    'name="workflow_help"', 'name="contact_consent"', "Send enquiry",
    "Tell me about one workflow that should work better.",
]
VISIBLE_FIELDS = {"name", "email", "company", "workflow_help", "contact_consent"}
HIDDEN_FIELDS = {
    "form-name", "bot-field", "route_key", "route_label", "lead_state",
    "page_source", "submitted_at", "interest_source",
}

FOOTER_COPYRIGHT = "© 2026 Proof Systems"
FOOTER_LEGAL = (
    "Proof Systems is the trading name of Mathew Glendenning, a sole trader. "
    "Correspondence address: Unit 171774, Courier Point, 13 Freeland Park, "
    "Wareham Road, Poole, BH16 6FH. Email: mat@proofsystems.co.uk"
)
CONSENT_VISIBLE = (
    "I agree that Mathew Glendenning, trading as Proof Systems, may use these "
    "details to assess my enquiry and contact me about it. I have read the privacy notice."
)


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.ids: set[str] = set()
        self.refs: list[tuple[str, str]] = []
        self.videos: list[dict] = []
        self.current_video: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        element_id = attr.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            self.ids.add(element_id)
        for name in ("href", "src", "poster"):
            if attr.get(name):
                self.refs.append((name, attr[name]))
        if tag == "video":
            self.current_video = {"attrs": attr, "sources": [], "tracks": []}
            self.videos.append(self.current_video)
        elif tag == "source" and self.current_video is not None:
            self.current_video["sources"].append(attr)
        elif tag == "track" and self.current_video is not None:
            self.current_video["tracks"].append(attr)
        if tag not in {"meta", "link", "img", "br", "input", "hr", "source", "track"}:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "video":
            self.current_video = None
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"unexpected closing tag: {tag}")


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
        current /= part
    return current.is_file()


def visible_text(raw: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def identity_errors(raw: str, label: str) -> list[str]:
    """Return public identity failures for one page; also used by mutation fixtures."""
    errors: list[str] = []
    text = visible_text(raw)
    disclosure = "Proof Systems is the trading name of Mathew Glendenning, a sole trader."
    if text.count(disclosure) != 1:
        errors.append(f"{label}: sole-trader disclosure count is {text.count(disclosure)}, expected 1")
    footer = re.search(r"<footer[\s\S]*?</footer>", raw, flags=re.I)
    if not footer:
        errors.append(f"{label}: missing footer")
        return errors
    legal = re.search(r'<p class="footer-legal">([\s\S]*?)</p>', footer.group(0), flags=re.I)
    if not legal:
        errors.append(f"{label}: missing footer legal block")
    else:
        legal_text = visible_text(legal.group(1))
        if FOOTER_LEGAL not in legal_text:
            errors.append(f"{label}: incomplete sole-trader footer identity")
        if 'href="mailto:mat@proofsystems.co.uk"' not in legal.group(1):
            errors.append(f"{label}: legal email is not a clickable mailto")
    for pattern, description in (
        (r"\bLtd\.?\b", "Ltd wording"),
        (r"registered office", "registered-office wording"),
        (r"company number", "company-number claim"),
        (r"\bincorporated\b", "incorporated-company claim"),
    ):
        if re.search(pattern, text, flags=re.I):
            errors.append(f"{label}: prohibited identity claim: {description}")
    return errors


def contrast_ratio(foreground: str, background: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index:index + 2], 16) / 255 for index in (0, 2, 4)]
        linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    first, second = luminance(foreground.lstrip("#")), luminance(background.lstrip("#"))
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)


def parse(path: pathlib.Path) -> tuple[str, PageParser]:
    raw = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    return raw, parser


def check_html_and_links(failures: list[str]) -> None:
    for path in PUBLIC_HTML:
        raw, parser = parse(path)
        rel = path.relative_to(ROOT)
        if parser.stack:
            fail(f"{rel}: unclosed tags {parser.stack}", failures)
        failures.extend(f"{rel}: {error}" for error in parser.errors)
        if 'lang="en-GB"' not in raw:
            fail(f"{rel}: missing British English language declaration", failures)
        for kind, value in parser.refs:
            parsed = urllib.parse.urlparse(value)
            if parsed.scheme in {"http", "https", "mailto", "data"} or value.startswith("#"):
                continue
            target_ref = urllib.parse.unquote(parsed.path)
            if not target_ref:
                continue
            target = (path.parent / target_ref).resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                fail(f"{rel}: missing local {kind} target {value}", failures)
                continue
            if parsed.fragment and target.suffix == ".html":
                target_raw = target.read_text(encoding="utf-8")
                if not re.search(rf'id=["\']{re.escape(parsed.fragment)}["\']', target_raw):
                    fail(f"{rel}: missing anchor target {value}", failures)


def check_required_routes(failures: list[str]) -> None:
    required = [
        "index.html", "workflow.html", "privacy.html", "training.html",
        "checkout.html", "video-series.html", "work/index.html", "_redirects",
        "assets/css/site.css", "assets/js/site.js", "assets/js/form.js",
        "assets/fonts/InterVariable.woff2", "assets/fonts/LICENSE.txt",
        "assets/brand/logo-light.svg", "assets/brand/icon-light.svg",
        "assets/img/social.jpg", "favicon.svg",
    ]
    required.extend(f"work/{slug}.html" for slug in STORY_SLUGS)
    for rel in required:
        if not exact_case_file(ROOT, rel):
            fail(f"missing required path: {rel}", failures)


def check_homepage_v2(failures: list[str]) -> None:
    raw, parser = parse(ROOT / "index.html")
    text = visible_text(raw)
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    required_copy = [
        "Systems built around how your business really works.",
        "When software doesn’t fit, the work finds a way around it.",
        "Sometimes the process is reshaped to suit the software.",
        "spreadsheets, email and separate files",
        "The team keeps the work moving. The information gets left behind",
        "connected information and accountability",
        "Keep the software that works. Connect the work that falls between it.",
        "I trace how the work really moves",
        "smallest shared layer",
        "Start with one workflow. Prove the useful change.",
        "Operational systems first.",
        "Evidence from construction operations",
        "These examples draw on construction experience",
        "synthetic data",
        "Discuss a workflow",
    ]
    for phrase in required_copy:
        if phrase not in text:
            fail(f"homepage missing V2 outcome copy: {phrase}", failures)
    for internal_phrase in ("They qualify the approach", "Primary work", "Supporting method", "Supporting route"):
        if internal_phrase in text:
            fail(f"homepage exposes internal strategy label: {internal_phrase}", failures)

    if 'class="home-v2"' not in raw:
        fail("homepage missing the V2 scope class", failures)
    if "data-v2-opening" not in raw or "data-opening-progress=\"1\"" not in raw:
        fail("homepage opening must have a complete no-JavaScript default", failures)
    if len(re.findall(r'class="v2-mark-node(?:\s|\")', raw)) != 5:
        fail("approved B opening must keep the five-node mark", failures)
    if "v2-mark-ghost" not in raw or "v2-mark-outline" not in raw:
        fail("approved B opening must keep its shallow-depth echo and outline", failures)
    if "setPath(main, points)" not in js or "setPath(branches[0], points)" not in js:
        fail("opening connectors must follow moving node endpoints", failures)
    if "progressThrough(opening)" not in js or 'addEventListener("scroll"' not in js:
        fail("opening must be driven by native scroll", failures)
    if "preventDefault" in js and any(event in js for event in ("wheel", "touchmove")):
        fail("site.js must not hijack wheel or touch scrolling", failures)
    if "scroll-snap" in css:
        fail("V2 must not use scroll snapping", failures)

    if "data-work-story" not in raw or 'data-story-step="4"' not in raw:
        fail("workflow story must have a complete no-JavaScript default", failures)
    for detail in (
        "R-2041", "Order change", "Due 16 September", "Due 18 September",
        "Revised date approved", "Requirement", "Owner", "Status",
        "Approval and history attached",
    ):
        if detail not in text:
            fail(f"connected-record illustration missing {detail}", failures)
    if text.find("Evidence from construction operations") < text.find("Keep the software that works"):
        fail("construction evidence must follow the general software-fit narrative", failures)
    if "@media (prefers-reduced-motion: reduce)" not in css or ".v2-opening { min-height: 100vh; }" not in css:
        fail("reduced motion must expose the complete opening without scroll travel", failures)
    if ".v2-work-story { min-height: 0; padding: 8rem 0; }" not in css:
        fail("reduced motion must expose the complete workflow in ordinary flow", failures)
    if '(max-width: 900px), (max-height: 760px)' not in js or "storyStaticQuery.matches" not in js:
        fail("tablet and phone workflow stories must use the readable static composition", failures)
    if "html:not(.motion-ready) .v2-flow" not in css:
        fail("no-JavaScript workflow must expose the readable vertical record trail", failures)
    if "html.story-static .v2-work-story" not in css:
        fail("short desktop windows must use the same unclipped static story composition", failures)
    if "@media (max-height: 700px) and (min-width: 901px)" not in css or ".v2-opening-sticky { min-height: 0; }" not in css:
        fail("short desktop windows must receive a viewport-height-safe opening", failures)
    if ".home-v2 .site-nav { position: fixed; background: rgba(11, 14, 16, 0.94); }" not in css:
        fail("no-JavaScript navigation must keep an opaque readable fallback", failures)
    if "html.motion-ready .home-v2 .site-nav:not(.is-compact) { background: transparent; }" not in css:
        fail("transparent opening navigation must be limited to successful enhancement", failures)
    for foreground, background, label in (
        ("#d9a061", "#0b0e10", "dark-opening eyebrow"),
        ("#d9a061", "#111518", "dark-story eyebrow"),
        ("#70451f", "#d9c5a4", "sand-section eyebrow"),
    ):
        if contrast_ratio(foreground, background) < 4.5:
            fail(f"{label} contrast is below 4.5:1", failures)
    if ".v2-approach-list strong" not in css or "color: #1b1d1c" not in css:
        fail("approach step titles need an explicit dark colour on sand", failures)
    if ".home-v2 .v2-all-systems { color: #1c1f1f" not in css:
        fail("Selected Systems ghost action needs explicit dark text on cream", failures)
    if contrast_ratio("#1c1f1f", "#f0ece2") < 4.5:
        fail("Selected Systems ghost action contrast is below 4.5:1", failures)

    for anchor in ("fit", "how", "proof", "about", "approach", "start", "proposition", "gap", "economics", "capability"):
        if anchor not in parser.ids:
            fail(f"homepage missing useful/legacy anchor #{anchor}", failures)
    if 'href="workflow.html"' not in raw or 'href="work/index.html"' not in raw:
        fail("homepage missing enquiry or systems destination", failures)
    if 'href="training.html"' not in raw:
        fail("homepage missing the supporting training route", failures)
    if 'class="card"' in raw or 'class="proof-grid"' in raw:
        fail("homepage must not regress to the V1 card-grid presentation", failures)

    if parser.videos:
        fail("homepage must stay poster-first; teaser videos are injected only when eligible", failures)
    for slug in TEASERS:
        teaser = f'assets/demo-media/{slug}-teaser.mp4'
        poster = f'assets/demo-media/{slug}-poster.jpg'
        if f'data-teaser-src="{teaser}"' not in raw or f'data-poster="{poster}"' not in raw:
            fail(f"homepage missing poster-first {slug} teaser", failures)
    for slug in FILM_STORY_SLUGS:
        if f"assets/demo-media/{slug}-demo.mp4" in raw:
            fail(f"homepage must not load the full {slug} film", failures)


def check_form(failures: list[str]) -> None:
    raw, _ = parse(ROOT / "workflow.html")
    text = visible_text(raw)
    js = (ROOT / "assets/js/form.js").read_text(encoding="utf-8")
    for phrase in FORM_REQUIRED:
        if phrase not in raw:
            fail(f"workflow.html missing {phrase}", failures)
    names = re.findall(r'<(?:input|textarea)[^>]*name="([^"]+)"', raw)
    visible = set(names) - HIDDEN_FIELDS
    if visible != VISIBLE_FIELDS:
        fail(f"visible form fields {sorted(visible)} != {sorted(VISIBLE_FIELDS)}", failures)
    if 'method="POST"' not in raw:
        fail("enquiry form must POST", failures)
    if "preventDefault" not in js or "file:" not in js or "127.0.0.1" not in js:
        fail("form.js must keep local submissions local and on-page", failures)
    for key in ("focused-build", "workflow-diagnostic", "ai-team-training"):
        if key not in js:
            fail(f"form.js missing allow-listed interest {key}", failures)
    if "INTERESTS[requested]" not in js or "history.replaceState" not in js:
        fail("form.js must validate and remove interest context from the URL", failures)
    consent = re.search(r'<label for="consent">([\s\S]*?)</label>', raw)
    if not consent:
        fail("workflow.html missing consent label", failures)
    else:
        value = re.sub(r"<[^>]+>", "", consent.group(1))
        value = re.sub(r"\s+", " ", value).strip()
        if value != CONSENT_VISIBLE:
            fail("workflow.html consent does not preserve the approved sole-trader wording", failures)
        if 'href="privacy.html"' not in consent.group(1):
            fail("workflow consent must link to the privacy notice", failures)


def check_stories_and_media(failures: list[str]) -> None:
    for slug in FILM_STORY_SLUGS:
        path = ROOT / "work" / f"{slug}.html"
        raw, parser = parse(path)
        if len(parser.videos) != 1:
            fail(f"{path.name}: expected one film, got {len(parser.videos)}", failures)
            continue
        video = parser.videos[0]
        attrs = video["attrs"]
        if "controls" not in attrs or "autoplay" in attrs or "loop" in attrs:
            fail(f"{path.name}: film must use controls without autoplay or looping", failures)
        if attrs.get("preload") not in {"none", "metadata"}:
            fail(f"{path.name}: invalid preload {attrs.get('preload')}", failures)
        source = f"../assets/demo-media/{slug}-demo.mp4"
        poster = f"../assets/demo-media/{slug}-poster.jpg"
        captions = f"../assets/demo-media/{slug}-demo.vtt"
        if source not in raw or poster not in raw or captions not in raw:
            fail(f"{path.name}: missing film, poster or captions", failures)
        if "What this film shows" not in raw or "Synthetic demonstration" not in raw:
            fail(f"{path.name}: missing film context or synthetic status", failures)
        tracks = video["tracks"]
        sources = video["sources"]
        if len(sources) != 1 or sources[0].get("src") != source or sources[0].get("type") != "video/mp4":
            fail(f"{path.name}: film source is not exactly associated with its story", failures)
        if len(tracks) != 1 or tracks[0].get("src") != captions:
            fail(f"{path.name}: captions are not exactly associated with their film", failures)
        elif tracks[0].get("kind") != "captions" or tracks[0].get("label") != "English descriptions" or tracks[0].get("srclang") != "en":
            fail(f"{path.name}: missing labelled English description track", failures)
        elif "default" in tracks[0]:
            fail(f"{path.name}: silent-film description track must not be forced by default", failures)

    ma = ROOT / "work" / "management-accounts.html"
    raw, parser = parse(ma)
    if parser.videos or "What the system covers" not in raw:
        fail("Management Accounts must remain a written system example", failures)
    for name in WITHDRAWN_MEDIA_NAMES:
        if name in raw or (ROOT / "assets" / "demo-media" / name).exists():
            fail(f"public tree still exposes withdrawn media {name}", failures)

    work = (ROOT / "work" / "index.html").read_text(encoding="utf-8")
    cards = re.findall(r'<article class="card"[\s\S]*?</article>', work)
    if len(cards) != 8:
        fail(f"Selected Systems must keep eight entries, found {len(cards)}", failures)
    if len([card for card in cards if ">Evidence shown<" in card]) != 7:
        fail("Selected Systems must keep seven film-evidence entries", failures)
    if "Management Accounts" not in work or "What the system covers" not in work:
        fail("Selected Systems must keep the written Management Accounts entry", failures)


def check_public_safety_and_identity(failures: list[str]) -> None:
    joined = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_HTML)
    for phrase in PUBLIC_REJECTED:
        if phrase in joined:
            fail(f"public HTML contains prohibited or stale phrase: {phrase}", failures)
    footer_pages = [ROOT / "index.html", ROOT / "workflow.html", ROOT / "privacy.html", ROOT / "training.html", ROOT / "work" / "index.html"]
    footer_pages.extend(ROOT / "work" / f"{slug}.html" for slug in STORY_SLUGS)
    for path in footer_pages:
        raw = path.read_text(encoding="utf-8")
        text = visible_text(raw)
        if FOOTER_COPYRIGHT not in text:
            fail(f"{path.relative_to(ROOT)} missing copyright identity", failures)
        failures.extend(identity_errors(raw, str(path.relative_to(ROOT))))

    # Focused mutation fixtures prove that retained identity safeguards fail closed.
    home_raw = (ROOT / "index.html").read_text(encoding="utf-8")
    incorporated = identity_errors(home_raw + "<p>Proof Systems is incorporated.</p>", "fixture-incorporated")
    if not any("incorporated-company claim" in error for error in incorporated):
        fail("identity checker mutation did not reject an incorporated-company claim", failures)
    unlinked = home_raw.replace(
        '<a href="mailto:mat@proofsystems.co.uk">mat@proofsystems.co.uk</a></p>',
        "mat@proofsystems.co.uk</p>",
        1,
    )
    if not any("not a clickable mailto" in error for error in identity_errors(unlinked, "fixture-unlinked")):
        fail("identity checker mutation did not reject an unlinked legal email", failures)
    duplicate = home_raw.replace("</footer>", f'<p>{FOOTER_LEGAL}</p></footer>', 1)
    if not any("disclosure count" in error for error in identity_errors(duplicate, "fixture-duplicate")):
        fail("identity checker mutation did not reject a duplicated disclosure", failures)

    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    footer_rule = re.search(r"\.footer-legal\s*\{([^}]*)\}", css)
    if not footer_rule:
        fail("shared stylesheet missing footer legal treatment", failures)
    else:
        body = footer_rule.group(1)
        size = re.search(r"font-size:\s*([\d.]+)rem", body)
        if not size or float(size.group(1)) < 0.875:
            fail("footer legal text must remain at least 0.875rem", failures)
        for contract in ("overflow-wrap: break-word", "white-space: normal", "line-height: 1.55"):
            if contract not in body:
                fail(f"footer legal treatment missing readable wrapping contract: {contract}", failures)


def check_redirects_and_shared_shell(failures: list[str]) -> None:
    redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
    entries = [tuple(line.split()) for line in redirects.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    expected = {
        ("/checkout", "/workflow.html", "301"),
        ("/checkout.html", "/workflow.html", "301"),
        ("/video-series", "/index.html", "301"),
        ("/video-series.html", "/index.html", "301"),
    }
    if set(entries) != expected:
        fail(f"_redirects entries {set(entries)} != approved destinations/statuses {expected}", failures)
    for path in [ROOT / "workflow.html", ROOT / "privacy.html", ROOT / "training.html", ROOT / "work" / "index.html"]:
        raw = path.read_text(encoding="utf-8")
        if "assets/css/site.css" not in raw and "../assets/css/site.css" not in raw:
            fail(f"{path.relative_to(ROOT)} missing shared styling", failures)
        if 'class="site-nav"' not in raw:
            fail(f"{path.relative_to(ROOT)} missing shared navigation", failures)
        if 'class="nav-cta"' not in raw or "Discuss a workflow" not in raw:
            fail(f"{path.relative_to(ROOT)} missing enquiry CTA", failures)
    js = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
    for contract in ("hashchange", "popstate", "pageshow", "history.pushState"):
        if contract not in js:
            fail(f"shared Selected Systems navigation lost {contract}", failures)


def check() -> int:
    failures: list[str] = []
    check_required_routes(failures)
    check_html_and_links(failures)
    check_homepage_v2(failures)
    check_form(failures)
    check_stories_and_media(failures)
    check_public_safety_and_identity(failures)
    check_redirects_and_shared_shell(failures)
    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print(
        "PASS V2 software-fit narrative, native-scroll B opening, connected-record story, "
        "no-JavaScript/reduced-motion finals, routes, links, responsive shell, enquiry form, "
        "seven captioned films, written Management Accounts example, public-copy safety and identity"
    )
    return 0


if __name__ == "__main__":
    sys.exit(check())
