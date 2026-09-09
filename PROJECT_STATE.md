# PROJECT_STATE

Last updated: 2026-09-09 (session 2, Sonnet 5) — Sprint 1 (P1) complete.

## Current phase

**P1 (Sprint 1) complete → P2 not started.**
Phases are defined in `docs/blueprint.md` section 10; Sprint 1's exact scope was section 11.

## Completed work

- **Blueprint** (session 1, Fable): `docs/blueprint.md`, `docs/taxonomy.md`, `docs/recon-rae-2026.md`.
- **Governance**: `CLAUDE.md`, `PROJECT_STATE.md` (this file), `CHANGELOG.md`, `DECISIONS.md`
  (D001–D014), `README.md`.
- **Schemas**: `schema/*.schema.json` for all 10 entity types (concept, paper, system, relation,
  problem, benchmark, result, transition, path, update_event) plus `schema/common.schema.json` for
  shared enums (axis keys, sections, tiers, relation types, etc).
- **Tooling** (`scripts/`, Python, isolated in `.venv/` — see below):
  - `validate.py` — schema validation (jsonschema, Draft 2020-12) + referential integrity across
    the whole graph (relation endpoints, paper→problem, paper axes→concept, transition options,
    path steps, MDX file existence, duplicate/filename-mismatch ids). `--strict` also fails on
    warnings (orphan MDX, axis-mismatched concept references).
  - `build_graph.py` — compiles `data/**/*.yaml` into `site/src/data/graph.json` (build-time
    import) and mirrors it to `site/public/graph.json` (client-side fetch for `/graph`). Both are
    gitignored generated artifacts (D013); regenerated automatically by the site's `predev`/
    `prebuild` npm hooks, or manually via `python scripts/build_graph.py`.
  - `verify_paper.py` — fetches an arXiv abstract by id, prints recorded-vs-fetched title/authors/
    date for review, and (unless `--dry-run`) sets `status.verified/verified_on/verified_by`. Never
    touches `summary`/`explanation` content itself.
- **Tests**: `tests/` (pytest, 16 tests) — schema self-validity, referential-integrity failure
  modes (dangling relation, filename/id mismatch, duplicate id, bad enum), graph-build shape, and a
  regression test that the real `data/` tree validates clean. Plus arXiv-parsing unit tests for
  `verify_paper.py` with no live network calls.
- **Seed data** (all validated, all `status.verified: true` — see "Papers reviewed" below):
  - 30 papers: 10-paper generation backbone (LDM, DiT, Flow Matching, Rectified Flow, SiT, SD3,
    VAR, MAR, JiT) + the RAE spine from blueprint.md §4.2 (DINOv2/v3, SigLIP2, MAE, unCLIP, Emu2,
    REPA, VA-VAE, REPA-E, MAETok, DC-AE, MetaQuery, BLIP3-o, RAE, SVG, SVG-T2I, Scale-RAE, RAEv2,
    Distilling Drifting Transformers, TokenFlow, Web-SSL).
  - FLUX modeled as the one `system` (not `paper`) entity — `data/systems/flux.yaml` — since it has
    no single arXiv paper; only FLUX.1 Kontext does (not seeded as a paper this sprint).
  - Totals: 64 entities (30 papers, 23 concepts, 7 problems, 2 transitions, 1 path, 1 system),
    54 relations. `python scripts/validate.py` passes clean.
  - 23 concepts covering all 6 design axes (representation ×8, objective ×5, architecture ×4,
    conditioning ×2, training-signal ×1, inference ×1) plus 2 background concepts (GAN, VQ-VAE).
  - 7 problems (exactly the cross-cutting nodes blueprint.md §4.2 names).
  - 2 transitions (pixels→representation-latents, diffusion→flow-matching).
  - 1 learning path ("DiT to RAE in 12 steps").
  - 54 relations across `data/relations/generation.yaml` (18) and `data/relations/rae.yaml` (36).
  - One full MDX narrative written and wired: `content/transitions/pixels-to-representation-
    latents.mdx`, referenced from its transition's `narrative` field. All other `explanation`/
    `narrative` fields are still `null` — full paper-page write-ups are P2 work.
- **Site** (`site/`, Astro 7 + `@astrojs/mdx` + `katex` + `d3`, plain CSS design tokens):
  - Pages: `/` (home, axis map + 4 entry points + recent-papers table), `/axes/[axis]` (all 6 axes,
    data-driven), `/transitions/pixels-to-representation-latents` (renders the real MDX narrative),
    `/papers/[id]` (dynamic, all 30 papers, tier-conditional template, one rendered KaTeX equation),
    `/graph` (D3 force-directed SVG prototype, drag + relation-type filter + click-for-detail,
    fetches `/graph.json` client-side), `/search` (Pagefind default UI).
  - Light/dark theme via CSS variables + `prefers-color-scheme` + a toggle button (localStorage).
  - Per-section color identity (7 hues) applied to headings/badges/left-borders only, per
    blueprint §5.
  - `npm run build` succeeds: 40 static pages, Pagefind indexes them (1405 words) as a postbuild
    step. Smoke-tested via `astro preview` — all 6 representative routes return HTTP 200 and
    `/graph.json` serves the expected 63 nodes / 54 edges.
- **Python env**: `.venv/` (gitignored) with PyYAML, jsonschema (pinned `<5` — `RefResolver` is
  deprecated in 4.18+, see D0-in-code comment in `validate.py`), requests, pytest. Deliberately
  isolated from the system/anaconda Python (see "Failed approaches" — do not `pip install --user`
  into the system environment again).

## Important decisions (see DECISIONS.md for full text)

D001 three-layer taxonomy · D002 Astro+D3+Pagefind stack · D003 YAML entities + JSON Schema ·
D004 no claim without fetched source · D005 images only · D006 pipeline candidates via PR, no
auto-merge · D007 model policy · D008 GAN/VAE/early-diffusion background-only · D009 tier
definitions · D010 Sprint 1 on Sonnet · **D011 track current Astro major (7, not a pinned "5")** ·
**D012 Sprint 1 seed-set composition and verification method** · **D013 graph.json is generated,
gitignored, and auto-rebuilt via npm hooks** · **D014 `/papers/[id]` is one dynamic route covering
all seeded papers, not a single hardcoded page**.

## Files created / changed this session (session 2)

`README.md`, `pyproject.toml`, `.gitignore` (additions), `schema/*.schema.json` (11 files),
`scripts/validate.py`, `scripts/build_graph.py`, `scripts/verify_paper.py`, `tests/conftest.py` +
4 test files, `data/concepts/*.yaml` (23), `data/papers/*.yaml` (30), `data/problems/*.yaml` (7),
`data/transitions/*.yaml` (2), `data/paths/*.yaml` (1), `data/relations/generation.yaml`,
`data/relations/rae.yaml`, `data/systems/flux.yaml`, `content/transitions/pixels-to-
representation-latents.mdx`, `site/` (full Astro project — package.json, astro.config.mjs,
tsconfig.json, src/layouts/Base.astro, src/styles/tokens.css, src/lib/graph.ts,
src/content.config.ts, src/pages/{index,graph,search}.astro, src/pages/axes/[axis].astro,
src/pages/papers/[id].astro, src/pages/transitions/pixels-to-representation-latents.astro),
`DECISIONS.md` (D011–D014), `PROJECT_STATE.md` (this file), `CHANGELOG.md`.
No git commit yet this session — `git init` ran in session 1; nothing has been committed to date.

## Papers reviewed

All 30 seed papers: **arXiv id fetched and title-matched** via `scripts/verify_paper.py`
(`status.verified: true, verified_by: sonnet, verified_on: 2026-09-09` in every
`data/papers/*.yaml`). This is abstract-level verification (matches the schema's own definition of
`verified`), not a full PDF read. Two transcription errors were caught and fixed this way: an
em-dash vs. hyphen in the BLIP3-o title, and a misattributed VA-VAE co-author (corrected to Bin
Yang). **No paper has had its full PDF read yet** — `explanation` MDX (the full before/problem/
core-idea/.../why-it-matters template) is null for all 30; that is explicitly P2 work, and per
D007 the landmark/core ones (rae-2025, scale-rae-2026, ldm-2022, dit-2023, sd3-2024, var-2024,
mar-2024, repa-2024, dinov2-2023, mae-2021, unclip-2022, jit-2025) should get a Fable pass, not
Sonnet.

## Conclusions so far

- Central organizing idea: **Follow the representation.** (unchanged from session 1)
- Working hypothesis (still untested beyond a first-pass search): editing in RAE-style semantic
  latents is underexplored. See `docs/recon-rae-2026.md`'s "RAE-editing gap" section — Phase 3
  needs a deeper Semantic-Scholar-citation pass before this is anything more than a first-pass read.
- The seed graph held up its own referential-integrity design on the first real run (63 entities,
  54 relations validated clean immediately) — the schema design from Sprint 1 task 2 appears sound
  for at least this scale; revisit if P2's larger data set exposes gaps.

## Unresolved questions

1. Which of the ~20 RAE follow-ups catalogued in `docs/recon-rae-2026.md` (beyond the 2 seeded —
   RAEv2, Distilling Drifting Transformers) deserve full paper entities in P2? Candidates by theme
   are already sorted in that file (decoder/reconstruction: LV-RAE, DecQ, Laminating; discrete/
   unified: VQRAE, IDEAL, dRAE; objective/sampling: MeanFlow-RAE, RepFusion).
2. Full PDF reads still needed (Fable, per D007): rae-2025, scale-rae-2026, raev2-2026 (named
   explicitly in the original Sprint 1 task list), plus — now that the seed set is built — every
   other landmark/core paper before its `explanation` MDX is written.
3. Non-RAE frontier recon (arXiv Jan–Sep 2026 for generation, editing, unified, medical) →
   `docs/recon-2026.md` — **not done yet**, explicitly deferred to a Fable session per the original
   task list (this was Sonnet-session-2 work only for schemas/data/site; recon is Fable-only).
4. FLUX.1 Kontext (arXiv 2506.15742) — real paper, not yet seeded as a `paper` entity; relevant
   once the editing section starts (P3). Currently only referenced in `data/systems/flux.yaml`'s
   release notes.
5. SVG-2025's and SVG-T2I-2025's `orgs` fields are empty — the arXiv Atom feed doesn't carry
   institutional affiliation, and I did not find it via search. Fill in during P2 if it becomes
   relevant to the "top universities/labs" prioritization.
6. Hosting: public vs. private repo, GitHub account (needed at P8 only — unchanged from session 1).
7. Pipeline LLM stages: paid API vs. Claude Code scheduled routine (needed at P7 only — unchanged).

## Failed approaches (do not repeat)

- **Do not `pip install --user` anything into the system/anaconda Python.** Early in this session,
  upgrading `jsonschema` via `pip install --user` shadowed the system's pinned `jsonschema==3.2.0`
  (which `label-studio` and other installed tools depend on) and broke `Draft202012Validator`
  imports project-wide. Reverted immediately (`pip install --user jsonschema==3.2.0`). Use the
  project's own `.venv/` for all Python tooling instead — see README.md.
- Astro's content-collection config file must be `site/src/content.config.ts`, not
  `site/src/content/config.ts` — the latter is Astro <7's location and throws
  `LegacyContentConfigError` on Astro 7. Already fixed; noted here so a future session doesn't
  "fix" it back.

## Exact next tasks (start of P2)

Per `docs/blueprint.md` section 10, P2 is: **RAE section complete** — problem→idea→method→evidence→
limitation→next chain written out for the RAE spine, 20 verified entries with full explanations
(not just metadata), latent-geometry and transport-path concept pages fleshed out, open problems
expanded; plus Generation axes pages content and 2 more transition narratives (only 1 of 2 seeded
transitions has its MDX written).

1. **Fable session**: read the RAE follow-up shortlist from unresolved-question 1 above and decide
   which become full paper entities; do the non-RAE frontier recon (`docs/recon-2026.md`); full-PDF
   read rae-2025, scale-rae-2026, and the other landmark/core papers listed in unresolved-question 2.
2. **Sonnet**: write `explanation` MDX for each landmark/core paper once Fable's reads land (content
   only — do not invent claims beyond what was actually read; leave a TODO + link if a claim needs a
   read that hasn't happened yet).
3. **Sonnet**: write the second transition's MDX narrative (diffusion→flow-matching).
4. **Sonnet**: expand `data/problems/*.yaml` — the `candidate_approaches` lists are currently thin
   placeholders for 2-3 of the 7 problems.
5. Re-run `scripts/validate.py` + `pytest` + `npm run build` after each batch; update this file and
   `CHANGELOG.md` after each meaningful unit of work, per `CLAUDE.md`'s protocol.

**Not yet started**: pipeline (`pipeline/`, P7), medical section (P5), editing section (P3), unified
section (P4), VFM/VLM brief pages (P4), publishing/GitHub Pages deploy (P8).
