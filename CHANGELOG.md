# CHANGELOG

## Unreleased

### 2026-09-11 — Session 11 continued — the medical audit, and a warning that was right for the wrong reason

**`line-medical-counterfactual` was a gap, and the field's own evidence points against the line's
bet.** The line held one paper, from 2020. Eight added, five from arXiv and three journal-only
verified through PubMed. The project blueprint had named "Ribeiro 2023" and "diffusion
counterfactuals" as expected follow-ups and never added them; both are now in, as
[Ribeiro et al. ICML 2023](https://doi.org/10.48550/arXiv.2306.15764) and Diff-SCM (CLeaR 2022).

The genuinely interesting finding is not the count. This line bets that a medically meaningful
counterfactual *requires* explicit causal machinery. The strongest clinical evidence in the area
comes from work that uses none:
- **Singla et al. (Medical Image Analysis 2022)** — a GAN counterfactual explainer with no structural
  causal model, and the only paper here validated by a reader study with diagnostic radiology
  residents. Counterfactual explanation was the only style that significantly improved their
  understanding of the classifier over no explanation.
- **DiffChest (Cell Reports Medicine 2024)** — a self-conditioned diffusion model, no causal graph,
  515,704 radiographs from 194,956 patients across the US and Europe, Fleiss' kappa at or above 0.8.
- **StylEx (EBioMedicine 2024)** — states outright that it is not designed to infer causality, then
  produces expert-panel-validated counterfactual attribute discovery across eight tasks in three
  modalities.

The causal papers are evaluated on axioms; the non-causal ones on clinicians. That asymmetry is now
recorded as the line's central unresolved problem rather than left implicit, and the three papers
above carry the `challenge` role in its arc.

**`line-medical-fm-latent` is genuinely small, and the warning that found it was right for the wrong
reason.** The single-org warning fired claiming every paper was from Oxford. It is not: STREAM's
authors are at **DEEPNOID Inc.**, a Korean medical-AI company, and the warning fired only because
that paper's `orgs` field was empty. The `orgs` are corrected. Deliberate searches across arXiv and
PubMed found no third group generating inside a medical foundation model's own representation space,
so the line now records honestly that it is two papers from two unrelated groups — one UK academic,
one Korean industry — who arrived at the same idea independently, and that no third exists yet.
That is the outcome the thin-line warning was built to make possible: it asks a question, and
"genuinely small" is an allowed answer as long as the line says so in its own text.

**Worth carrying forward:** an empty `orgs` field made a coverage warning misfire into a false claim
about a research group. Data gaps do not stay inert; they get rendered as assertions.

### 2026-09-11 — Session 11 continued — explanations, four corrections, one silent bug

**39 of the 42 audit papers now carry full-text `explained` blocks**, each reporting guidance scale
and interval alongside every FID, because this atlas treats those as confounds rather than footnotes.
Three remain (Q8).

**Four claims of the atlas's own were corrected by the full-text reads.** This is the same failure
mode as session 8's seven unsupported claims, and it is worth recording that it recurs whenever the
atlas writes from a summary rather than a source:
- **SiD2** was recorded as matching or beating latent diffusion at ImageNet 512. It does not. Its
  1.48 sits behind EDM2-XXL's 1.40 in the paper's own matched-setting table, and the authors concede
  latent diffusion scales slightly better. The rediscovery argument survives on the corrected number.
- **simple diffusion** was recorded as arguing cascades are unnecessary. It argues that one
  end-to-end model can be *comparable* to cascades and to latent diffusion, and does not refute
  cascades on their own terms.
- **Fluid** was recorded as finding continuous tokens beat discrete ones *as models grow*. It claims
  only that continuous wins at every scale tested, and reports GenEval plateauing from 3.1B to 10.5B
  while FID keeps improving.
- **Re-Imagen** was recorded as the origin of "generation failures are knowledge failures". Its own
  framing is narrower: rare and long-tail *entity* memorisation. The atlas now marks its own broader
  reading as an extrapolation rather than the paper's thesis.
- Also noted: **Edify Image** reports no FID or quantitative benchmark at all, so it cannot be placed
  against the numbers on its line. **Demystifying Transition Matching** was confirmed genuinely
  independent of Meta FAIR (KAIST and AWS authors), which is why it carries weight as external
  validation. **Transition Matching Distillation** claims only its narrow video result, not a general
  validation of the paradigm, and its own ablation shows plain TM pretraining nearly matching the
  full objective.

**A silent rendering bug, found while adding prose and older than this session.** Astro's glob loader
keys a content entry by its *filename*, not by the `id` in its frontmatter, and `getEntry()` returns
nothing on a miss rather than failing the build. `content/lines/representation-latent.mdx` — the RAE
deep dive, the centrepiece of this atlas and the user's own research area — has therefore been
written but never rendered on the site. No error, no warning, just a page missing its argument.
Renamed to match its id, and `validate.py` now treats a filename/id mismatch as an **error** rather
than a warning, with a test.

**Two research lines gained narrative prose**, bringing the total from two to four of thirty-four.
`/lines/line-pixel-space` now explains the three-way split, carries an explicit section on why its
nine ImageNet FIDs between 1.51 and 2.15 cannot be read as a ranking, and ends with the atlas
admitting in public that its previous "mostly from one group" claim was its own gap.
`/lines/line-cascaded-pixel` makes the rediscovery argument, including why the citation graph does
not connect these papers to the current wave: the connection is in the claim, not the references.

### 2026-09-10 — Session 11 (Opus 5) — coverage audit: the atlas was wrong about pixel space

Triggered by the user noticing the pixel-space section held only two papers. It did, and that was a
failure of the atlas, not a fact about the field. Two independent audits were run, one over every
research line with a thin arc, one over pixel-space specifically. **All seven thin lines turned out
to be atlas gaps. None was genuinely small.** 42 verified papers added, every one fetched from arXiv
with its recorded title checked against the fetched title before it entered `data/`.

**The pixel-space finding is a taxonomy correction, not just missing papers.**
- What the atlas called one line is three separate bets. `line-pixel-space` is now *single-stage
  pixel transformers* (tokenizer-free, one stage, large patches). A new `line-cascaded-pixel` holds
  the older *cascaded and multiscale* bet — CDM 2021, simple diffusion 2023, HDiT 2024, SiD2 2024,
  Edify Image 2024, PixelFlow 2025 — which is a different claim (resolution was the problem, not
  pixels) with a different origin and a five-year head start. Latent Forcing and CrossFlow went to
  `line-latent-hybrid` as the explicit counter-position: the latent as computational scratchpad
  rather than as the generative space.
- **The line's stated origin was wrong.** PixNerd (2507.23268, July 2025) predates JiT (November
  2025) by four months and reaches the same conclusion independently. JiT is now recorded as an
  origin for the argument the field actually heard, not as the first to make it.
- **SiD2 reached FID 1.48 on ImageNet 512 in pixel space in October 2024**, a year before the
  tokenizer-free wave argued the case. Stated carefully after a full-text check: it is *not* the
  parity result it is often cited as. In the paper's own matched table EDM2-XXL with a guidance
  interval reaches 1.40, and the authors concede latent diffusion still scales slightly better. What
  survives is still strong — pixel space was within 0.08 FID of the best latent model a year early,
  and nothing on the single-stage line has beaten 1.48 at 512 since.
- The line's own `weaknesses` field claimed pixel-space results were "mostly from one group". That
  was the atlas's coverage gap asserted as a property of the field. Verified affiliations now show
  at least a dozen groups: NVIDIA, Google DeepMind, Yandex Research, Alibaba (AMAP and Token Hub),
  Tencent Youtu, KAIST, NTU Singapore, UESTC, Nanjing University, NUS, Peking University, HKU,
  Stability AI, Stanford, Caltech, and the ByteDance Seed authors on PixNerd.
- The `weaknesses` field is rewritten to the objections that actually survive: attention cost still
  scales badly with resolution, nearly every headline number is class-conditional ImageNet, PixelDiT
  itself concedes no mature training recipe exists for pixel noise distributions, and the two lowest
  FIDs are single-version preprints from authors who overlap.

**The most severe gap was elsewhere: `line-guidance-sampling` had no classifier-free guidance.**
A line whose entire subject is inference-time technique was missing the paper that created the
technique. Added CFG (Ho & Salimans 2207.12598), autoguidance, guidance interval, CFG++ and APG, so
the arc now runs from the origin rather than starting mid-history.

**Other lines repaired:** normalizing flows was missing TarFlow, the paper STARFlow scales — the
line began at the scale-up, not the origin. Continuous tokens was missing Fluid, the direct
large-scale test of MAR's own bet, and GIVT, which drops the codebook a different way and predates
MAR. Cross-attention VLM was missing BLIP-2. Agentic generation appeared to begin in 2026 and
actually begins with Re-Imagen in 2022. Agglomerative distillation looked like one company's idea
until UNIC (NAVER) and Theia (Boston Dynamics AI Institute) were added.

**Method note.** Affiliations were taken only from author blocks actually read in fetched HTML.
HyperDiT and Observation Operators are left with empty `orgs` because their affiliation blocks are
not legible in any fetchable rendering; the atlas prints nothing rather than an inference. Four
papers had been recorded under short titles that turned out to be truncations of the real ones, all
corrected against the fetched title.

**Systemic fix carried forward from the previous session.** `scripts/validate.py` now warns when a
line's arc holds two or fewer papers, or when every paper in a line shares one organization. Both
warnings fired on the lines this session repaired, which is what makes this a check rather than a
one-off cleanup. Where the warning is a true fact about the field rather than a gap — the
normalizing-flows line really is all Apple — the line's own text now says so.

### 2026-09-10 — Session 8 (Opus 5) — the standing queue completed
- **Every paper is now explained** (Q1/Q2). All 154 carry the structured account: before, problem,
  idea, method, evidence, limitations, why it matters. 152 written from full text; two remain at
  abstract depth because no HTML render exists, and the validator still flags those two by design.
- **Four runnable notebooks** (Q4), all executed on an A100 with outputs committed: the latent
  round-trip, the editing-mechanism comparison, the RAE-against-VAE comparison using the official
  implementation, and a guidance sweep that is the runnable argument for why `/compare` refuses to
  publish a leaderboard.
- **Vendor claims resolved** (Q6) against primary sources, recorded in `docs/refuted-claims.md`.
  Three refuted outright, one partly, three confirmed and added as system entities.
- **Seven unsupported claims removed or corrected**, all caught by reading full text rather than
  trusting summaries. The atlas had been asserting a 62x speedup absent from its paper, describing a
  MNIST-only result as a methodological advance in image generation, calling a hybrid model
  autoregressive, understating a model's training resolution, misquoting a benchmark's top score and
  the model that set it, calling a paper widely reused when it reports no numbers, and repeating an
  unconfirmable oral acceptance.
- **One misclassification fixed**: MedEdit was under the borrowed-VAE line but is pixel-space.
- 296 entities, 252 pages, 28 tests, validation clean.

### 2026-09-10 — Session 10 (Sonnet 5) — WORK_QUEUE Q1/Q2, all 38 unified/VFM/VLM/RAE papers explained
- **Every paper with first `sections` entry `unified`, `vfm`, `vlm`, or `rae` and no `explained`
  block now has one**, all 38 at `depth: full-text` (no abstract fallbacks needed). Scope computed
  by reading each file's actual `sections:` list, first entry only, to avoid collision with the
  concurrent sessions working the `generation`-first, `editing`-first, and `medical`-first papers.
  Fanned out across 7 parallel subagents by section/tier: unified landmark+core (transfusion-2024,
  chameleon-2024, emu35-2025, janus-pro-2025, bagel-2025, emu3-2024, janus-2024, showo2-2025,
  omnigen2-2025) + strong-followup (unieval-2025); VFM core (dinov3-2025, siglip-2023, ijepa-2023,
  perception-encoder-2025, registers-2023, radio-2023) + strong-followup/emerging (aimv2-2024,
  radiov25-2024, webssl-2025, vjepa2-2025, cradiov4-2026); VLM landmark+core+emerging
  (flamingo-2022, llava-2023, qwen2vl-2024, qwen25vl-2025, internvl3-2025, llava-onevision-2024,
  qwen3vl-2025); RAE core (reg-2025, blip3o-2025, emu2-2024, metaquery-2025, repa-spatial-2025) +
  strong-followup/emerging (distilling-rae-2026, drae-2026, gigatok-2025, vfmvae-2025,
  tokenizer-post-training-2025). Each subagent fetched `arxiv.org/html/<id>v1` (v3 for bagel-2025,
  since v1/v2 both 404'd) and wrote directly into `data/papers/*.yaml`. `scripts/validate.py`
  clean, 0 errors, after every file.
- **Unified-model `method` fields state precisely what is shared vs. separate**, per the task's
  organizing axis: Chameleon and Emu3 are genuinely one vocabulary/one loss/one backbone with no
  diffusion component; Transfusion is one backbone with two losses (CE + diffusion MSE) summed;
  Janus and Janus-Pro explicitly decouple the visual encoder (continuous for understanding, discrete
  VQ for generation) into one shared autoregressive backbone; Show-o2 fuses SigLIP-distilled and
  VAE-latent paths into one backbone with two loss heads (CE + flow matching); BAGEL is a genuine
  mixture-of-transformer-experts (separate FFN params per modality, shared self-attention only);
  OmniGen2 is the most decoupled — a frozen MLLM glued to a separately trained diffusion transformer
  via hidden-state conditioning, so understanding cannot degrade by construction. Generation-degrades-
  understanding was explicitly reported (and quantified) for Transfusion and BAGEL; explicitly denied
  by Emu3, Janus-Pro, and Chameleon's own framing. UniEval (a benchmark, not a model) supplies direct
  evidence of the tension: Show-o ranks 1st in generation-only scoring but drops to 7th when graded by
  its own understanding half, from an 89.2% single-answer bias.
- **VFM `method` fields state supervision type and generative use, or explicitly say there is
  none.** None of the 11 VFM papers done this session (DINOv3, SigLIP, I-JEPA, Perception Encoder,
  Registers, RADIO, AIMv2, RADIOv2.5, Web-SSL, V-JEPA2, C-RADIOv4) discuss feeding their own features
  to a generative model — that connection is made only by later papers (REPA, RAE, Scale-RAE) citing
  these as candidate encoders, not by these papers themselves. V-JEPA2 explicitly argues against
  generative pixel-prediction objectives, beating a Cosmos latent-diffusion-7B baseline on robot
  planning with a discriminative JEPA-style predictor instead. I-JEPA's existing `summary` field
  claiming it "was tested as a REPA target and found weaker than DINOv2" is confirmed to be an
  external (REPA-paper) finding, not something I-JEPA's own paper states — flagged explicitly in its
  `why_it_matters` field so the entry doesn't misattribute the claim.
- **VLM `method` fields state the fusion mechanism and frozen/trained LLM status.** Flamingo uses
  gated cross-attention with both vision encoder and LM fully frozen; LLaVA and every Qwen-VL
  generation use a linear/MLP projector into the token stream, with the LLM frozen only in early
  alignment stages then trained; InternVL3 is distinctive in training vision encoder and LLM jointly
  from the start with nothing frozen; Qwen3-VL adds DeepStack, injecting intermediate ViT-layer
  features into the first three LLM layers. Qwen2.5-VL and Qwen3-VL's roles as text encoder /
  instruction parser for generation systems (Qwen-Image, Step1X-Edit) are atlas-level claims from
  other papers, not claims either VLM paper makes about itself — kept distinct in `why_it_matters`.
- **RAE `method` fields state encoder/tokenizer and frozen-vs-trained status per paper.** MetaQuery's
  query-bridge (64-512 learnable queries through a fully frozen MLLM, only queries+connector+decoder
  trained) and BLIP3-o/Emu2's diffusion-on-CLIP-embedding approach are now precisely distinguished
  from REG (DINOv2 class token concatenated onto an ordinary VAE latent, not a replacement encoder)
  and from GigaTok/VFM-VAE (own trained tokenizers, not frozen-foundation-model RAE). repa-spatial-
  2025's 27-encoder study is confirmed: patch-level spatial structure (|r|>0.85 with FID) predicts
  REPA gains, global linear-probe accuracy does not (|r|=0.26) — flagged as in tension with BLIP3-o/
  Emu2's choice of CLIP-family embeddings (weaker on spatial structure) for generation, though no
  paper addresses this tension directly. distilling-rae-2026 reconfirmed as operating in frozen RAE
  latent space, adapting the Drifting Models one-step objective (with the auxiliary MAE dropped) to
  RAE's anisotropic geometry, closer to "distilling a flow-matching teacher via the Drifting
  objective" than a literal distillation of a separate model class.
- One recurring YAML authoring trap flagged by subagents but left unfixed in files outside this
  session's scope (their content, not their fault): a plain unquoted scalar containing a mid-sentence
  colon-plus-space breaks the YAML parser. Pre-existing instances noted in bagel-2025 (later fixed by
  this session's own edit), chung-ye-2021, ip-adapter-2023, kontext-2025, ominicontrol-2024,
  retinal-fm-latent-2026, editscore-2025 — worth a validator lint rule.
- `WORK_QUEUE.md` Q1/Q2 and `PROJECT_STATE.md` updated to record this batch.

### 2026-09-10 — Session 9 (Sonnet 5) — WORK_QUEUE Q1/Q2, all 40 editing papers explained
- **Every paper with `editing` in `sections` and no `explained` block now has one**, all at `depth:
  full-text` (none fell back to abstract). Scope was computed by loading each `sections` list
  directly, not by grepping for the word "editing" in the file (that over-matches: it would have
  pulled in var-2024, qwen-image-2025, metaquery-2025, qwen25vl-2025, t2i-adapter-2023,
  nextstep1-2025, hidream-2025 and agentic-visual-generation-2026, none of which actually carry
  `editing` in their `sections` field). 40 papers done: bagel-2025, fireflow-2024,
  biomedjourney-2023, didae-2026, emu35-2025, plug-and-play-2022, ip-adapter-2023, mededit-2024,
  rf-inversion-2024, seedream4-2025, emu-edit-2023, hidream-o1-2026, radedit-2023, unispace-2026,
  krisbench-2025, acepp-2025, magicbrush-2023, icebench-2025, omnigen2-2025, kontext-2025,
  controlnet-2023, refedit-2025, imgedit-2025, ominicontrol-2024, pulid-2024, rpiae-2026,
  editscore-2025, stable-flow-2024, instantid-2024, masactrl-2023, icedit-2025, kv-edit-2025,
  instructpix2pix-2022, step1x-edit-2025, pico-banana-2025, prompt-to-prompt-2022,
  qwen-image-2-2026, rf-solver-2024, psvae-2025, risebench-2025. (biomedjourney-2023,
  mededit-2024, radedit-2023 were already written in session 8's medical pass and were only
  re-verified, not rewritten.) Fanned out across 8 parallel subagents in 3 waves (landmark, core,
  strong-followup/emerging), each fetching `arxiv.org/html/<id>vN` and writing directly into
  `data/papers/*.yaml`.
- **Every editing-method paper's `method` field now states two things explicitly**, per the task's
  organizing axis for the whole editing section: which space the edit happens in (VAE latent /
  pixel / a representation-model latent / discrete tokens / attention-and-feature-space only with
  no new latent written), and what mechanism, if any, protects regions the user did not ask to
  change (mask, attention/KV injection, latent blending, locality loss, or explicitly none — several
  papers, e.g. InstructPix2Pix, IP-Adapter, ControlNet, HiDream-O1, PS-VAE, Step1X-Edit, have no
  inference-time protection mechanism at all and rely on learned behavior alone). Benchmark/dataset
  papers in scope (krisbench-2025, icebench-2025, risebench-2025, magicbrush-2023, pico-banana-2025)
  were written as dataset/evaluation contributions instead of being forced into that framing.
- **PS-VAE/RPiAE frozen-encoder claim reconfirmed with exact quotes.** PS-VAE's fetched text states
  directly: "we unfreeze the representation encoder during pixel decoder training... By removing the
  detach operation ... we enable gradients to propagate from the pixel decoder back to the encoder,"
  with a semantic-reconstruction loss keeping it anchored. RPiAE's Stage 1 similarly trains the
  encoder end-to-end, using a frozen "Pivot Replica Encoder" only as a regularization anchor via an
  L2 pivot loss, not as the generative encoder itself. Both confirm the prior session's finding that
  a frozen encoder degrades editing fidelity and both fix it by unfreezing.
- **Version conflict found in RISEBench.** The atlas's stored `abstract` (matching the paper's
  original release) reports the best model, GPT-4o-Image, at 28.8% accuracy. The fetched arXiv v2
  HTML full text instead names the top model "GPT-4o-Native" at 35.9% accuracy, Gemini-2-Flash
  second at 10.9%. Both versions agree qualitatively (best model well under 50%). Documented inside
  `explained.evidence` rather than silently resolved; the stored `abstract`/`summary` fields were
  left untouched per the task's file-preservation rule.
- **ACE++ (acepp-2025) reports no quantitative benchmark numbers anywhere in the fetched paper**,
  only qualitative visualizations — worth noting since the existing `summary` field calls it "widely
  reused," a plausible but paper-unevidenced claim.
- **Stale claim found in hidream-o1-2026's existing `summary`**: it states the model is "so far
  trained only at 512x512," but the fetched paper describes three training stages at
  512-&gt;1024-&gt;2048 resolution with results reported up to 2048x2048. Not corrected (out of this
  task's scope, which only adds `explained`), flagged here for a future session.
- Emu-Edit's protection mechanism turned out to be task-dependent rather than uniform: a DINO-derived
  mask blends edited/original latents for region-based tasks, free-form and global edits have no
  locality constraint at all, and multi-turn edits use pixel-thresholding (alpha=0.03) instead.
- `scripts/validate.py` clean (0 errors, 2 pre-existing unrelated warnings: genfirst-2026 and
  pinaya-2022, both outside this task's scope) after every edit. Only `data/papers/*.yaml` touched.
  Several other concurrent sessions were editing unrelated `data/papers/*.yaml` files throughout
  this session (visible via `git status`); none of that was touched, stashed, or reset.

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
