# CHANGELOG

## Unreleased

### 2026-09-09 — Session 1 (Fable 5.1, plan mode)
- Added project blueprint (`docs/blueprint.md`) covering scope, taxonomy, research families,
  backbone paper map, site design, data schema, repo layout, 3-day update pipeline, model strategy,
  phases, and Sprint 1.
- Added governance: `CLAUDE.md` (resume protocol + rules), `PROJECT_STATE.md`, `DECISIONS.md`
  (D001–D010), `docs/taxonomy.md`.
- Created directory skeleton and `git init` (no commit yet).
- RAE recon: located Scale-RAE (2601.16208), RAEv2 (2605.18324), LLaDA-Image (2609.03796) and ~20
  RAE follow-ups via arXiv API; abstract summaries and candidate tiers in `docs/recon-rae-2026.md`.
  First-pass search found no dedicated RAE/VFM-latent image-editing paper.

### 2026-09-09 — Session 2 (Sonnet 5) — Sprint 1 / P1 complete
- Schemas: `schema/*.schema.json` for all 10 entity types + shared `common.schema.json`.
- Tooling: `scripts/validate.py` (schema + full referential integrity), `scripts/build_graph.py`
  (`data/` → `graph.json`, mirrored to `site/public/` for client-side fetch), `scripts/verify_paper.py`
  (arXiv fetch + title-match + `status.verified` flip). Isolated `.venv/` (see Decisions/Failed
  approaches — do not `pip install --user` system-wide again).
- Tests: `tests/` — 16 pytest cases covering schema self-validity, 4 referential-integrity failure
  modes, graph-build shape, arXiv-parsing (no live network), and a regression check that real `data/`
  validates clean.
- Seed data: 30 papers (10-paper generation backbone + full RAE spine from blueprint.md §4.2),
  23 concepts across all 6 design axes, 7 problems (the exact cross-cutting set blueprint.md names),
  2 transitions, 1 learning path, 1 system (FLUX — no single arXiv paper), 54 relations. Every
  paper's arXiv id fetched and title-verified via `verify_paper.py`; 2 transcription errors caught
  and fixed (BLIP3-o title punctuation, a VA-VAE co-author name). `validate.py` passes clean:
  64 entities, 54 relations, 0 errors.
- One full MDX narrative written: `content/transitions/pixels-to-representation-latents.mdx`.
- Site: Astro 7 (blueprint assumed "Astro 5" pre-release — tracking current major instead, see
  D011) + `@astrojs/mdx` + `katex` + `d3`, plain CSS design tokens with light/dark + 7-hue section
  identity. Pages: home, `/axes/[axis]` (all 6), one transition page (renders the real MDX), 
  `/papers/[id]` (dynamic, all 30 papers, tier-conditional template, one rendered KaTeX equation),
  `/graph` (D3 force-directed prototype with drag/filter/click-detail), `/search` (Pagefind).
  `npm run build` succeeds (40 static pages); smoke-tested via `astro preview` (all routes 200).
  `graph.json` is generated + gitignored, auto-rebuilt via npm `predev`/`prebuild` hooks.
- Governance: `README.md` added; `DECISIONS.md` D011–D014; `PROJECT_STATE.md` fully rewritten for
  P1-complete state with exact P2 next tasks.
