#!/usr/bin/env python3
"""Check the generated static portal before deployment (stdlib only).

This validates the files that will be uploaded. It does *not* claim to
replace a real browser/accessibility review or a live GitHub Pages check.
"""
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site").resolve()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class LocalLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for field in ("href", "src"):
            value = attributes.get(field)
            if value:
                self.links.append((tag, field, value))


def check_local_links(page, html):
    parser = LocalLinks()
    parser.feed(html)
    for tag, field, raw in parser.links:
        url = urlsplit(raw)
        if url.scheme or url.netloc:
            continue
        path = unquote(url.path)
        if not path:
            continue  # local #fragment; no filesystem path
        target = (page.parent / path).resolve()
        try:
            target.relative_to(SITE)
        except ValueError as exc:
            raise AssertionError(
                f"{page.name}: {tag} {field} escapes the deployed site: {raw}"
            ) from exc
        if target.is_dir():
            target = target / "index.html"
        require(target.is_file(), f"{page.name}: broken {tag} {field}={raw}")


def check_page(filename):
    page = SITE / filename
    require(page.is_file(), f"Missing public page: {filename}")
    html = page.read_text(encoding="utf-8")
    require(re.search(r'<html\\b[^>]*\\bdata-theme="dark"', html),
            f"{filename}: missing dark-first HTML default")
    require('id="theme-toggle"' in html, f"{filename}: missing theme toggle")
    require('href="./assets/styles.css"' in html,
            f"{filename}: missing shared stylesheet")
    check_local_links(page, html)
    return html


def main():
    resources = json.loads((ROOT / "content/resources.json").read_text())
    courses = json.loads((ROOT / "content/courses.json").read_text())
    home = check_page("index.html")
    quick = check_page("quick-reference.html")

    require((SITE / ".nojekyll").is_file(), "Missing .nojekyll for Pages")
    for marker in ("COURSES", "FILTERS", "RESOURCES"):
        require(home.count(f"<!-- {marker}_BEGIN -->") == 1,
                f"{marker}: missing/duplicate BEGIN marker")
        require(home.count(f"<!-- {marker}_END -->") == 1,
                f"{marker}: missing/duplicate END marker")

    require('href="./quick-reference.html"' in home,
            "Homepage must link to Quick Reference")
    require('href="./"' in quick, "Quick Reference must link home")
    require('id="resource-search"' in home, "Missing searchable toolbox")
    require('id="quick-search"' in quick, "Missing quick-reference search")
    require("learning-lab-theme" in (SITE / "assets/app.js").read_text(),
            "Theme persistence removed from portal script")

    for course in courses:
        target = f'https://rhhanson-umd.github.io/{course["id"]}/'
        require(escape(target, quote=True) in home,
                f"Missing course card link: {course['id']}")

    categories = {category["id"] for category in resources["categories"]}
    require(len(categories) == len(resources["categories"]), "Duplicate category ID")
    for category in categories:
        require(f'data-category-group="{escape(category)}"' in home,
                f"Missing resource category: {category}")

    urls = [resource["url"] for resource in resources["resources"]]
    require(len(urls) == len(set(urls)), "Duplicate toolbox URL")
    for resource in resources["resources"]:
        require(resource["category"] in categories,
                f"Unknown category: {resource['category']}")
        require(escape(resource["url"], quote=True) in home,
                f"Missing toolbox link: {resource['name']}")

    print(f"Static Pages checks passed: {len(courses)} courses, "
          f"{len(urls)} resources, {len(categories)} categories, "
          "two dark-first pages and all local linked files.")


if __name__ == "__main__":
    main()
