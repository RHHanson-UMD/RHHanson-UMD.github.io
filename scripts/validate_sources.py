#!/usr/bin/env python3
"""Validate public-safe Learning Lab source metadata without third-party packages.

This checks a deliberately strict subset of the companion JSON Schema, plus
cross-field safeguards. It does not classify files or authorize publication.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/source-record.schema.json").read_text())
FIELDS = SCHEMA["properties"]


def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    for field in SCHEMA["required"]:
        if field not in record:
            errors.append(f"missing {field}")
    for field in record:
        if field not in FIELDS:
            errors.append(f"unknown field {field}")
    if errors:
        return errors
    if not isinstance(record["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", record["id"]):
        errors.append("invalid id")
    if not isinstance(record["course"], str) or not record["course"].strip():
        errors.append("invalid course")
    for field in ("access", "redistribution"):
        if record[field] not in FIELDS[field]["enum"]:
            errors.append(f"invalid {field}")
    if type(record["public_metadata_approved"]) is not bool:
        errors.append("public_metadata_approved must be boolean")
    for section in ("classification", "verification"):
        value = record[section]
        spec = FIELDS[section]
        if not isinstance(value, dict):
            errors.append(f"{section} must be an object")
            continue
        for required in spec["required"]:
            if required not in value:
                errors.append(f"missing {section}.{required}")
        for key, item in value.items():
            if key not in spec["properties"]:
                errors.append(f"unknown {section}.{key}")
            elif "enum" in spec["properties"][key] and item not in spec["properties"][key]["enum"]:
                errors.append(f"invalid {section}.{key}")
    c = record["classification"]
    if isinstance(c, dict) and all(k in c for k in ("tier", "status", "requires_clarification", "evidence", "method", "subtype")):
        if type(c["requires_clarification"]) is not bool:
            errors.append("requires_clarification must be boolean")
        if not isinstance(c["evidence"], list) or not all(isinstance(x, str) for x in c["evidence"]) or len(c["evidence"]) > 20:
            errors.append("classification.evidence must be a list of at most 20 strings")
        if not isinstance(c["subtype"], str) or not c["subtype"]:
            errors.append("classification.subtype must be nonempty")
        if c["tier"] == "unknown" and (c["status"] != "needs_clarification" or not c["requires_clarification"]):
            errors.append("unknown tier requires clarification")
        if c["status"] == "needs_clarification" and not c["requires_clarification"]:
            errors.append("needs_clarification requires prompt flag")
        if c["status"] == "confirmed" and c["requires_clarification"]:
            errors.append("confirmed classification cannot require clarification")
        if c["status"] == "confirmed" and not c["evidence"]:
            errors.append("confirmed classification requires evidence")
    v = record["verification"]
    if isinstance(v, dict):
        if "method" in v and v["method"] is not None and not isinstance(v["method"], str):
            errors.append("verification.method must be string or null")
        if "related_source_ids" in v and (not isinstance(v["related_source_ids"], list) or not all(isinstance(x, str) for x in v["related_source_ids"])):
            errors.append("invalid verification.related_source_ids")
    if "derived_from" in record and (not isinstance(record["derived_from"], list) or not all(isinstance(x, str) for x in record["derived_from"])):
        errors.append("invalid derived_from")
    if "course_role" in record and record["course_role"] not in FIELDS["course_role"]["enum"]:
        errors.append("invalid course_role")
    if record["public_metadata_approved"] and record["redistribution"] == "unknown":
        errors.append("public metadata approval cannot imply unknown redistribution rights; review separately")
    return errors


def main(argv):
    if not argv:
        print("Usage: python scripts/validate_sources.py <record.json> [...]", file=sys.stderr)
        return 2
    failed = False
    for name in argv:
        try:
            record = json.loads(Path(name).read_text())
            errors = validate(record)
        except (OSError, ValueError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            for error in errors:
                print(f"{name}: {error}", file=sys.stderr)
        else:
            print(f"{name}: valid metadata (not a publication approval)")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
