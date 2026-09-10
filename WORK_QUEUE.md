# WORK QUEUE

Standing task list from user review on 2026-09-10. Worked top to bottom. Each item records what
was done, so a future session can resume mid-item without re-deriving context.

Status key: `TODO` · `IN PROGRESS` · `DONE` · `BLOCKED`

---

## Q1 + Q2 — Written explanations for every paper
**Status: IN PROGRESS**

The stored abstract is a floor, not the goal. Every paper should have the structured `explained`
block that LLaDA-Image has: before / problem / idea / method / evidence / limitations /
why-it-matters, with `depth` recording abstract vs full-text.

- [x] Schema (`explained` object, required `depth`) — session 6
- [x] Abstracts stored verbatim on all papers with an arXiv id — session 6
- [x] Full-text write-ups: LLaDA-Image, Drifting Models, RAE, JiT, Scale-RAE — session 6
- [x] 23 more full-text write-ups (representation/latent-design area) — session 7: repa-2024,
      vavae-2025, repae-2025, maetok-2025, svg-2025, svg-t2i-2025, raev2-2026, dcae-2024, decq-2026,
      lvrae-2026, flatdino-2026, pae-2026, genfirst-2026 (abstract-depth — no HTML render exists),
      latent-diffusability-2026, dinov2-2023, siglip2-2025, mae-2021, unclip-2022, tokenflow-2024,
      dit-2023, sit-2024, ldm-2022, sd3-2024. 28 papers done total; validator warned on 73 remaining
      landmark/core papers after this batch (down from 87 minus the 5 already done minus these 23,
      so the count also reflects new landmark/core papers added by other concurrent sessions).
- [ ] Remaining landmark + core papers (validator warns on each; run `scripts/validate.py` for the
      current count)
- [ ] Strong-followup and emerging papers

**Method that works:** fetch `arxiv.org/html/<id>v1` and extract intro + method + limitations. The
abs page alone is too thin — it usually yields "the abstract does not state a problem". Batch through
subagents, then verify claims against the fetched text before writing.

---

## Q3 — Make editing discoverable, and answer "can this model do both?"
**Status: TODO**

A reader's real question is: *does this model generate, edit, or both, and what space does it work
in?* That is currently spread across lines and sections, and HiDream-O1-Image is hard to find at all.

- [ ] A capability matrix: model × (generates / edits / understands) × latent space × open weights
- [ ] Make it reachable from the top nav, not buried under a section
- [ ] Ensure every named system (HiDream-O1, BAGEL, Emu3.5, Qwen-Image-Edit, Kontext, Seedream,
      Nano Banana, GPT-Image) appears in it and is findable by search

---

## Q4 — Runnable notebooks with real outputs
**Status: TODO**

For well-known methods and anything claiming to be great, a notebook that runs inference with 1-2
samples, so a reader sees how each method behaves without cloning six repos. Not new research — just
the authors' own material, assembled, with their GitHub credited in the cell that uses it.

**Hardware confirmed (session 7):** 3× NVIDIA A100 80GB, 734GB free disk, 103GB HF cache already
populated. Working env: `/home/exx/anaconda3/envs/dediffusion/bin/python` (torch 2.10.0+cu128,
diffusers 0.36.0, CUDA available).

**Already cached locally — start with these, no download needed:**
`nyu-visionx--RAE-collections`, `nyu-visionx--Scale-RAE-Qwen1.5B_DiT2.4B`,
`nyu-visionx--siglip2_decoder`, `stabilityai--stable-diffusion-3-medium-diffusers`,
`stabilityai--stable-diffusion-xl-base-1.0`, `runwayml--stable-diffusion-v1-5`,
`sd2-community--stable-diffusion-2-1-unclip-small`, `h94--IP-Adapter`, `facebook--dinov2-base`,
`facebook--vit-mae-base`, `google--siglip2-so400m-patch14-224`, CLIP variants.

- [ ] Notebook harness: shared setup cell, deterministic seeds, output images committed
- [ ] Generation notebooks (SD1.5 / SDXL / SD3 as the VAE-latent baseline; RAE / Scale-RAE as the
      representation-latent case — the direct comparison the atlas argues about)
- [ ] Editing notebooks (IP-Adapter reference conditioning; an inversion method; a training-free
      attention method)
- [ ] Site section rendering the notebooks with their outputs, linking to source repos
- [ ] Run instructions on the site, one click from the GitHub page

**Design constraint:** each cell credits the upstream repo it borrows from. This assembles, it does
not reimplement.

---

## Q5 — Vision foundation models and VLM sections
**Status: TODO**

Both render empty. The user considers these foundational to any vision task and wants them tracked.

- [ ] VFM section: DINOv2/v3, SigLIP2, MAE, I-JEPA, Perception Encoder, AIMv2, Web-SSL, registers,
      SAM, Depth Anything — with lines grouping them by what supervision they use
- [ ] VLM section: encoder+projector (LLaVA), cross-attention (Flamingo), early fusion (Chameleon,
      Fuyu), native resolution (Qwen-VL family), and why each matters to generation
- [ ] Explicit link from these to where they are consumed: as alignment targets (REPA), as
      generative latents (RAE), as text encoders (Qwen-Image), as instruction parsers (Step1X-Edit)

---

## Q6 — Unverified items still excluded
**Status: TODO** (carried from session 4)

Only secondary sources found; must be checked against vendor primary sources before entering:
Qwen-Image-3.0, FLUX 3 open weights, GPT-Image 2.5, Nano Banana 2 Lite, MAI-Image-2.6, SD4.

---

## Standing instructions
- Compact context around 90% and keep this file current, so work stays traceable across sessions.
- After each meaningful unit: update this file, `PROJECT_STATE.md`, and `CHANGELOG.md`.
- No explanatory claim without a fetched source (D004).
