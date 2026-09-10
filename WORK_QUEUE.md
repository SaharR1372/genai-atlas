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
- [x] All 19 medical-imaging papers with no `explained` block — session 8: chung-ye-2021,
      dar-memorization-2023, frd-2024, roentgen-2022, maisi-2024, biomedjourney-2023, jalal-2021,
      staindiffuser-2024, dscm-2020, mededit-2024, monai-gen-2023, synthrad-2024, pixcell-2025,
      radedit-2023, syndiff-2022, retinal-fm-latent-2026, stream-2026, ktena-2024 (DOI-only, via
      PubMed). All full-text depth. Found `mededit-2024` miscategorized under
      `line-medical-transfer-vae` (it is pixel-space, no VAE at all) — flagged, not fixed, since
      the task scope was `data/papers/*.yaml` only. See CHANGELOG's session 8 entry.
- [ ] Remaining landmark + core papers (validator warns on each; run `scripts/validate.py` for the
      current count)
- [ ] Strong-followup and emerging papers

**Method that works:** fetch `arxiv.org/html/<id>v1` and extract intro + method + limitations. The
abs page alone is too thin — it usually yields "the abstract does not state a problem". Batch through
subagents, then verify claims against the fetched text before writing.

---

## Q3 — Make editing discoverable, and answer "can this model do both?"
**Status: DONE** (session 7)

A reader's real question is: *does this model generate, edit, or both, and what space does it work
in?* That is currently spread across lines and sections, and HiDream-O1-Image is hard to find at all.

- [x] `/models` capability matrix: 40 systems × (generate / edit / multi-ref / understand /
      tokenize) × basis × availability, filterable. 10 of 40 do both generation and editing.
- [x] `capabilities` and `openness` added to the paper schema and populated
- [x] In the top nav as "Models"
- [x] HiDream-O1-Image called out on the page as the one system with no autoencoder at all
- Note: closed systems without a paper (Nano Banana, GPT-Image) are still absent from the atlas
  entirely — they belong under Q6, not here.

---

## Q4 — Runnable notebooks with real outputs
**Status: IN PROGRESS** (2 of ~5 built, session 7)

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

- [x] Harness: `notebooks/build.py` builds and executes from plain-Python specs in
      `notebooks/specs/*.py`, so sources stay reviewable in a diff. `notebooks/publish.sh` renders
      to static HTML for the site.
- [x] `latents.ipynb` — round-trips one image through SD1.5 / SDXL / SD3 autoencoders, measures
      PSNR and where the error lives, then contrasts a DINOv2 feature map against an SD latent.
      Executed on A100, 4 embedded figures, 0 errors.
- [x] `editing.ipynb` — SDEdit vs latent masked blending vs IP-Adapter on one image, with
      difference maps showing the strength of each preservation guarantee. Executed, 4 figures.
- [x] `/notebooks` site section with framing, credits and run instructions
- [ ] RAE / Scale-RAE inference notebook — **the one the atlas most needs**. Weights are cached
      (`nyu-visionx--Scale-RAE-Qwen1.5B_DiT2.4B`, `nyu-visionx--siglip2_decoder`) but the pipeline
      is custom, not diffusers, so it needs the Scale-RAE repo code cloned first:
      https://github.com/ZitengWangNYU/Scale-RAE
- [ ] An inversion notebook (RF-Inversion or similar) and a training-free attention method

**Gotchas hit, do not rediscover:**
- SDXL base has only `unet` cached; use `madebyollin/sdxl-vae-fp16-fix` for the SDXL VAE.
- `runwayml/stable-diffusion-inpainting` is not cached; the masked-blend was implemented inline
  instead, which is more instructive anyway.
- NumPy 2 removed `ndarray.ptp()`; use `np.ptp(arr, axis=...)`.
- Notebooks pass `local_files_only=True` so a run never silently downloads.

**Design constraint:** each cell credits the upstream repo it borrows from. This assembles, it does
not reimplement.

---

## Q5 — Vision foundation models and VLM sections
**Status: DONE** (session 7)

Both render empty. The user considers these foundational to any vision task and wants them tracked.

- [x] 19 papers added, all arXiv-verified. VFM section now has 16 papers, VLM 12.
- [x] 6 new lines: self-distillation, contrastive language-image, agglomerative distillation,
      encoder+projector, cross-attention VLM, native-resolution VLM.
- [x] The connection is made explicit throughout: DINOv2 as REPA's alignment target, DINOv2/SigLIP2/
      MAE as RAE's candidate latents, DINOv3 for SVG, SigLIP-2 So400M for Scale-RAE, Qwen2.5-VL as
      both Qwen-Image's text encoder and Step1X-Edit's instruction parser.
- [x] New open problem `which-encoder-for-generation`: REPA and RAE independently rank DINOv2 first,
      but disagree on why. A 27-encoder study (2512.10794) argues patch-level spatial structure
      predicts the gain, not global linear-probe accuracy. Nobody has tested whether Web-SSL's
      language-free scaling advantage transfers to generation at all.
- Note: Fuyu-8B and Llama 3.2 Vision have **no arXiv paper** (model cards only), so they are
  described in line prose rather than given paper entries.

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
