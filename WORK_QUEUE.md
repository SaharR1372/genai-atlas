# WORK QUEUE

Standing task list from user review on 2026-09-10. Worked top to bottom. Each item records what
was done, so a future session can resume mid-item without re-deriving context.

Status key: `TODO` · `IN PROGRESS` · `DONE` · `BLOCKED`

---

## Q1 + Q2 — Written explanations for every paper
**Status: DONE** (session 8)

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
- [x] All 40 papers with `editing` in `sections` and no `explained` block — session 9: bagel-2025,
      fireflow-2024, biomedjourney-2023 (re-verified, already done in session 8), didae-2026,
      emu35-2025, plug-and-play-2022, ip-adapter-2023, mededit-2024 (re-verified, already done in
      session 8), rf-inversion-2024, seedream4-2025, emu-edit-2023, hidream-o1-2026, radedit-2023
      (re-verified, already done in session 8), unispace-2026, krisbench-2025, acepp-2025,
      magicbrush-2023, icebench-2025, omnigen2-2025, kontext-2025, controlnet-2023, refedit-2025,
      imgedit-2025, ominicontrol-2024, pulid-2024, rpiae-2026, editscore-2025, stable-flow-2024,
      instantid-2024, masactrl-2023, icedit-2025, kv-edit-2025, instructpix2pix-2022,
      step1x-edit-2025, pico-banana-2025, prompt-to-prompt-2022, qwen-image-2-2026, rf-solver-2024,
      psvae-2025, risebench-2025. All 40 at `depth: full-text` (none needed to fall back to
      abstract). Every editing-method paper's `method` field states the space the edit happens in
      (VAE latent / pixel / representation latent / discrete tokens / attention-and-feature-only)
      and what, if anything, protects unedited regions. See CHANGELOG's session 9 entry for the
      cross-paper findings (PS-VAE/RPiAE encoder-unfreezing confirmed, RISEBench version conflict,
      ACE++ has no quantitative benchmark, HiDream-O1's stale 512px claim, Emu-Edit's mixed
      mask/no-mask protection).
- [x] All 38 papers whose first `sections` entry is `unified`, `vfm`, `vlm`, or `rae`, and no
      `explained` block — session 10: transfusion-2024, chameleon-2024, emu35-2025, janus-pro-2025,
      bagel-2025, emu3-2024, janus-2024, showo2-2025, omnigen2-2025, unieval-2025 (unified);
      dinov3-2025, siglip-2023, ijepa-2023, perception-encoder-2025, registers-2023, radio-2023,
      aimv2-2024, radiov25-2024, webssl-2025, vjepa2-2025, cradiov4-2026 (vfm); flamingo-2022,
      llava-2023, qwen2vl-2024, qwen25vl-2025, internvl3-2025, llava-onevision-2024, qwen3vl-2025
      (vlm); reg-2025, blip3o-2025, emu2-2024, metaquery-2025, repa-spatial-2025,
      distilling-rae-2026, drae-2026, gigatok-2025, vfmvae-2025, tokenizer-post-training-2025
      (rae). All 38 at `depth: full-text`. Scope computed strictly from each file's own `sections:`
      first entry (not a grep for the section name) to avoid collision with the concurrent
      generation/editing/medical sessions. See CHANGELOG's session 10 entry for what's-actually-
      unified per paper, VFM generative-use findings, VLM fusion mechanisms, RAE frozen/trained
      encoder status, and a flagged YAML-authoring gotcha (mid-sentence colon-space breaks the
      parser in several files outside this session's scope).
- [ ] Remaining landmark + core papers outside the editing/medical/unified/vfm/vlm/rae subsets
      (validator warns on each; run `scripts/validate.py` for the current count — as of session 10
      only `genfirst-2026` (abstract-depth) and `pinaya-2022` remain among landmark/core warnings,
      both first-section `generation`/`medical` respectively and outside every session's scope so far)
- [ ] Strong-followup and emerging papers outside the editing/medical/unified/vfm/vlm/rae subsets

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
**Status: DONE** (4 built, session 8)

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
- [x] `rae.ipynb` — the official RAE implementation cloned to `external/RAE`, three released
      decoders (DINOv2, SigLIP2, MAE) run against SD's VAE on one image. **Gotcha worth keeping:**
      RAE's encoder normalizes with an image-processor mean and std, so it expects [0,1] input, not
      diffusers' [-1,1]. The wrong convention costs about 8 dB and looks like a broken model.
      Result: three metrics, three different winners.
- [x] `guidance.ipynb` — one frozen model, one prompt, one seed, guidance scale swept. CLIP-measured
      prompt adherence spans 0.125 and peaks in the middle. This is the runnable argument for why
      `/compare` refuses to publish a leaderboard.
- [ ] Optional future: stage-2 RAE generation (weights are in the same collection under `DiTs/`),
      an inversion method, a training-free attention method.

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
**Status: DONE** (session 8)

All checked against vendor primary sources. Results in `docs/refuted-claims.md`.

- **Refuted**: Qwen-Image-3.0 does not exist. Microsoft's current model is MAI-Image-2.5, not 2.6.
  Stability's most recent image model is still SD 3.5, not SD4.
- **Partly refuted**: FLUX 3 was announced 2026-07-23, but only its video model is in early access,
  the vendor's own docs still direct image work to FLUX.2, and no FLUX 3 repo exists in their
  Hugging Face org. Recorded on the FLUX system entity as announced rather than released.
- **Confirmed and added** as `system` entities: GPT-Image 2.5 (two model ids, API only),
  Gemini's image-lite model (id confirmed, release date not), Krea 2 (open weights under a gated
  community licence).
- **Reclassified**: Kroma v0.2 is a community fine-tune of Krea 2 by an independent user, not a
  vendor base model, so it does not get a peer entry.

---

## Standing instructions
- Compact context around 90% and keep this file current, so work stays traceable across sessions.
- After each meaningful unit: update this file, `PROJECT_STATE.md`, and `CHANGELOG.md`.
- No explanatory claim without a fetched source (D004).

---

## Q7 — Run the open models and report how they actually perform
**Status: IN PROGRESS** (session 9)

User asked to run the newly-verified open models. First correction: of the six items they named,
**none were blocked by authentication**. Three do not exist (`Qwen/Qwen-Image-3.0`,
`black-forest-labs/FLUX.3-dev`, `stabilityai/stable-diffusion-4` all return repository-not-found),
and two are closed vendor APIs that were never on the Hub. A token unlocks only gated models, of
which Krea 2 is the one on our list.

**Chosen for this pass:** Qwen-Image, LLaDA-Image-Turbo, HiDream-O1-Image-Dev. Krea 2 and the rest
deferred to a later pass at the user's request.

### Download status
- [x] `HiDream-ai/HiDream-O1-Image-Dev` 35GB, 139s
- [x] `inclusionAI/LLaDA-Image-Turbo` 49GB, 366s
- [ ] `Qwen/Qwen-Image` 58GB, in progress

### Environment findings, do not rediscover
- **Qwen-Image needs nothing special.** `diffusers` 0.36 in the `dediffusion` env already exposes
  `QwenImagePipeline` and `QwenImageEditPipeline`.
- **HiDream-O1 needs `transformers==4.57.1`**, but `dediffusion` has 5.2.0 and downgrading would
  break the other four notebooks. Building an isolated env at `external/hidream-env` instead. Its
  architecture is `Qwen3VLForConditionalGeneration`, and its own README warns PyTorch 2.9.x is not
  recommended. Code: `external/HiDream-O1-Image` (`inference.py`, `--model_type dev` for the
  distilled weights).
- **LLaDA-Image-Turbo** ships a diffusers-style `model_index.json` but with custom classes
  (`LLaDAImageQueryFormerModel`, `LLaDAImageSigVQModel`, `LLaDAImageTextProjectionModel`) that need
  `external/LLaDA-Image`. Worth noting for the atlas: it has a `vae/` component, which confirms the
  entry filing it under the VAE-latent line.
- `python -m venv` fails on this machine (ensurepip returns non-zero); use `conda create -p` instead.

### Confirmed against the model card
HiDream-O1's own card states it is a "Pixel-level Unified Transformer (UiT) without external VAEs or
disjoint text encoders, which natively encodes raw pixels, text, and task-specific conditions in a
single shared token space." That matches what the atlas already claims about it, from an independent
source.

### Next
- [ ] Generate from all three on identical prompts and seeds, and record what each is actually good at
- [ ] A comparison notebook, and results folded into `/models` and `/compare`

---

## Q8 — explanations for the 42 papers added by the coverage audit (2026-09-10, IN PROGRESS)

Session 11 added 42 verified papers. Ten now carry full-text `explained` blocks. **32 still have
only a `summary`.** The Sonnet subagent fan-out that was writing them hit the account's session rate
limit mid-flight and four of five batches were lost; the JSON handoff files they were told to write
are the recovery point, and only `explained_guidance.json` survived.

Already done (do not redo): cfg-2022, autoguidance-2024, guidance-interval-2024, cfgpp-2024,
apg-2024, ssg-2026, registers-pixel-2026, mosaik-2026, pixel-ar-pra-2026, pixel-survey-2026.

Still needed, grouped as the batches were:
- **flows/TM**: tarflow-2024, starflow2-2026, tm-demystify-2025, tm-design-space-2025,
  tm-distill-2026, givt-2023, fluid-2024
- **VLM/agentic/VFM**: blip2-2023, otter-2023, nvlm-2024, re-imagen-2022, idea2img-2023,
  genartist-2024, unic-2024, theia-2024
- **pixel single-stage**: pixnerd-2025, pixeldit-2026, dip-2026, hyperdit-2026, no-vae-2025,
  pixelrepa-2026, pixsgr-2026, obsop-2026, pixel-t2i-empirical-2026
- **cascaded/hybrid**: cdm-2021, simple-diffusion-2023, sid2-2024, hdit-2024, edify-image-2024,
  pixelflow-2025, latent-forcing-2026, crossflow-2026

Method that worked: one subagent per batch, each fetching `arxiv.org/html/<id>v1` for full text,
writing a single JSON file of `{paper_id: {before, problem, idea, method, evidence, limitations,
why_it_matters, depth}}` into the scratchpad rather than editing YAML directly (concurrent YAML
writes have corrupted files in this project before), then the parent applies it. Instruct every
agent to report guidance scale AND interval alongside every FID, since this atlas treats those as
first-class confounds.

Questions to put to the sources while doing this, still unanswered:
- Does PixNerd's own framing support the atlas's new priority claim that it, not JiT, is this line's
  technical origin? The atlas is asserting this and has not yet verified it against PixNerd's text.
- Does PixelREPA really find REPA *hurts* JiT, and with what before/after numbers?
- Is calling `no-vae-2025` tokenizer-free fair, given it keeps a self-supervised pretrained encoder?
- Does SiD2 position its ImageNet-512 FID 1.5 against latent diffusion, and at what guidance/params?
- Is Fluid's claim really that continuous beats discrete *as scale grows*, and random vs raster order?

## Q9 — medical thin lines (2026-09-10, NOT STARTED)

The audit agent for this was killed by the same rate limit before returning anything.
`line-medical-counterfactual` holds exactly one paper, from 2020, on a line marked `ascendant` — the
validator now flags it as 75 months stale. The project blueprint itself named "Ribeiro 2023" and
"diffusion counterfactuals" as expected follow-ups that were never added, so this is near-certainly a
gap. `line-medical-fm-latent` has two papers, both 2026, both Oxford; that one may genuinely be
that small, and recording an honest "nobody else has done this" is an acceptable outcome.
Use the PubMed MCP tools, not just arXiv.

