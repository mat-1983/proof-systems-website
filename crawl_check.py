#!/usr/bin/env python3
"""HTTP crawl of public routes with local asset and link verification."""

from __future__ import annotations

import html.parser
import http.server
import os
import pathlib
import socketserver
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent

ROUTES = [
    "/",
    "/index.html",
    "/workflow.html",
    "/privacy.html",
    "/checkout.html",
    "/video-series.html",
    "/training.html",
    "/assets/fonts/InterVariable.woff2",
    "/assets/brand/logo-light.svg",
    "/assets/brand/icon-light.svg",
    "/work/",
    "/work/index.html",
    "/work/sitelog.html",
    "/work/budgetflow.html",
    "/work/applications-ledger.html",
    "/work/cpr.html",
    "/work/probables.html",
    "/work/ledgerlink.html",
    "/work/cashflow.html",
    "/work/management-accounts.html",
    "/favicon.svg",
    "/assets/css/site.css",
    "/assets/js/site.js",
    "/assets/js/form.js",
    "/assets/img/social.jpg",
]

FULL_FILMS = {
    "/assets/demo-media/sitelog-demo.mp4",
    "/assets/demo-media/budgetflow-demo.mp4",
    "/assets/demo-media/ledgerlink-demo.mp4",
    "/assets/demo-media/cpr-demo.mp4",
    "/assets/demo-media/applications-ledger-demo.mp4",
    "/assets/demo-media/cashflow-demo.mp4",
    "/assets/demo-media/probables-demo.mp4",
    "/assets/demo-media/management-accounts-demo.mp4",
}


class AssetParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: (value or "") for key, value in attrs}
        if tag == "a" and attr.get("href"):
            self.refs.append(("href", attr["href"]))
        if tag in {"link", "img"} and attr.get("href"):
            self.refs.append((tag, attr["href"]))
        if tag in {"img", "script", "source", "track"} and attr.get("src"):
            self.refs.append((tag, attr["src"]))
        if tag == "video" and attr.get("poster"):
            self.refs.append(("poster", attr["poster"]))
        if tag == "div" and attr.get("data-teaser-src"):
            self.refs.append(("teaser", attr["data-teaser-src"]))
        if tag == "div" and attr.get("data-poster"):
            self.refs.append(("teaser-poster", attr["data-poster"]))


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def fetch(base: str, path: str) -> tuple[int, bytes, str]:
    url = urllib.parse.urljoin(base, path)
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read(), response.headers.get_content_type()
    except urllib.error.HTTPError as error:
        return error.code, error.read() if error.fp else b"", ""


def local_target(page_path: str, value: str) -> str | None:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme in {"mailto", "https", "http"}:
        return None
    if not parsed.path:
        return None
    if parsed.path.startswith("/"):
        return parsed.path
    directory = page_path.rsplit("/", 1)[0]
    if page_path.endswith("/"):
        directory = page_path.rstrip("/")
    joined = urllib.parse.urljoin(directory + "/", parsed.path)
    return joined


def check() -> int:
    failures: list[str] = []
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args, **kwargs: None
    os.chdir(ROOT)
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        httpd.allow_reuse_address = True
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}/"
        try:
            homepage_assets: set[str] = set()
            for route in ROUTES:
                status, body, content_type = fetch(base, route)
                if status != 200:
                    fail(f"{route} returned {status}", failures)
                    continue
                if route.endswith(".html") or route in {"/", "/work/"}:
                    if not body.lstrip().startswith(b"<!doctype html>") and not body.lstrip().lower().startswith(b"<html"):
                        fail(f"{route} did not return HTML", failures)
                    parser = AssetParser()
                    parser.feed(body.decode("utf-8", errors="replace"))
                    parser.close()
                    if route in {"/", "/index.html"}:
                        for kind, value in parser.refs:
                            target = local_target(route if route != "/" else "/index.html", value)
                            if target:
                                homepage_assets.add(target)
                    for kind, value in parser.refs:
                        target = local_target(route if route != "/" else "/index.html", value)
                        if not target:
                            if value.startswith("http://"):
                                fail(f"{route}: insecure URL {value}", failures)
                            continue
                        if target.endswith("/"):
                            check_path = target
                        else:
                            check_path = target
                        status, _, _ = fetch(base, check_path)
                        if status != 200:
                            fail(f"{route} -> {kind} {value} returned {status}", failures)
            overlap = homepage_assets & FULL_FILMS
            if overlap:
                fail(f"homepage crawl referenced full films: {sorted(overlap)}", failures)
            teasers = {item for item in homepage_assets if item.endswith("-teaser.mp4")}
            if len(teasers) != 3:
                fail(f"homepage should declare 3 teaser clips, found {sorted(teasers)}", failures)
        finally:
            httpd.shutdown()
            httpd.server_close()

    if failures:
        print(f"FAIL {len(failures)} check(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print("PASS HTTP crawl of public routes, local assets and poster-first homepage media")
    return 0


if __name__ == "__main__":
    sys.exit(check())
