#!/usr/bin/env python3
"""
Fetch a paper's arXiv abstract and flip its status.verified fields, so we never
add explanatory claims about a paper without having fetched a source for it (D004).

This script never invents or rewrites `summary`/`explanation` content — it only
reports the fetched title/authors/date next to what's recorded, and flags
mismatches for a human/model to look at. Flip verified=true only after you've
actually read the abstract (or PDF, for landmark/core papers) it printed.

Usage:
    python scripts/verify_paper.py rae-2025                  # by paper id (data/papers/rae-2025.yaml)
    python scripts/verify_paper.py rae-2025 --by fable        # record who verified it
    python scripts/verify_paper.py --all-unverified           # process every paper with an arxiv id
    python scripts/verify_paper.py rae-2025 --dry-run         # fetch + report only, no file write

Note: PyYAML round-trips without preserving comments or key order beyond what we
set explicitly below (we write with sort_keys=False, but any hand-added comments
in the source YAML will be lost). Fine for now since generated files carry no
comments; switch to ruamel.yaml if that changes.
"""
from __future__ import annotations

import argparse
import re
import time
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
ARXIV_API = "http://export.arxiv.org/api/query"
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


# arXiv asks API clients to leave ~3s between requests and rate-limits (HTTP 429) otherwise.
ARXIV_MIN_INTERVAL = 6.0
_last_request_at = 0.0


def fetch_arxiv(arxiv_id: str, retries: int = 4) -> dict:
    """Fetch one entry, throttled and with exponential backoff on 429/5xx."""
    global _last_request_at

    resp = None
    for attempt in range(retries):
        wait = ARXIV_MIN_INTERVAL - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
        _last_request_at = time.monotonic()

        resp = requests.get(ARXIV_API, params={"id_list": arxiv_id}, timeout=30)
        if resp.status_code in (429, 500, 502, 503, 504):
            backoff = ARXIV_MIN_INTERVAL * (2 ** (attempt + 1))
            print(f"  (arXiv returned {resp.status_code}; retrying in {backoff:.0f}s)")
            time.sleep(backoff)
            continue
        break

    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    entry = root.find("a:entry", ATOM_NS)
    if entry is None:
        raise ValueError(f"arXiv API returned no entry for id_list={arxiv_id}")

    title = entry.findtext("a:title", default="", namespaces=ATOM_NS).strip()
    if title.lower().startswith("error"):
        raise ValueError(f"arXiv API error for {arxiv_id}: {title}")

    summary = entry.findtext("a:summary", default="", namespaces=ATOM_NS).strip()
    published = entry.findtext("a:published", default="", namespaces=ATOM_NS).strip()
    authors = [
        a.findtext("a:name", default="", namespaces=ATOM_NS).strip()
        for a in entry.findall("a:author", ATOM_NS)
    ]
    pdf_link = None
    for link in entry.findall("a:link", ATOM_NS):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_link = link.get("href")

    return {
        "arxiv_id": arxiv_id,
        "title": re.sub(r"\s+", " ", title),
        "summary": re.sub(r"\s+", " ", summary),
        "authors": authors,
        "published": published[:10] if published else None,  # YYYY-MM-DD
        "pdf": pdf_link,
    }


def verify_one(paper_id: str, by: str, dry_run: bool) -> bool:
    f = PAPERS_DIR / f"{paper_id}.yaml"
    if not f.exists():
        print(f"ERROR {paper_id}: no such file {f}", file=sys.stderr)
        return False

    doc = yaml.safe_load(f.read_text())
    arxiv_id = doc.get("arxiv")
    if not arxiv_id:
        print(f"SKIP  {paper_id}: no arxiv id on file")
        return False

    try:
        fetched = fetch_arxiv(arxiv_id)
    except Exception as e:  # noqa: BLE001 - report and move on
        print(f"ERROR {paper_id} (arxiv:{arxiv_id}): fetch failed: {e}", file=sys.stderr)
        return False

    print(f"\n=== {paper_id} (arxiv:{arxiv_id}) ===")
    print(f"  recorded title : {doc.get('title')}")
    print(f"  fetched title  : {fetched['title']}")
    if doc.get("title", "").strip().lower() != fetched["title"].strip().lower():
        print("  WARN title mismatch — check this is the right arXiv id")
    print(f"  fetched date   : {fetched['published']}  (recorded: {doc.get('date')})")
    print(f"  fetched authors: {', '.join(fetched['authors'])}")
    print(f"  abstract       : {fetched['summary'][:280]}{'...' if len(fetched['summary']) > 280 else ''}")

    if dry_run:
        print("  (dry-run: not writing)")
        return True

    # Store the authors' own abstract so every paper page has a primary-source account of
    # the problem and method, even before an atlas explanation is written for it.
    doc["abstract"] = fetched["summary"]

    doc.setdefault("status", {})
    doc["status"]["verified"] = True
    doc["status"]["verified_on"] = date.today().isoformat()
    doc["status"]["verified_by"] = by
    f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))
    print(f"  -> wrote status.verified=true, verified_by={by}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_id", nargs="?", help="id of a paper in data/papers/")
    parser.add_argument("--all-unverified", action="store_true")
    parser.add_argument("--by", default="sonnet", help="who verified this (human|fable|sonnet|haiku)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--refresh", action="store_true",
                        help="re-fetch papers that are already verified (e.g. to backfill abstracts)")
    args = parser.parse_args()

    if not args.paper_id and not args.all_unverified:
        parser.error("provide a paper id or --all-unverified")

    ids: list[str]
    if args.all_unverified:
        ids = []
        for f in sorted(PAPERS_DIR.glob("*.yaml")):
            doc = yaml.safe_load(f.read_text())
            if not doc.get("arxiv"):
                continue
            needs = not doc.get("status", {}).get("verified")
            if args.refresh:
                needs = needs or not doc.get("abstract")
            if needs:
                ids.append(f.stem)
    else:
        ids = [args.paper_id]

    if not ids:
        print("Nothing to verify.")
        return 0

    ok = all([verify_one(pid, args.by, args.dry_run) for pid in ids])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
