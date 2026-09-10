"""
Orchestrator for the living-update run. Intended to be called every 3 days.

    python -m pipeline.run                 # discover, score, write candidate queue
    python -m pipeline.run --days 14       # wider sweep, e.g. after a gap
    python -m pipeline.run --dry-run       # report only, write nothing
    python -m pipeline.run --top 40        # how many admitted candidates to keep

What this does NOT do, by design (D006): decide anything. It produces
`data/monitor/candidates/*.yaml` plus a run report. A human, or a review session
following CLAUDE.md, reads the queue, verifies with scripts/verify_paper.py, writes a
real entry, and deletes the candidate. Nothing reaches data/papers/ automatically.
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone

import yaml

from . import config
from .discover import discover
from .score import assess_all


def _slug(title: str, arxiv: str) -> str:
    import re
    words = re.sub(r"[^a-z0-9 ]+", "", title.lower()).split()[:4]
    stem = "-".join(words) or "candidate"
    return f"{stem}-{arxiv.replace('.', '')}"


def write_candidate(a) -> str:
    c = a.candidate
    doc = {
        "id": _slug(c.title, c.arxiv),
        "type": "paper",
        "title": c.title,
        "arxiv": c.arxiv,
        "date": (c.published or "")[:7],
        "venue": {"name": "arXiv", "status": "preprint"},
        "orgs": [],
        "authors": c.authors[:8],
        "tier": "emerging",          # automation never proposes higher than this (D006)
        "sections": a.sections,
        "links": {"code": None, "weights": None, "project": None, "pdf": None},
        "status": {"code": "none", "weights": "none", "verified": False,
                   "verified_on": None, "verified_by": None},
        "summary": c.abstract[:700],
        "explanation": None,
        # review metadata, stripped when promoted into data/papers/
        "_review": {
            "score": round(a.score, 1),
            "reasons": a.reasons,
            "source": c.source,
            "hf_upvotes": c.hf_upvotes,
            "discovered_on": date.today().isoformat(),
        },
    }
    path = config.CANDIDATES / f"{doc['id']}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))
    return doc["id"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=config.LOOKBACK_DAYS)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    started = datetime.now(timezone.utc)
    print(f"Discovering papers from the last {args.days} days...")
    cands = discover(args.days)
    print(f"  {len(cands)} raw candidates")

    assessments = assess_all(cands)
    admitted = [a for a in assessments if a.admitted][: args.top]
    dupes = [a for a in assessments if a.duplicate_of]
    off_topic = [a for a in assessments if a.excluded_by == "no core image-generation term"]
    excluded = [a for a in assessments if a.excluded_by and a.excluded_by != "no core image-generation term"]
    irrelevant = [a for a in assessments if not a.sections and not a.excluded_by and not a.duplicate_of]

    print(f"  {len(dupes)} already in the atlas")
    print(f"  {len(off_topic)} not about image generation or editing")
    print(f"  {len(excluded)} out of scope (video/3D/audio, perception, LLM/agent work)")
    print(f"  {len(irrelevant)} matched no section")
    print(f"  {len(admitted)} admitted to the review queue\n")

    for a in admitted:
        print(f"  [{a.score:5.1f}] {a.candidate.arxiv}  {a.candidate.title[:78]}")
        for r in a.reasons:
            print(f"          · {r}")

    if args.dry_run:
        print("\n(dry run: no candidate files written)")
        return 0

    written = [write_candidate(a) for a in admitted]

    config.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {}
    if config.STATE_FILE.exists():
        state = json.loads(config.STATE_FILE.read_text())
    state["last_run"] = started.isoformat()
    state["last_run_stats"] = {
        "raw": len(cands), "admitted": len(admitted), "duplicates": len(dupes),
        "off_topic": len(off_topic), "out_of_scope": len(excluded),
        "irrelevant": len(irrelevant),
    }
    state.setdefault("runs", []).append(
        {"at": started.isoformat(), "admitted": written}
    )
    state["runs"] = state["runs"][-30:]
    config.STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")

    print(f"\nWrote {len(written)} candidates to {config.CANDIDATES.relative_to(config.ROOT)}/")
    print("Review them, then promote with scripts/verify_paper.py. Nothing is added automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
