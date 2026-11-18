#!/usr/bin/env python3
"""Verify the *deployed* GitHub Pages artifact, not just the repository files.

This is an HTTP smoke check; it does not replace a keyboard/browser audit.
The deploy workflow adds deployment-sha.txt only to the uploaded artifact so
we can distinguish a fresh deployment from an older cached page.
"""
import argparse
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

FILES = (
    "deployment-sha.txt",
    "index.html",
    "quick-reference.html",
    "assets/styles.css",
    "assets/app.js",
)
MAX_RESPONSE_BYTES = 2_000_000


def inspect_payloads(pages, expected_sha):
    """Return actionable failures for five fetched public files."""
    problems = []
    for path in FILES:
        if path not in pages:
            problems.append(f"Missing response: {path}")
    if problems:
        return problems

    sha = pages["deployment-sha.txt"].strip()
    if sha != expected_sha:
        problems.append(
            f"Deployment marker differs: got {sha[:40]!r}, "
            f"expected {expected_sha[:40]!r}"
        )
    home = pages["index.html"]
    quick = pages["quick-reference.html"]
    css = pages["assets/styles.css"]
    js = pages["assets/app.js"]
    for label, html, search_id in (
        ("Homepage", home, 'id="resource-search"'),
        ("Quick Reference", quick, 'id="quick-search"'),
    ):
        if '<html lang="en" data-theme="dark">' not in html:
            problems.append(f"{label}: expected dark-first Learning Lab HTML")
        if search_id not in html:
            problems.append(f"{label}: missing searchable content ({search_id})")
        if 'id="theme-toggle"' not in html:
            problems.append(f"{label}: missing theme toggle")
    if 'href="./quick-reference.html"' not in home:
        problems.append("Homepage: missing Quick Reference navigation")
    if "color-scheme:dark" not in css or "--bg:" not in css:
        problems.append("Stylesheet: expected dark palette variables")
    if "learning-lab-theme" not in js:
        problems.append("JavaScript: theme persistence missing")
    return problems


def fetch_text(base_url, path, attempt, expected_sha):
    base = base_url.rstrip("/") + "/"
    # A unique URL per attempt reduces the risk of accepting a stale CDN copy.
    url = urljoin(base, path) + f"?verify={expected_sha[:12]}-{attempt}"
    req = Request(
        url,
        headers={
            "User-Agent": "LearningLab-Pages-SmokeCheck/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urlopen(req, timeout=15) as response:
        data = response.read(MAX_RESPONSE_BYTES + 1)
    if len(data) > MAX_RESPONSE_BYTES:
        raise ValueError(f"{path} exceeds {MAX_RESPONSE_BYTES} bytes")
    return data.decode("utf-8", errors="replace")


def verify(base_url, expected_sha, attempts, delay_seconds):
    for attempt in range(1, attempts + 1):
        try:
            pages = {
                path: fetch_text(base_url, path, attempt, expected_sha)
                for path in FILES
            }
            errors = inspect_payloads(pages, expected_sha)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            errors = [f"HTTP failure: {type(exc).__name__}: {exc}"]
        if not errors:
            print(
                f"LIVE Pages verified on attempt {attempt}/{attempts}: "
                f"{base_url.rstrip('/')}/ (commit {expected_sha})"
            )
            return True
        print(f"Attempt {attempt}/{attempts}: " + "; ".join(errors), flush=True)
        if attempt < attempts:
            time.sleep(delay_seconds)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--delay-seconds", type=float, default=10.0)
    args = parser.parse_args()
    if not args.base_url.startswith(("https://", "http://")):
        parser.error("--base-url must be an HTTP(S) URL")
    if not args.expected_sha or len(args.expected_sha) != 40 or any(
        char not in "0123456789abcdef" for char in args.expected_sha.lower()
    ):
        parser.error("--expected-sha must be a complete 40-character Git SHA")
    if args.attempts < 1 or args.delay_seconds < 0:
        parser.error("--attempts must be positive and --delay-seconds nonnegative")
    if not verify(args.base_url, args.expected_sha, args.attempts, args.delay_seconds):
        sys.exit("Published GitHub Pages did not match the deployed commit.")


if __name__ == "__main__":
    main()
