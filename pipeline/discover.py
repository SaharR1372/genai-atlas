"""
Stage 1: discovery. Pull recent candidate papers from arXiv and Hugging Face daily papers.

Deterministic and free — no LLM, no API key. Everything downstream filters what this
produces; nothing here decides what enters the atlas.
"""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone

import requests

from . import config

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
HF_PAPERS = "https://huggingface.co/api/daily_papers"

# arXiv asks for ~3s between API calls.
_MIN_INTERVAL = 3.0
_last_call = 0.0


@dataclass
class Candidate:
    arxiv: str
    title: str
    abstract: str
    authors: list[str]
    published: str
    categories: list[str] = field(default_factory=list)
    source: str = "arxiv"
    hf_upvotes: int | None = None

    def as_dict(self) -> dict:
        return asdict(self)


def _throttle() -> None:
    global _last_call
    wait = _MIN_INTERVAL - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.monotonic()


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _parse_feed(xml_text: str, source: str) -> list[Candidate]:
    root = ET.fromstring(xml_text)
    out: list[Candidate] = []
    for entry in root.findall("a:entry", ATOM):
        raw_id = entry.findtext("a:id", default="", namespaces=ATOM)
        m = re.search(r"abs/([0-9]{4}\.[0-9]{4,5})", raw_id)
        if not m:
            continue
        out.append(
            Candidate(
                arxiv=m.group(1),
                title=_clean(entry.findtext("a:title", default="", namespaces=ATOM)),
                abstract=_clean(entry.findtext("a:summary", default="", namespaces=ATOM)),
                authors=[
                    _clean(a.findtext("a:name", default="", namespaces=ATOM))
                    for a in entry.findall("a:author", ATOM)
                ],
                published=entry.findtext("a:published", default="", namespaces=ATOM)[:10],
                categories=[
                    c.get("term", "") for c in entry.findall("{http://arxiv.org/schemas/atom}category")
                ],
                source=source,
            )
        )
    return out


def from_arxiv(days: int = config.LOOKBACK_DAYS, max_results: int = 300) -> list[Candidate]:
    """Recent submissions in the atlas's categories, newest first."""
    cats = " OR ".join(f"cat:{c}" for c in config.ARXIV_CATEGORIES)
    found: dict[str, Candidate] = {}
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()

    # arXiv's date filtering is unreliable across mirrors, so sort by date and stop
    # once we pass the cutoff rather than trusting a submittedDate range query.
    for start in range(0, max_results, 100):
        _throttle()
        resp = requests.get(
            ARXIV_API,
            params={
                "search_query": f"({cats})",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "start": start,
                "max_results": 100,
            },
            timeout=45,
        )
        if resp.status_code != 200:
            print(f"  arXiv returned {resp.status_code}; stopping discovery early")
            break
        batch = _parse_feed(resp.text, "arxiv")
        if not batch:
            break
        for c in batch:
            found[c.arxiv] = c
        if batch[-1].published and batch[-1].published < cutoff:
            break

    return [c for c in found.values() if not c.published or c.published >= cutoff]


def from_huggingface(days: int = config.LOOKBACK_DAYS) -> list[Candidate]:
    """
    Hugging Face daily papers — a decent proxy for what the community is actually
    talking about, which pure arXiv listing misses.
    """
    out: list[Candidate] = []
    try:
        resp = requests.get(HF_PAPERS, timeout=30)
        resp.raise_for_status()
        items = resp.json()
    except Exception as e:  # noqa: BLE001
        print(f"  Hugging Face daily papers unavailable ({e}); skipping this source")
        return out

    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    for item in items:
        paper = item.get("paper", {}) or {}
        arxiv_id = paper.get("id", "")
        if not re.fullmatch(r"[0-9]{4}\.[0-9]{4,5}", arxiv_id or ""):
            continue
        published = (item.get("publishedAt") or paper.get("publishedAt") or "")[:10]
        if published and published < cutoff:
            continue
        out.append(
            Candidate(
                arxiv=arxiv_id,
                title=_clean(paper.get("title", "")),
                abstract=_clean(paper.get("summary", "")),
                authors=[a.get("name", "") for a in paper.get("authors", []) if a.get("name")],
                published=published,
                source="huggingface",
                hf_upvotes=paper.get("upvotes"),
            )
        )
    return out


def discover(days: int = config.LOOKBACK_DAYS) -> list[Candidate]:
    """All sources, merged on arXiv id. HF metadata wins where both have the paper."""
    merged: dict[str, Candidate] = {}
    for c in from_arxiv(days):
        merged[c.arxiv] = c
    for c in from_huggingface(days):
        if c.arxiv in merged:
            merged[c.arxiv].hf_upvotes = c.hf_upvotes
            merged[c.arxiv].source = "arxiv+huggingface"
        else:
            merged[c.arxiv] = c
    return list(merged.values())
