#!/usr/bin/env python3
"""
Validate every YAML entity under data/ against its JSON Schema, then check
referential integrity across the whole graph (relation endpoints, paper->problem
links, paper axes -> concept ids, learning-path steps, MDX file existence, etc).

Usage:
    python scripts/validate.py [--strict]

--strict also fails the run on warnings (e.g. orphan MDX files, unreferenced
concepts). Default: warnings are printed but do not affect the exit code.

Exit code 0 = all good. Exit code 1 = schema or referential-integrity errors.
"""
from __future__ import annotations

import json
import sys
import warnings as _warnings
from pathlib import Path

import yaml

# RefResolver is deprecated in jsonschema>=4.18 in favor of the `referencing` library.
# We pin jsonschema<5 (see pyproject.toml) and keep RefResolver for now since it is simpler
# for this small, static schema set; revisit if/when we upgrade past jsonschema 5.
# Must be set before importing RefResolver, since jsonschema warns on attribute access.
_warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*RefResolver.*")

from jsonschema import Draft202012Validator, RefResolver  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
DATA_DIR = ROOT / "data"
CONTENT_DIR = ROOT / "content"

# directory (under data/) -> (schema filename, "single" | "array")
DIR_SCHEMA_MAP = {
    "lines": ("line.schema.json", "single"),
    "concepts": ("concept.schema.json", "single"),
    "papers": ("paper.schema.json", "single"),
    "systems": ("system.schema.json", "single"),
    "problems": ("problem.schema.json", "single"),
    "benchmarks": ("benchmark.schema.json", "single"),
    "results": ("result.schema.json", "single"),
    "transitions": ("transition.schema.json", "single"),
    "paths": ("path.schema.json", "single"),
    "updates": ("update_event.schema.json", "single"),
    "relations": ("relation.schema.json", "array"),
}


def load_schema_store() -> dict:
    store = {}
    for f in SCHEMA_DIR.glob("*.schema.json"):
        schema = json.loads(f.read_text())
        schema_id = schema.get("$id", f.name)
        store[schema_id] = schema
        # also register by bare filename so relative $ref: "common.schema.json#/..." resolves
        store[f.name] = schema
    return store


def make_validator(schema_filename: str, store: dict) -> Draft202012Validator:
    schema = store[schema_filename]
    resolver = RefResolver(base_uri=f"{schema_filename}", referrer=schema, store=store)
    return Draft202012Validator(schema, resolver=resolver)


def _rel(p: Path, root: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def run(data_dir: Path = DATA_DIR, content_dir: Path = CONTENT_DIR, root: Path = ROOT) -> tuple[list[str], list[str], int, int]:
    """Returns (errors, warnings, entity_count, relation_count)."""
    errors: list[str] = []
    warnings: list[str] = []

    store = load_schema_store()
    validators = {
        dirname: (make_validator(schema_file, store), mode)
        for dirname, (schema_file, mode) in DIR_SCHEMA_MAP.items()
    }

    registry: dict[str, dict] = {}
    relations: list[tuple[dict, str]] = []
    referenced_mdx: set[Path] = set()

    def rel(p: Path) -> str:
        return _rel(p, root)

    # ---- pass 1: schema validation + populate registry ----
    for dirname, (validator, mode) in validators.items():
        d = data_dir / dirname
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            try:
                loaded = yaml.safe_load(f.read_text())
            except yaml.YAMLError as e:
                errors.append(f"{rel(f)}: YAML parse error: {e}")
                continue

            if mode == "array":
                if not isinstance(loaded, list):
                    errors.append(f"{rel(f)}: expected a YAML list of relations")
                    continue
                for i, item in enumerate(loaded):
                    for err in validator.iter_errors(item):
                        errors.append(f"{rel(f)}[{i}]: {err.message} (at {'/'.join(str(p) for p in err.path)})")
                    if isinstance(item, dict) and "from" in item and "to" in item:
                        relations.append((item, rel(f)))
                continue

            if not isinstance(loaded, dict):
                errors.append(f"{rel(f)}: expected a YAML mapping")
                continue
            for err in validator.iter_errors(loaded):
                errors.append(f"{rel(f)}: {err.message} (at {'/'.join(str(p) for p in err.path)})")

            entity_id = loaded.get("id")
            if entity_id is None:
                continue
            if f.stem != entity_id:
                errors.append(f"{rel(f)}: filename '{f.stem}' does not match id '{entity_id}'")

            if entity_id in registry:
                errors.append(
                    f"{rel(f)}: duplicate id '{entity_id}' (already defined in "
                    f"{registry[entity_id]['file']})"
                )
            else:
                registry[entity_id] = {"type": dirname, "file": rel(f), "entity": loaded}

            for field in ("explanation", "explains", "narrative"):
                path_str = loaded.get(field)
                if path_str:
                    mdx_path = root / path_str
                    referenced_mdx.add(mdx_path)
                    if not mdx_path.exists():
                        errors.append(f"{rel(f)}: {field} points to missing file '{path_str}'")

    # candidate papers: shape-only validation, not added to registry
    candidate_dir = data_dir / "monitor" / "candidates"
    if candidate_dir.exists():
        paper_validator, _ = validators["papers"]
        for f in sorted(candidate_dir.glob("*.yaml")):
            try:
                loaded = yaml.safe_load(f.read_text())
            except yaml.YAMLError as e:
                errors.append(f"{rel(f)}: YAML parse error: {e}")
                continue
            if not isinstance(loaded, dict):
                errors.append(f"{rel(f)}: expected a YAML mapping")
                continue
            for err in paper_validator.iter_errors(loaded):
                errors.append(f"{rel(f)} (candidate): {err.message}")
            if loaded.get("status", {}).get("verified") is True:
                errors.append(f"{rel(f)}: candidate papers must have status.verified: false")

    # ---- pass 2: referential integrity ----
    def check_id_exists(entity_id, source: str, allowed_types: set[str] | None = None):
        if entity_id not in registry:
            errors.append(f"{source}: references unknown id '{entity_id}'")
            return
        if allowed_types and registry[entity_id]["type"] not in allowed_types:
            errors.append(
                f"{source}: id '{entity_id}' exists but has type "
                f"'{registry[entity_id]['type']}', expected one of {sorted(allowed_types)}"
            )

    for relation, src in relations:
        check_id_exists(relation["from"], f"{src} relation from='{relation['from']}'")
        check_id_exists(relation["to"], f"{src} relation to='{relation['to']}'")
        if relation["from"] == relation["to"]:
            errors.append(f"{src}: relation from == to == '{relation['from']}' (self-loop)")

    for entity_id, rec in registry.items():
        entity, etype, src = rec["entity"], rec["type"], rec["file"]

        if etype == "papers":
            for pid in entity.get("problems", []):
                check_id_exists(pid, f"{src} paper.problems -> '{pid}'", {"problems"})
            for lid in entity.get("lines", []):
                check_id_exists(lid, f"{src} paper.lines -> '{lid}'", {"lines"})

            # Coverage, tracked as warnings so the atlas reports its own gaps rather than
            # letting a landmark paper sit with nothing but a one-line summary.
            if entity.get("tier") in ("landmark", "core"):
                if not entity.get("explained"):
                    warnings.append(
                        f"{src}: {entity['tier']} paper has no `explained` block "
                        f"(a reader gets only the summary)"
                    )
                elif entity["explained"].get("depth") == "abstract":
                    warnings.append(
                        f"{src}: {entity['tier']} paper explained from the abstract only; "
                        f"a full-text read would firm up method and ablation detail"
                    )
            if entity.get("arxiv") and not entity.get("abstract"):
                warnings.append(f"{src}: no abstract stored (run verify_paper.py --refresh)")
            for axis_key, concept_ids in entity.get("axes", {}).items():
                for cid in concept_ids:
                    check_id_exists(cid, f"{src} paper.axes.{axis_key} -> '{cid}'", {"concepts"})
                    if cid in registry and registry[cid]["entity"].get("axis") not in (axis_key, "background"):
                        warnings.append(
                            f"{src}: paper.axes.{axis_key} references concept '{cid}' whose own "
                            f"axis is '{registry[cid]['entity'].get('axis')}'"
                        )

        elif etype == "lines":
            for step in entity.get("arc", []):
                paper_id = step["paper"]
                check_id_exists(paper_id, f"{src} line.arc -> '{paper_id}'", {"papers"})
                # membership must be declared on both sides, or the site's line pages and the
                # paper pages will disagree about who belongs to what
                if paper_id in registry:
                    declared = registry[paper_id]["entity"].get("lines", [])
                    if entity_id not in declared:
                        errors.append(
                            f"{src}: line.arc lists paper '{paper_id}' but that paper does not "
                            f"declare lines: ['{entity_id}'] (declared: {declared})"
                        )
            for pid in entity.get("open_questions", []):
                check_id_exists(pid, f"{src} line.open_questions -> '{pid}'", {"problems"})
            for lid in entity.get("competes_with", []):
                check_id_exists(lid, f"{src} line.competes_with -> '{lid}'", {"lines"})

        elif etype == "problems":
            for pid in entity.get("attacked_by", []):
                check_id_exists(pid, f"{src} problem.attacked_by -> '{pid}'", {"papers"})
            for pid in entity.get("solved_by", []):
                check_id_exists(pid, f"{src} problem.solved_by -> '{pid}'", {"papers"})

        elif etype == "transitions":
            check_id_exists(entity["from_option"], f"{src} transition.from_option", {"concepts"})
            check_id_exists(entity["to_option"], f"{src} transition.to_option", {"concepts"})
            for pid in entity.get("key_papers", []):
                check_id_exists(pid, f"{src} transition.key_papers -> '{pid}'", {"papers"})

        elif etype == "paths":
            for step in entity.get("steps", []):
                check_id_exists(step["id"], f"{src} path.steps -> '{step['id']}'")

        elif etype == "benchmarks":
            introducer = entity.get("introduced_by")
            if introducer:
                check_id_exists(introducer, f"{src} benchmark.introduced_by", {"papers"})

        elif etype == "results":
            check_id_exists(entity["paper"], f"{src} result.paper", {"papers"})
            check_id_exists(entity["benchmark"], f"{src} result.benchmark", {"benchmarks"})

        elif etype == "updates":
            check_id_exists(entity["target"], f"{src} update_event.target")

        elif etype == "systems":
            for rel_item in entity.get("releases", []):
                paper_id = rel_item.get("paper")
                if paper_id:
                    check_id_exists(paper_id, f"{src} system.releases[].paper -> '{paper_id}'", {"papers"})
            for axis_key, concept_ids in entity.get("axes", {}).items():
                for cid in concept_ids:
                    check_id_exists(cid, f"{src} system.axes.{axis_key} -> '{cid}'", {"concepts"})

    if content_dir.exists():
        for mdx in content_dir.rglob("*.mdx"):
            if mdx not in referenced_mdx:
                warnings.append(f"orphan MDX file not referenced by any entity: {rel(mdx)}")

    return errors, warnings, len(registry), len(relations)


def main() -> int:
    strict = "--strict" in sys.argv
    errors, warns, n_entities, n_relations = run()

    print(f"Checked {n_entities} entities across {len(DIR_SCHEMA_MAP)} types, {n_relations} relations.")

    if warns:
        print(f"\n{len(warns)} warning(s):")
        for w in warns:
            print(f"  WARN  {w}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ERROR {e}")
        return 1

    if strict and warns:
        print("\n--strict set: failing due to warnings above.")
        return 1

    print("\nOK: no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
