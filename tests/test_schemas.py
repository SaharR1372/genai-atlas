"""Every schema/*.schema.json must itself be a valid JSON Schema (draft 2020-12)."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"


def test_all_schema_files_are_valid_json():
    files = list(SCHEMA_DIR.glob("*.schema.json"))
    assert files, "no schema files found"
    for f in files:
        json.loads(f.read_text())  # raises if malformed


def test_all_schemas_are_valid_json_schema():
    for f in SCHEMA_DIR.glob("*.schema.json"):
        schema = json.loads(f.read_text())
        Draft202012Validator.check_schema(schema)


def test_expected_entity_schemas_exist():
    expected = {
        "concept", "paper", "system", "relation", "problem",
        "benchmark", "result", "transition", "path", "update_event",
    }
    found = {f.stem.replace(".schema", "") for f in SCHEMA_DIR.glob("*.schema.json")} - {"common"}
    assert expected <= found, f"missing schemas: {expected - found}"
