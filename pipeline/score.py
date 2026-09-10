"""
Stages 2-4: relevance filter, quality score, and duplicate check.

All rule-based. The point is not to decide what belongs in the atlas — a human or a
review session does that (D006) — but to turn a few hundred daily preprints into a
short, ranked queue that is actually reviewable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

from . import config
from .discover import Candidate


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


@dataclass
class Assessment:
    candidate: Candidate
    sections: list[str] = field(default_factory=list)
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    duplicate_of: str | None = None
    excluded_by: str | None = None

    @property
    def admitted(self) -> bool:
        return (
            self.excluded_by is None
            and self.duplicate_of is None
            and bool(self.sections)
            and self.score >= config.MIN_SCORE
        )


def load_atlas_index() -> dict:
    """Existing ids, arXiv ids, and normalized titles, for the duplicate check."""
    arxiv_ids, titles, shorts = set(), set(), {}
    papers_dir = config.DATA / "papers"
    if papers_dir.exists():
        for f in papers_dir.glob("*.yaml"):
            doc = yaml.safe_load(f.read_text()) or {}
            if doc.get("arxiv"):
                arxiv_ids.add(str(doc["arxiv"]))
            if doc.get("title"):
                titles.add(_norm_title(doc["title"]))
            shorts[f.stem] = doc.get("short") or doc.get("title", "")
    return {"arxiv_ids": arxiv_ids, "titles": titles, "papers": shorts}


def assess(cand: Candidate, atlas: dict) -> Assessment:
    a = Assessment(candidate=cand)
    haystack = f"{cand.title} {cand.abstract}".lower()

    # ---- duplicate check (deterministic, runs first: cheapest rejection) ----
    if cand.arxiv in atlas["arxiv_ids"]:
        a.duplicate_of = cand.arxiv
        return a
    if _norm_title(cand.title) in atlas["titles"]:
        a.duplicate_of = "title match"
        return a

    # ---- scope exclusion (D005: images only) ----
    for term in config.EXCLUDE_TERMS:
        if term in haystack:
            a.excluded_by = term
            return a

    # ---- hard gate: must actually be about generating or editing images ----
    core_hits = [t for t in config.REQUIRED_CORE_TERMS if t in haystack]
    if not core_hits:
        a.excluded_by = "no core image-generation term"
        return a
    a.reasons.append(f"core topic: {', '.join(core_hits[:3])}")
    # a core term in the TITLE is much stronger evidence than one buried in the abstract
    if any(t in cand.title.lower() for t in config.REQUIRED_CORE_TERMS):
        a.score += config.SCORE_WEIGHTS["core_in_title"]
        a.reasons.append("core topic appears in the title")

    # ---- relevance: which sections does it touch? ----
    for section, terms in config.SECTION_TERMS.items():
        if any(t in haystack for t in terms):
            a.sections.append(section)
    if not a.sections:
        return a
    a.score += config.SCORE_WEIGHTS["section_hit"] * len(a.sections)
    a.reasons.append(f"matches sections: {', '.join(a.sections)}")

    # ---- quality signals ----
    author_blob = " ".join(cand.authors).lower()
    if any(org in haystack or org in author_blob for org in config.STRONG_ORGS):
        a.score += config.SCORE_WEIGHTS["strong_org"]
        a.reasons.append("affiliated with a major lab or university")

    hits = [n for n in config.NOTABLE_AUTHORS if n.lower() in author_blob]
    if hits:
        a.score += config.SCORE_WEIGHTS["notable_author"]
        a.reasons.append(f"notable author: {', '.join(hits)}")

    # does it reference something already in the atlas by name?
    named = [
        short for short in atlas["papers"].values()
        if short and len(short) > 3 and short.lower() in haystack
    ]
    if named:
        a.score += config.SCORE_WEIGHTS["cites_atlas_paper"]
        a.reasons.append(f"mentions atlas work: {', '.join(sorted(set(named))[:4])}")

    if "github.com" in haystack or "code is available" in haystack or "we release" in haystack:
        a.score += config.SCORE_WEIGHTS["has_code"]
        a.reasons.append("code or weights released")

    title_l = cand.title.lower()
    if any(sig in title_l for sig in config.TITLE_SIGNALS):
        a.score += config.SCORE_WEIGHTS["title_signal"]
        a.reasons.append("title suggests a substantive contribution")

    # community signal, when we have it
    if cand.hf_upvotes:
        bump = min(cand.hf_upvotes / 10.0, 5.0)
        a.score += bump
        a.reasons.append(f"{cand.hf_upvotes} upvotes on Hugging Face daily papers")

    return a


def assess_all(cands: list[Candidate]) -> list[Assessment]:
    atlas = load_atlas_index()
    out = [assess(c, atlas) for c in cands]
    out.sort(key=lambda a: a.score, reverse=True)
    return out
