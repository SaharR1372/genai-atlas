# CHANGELOG

## Unreleased

### 2026-09-10 — Session 8 (Sonnet 5) — WORK_QUEUE Q1/Q2, all 19 medical papers explained
- **All 19 medical-imaging papers with no `explained` block now have one**, all at `depth:
  full-text`: chung-ye-2021, dar-memorization-2023, frd-2024, roentgen-2022, maisi-2024,
  biomedjourney-2023, jalal-2021, staindiffuser-2024, dscm-2020, mededit-2024, monai-gen-2023,
  synthrad-2024, pixcell-2025, radedit-2023, syndiff-2022, retinal-fm-latent-2026, stream-2026, and
  ktena-2024 (Nature Medicine, no arXiv; full text pulled via PubMed Central, PMCID PMC11031395).
  Fanned out across 4 parallel subagents, each fetching `arxiv.org/html/<id>vN` (or PubMed for the
  one DOI-only paper) and writing directly into `data/papers/*.yaml`.
- Every block states the paper's **generation space** (pixel / domain-trained VAE / borrowed
  natural-image VAE / foundation-model latent / normalizing flow) and the paper's own stated
  rationale for it, or explicitly notes the absence of one, per the medical-specific requirement.
- **Miscategorization found and flagged (not fixed this session, per file-scope constraint):**
  `mededit-2024.yaml` is tagged `lines: [line-medical-transfer-vae]`, but the fetched full text
  shows it is a plain pixel-space DDPM (RePaint-style inpainting on 128x128 T1 slices) with no VAE,
  VQGAN, or latent of any kind — it does not fine-tune Stable Diffusion or use any borrowed
  autoencoder. The line's `core_bet` ("keeping its natural-image VAE frozen") does not describe
  this paper's mechanism at all. `data/lines/line-medical-transfer-vae.yaml` needs its arc entry
  for mededit-2024 reassigned to `line-medical-pixel-space`, or removed, in a future session.
- Two more findings from the fetched text, consistent with (not contradicting) existing line
  claims: `dar-memorization-2023` is the direct evidentiary source for
  `line-medical-domain-vae`'s "demonstrated memorization risk" weakness (59% of coronary CT
  training volumes, 33% of sampled MRI candidates confirmed memorized); `ktena-2024`'s fetched full
  text confirms `line-medical-pixel-space`'s claim that it carries "the strongest downstream
  evidence in the whole medical section" — three-modality downstream gains plus a genuine
  dermatologist reader study — while itself arguing no rationale for pixel space at all.
- `scripts/validate.py` clean (0 errors, 0 warnings on any of the 19 files) after every edit. Only
  `data/papers/*.yaml` touched, per the task's own constraint.

### 2026-09-10 — Session 7 (Opus 5) — notebooks, capability matrix, VFM/VLM sections
- **Runnable notebooks with real outputs** (queue Q4). `latents.ipynb` measures what each generation
  of autoencoder discards and contrasts a DINOv2 feature map against an SD latent; `editing.ipynb`
  runs three editing mechanisms on one image with difference maps showing how strong each
  preservation guarantee actually is. Both executed on an A100 80GB with outputs committed. Built
  from plain-Python specs so the sources stay reviewable in a diff.
- **`/models` capability matrix** (Q3): 40 systems by what they can do, what latent they are built
  on, and how available they are. Answers "does this model generate, edit, or both, and on what".
- **VFM and VLM sections filled** (Q5): 19 verified papers, 6 new lines, and the connection to
  generation made explicit — which encoders are alignment targets, which are generative latents,
  which VLMs serve as text encoders and instruction parsers.
- **New open problem** `which-encoder-for-generation`: REPA and RAE independently rank DINOv2 first
  as a generative substrate but disagree about the cause, and a 27-encoder study argues the
  predictor is patch-level spatial structure rather than linear-probe accuracy.
- **A claim removed**: SVG's widely repeated 62x training speedup could not be found in the paper
  body on a full-text read, so it is no longer attributed to the paper.
- **28 papers now carry full written explanations**, 27 from full text.
- 293 entities, 252 pages, 28 tests, validation clean.

### 2026-09-10 — Session 7 (Sonnet 5) — WORK_QUEUE Q1/Q2, 23 more full explanations
- **23 more `explained` blocks written**, all in the representation/latent-design area, from
  fetched arXiv full text: repa-2024, vavae-2025, repae-2025, maetok-2025, svg-2025, svg-t2i-2025,
  raev2-2026, dcae-2024, decq-2026, lvrae-2026, flatdino-2026, pae-2026, genfirst-2026,
  latent-diffusability-2026, dinov2-2023, siglip2-2025, mae-2021, unclip-2022, tokenflow-2024,
  dit-2023, sit-2024, ldm-2022, sd3-2024. 22 at `depth: full-text`; genfirst-2026 at
  `depth: abstract` since its arXiv HTML render does not exist under v1/v2/ar5iv and its PDF
  exceeded the fetch size limit.
- **Findings that refine or correct the atlas's own prior claims**, all recorded directly in each
  paper's `explained` block rather than only here: REPA-E's gFID numbers differ between arXiv v1
  (1.83/1.26) and v2 (1.69/1.12) — v2 matches the stored abstract and is the source of record.
  latent-diffusability-2026's fetched text explicitly states it does not compare a pure frozen-encoder
  RAE tokenizer against VAE tokenizers, which nuances the existing `summary`'s "reconstruction-only,
  representation-only, and hybrid" framing. genfirst-2026's abstract describes a purely trained,
  VAE-style end-to-end curriculum with no frozen foundation encoder mentioned anywhere, which is a
  meaningfully different kind of "hybrid" than `line-latent-hybrid` implies. svg-2025's existing
  summary claim of "62x faster training, 35x faster inference" could not be confirmed anywhere in
  the fetched paper body and was not repeated in `explained`. SVG-T2I's conditioning mechanism
  (Lumina-Image-2.0-style single-stream joint attention, not a MetaQuery query-bridge) was confirmed
  directly from the text, matching what the atlas already recorded.
- Validator clean after every file (`scripts/validate.py`: 0 errors); no file outside
  `data/papers/*.yaml` touched by this batch.

### 2026-09-10 — Session 6 (Opus 5) — real paper explanations
- **Abstracts stored verbatim.** `verify_paper.py` now writes the authors' own abstract onto every
  paper (`--refresh` backfills), so no paper page is ever empty of substance.
- **Structured `explained` block** on the paper schema: before, problem, idea, method, evidence,
  limitations, why it matters, plus a `depth` field recording whether the account came from the
  abstract or the full text. The depth is shown on the page so a reader knows how far to trust the
  method detail. Written from full text for LLaDA-Image, Drifting Models, RAE, JiT and Scale-RAE.
- **Two new research lines** for recent papers no existing line claimed: evaluation and benchmarks,
  and agentic/search-augmented generation.
- **Coverage tracked**: the validator now warns on every landmark/core paper lacking an explanation
  and every paper lacking a stored abstract, and `/updates` reports the counts.

### 2026-09-10 — Session 5 (Opus 5) — medical split out, landing page rebuilt
- **Medical imaging separated into its own domain** (D020): a dedicated `/medical` area organized by
  which space each line generates in and why that space was chosen, plus its own open problems and
  paper index. Medical entities are filtered out of the general lines, timeline and problems views;
  the research graph gains a domain switch. `isMedical()` is the single definition of the split.
- **Landing page rebuilt** (D021) for a visitor arriving cold from a shared link: leads with the
  representation spectrum as one diagram, then the six design questions with every line under them,
  then what the atlas does that a paper list does not, the medical domain as a distinct block,
  reading paths, and recent additions. All figures derive from `atlasStats()` at build time.
- **New `/updates` page** reporting the pipeline's actual last run, the current review queue with the
  reason each candidate was surfaced, and the verification standards.
- Open Graph and Twitter card tags added, since the site is meant to be shared.
- 222 pages, 264 entities, 28 tests, validation clean.

### 2026-09-10 — Session 4 (Opus 5) — conditioning, editing, medical, and a live pipeline
- **Living-update pipeline built** (the "every 3 days" requirement): discovery from arXiv and
  Hugging Face daily papers, rule-based relevance and quality scoring, duplicate detection, a ranked
  candidate queue, and a GitHub Actions cron. Nothing auto-merges (D006). A hard core-topic gate was
  needed: the first live run surfaced world-action models and LLM post-training papers, since they
  share nearly all of generative vision's vocabulary. 310 raw candidates now reduce to ~5 relevant.
- **Conditioning section**: 14 mechanism explainers, 10 papers, a new adapter-conditioning line, a
  text-conditioning-evolution narrative, and the finding that RAE-family systems borrow their
  conditioning wholesale — Scale-RAE adopts MetaQuery, SVG-T2I uses Lumina's joint attention, and
  RAE/SVG themselves are class-conditional with no text pathway.
- **Editing section**, categorized by which space the edit happens in: five lines covering VAE
  latent, training-free attention manipulation, flow inversion, representation latent, and unified
  models. HiDream-O1-Image confirmed as the pixel-level unified case with no VAE at all.
- **Medical section**: 19 papers, five lines organized by generation space, and the finding that
  medical work splits by task rather than era — pixel space where inverse problems demand it,
  domain-trained 3D VAEs for volumes, borrowed natural-image VAEs for 2D, and exactly two 2026
  papers generating inside a medical foundation model's space.
- **Currency**: brought up to September 2026, including LLaDA-Image, GenFirst, dRAE and Second Order
  Drifting Models.
- 264 entities, 124 papers, 25 lines, 221 pages, 28 tests. Six title errors caught by verification.

### 2026-09-10 — Session 4 (Sonnet 5) — conditioning-mechanism design space
- **Research task**: mapped the full conditioning-mechanism design space (how text/reference/control
  signals reach the generator) across UNet, DiT, unified-model, and RAE-family systems, per direct
  request. Every mechanism claim traces to a freshly fetched arXiv abstract or HTML source this session
  (D004); several were quoted verbatim from paper text via `arxiv.org/html/<id>`.
- **9 new concepts** (`data/concepts/`): `adaln-modulation`, `query-bridge`, `clip-text-encoder`,
  `t5-text-encoder`, `adapter-conditioning`, `decoupled-cross-attention`, `identity-preserving-conditioning`,
  `native-token-conditioning`, `single-stream-dit` — filling gaps in the `conditioning` axis (previously
  only `cross-attention`, `joint-attention`, `mmdit`, `sequence-concat`, `vlm-text-encoder` existed, all
  with `explains: null`).
- **10 new papers, all arXiv-verified**: ControlNet (2302.05543), T2I-Adapter (2302.08453), IP-Adapter
  (2308.06721), InstantID (2401.07519), PuLID (2404.16022), OminiControl (2411.15098), Chameleon
  (2405.09818), Emu3 (2409.18869), CLIP (2103.00020), Imagen (2205.11487 — the last two are pre-2023
  exceptions to D008, justified and logged as **D018**).
- **New line**: `line-adapter-conditioning` (ControlNet → T2I-Adapter → IP-Adapter → InstantID/PuLID →
  challenged by OminiControl), `competes_with: [line-in-context-editing]`. `line-in-context-editing`'s
  arc gained OminiControl as a `precursor` (predates ACE++ by ~2 months with the same mechanism for
  general control, not editing specifically — flagged, not silently reassigned as origin).
- **New problem**: `conditioning-mechanism-in-semantic-latent` — no paper has directly compared
  conditioning mechanisms on a matched RAE-family backbone; Scale-RAE and SVG-T2I each transplanted an
  existing mechanism from the VAE-latent literature unmodified.
- **New transition**: `text-conditioning-evolution` (`content/transitions/text-conditioning-evolution.mdx`,
  full narrative + site page at `/transitions/text-conditioning-evolution`), covering UNet cross-attention
  (2022) through MM-DiT/single-stream joint attention, adapters and their in-context challenger, native-token
  unified models, and the query-bridge mechanism, to the 2025-26 RAE-family split.
- **Key finding (the session's central ask)**: the two published RAE-family text-to-image systems use
  *different* conditioning mechanisms, transplanted unmodified from the VAE-latent literature — SVG-T2I
  uses Lumina-Image 2.0's single-stream joint attention (Gemma2-2B text encoder); Scale-RAE explicitly
  states it "adopts the MetaQuery architecture" (256 learnable queries, Qwen-2.5 1.5B, MLP connector into
  a DiT). Both confirmed via `arxiv.org/html/<id>` fetches, not recollection. RAE (2510.11690) and SVG
  (2510.15301) themselves are class-conditional ImageNet models with no text conditioning at all —
  a fact the previous sessions' summaries did not state explicitly.
- **14 new `explains`/`narrative` MDX files** written in `content/concepts/` and `content/lines/`
  (mechanism + verified quotes + trade-offs, 2-4 sentences per the requested format), plus the transition
  narrative above.
- **16 new relations** in a new `data/relations/conditioning.yaml`, including two paper-internal
  mechanism ablations found and cited as the closest things to a systematic conditioning-mechanism
  comparison in the literature this session found: DiT's in-context/cross-attention/adaLN-Zero ablation,
  and SD3's cross-attention/"vanilla"/MM-DiT ablation (SD3's own text: MM-DiT "significantly outperforms
  the cross-attention and vanilla variants").
- **Axes backfilled** on 13 existing papers that were missing `axes.conditioning` (ldm-2022, dit-2023,
  metaquery-2025, blip3o-2025, scale-rae-2026, svg-t2i-2025, lumina2-2025, qwen-image-2025,
  hunyuanimage3-2025, janus-pro-2025, icedit-2025) and 2 concepts with empty `introduced_by`
  (cross-attention → ldm-2022).
- **Governance**: `DECISIONS.md` D018 (pre-2023 conditioning-lineage exception to D008) and D019 (logs
  that this task ran on Sonnet, not Fable, despite D007 — flags the taxonomy/line-arc judgment calls a
  Fable/Opus pass should still review).
- `python scripts/validate.py --strict` and `pytest` (28 tests) both pass clean: 227 entities, 66
  relations, 0 errors/warnings. `npm run build` succeeds: 185 static pages (up from 145).
- Not done, left open: D14/D15 (a dedicated survey paper systematically comparing conditioning
  mechanisms, and confirmed genuinely-new 2025-26 mechanisms beyond OminiControl) — WebSearch quota was
  exhausted and arXiv's search API rate-limited (HTTP 429) partway through this session; stated as
  unresolved rather than guessed. FLUX.2's reported Mistral text encoder is recorded as unverified (no
  arXiv paper found) rather than asserted as fact.

### 2026-09-09 — Session 3 (Opus 5) — restructured around research lines
- **Pushed to GitHub**: https://github.com/SaharR1372/genai-atlas (branch `main`).
- **New primary structure**: added the `line` entity type (D015) and rebuilt navigation around it.
  15 research lines, each with a core bet, status, ordered arc, strengths, weaknesses, and the open
  problems it does not solve. `/lines` and `/lines/[id]` replace the axis map as the entry point.
- **Coverage**: +44 papers (74 total), every one arXiv-verified by `verify_paper.py`. Fills gaps
  found in user review — Drifting Models (2602.04770), the natively-few-step family (MeanFlow,
  Shortcut Models, Inductive Moment Matching), the normalizing-flow revival (STARFlow), VAE/
  representation hybrids (DecQ, LV-RAE, FlatDINO, PAE, VFM-VAE), 2025-26 top-venue work across
  editing, unified models, RL alignment, and evaluation.
- **Benchmarks**: 4 benchmarks and 46 sourced results, with guidance method, training budget,
  parameter count, NFE and per-number caveats as schema fields (D016). New `/compare` page states
  plainly what the numbers do and do not support.
- **New pages**: `/compare`, `/problems`, `/timeline`; paper pages now show line membership and
  reported results.
- **Tooling**: `verify_paper.py` now throttles to arXiv's ~3s guidance and backs off on HTTP 429;
  `validate.py` gained line-membership consistency checks (a line's arc and a paper's `lines` must
  agree). 18 tests passing.
- **Corrections caught by verification**: OmniGen2 and RefEdit titles were wrong in the first draft
  and were fixed against the fetched arXiv metadata.

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
