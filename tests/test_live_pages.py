"""Offline tests for the post-deployment Pages verification gate."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.verify_live_site import FILES, inspect_payloads  # noqa: E402

SHA = "0123456789abcdef0123456789abcdef01234567"


def expected_pages():
    return {
        "deployment-sha.txt": SHA + "\n",
        "index.html": (
            '<html lang="en" data-theme="dark">'
            '<button id="theme-toggle"></button>'
            '<input id="resource-search">'
            '<a href="./quick-reference.html">Quick Reference</a></html>'
        ),
        "quick-reference.html": (
            '<html lang="en" data-theme="dark">'
            '<button id="theme-toggle"></button>'
            '<input id="quick-search"></html>'
        ),
        "assets/styles.css": ':root {color-scheme:dark;--bg:#0d141f}',
        "assets/app.js": "const key='learning-lab-theme';",
    }


class LivePagesGateTests(unittest.TestCase):
    def test_known_good_artifact(self):
        self.assertEqual(inspect_payloads(expected_pages(), SHA), [])

    def test_version_marker_rejects_old_deployment(self):
        pages = expected_pages()
        pages["deployment-sha.txt"] = "f" * 40
        self.assertIn("Deployment marker differs",
                      " ".join(inspect_payloads(pages, SHA)))

    def test_readme_served_instead_of_homepage(self):
        pages = expected_pages()
        pages["index.html"] = "<html><body><h1>README.md</h1></body></html>"
        errors = " ".join(inspect_payloads(pages, SHA))
        self.assertIn("Homepage", errors)
        self.assertIn("Quick Reference navigation", errors)

    def test_missing_quick_reference_fails(self):
        pages = expected_pages()
        del pages["quick-reference.html"]
        self.assertIn("Missing response: quick-reference.html",
                      inspect_payloads(pages, SHA))

    def test_missing_stylesheet_fails(self):
        pages = expected_pages()
        pages["assets/styles.css"] = "body { color: red }"
        self.assertTrue(any("Stylesheet" in error
                            for error in inspect_payloads(pages, SHA)))

    def test_all_expected_paths(self):
        self.assertEqual(set(expected_pages()), set(FILES))


if __name__ == "__main__":
    unittest.main()
