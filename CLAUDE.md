# Generative Vision Atlas — session bootstrap

This repository is a living research atlas of modern generative vision (2023–2026). It spans many
sessions. Never rely on chat history.

## Resume protocol (do this first, every session)
1. Read `PROJECT_STATE.md` in full.
2. Read the top of `CHANGELOG.md` (Unreleased + last release).
3. Skim `DECISIONS.md` for the decision ids referenced in the state file.
4. If `scripts/validate.py` exists, run it. Fix errors before adding content.
5. Continue from **Exact next tasks** in `PROJECT_STATE.md`.
6. After every meaningful unit of work, update `PROJECT_STATE.md` and `CHANGELOG.md` before doing
   anything else.

## Rules
- Organize papers around ideas, representations, objectives, architectures, capabilities, and
  problems. Never produce a flat paper list. See `docs/blueprint.md` §2 for the taxonomy.
- **No explanatory claim without a fetched source** (D004). A paper entry stays `verified: false`
  until its abstract or PDF was fetched and read in the session that wrote the explanation.
- Do not add every arXiv paper. Tiers: landmark / core / strong-followup / emerging / watchlist (D009).
- Video, 3D, audio are out of scope except as pointer nodes (D005).
- Long-form text lives in `content/**/*.mdx`; structured facts live in `data/**/*.yaml` and must
  validate against `schema/*.schema.json`.
- Do not ask the user for permission for normal research, coding, schema, or site decisions. Log
  important decisions in `DECISIONS.md`. Stop only for credentials, paid services, destructive
  external actions, or public publishing.

## Model policy (D007)
- Fable 5.1 (or Opus 5 as cheaper substitute): taxonomy, transition narratives, RAE synthesis,
  "what is unified" matrix, editing-gap investigation, medical evidence appraisal, resolving
  conflicting papers, reviewing landmark/core explanations, hard architecture problems.
- Sonnet 5: site code, schemas, validators, pipeline code, drafting core/strong explanations from a
  fetched PDF.
- Haiku 4.5: metadata, YAML entries, formatting, changelog lines, pipeline filters.
- Never use Fable/Opus for routine metadata, formatting, or easy code.

## Layout
See `docs/blueprint.md` §7. Key dirs: `data/` (YAML entities), `content/` (MDX), `schema/`,
`scripts/`, `site/` (Astro), `pipeline/` (3-day update system), `docs/`.
