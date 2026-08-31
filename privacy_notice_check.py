#!/usr/bin/env python3
"""Deterministic local checks for the Proof Systems privacy notice."""

from __future__ import annotations

import html.parser
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
PRIVACY = ROOT / "privacy.html"
HTML_FILES = {path.name: path for path in ROOT.glob("*.html")}

REQUIRED_HEADINGS = [
    "Who is responsible",
    "General workflow enquiries",
    "Paid B2B enquiries and client work",
    "Why the information is used",
    "What is not collected by default",
    "How it is handled",
    "How long it is kept",
    "Your rights",
    "Complaints",
]

ENQUIRY_PHRASES = [
    "name, business email, company, a general description of the work or workflow you would like to improve",
    "consent to contact",
    "used only to review the enquiry and respond about it",
    "Please do not submit customer names, passwords, confidential documents, detailed financial data, special-category information or other sensitive personal data",
    "processed through Netlify Forms and may be delivered to Proof Systems by email",
]

REQUIRED_PHRASES = [
    "Mathew Glendenning, trading as Proof Systems",
    "mat@proofsystems.co.uk",
    "qualify the enquiry",
    "prepare a quote or contract",
    "deliver the work",
    "provide support",
    "handle a complaint",
    "business, legal and tax records",
    "Where you yourself are the contracting party, such as a sole trader",
    "taking steps you have asked for before a contract, and performing that contract",
    "limited company or another separate business entity",
    "legitimate interests in responding to the enquiry",
    "administering, delivering and supporting the B2B work",
    "where that use is necessary and those interests are balanced against your rights",
    "legitimate interests",
    "do not rely on consent as a blanket permission",
    "legal obligation",
    "special-category data",
    "criminal-offence data",
    "significant automated decisions",
    "standing access",
    "named people, time-bounded and reauthorised",
    "Client material is not put into an AI service unless the engagement and applicable safeguards permit it",
    "Google Workspace",
    "may process information outside the United Kingdom",
    "UK Extension to the EU-US Data Privacy Framework",
    "contractual clauses as applicable transfer mechanisms",
    "Cloud Data Processing Addendum",
    "UK contractual safeguards for restricted transfers",
    "current provider and transfer details",
    "reviewed and deleted after 90 days unless a hold or continuing purpose applies",
    "deleted within 14 days after checked notes exist",
    "deleted within 90 days after a checked summary or handover exists",
    "reviewed 12 months after handover or termination",
    "deliberately retained for a recorded reason",
    "Contract, invoice, complaint, claim, security and statutory records may be retained longer where required",
    "Deletion is controlled and approval-gated",
    "I do not promise automatic deletion",
    "These rights can depend on the circumstances and on the lawful basis",
    "There is not an absolute right to deletion",
    "Last updated 29 August 2026",
    "https://ico.org.uk/make-a-complaint/",
]

REJECTED_PHRASES = [
    "will not invent",
    "complete, current public account",
    "performing a contract with your business",
    "taking steps at your request before a contract, and performing a contract with your business",
    "I have not listed specific countries or transfer mechanisms",
]

PROHIBITED_PATTERNS = [
    (r"C2015591", "ICO application/security reference"),
    (r"10_business", "private filesystem path"),
    (r"20_clients", "private filesystem path"),
    (r"/Users/", "absolute filesystem path"),
    (r"DATA-SOP", "private legal pack identifier"),
    (r"ToB-v", "private legal pack identifier"),
    (r"Coversure", "insurance provider"),
    (r"Hiscox", "insurance provider"),
    (r"premium", "insurance wording"),
    (r"policy schedule", "insurance wording"),
    (r"Pantera", "client name"),
    (r"Xonetic", "client/prospect name"),
    (r"Postbox", "private service address"),
    (r"WC1", "postal address fragment"),
    (r"\u2014", "em dash"),
    (r"\u2013", "en dash"),
]

EMAIL = "mat@proofsystems.co.uk"
ICO_PREFIX = "https://ico.org.uk/make-a-complaint"


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.tags: list[str] = []
        self.stack: list[str] = []
        self.lang = ""
        self.title = ""
        self.charset = False
        self.viewport = False
        self.h1: list[str] = []
        self.h2: list[str] = []
        self.h2_ids: list[str] = []
        self.section_id = ""
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.mailto: list[str] = []
        self.section_count = 0
        self.has_header = False
        self.has_main = False
        self.has_nav = False
        self.has_footer = False
        self._capture: list[str] | None = None
        self._capture_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        self.tags.append(tag)
        if tag not in {"meta", "link", "img", "br", "input", "hr", "source"}:
            self.stack.append(tag)
        if tag == "html":
            self.lang = attr.get("lang", "")
        if tag == "meta" and attr.get("charset", "").lower() == "utf-8":
            self.charset = True
        if tag == "meta" and attr.get("name") == "viewport":
            self.viewport = True
        if tag == "header":
            self.has_header = True
        if tag == "main":
            self.has_main = True
        if tag == "nav":
            self.has_nav = True
        if tag == "footer":
            self.has_footer = True
        if tag == "section":
            self.section_count += 1
            self.section_id = attr.get("id", "")
        element_id = attr.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            self.ids.add(element_id)
        if tag == "h2":
            self.h2_ids.append(element_id or self.section_id)
            self._start_capture()
        if tag in {"h1", "title"}:
            self._start_capture()
        if tag == "a":
            href = attr.get("href", "")
            if href:
                self.hrefs.append(href)
            if href.startswith("mailto:"):
                self.mailto.append(href.split(":", 1)[1])

    def handle_endtag(self, tag: str) -> None:
        if tag == "section":
            self.section_id = ""
        if tag in {"h1", "h2", "title"}:
            text = "".join(self._capture_buf).strip()
            if tag == "h1":
                self.h1.append(text)
            elif tag == "h2":
                self.h2.append(text)
            else:
                self.title = text
            self._capture = None
            self._capture_buf = []
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            self.errors.append(f"unexpected closing tag </{tag}>")

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._capture_buf.append(data)

    def _start_capture(self) -> None:
        self._capture = True
        self._capture_buf = []


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def check() -> int:
    failures: list[str] = []
    if not PRIVACY.is_file():
        print("FAIL privacy.html is missing")
        return 1

    raw = PRIVACY.read_text(encoding="utf-8")
    if raw[0] != "<":
        fail("privacy.html is not HTML", failures)

    parser = PageParser()
    try:
        parser.feed(raw)
        parser.close()
    except html.parser.HTMLParseError as error:
        fail(f"HTML parse error: {error}", failures)
        print_result(failures)
        return 1

    if parser.stack:
        fail(f"unclosed tags: {parser.stack}", failures)
    if parser.errors:
        failures.extend(parser.errors)
    if parser.lang != "en-GB":
        fail(f"expected lang=en-GB, got {parser.lang!r}", failures)
    if not parser.charset:
        fail("missing utf-8 charset", failures)
    if not parser.viewport:
        fail("missing viewport meta", failures)
    if parser.title != "Privacy | Proof Systems":
        fail(f"unexpected title: {parser.title!r}", failures)
    if parser.h1 != ["Privacy notice"]:
        fail(f"unexpected h1: {parser.h1!r}", failures)
    if not parser.has_header or not parser.has_main or not parser.has_nav or not parser.has_footer:
        fail("missing header, main, nav or footer", failures)
    css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    if "overflow-x: hidden" not in css and "overflow-x:hidden" not in css:
        fail("missing overflow-x:hidden", failures)
    if ".doc-main" not in css:
        fail("missing privacy readable column class", failures)
    if 'href="assets/css/site.css"' not in raw:
        fail("privacy.html must use shared CSS", failures)
    if 'href="favicon.svg"' not in raw:
        fail("missing favicon link", failures)
    if parser.section_count < 9:
        fail(f"expected at least 9 sections, got {parser.section_count}", failures)
    if parser.h2 != REQUIRED_HEADINGS:
        fail(f"unexpected h2 headings: {parser.h2}", failures)
    if any(not heading_id for heading_id in parser.h2_ids):
        fail("every h2 must have an id", failures)

    visible = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = html_unescape(visible)
    visible_compact = re.sub(r"\s+", " ", visible)

    if "founding diagnostic" in visible_compact.lower() or "founding cohort" in visible_compact.lower():
        fail("privacy notice still describes founding diagnostic applications", failures)

    for phrase in ENQUIRY_PHRASES + REQUIRED_PHRASES:
        if phrase not in visible_compact and phrase not in raw:
            fail(f"missing required phrase: {phrase}", failures)

    for phrase in REJECTED_PHRASES:
        if phrase in visible_compact or phrase in raw:
            fail(f"rejected wording still present: {phrase}", failures)

    if "performing a contract with your business" in visible_compact:
        fail("contract basis must not be applied to a separate business entity", failures)
    if "Where you yourself are the contracting party" not in visible_compact:
        fail("must distinguish contract basis for the individual contracting party", failures)
    if "limited company" not in visible_compact:
        fail("must state legitimate interests for company/entity contacts", failures)

    if visible_compact.count(EMAIL) < 4:
        fail(f"expected mat@proofsystems.co.uk at least 4 times in visible text, got {visible_compact.count(EMAIL)}", failures)
    if any(address != EMAIL for address in parser.mailto):
        fail(f"inconsistent mailto addresses: {parser.mailto}", failures)
    if not parser.mailto:
        fail("no mailto links", failures)

    if "consent as a blanket" not in visible_compact:
        fail("must reject consent as a blanket basis", failures)

    ico_links = [href for href in parser.hrefs if "ico.org.uk" in href]
    if not ico_links:
        fail("missing ICO complaints link", failures)
    for href in ico_links:
        if not href.startswith(ICO_PREFIX) or not href.startswith("https://"):
            fail(f"ICO link is not the official HTTPS complaints URL: {href}", failures)

    for href in parser.hrefs:
        parsed = urllib.parse.urlparse(href)
        if href.startswith("#"):
            target = href[1:]
            if target not in parser.ids:
                fail(f"broken fragment: {href}", failures)
            continue
        if parsed.scheme in {"mailto", "https"}:
            if parsed.scheme == "https" and not (
                href.startswith("https://ico.org.uk/")
                or href.startswith("https://www.linkedin.com/in/mathew-glendenning-90670649/")
            ):
                fail(f"unexpected external URL: {href}", failures)
            continue
        if parsed.scheme and parsed.scheme not in {"http", "https", "mailto"}:
            fail(f"unsupported URL scheme: {href}", failures)
            continue
        if parsed.scheme == "http":
            fail(f"insecure URL: {href}", failures)
            continue
        path = parsed.path
        if path not in HTML_FILES and path not in {"favicon.svg"}:
            fail(f"internal link does not resolve: {href}", failures)

    for pattern, label in PROHIBITED_PATTERNS:
        if re.search(pattern, raw):
            fail(f"prohibited {label} present ({pattern})", failures)

    if re.search(r"automatically deleted|automatic deletion|auto-delete", raw, re.I):
        if "do not promise automatic deletion" not in visible_compact:
            fail("must not promise automated deletion", failures)

    print_result(failures)
    return 1 if failures else 0


def html_unescape(text: str) -> str:
    return (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&#39;", "'")
        .replace("&rsquo;", "\u2019")
        .replace("&lsquo;", "\u2018")
    )


def print_result(failures: list[str]) -> None:
    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return
    print("PASS privacy.html structure, required wording, links, email consistency and prohibited-term scan")


if __name__ == "__main__":
    sys.exit(check())
