import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_sources import validate

EXAMPLE = json.loads((ROOT / "examples/source-record.example.json").read_text())


class ProvenanceTests(unittest.TestCase):
    def test_example_valid(self):
        self.assertEqual(validate(EXAMPLE), [])

    def test_unknown_requires_prompt(self):
        item = copy.deepcopy(EXAMPLE)
        item["classification"]["tier"] = "unknown"
        self.assertTrue(validate(item))
        item["classification"]["status"] = "needs_clarification"
        item["classification"]["requires_clarification"] = True
        self.assertEqual(validate(item), [])

    def test_confirmation_requires_evidence(self):
        item = copy.deepcopy(EXAMPLE)
        item["classification"]["status"] = "confirmed"
        item["classification"]["evidence"] = []
        self.assertTrue(validate(item))

    def test_reject_invalid_types(self):
        for key, value in [("public_metadata_approved", "false"), ("access", "private-ish")]:
            item = copy.deepcopy(EXAMPLE)
            item[key] = value
            self.assertTrue(validate(item))

    def test_reject_unknown_fields(self):
        item = copy.deepcopy(EXAMPLE)
        item["private_drive_url"] = "restricted"
        self.assertTrue(validate(item))

    def test_reject_missing_and_invalid_nested_fields(self):
        item = copy.deepcopy(EXAMPLE)
        del item["classification"]["tier"]
        self.assertTrue(validate(item))
        item = copy.deepcopy(EXAMPLE)
        item["verification"]["status"] = "certain"
        self.assertTrue(validate(item))


if __name__ == "__main__":
    unittest.main()
