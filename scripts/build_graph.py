#!/usr/bin/env python3
"""
Compile every YAML entity + relation under data/ into a single JSON graph the
Astro site (and future tooling) can load directly: site/src/data/graph.json.

Does not validate — run scripts/validate.py first (this script assumes clean data
and will happily emit a broken graph.json if referential integrity is off).

Usage:
    python scripts/build_graph.py [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEFAULT_OUT = ROOT / "site" / "src" / "data" / "graph.json"
# Also mirrored to public/ so the client-side /graph page can fetch it at runtime
# (src/data/graph.json is for build-time imports only, e.g. site/src/lib/graph.ts).
PUBLIC_OUT = ROOT / "site" / "public" / "graph.json"

# node-producing directories under data/ (everything except relations/, monitor/)
NODE_DIRS = [
    "lines",
    "concepts", "papers", "systems", "problems",
    "benchmarks", "results", "transitions", "paths", "updates",
]

# fields to lift onto the graph node's top level for easy client-side filtering,
# per entity type; everything else stays nested under "data".
NODE_LABEL_FIELD = {
    "lines": "name",
    "concepts": "name",
    "papers": "title",
    "systems": "name",
    "problems": "statement",
    "benchmarks": "name",
    "results": "id",
    "transitions": "title",
    "paths": "title",
    "updates": "kind",
}


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def load_yaml(f: Path):
    return yaml.safe_load(f.read_text())


def build(data_dir: Path = DATA_DIR) -> dict:
    nodes = []
    edges = []

    for dirname in NODE_DIRS:
        d = data_dir / dirname
        if not d.exists():
            continue
        for f in sorted(d.glob("*.yaml")):
            entity = load_yaml(f)
            if not isinstance(entity, dict) or "id" not in entity:
                print(f"WARN skipping {rel(f)}: not a valid entity", file=sys.stderr)
                continue
            node = {
                "id": entity["id"],
                "nodeType": dirname,
                "label": entity.get(NODE_LABEL_FIELD.get(dirname, "id"), entity["id"]),
                "sections": entity.get("sections", []),
                "tier": entity.get("tier"),
                "date": entity.get("date"),
                "axes": entity.get("axes"),
                "data": entity,
            }
            nodes.append(node)

    relations_dir = data_dir / "relations"
    if relations_dir.exists():
        for f in sorted(relations_dir.glob("*.yaml")):
            items = load_yaml(f) or []
            for item in items:
                edges.append(
                    {
                        "from": item["from"],
                        "to": item["to"],
                        "type": item["type"],
                        "evidence": item.get("evidence"),
                        "confidence": item.get("confidence"),
                        "status": item.get("status"),
                    }
                )

    return {
        "generated_from": "data/",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    graph = build()
    payload = json.dumps(graph, indent=2, default=str) + "\n"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(payload)
    print(f"Wrote {args.out} ({graph['node_count']} nodes, {graph['edge_count']} edges)")

    if args.out == DEFAULT_OUT:
        PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
        PUBLIC_OUT.write_text(payload)
        print(f"Wrote {PUBLIC_OUT} (mirror for client-side fetch on /graph)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
