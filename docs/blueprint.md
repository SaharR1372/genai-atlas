# Generative Vision Atlas — Project Blueprint (v0)

## Context

You want a living research website + GitHub knowledge base for modern generative vision (2023–2026), organized around ideas rather than papers, with a research graph, a 3-day update pipeline, and persistent project state so any future session can resume with zero chat context. This document is the blueprint only. Nothing is built yet. The directory currently contains only `request.md`.

Two honesty notes that shape the plan:

- My training knowledge ends around June 2026. You cite LLaDA-Image (arXiv 2609.03796, Sept 2026) and RAE follow-ups on latent distributions and transport paths that I may not know. Every entry in this blueprint marked **(verify)** must be fetched and checked before it enters the atlas. Sprint 1 includes a "frontier recon" step for Jan–Sep 2026.
- Fable 5.1 is the most capable model available to you. Opus 5 is a tier below it, and Sonnet 5 / Haiku 4.5 are cheaper still. Your "switch to Opus for hard tasks" instruction therefore maps to: **use Fable (or Opus as the cheaper heavy option) for the hard tasks; Sonnet for routine coding and drafting; Haiku for pipeline filters.** Details in section 9.

---

## 1. Scope

### In scope (deep coverage)
- Image generation 2023–2026: latent diffusion → DiT → flow matching → modern T2I systems; AR and discrete-token generation; masked/discrete diffusion; few-step/one-step alternatives; guidance; alignment (DPO/GRPO); text-encoder evolution.
- **Representation-space generation (the RAE line)** — the deepest section: VAE-latent limitations, foundation representations, REPA → VA-VAE → REPA-E → RAE → SVG/JiT debate, latent dimension/geometry, priors, transport paths, decoders, conditioning, scaling.
- Image editing 2023–2026: instruction, reference/subject, structural control, inversion for flow models, attention manipulation in DiT/MMDiT, training-free vs trained, in-context editing (Kontext/Qwen-Image-Edit/FLUX.2), native editing in unified models, editing benchmarks and RL for editing. Includes the explicit investigation: *is RAE / foundation-representation editing underexplored?*
- Unified understanding + generation: Chameleon, Transfusion, Show-o, Janus, Emu2/3/3.5, BAGEL, MetaQuery/BLIP3-o, OmniGen2, HunyuanImage 3.0, Qwen-Image family, MMaDA/Muddit/LLaDA-Image, closed systems (GPT-4o image, Nano Banana). For each: *what is actually unified*.
- Vision foundation models **as they matter for generation**: DINOv2/v3, SigLIP2, MAE, JEPA, Perception Encoder, Web-SSL, unified tokenizers, SAM/Depth Anything as control sources.
- VLM architecture families — **brief**, only as needed to understand unified models (encoder+projector, cross-attention, early fusion, native-resolution).
- Medical generative imaging — separate section, evidence-first: synthesis, reconstruction, modality translation, editing/counterfactuals, pathology, multimodal medical models, synthetic data, evaluation beyond FID/SSIM.

### Brief background only (one concept page each, linked, never expanded)
GANs; early VAE/VQ-VAE/VQGAN; DDPM/score matching; classifier-free guidance; DALL-E 2 / unCLIP prior (kept because it is the ancestor of CLIP-feature generation); CLIP; MAE; MaskGIT; Parti; Textual Inversion/DreamBooth; SDEdit/Prompt-to-Prompt/Null-text inversion (ancestors of modern editing).

### Out of scope (cross-reference only)
Video generation (Wan, Veo, Sora, HunyuanVideo, etc. get a single "video" pointer node when a method matters, e.g. V-JEPA 2 or 3D-VAEs); 3D/NeRF/Gaussian splatting; audio; pure LLM/NLP diffusion beyond what LLaDA/MDLM contribute to masked image diffusion; safety/watermarking; hardware/serving.

**Decision D005**: images only; video is a pointer, not a section. Revisit in a later phase if the unified-model story forces it (Emu3.5, Show-o2 already touch video).

---

## 2. Taxonomy (challenging yours)

Your proposal: representations · generative objectives · architectures · conditioning · capabilities · transitions.

**What is right**: the first four are true *design axes* — every modern system is a point in that space, and the field moves when one axis becomes the binding constraint. Keep them.

**What is wrong or missing**:
1. "Capabilities" and "transitions" are different *kinds* of thing from the four design axes. Capabilities are what the system is *for*; transitions are *history*. Mixing them into one flat list produces a muddled site.
2. Two design axes are missing, and they explain a large share of 2024–2026 progress:
   - **Training signal** — data curation, synthetic captioning, interleaved data, reward models, DPO/GRPO alignment, distillation targets. Seedream, Qwen-Image, FLUX.2, BAGEL differ from each other mostly here.
   - **Inference** — sampling steps, guidance (CFG, autoguidance, guidance interval), distillation (DMD, LADD), timestep shift. This axis is *why flow matching won*.
3. **Evaluation** is not a design axis but must be first-class, because your medical section explicitly demands "evidence, not FID", and the editing section is currently being reshaped by benchmarks (GEdit-Bench, ImgEdit, RISEBench).

### Proposed three-layer taxonomy

**Layer A — Design axes (6).** The atlas's coordinate system. Each axis is a page listing its *options* as concept nodes, the arguments between options, and the systems that made each choice.

| Axis | Options (concept nodes) |
|---|---|
| Representation | pixels · VAE latent (KL-f8, 16ch) · deep-compression latent (DC-AE) · discrete VQ tokens · multi-scale tokens (VAR) · continuous tokens (MAR/Fluid) · semantic/foundation latent (RAE, SVG) · hybrid semantic+detail · unified tokenizers (TokenFlow/UniTok/DualViTok) |
| Objective | ε/v/x0-prediction diffusion · flow matching / rectified flow · consistency / MeanFlow / shortcut · next-token AR · next-scale AR · masked/discrete diffusion · diffusion-loss AR (MAR) · mixed (Transfusion) |
| Architecture | UNet · DiT · MMDiT (dual-stream) · single-stream DiT · LLM-decoder-as-generator · Mixture-of-Transformers · frozen-MLLM + diffusion head · diffusion decoder on top of AR |
| Conditioning & control | cross-attention · joint attention · in-context / sequence concat (Kontext, OminiControl) · adapters (ControlNet, IP-Adapter) · learnable queries (MetaQuery) · text-encoder lineage (CLIP → T5 → LLM/VLM) |
| Training signal | curated/synthetic captions · interleaved data · reward models (ImageReward, HPS, EditScore) · Diffusion-DPO · Flow-GRPO/DanceGRPO · distillation · representation alignment (REPA) |
| Inference | steps/schedules · timestep shift · CFG and variants · autoguidance · few-step distillation · KV-cache editing |

**Layer B — Sections (7).** Your seven areas, each with a subtle color identity. These are *capability domains* that cut across the axes. The RAE section is a deep-dive told as problem → idea → method → evidence → limitation → next.

**Layer C — Evolution.** Transitions (why the field moved), Open Problems (where it is going), Timeline Graph (how branches converge). Each transition page is a narrative with a mini-graph and a "what did this replace / what did it cost" table.

**Eras (used only as a timeline backdrop, not as taxonomy)**: 2022–23 latent-UNet era · 2024 DiT + flow era · 2025 in-context / unified / RL era · 2026 representation + reasoning era (verify how 2026 actually shaped up).

**Decision D001**: adopt the three-layer taxonomy (axes / sections / evolution). Record the reasoning in `docs/taxonomy.md`.

---

## 3. Major modern research families

Each family below becomes a cluster in the graph and a "family card" on its section page.

1. **Latent flow-matching transformers** (SD3/MMDiT → FLUX.1 → Qwen-Image / Seedream / HunyuanImage / FLUX.2 / Z-Image). The dominant open T2I recipe. Differentiators now sit in training signal and text encoder, not objective.
2. **Representation-aligned and representation-space generation** (REPA → VA-VAE → REPA-E → MAETok → RAE, SVG; contested by pixel-space JiT). Your core line.
3. **Discrete-token and AR generation** (MUSE, VAR, LlamaGen, Infinity, MAR, Fluid; GPT-4o image as closed evidence that AR scales). Includes the "AR needs a better tokenizer" sub-story.
4. **Masked / discrete diffusion for images and unified models** (MaskGIT lineage → Meissonic → MMaDA → Muddit → LLaDA-V/LLaDA-Image (verify)).
5. **Few-step and one-step generation** (consistency models → LCM → DMD/DMD2 → LADD → MeanFlow / shortcut / transition matching).
6. **Alignment and RL for generation/editing** (ImageReward, HPSv2, Diffusion-DPO, Flow-GRPO, DanceGRPO, EditScore/Edit-R1).
7. **In-context conditioning for editing and control** (OminiControl, ICEdit, FLUX.1 Kontext, Qwen-Image-Edit, FLUX.2, Seedream 4.0). The transition from adapters and cross-attention to "everything is a token in one sequence".
8. **Training-free editing on flow transformers** (RF-Inversion, RF-Solver, FireFlow, KV-Edit, Stable Flow, Add-it). Includes the question of whether training-free editing is still relevant once trained in-context editors exist.
9. **Unified understanding + generation** — five sub-designs: (a) single transformer, discrete tokens (Chameleon, Emu3); (b) mixed objective in one transformer (Transfusion, Show-o); (c) decoupled encoders, shared LLM (Janus); (d) MoT / two-expert (BAGEL, LMFusion); (e) frozen MLLM + diffusion head via queries (MetaQuery, BLIP3-o, OmniGen2, Qwen-Image's encoder use).
10. **Vision foundation representations as the substrate** (DINOv2/v3, SigLIP2, MAE, JEPA, Perception Encoder, Web-SSL; unified tokenizers TokenFlow/UniTok/TA-TiTok).
11. **Medical generative imaging** — sub-families: synthesis (RoentGen, MAISI, MINIM), reconstruction/inverse problems (DPS lineage), translation (SynDiff, SynthRAD), counterfactual/editing (RadEdit, causal counterfactuals), pathology (virtual staining + pathology FMs), multimodal medical (Med-Gemini, MedGemma, MAIRA-2, Lingshu), synthetic-data evidence (Ktena et al. 2024).

---

## 4. Initial high-value paper/model map (backbone, ~85 entries)

Tier definitions (**Decision D009**):
- **Landmark** — origin of an axis option or changed the direction of a family.
- **Core** — required to understand a branch as it stands today.
- **Strong Follow-up** — meaningful improvement inside a branch.
- **Emerging** — under ~12 months old, promising, unproven.
- **Watchlist** — closed systems or uncertain relevance; tracked with metadata only.

Every entry is `verified: false` until its abstract/PDF has been fetched and read in-session (**Decision D004**: no explanatory claim without a fetched source).

### 4.1 Image generation

| Entry | Tier | Why it anchors |
|---|---|---|
| LDM / Stable Diffusion (Rombach 2022) | Landmark (background) | The pixel → latent transition |
| DiT (Peebles & Xie 2023) | Landmark | UNet → transformer |
| Flow Matching (Lipman 2023); Rectified Flow (Liu 2023) | Landmark | Diffusion → flow objective |
| SD3 / MMDiT "Scaling Rectified Flow Transformers" (Esser 2024) | Landmark | Joint attention, logit-normal timesteps, T5+CLIP |
| SiT (Ma 2024) | Core | Interpolant framework; the RAE line's testbed |
| PixArt-α (2023) | Core | Efficient T2I DiT, T5 text encoder |
| FLUX.1 (BFL 2024) / FLUX.2 (Nov 2025) | Core | Open reference system; FLUX.2 = multi-reference editing + Mistral text encoder |
| Sana + DC-AE (NVIDIA/MIT 2024) | Strong | Deep-compression latents, linear DiT |
| Qwen-Image (Alibaba Aug 2025) | Core | VLM as text encoder, text rendering, MMDiT |
| Seedream 3.0 / 4.0 (ByteDance 2025) | Core (report) | Unified gen+edit, RL alignment recipe |
| HunyuanImage 2.1 / 3.0 (Tencent 2025) | Strong | 3.0 = native multimodal MoE generator |
| Z-Image (Alibaba Nov 2025) | Emerging | Single-stream DiT efficiency claim (verify) |
| Lumina-Image 2.0 (2025) | Emerging | Unified next-DiT, Gemma encoder |
| GPT-4o image gen / gpt-image-1 (OpenAI 2025) | Watchlist (landmark system) | Closed evidence that AR-style native generation works at scale |
| Gemini 2.5 Flash Image "Nano Banana" / Nano Banana Pro (Google 2025) | Watchlist (landmark system) | Closed native editing SOTA |
| Imagen 3/4 | Watchlist | Closed |
| MUSE (Google 2023) | Core | Masked-token T2I |
| VAR (ByteDance 2024) | Landmark | Next-scale AR |
| LlamaGen (2024) | Core | Plain LLM AR baseline |
| MAR "AR without VQ" (Li, He 2024) | Landmark | Diffusion loss on continuous tokens |
| Fluid (Google 2024) | Core | Scaling continuous-token AR for T2I |
| Infinity (ByteDance 2024) | Strong | Bitwise VAR at T2I scale |
| Meissonic (2024) | Core | Masked diffusion T2I at scale |
| MMaDA (2025); Muddit (2025) | Emerging | Unified masked diffusion |
| LLaDA-V (2025); LLaDA-Image (2026, **verify**) | Emerging | Diffusion-LLM lineage into images |
| Consistency Models (Song 2023) | Core | One-step lineage origin |
| DMD / DMD2 (Yin 2024) | Core | Distribution-matching distillation |
| LADD / SD3-Turbo (2024) | Strong | Latent adversarial distillation |
| MeanFlow (He 2025) | Strong | One-step from first principles |
| Autoguidance (Karras 2024); CFG-interval (2024) | Core | Inference-axis anchors |
| Diffusion-DPO (Wallace 2024) | Core | Preference alignment for diffusion |
| Flow-GRPO; DanceGRPO (2025) | Strong | Online RL for flow models |
| ImageReward (2023); HPSv2 (2023) | Core | Reward models |
| "Back to Basics" JiT (Li & He Nov 2025) | Strong / challenger | Pixel-space return; challenges the latent orthodoxy and RAE |

### 4.2 Representation-space / RAE line (the spine)

| Entry | Tier | Role in the problem → next chain |
|---|---|---|
| SD-VAE / 16-ch VAE analysis (SD3, Emu) | Core (background) | Problem: VAE latents are reconstruction-optimized, low-semantic |
| DINOv2 (2023); DINOv3 (Aug 2025) | Landmark / Core | The representation substrate |
| SigLIP / SigLIP 2 (2025) | Core | Language-aligned substrate |
| MAE (2021) | Background | Used as RAE encoder ablation |
| unCLIP / DALL-E 2 prior (2022) | Background | First "generate in CLIP space" |
| Emu / Emu2 (BAAI 2023–24) | Core | AR regression on CLIP features + diffusion decoder |
| REPA (Yu, Xie et al. ICLR 2025) | Landmark | Idea: align DiT hidden states to DINOv2 → 17× faster |
| VA-VAE / LightningDiT (Yao 2025) | Core | Align the VAE itself; the reconstruction–generation dilemma |
| REPA-E (Leng 2025) | Core | End-to-end VAE training through the REPA loss |
| MAETok (2025); ViTok "Learnings from scaling visual tokenizers" (Meta 2025) | Core | Latent geometry: fewer GMM modes → easier generation; tokenizer scaling laws |
| DC-AE (2024) | Core | Dimension/compression trade-off |
| MetaQuery (2025); BLIP3-o (2025) | Core | Diffusion over CLIP features from a frozen MLLM |
| **RAE — Diffusion Transformers with Representation Autoencoders (Zheng, Xie et al. Oct 2025)** | Landmark | Frozen encoder + trained decoder; high-dim latents; width ≥ token-dim; dimension-dependent noise shift; noise-augmented decoding; DiT^DH |
| SVG "Latent diffusion without VAE" (2025, **verify authors**) | Core (competitor) | DINOv3 features + residual detail branch |
| Scaling T2I DiTs with RAE (**verify**, 2025/26) | Core | RAE at text-conditioned scale |
| RAE follow-ups on priors / transport / training / baselines (**you to provide refs; verify**) | Emerging | Gaussian vs mixture source, straighter paths, better baselines |
| JiT (Nov 2025) | Challenger | "You don't need a tokenizer" |
| Unified tokenizers: TokenFlow, UniTok, TA-TiTok, DualViTok (2024–25) | Strong | Semantic + pixel codebooks for AR/unified |
| Web-SSL "Scaling language-free visual representation learning" (2025) | Strong | Does language supervision matter for the substrate? |

Cross-cutting open-problem nodes for this section: `vae-latent-semantics`, `high-dim-latent-diffusion`, `reconstruction-generation-dilemma`, `semantic-latent-detail-loss`, `latent-prior-shape` (Gaussian vs mixture), `transport-path-straightness`, `latent-vs-pixel-space`.

### 4.3 Image editing

| Entry | Tier | Role |
|---|---|---|
| SDEdit; Prompt-to-Prompt; Null-text inversion (2021–22) | Background | Ancestors |
| InstructPix2Pix (2023) | Landmark | Instruction editing via synthetic pairs |
| ControlNet (2023); T2I-Adapter | Landmark | Structural control |
| IP-Adapter (2023) | Core | Reference conditioning via decoupled cross-attention |
| MasaCtrl; Plug-and-Play (2023) | Core | Attention manipulation |
| Emu Edit (Meta 2023); MagicBrush | Core | Trained multi-task editing + benchmark |
| InstantID; PuLID (2024) | Core | Identity preservation |
| OmniGen (2024) → OmniGen2 (2025) | Core | Unified in-context generation/editing |
| OminiControl (2024) | Core | Minimal token-concat conditioning for DiT |
| RF-Inversion (2024); RF-Solver; FireFlow | Core | Inversion for rectified flow |
| Stable Flow (2024); Add-it | Strong | Vital-layer attention in MMDiT |
| KV-Edit (2025) | Strong | Training-free background preservation via KV cache |
| Step1X-Edit + GEdit-Bench (2025) | Core | Open instruction editor + benchmark |
| ICEdit (2025) | Strong | In-context editing with tiny data |
| **FLUX.1 Kontext (June 2025)** | Landmark | Sequence-concat in-context editing at scale |
| Qwen-Image-Edit / -2509 / -2511 (2025) | Core | Multi-image, semantic + appearance dual conditioning |
| FLUX.2 (Nov 2025) | Core | Multi-reference editing |
| Seedream 4.0; Nano Banana; GPT-Image-1 | Core / Watchlist | Native unified editing SOTA (closed except Seedream report) |
| BAGEL; Emu3.5 (editing paths) | Core | Editing inside unified models |
| ImgEdit; RISEBench; KRIS-Bench (2025) | Core (eval) | Modern editing benchmarks incl. reasoning |
| EditScore / Edit-R1 (2025) | Emerging | Reward models + RL for editing |
| DIFT / diffusion hyperfeatures (2023) | Core (bridge) | Foundation/diffusion features for correspondence-based editing |

**RAE-editing investigation (planned, Phase 3)**. Working hypothesis to test, not a conclusion: as of mid-2026 I know of no major work doing instruction or reference editing *in RAE-style semantic latents*. Nearest neighbors are CLIP-feature generation with weak pixel fidelity (Emu2, BLIP3-o, MetaQuery) and SVG's residual branch. The crux is structural: editing requires preserving unedited pixels, and semantic latents drop exactly the high-frequency detail that preservation needs. The investigation will (a) run targeted searches, (b) read the user-provided RAE follow-ups, (c) write a `problems/semantic-latent-editing.yaml` node with candidate approaches (hybrid latents, source-conditioned decoders, KV-cache of source tokens, latent-space inversion). This is a Fable-level task.

### 4.4 Vision foundation models for generation
DINOv2 · DINOv3 · SigLIP 2 · MAE · I-JEPA / V-JEPA 2 · Perception Encoder · AIMv2 · Web-SSL · "Vision Transformers need registers" · l-DAE "Deconstructing DDMs for SSL" (diffusion as representation learner) · Cambrian-1 (which encoders help MLLMs) · SAM 2/3 and Depth Anything 2/3 as control sources (verify SAM 3 / DA3 details) · unified tokenizers (listed in 4.2).

### 4.5 VLM families (brief)
LLaVA / LLaVA-OneVision (encoder + projector) · Flamingo / Llama 3.2 Vision (cross-attention) · Fuyu / Chameleon (early fusion) · Qwen2-VL → Qwen2.5-VL → Qwen3-VL (native resolution, M-RoPE; matters because Qwen-Image uses it as encoder) · InternVL 2.5/3 · PaliGemma 2 · Gemini / GPT-4o (closed). One comparison table, five concept nodes, no deep paper pages.

### 4.6 Unified understanding + generation

| Entry | Tier | What is unified (to be filled as a matrix: representation / tokenizer / backbone / parameters / objective / pathways) |
|---|---|---|
| Chameleon (Meta 2024) | Landmark | Everything shared; discrete tokens; single AR objective |
| Transfusion (Meta 2024) | Landmark | Shared backbone; AR text + continuous diffusion images |
| Show-o (2024) → Show-o2 (2025) | Core / Strong | AR + discrete diffusion in one transformer; Show-o2 moves to 3D-VAE latents |
| Janus (DeepSeek 2024) → Janus-Pro; JanusFlow | Core / Strong | Decoupled visual encoders, shared LLM |
| Emu3 (2024) → Emu3.5 (2025) | Core / Strong | Next-token everything; 3.5 adds native interleaved editing |
| Mixture-of-Transformers; LMFusion (Meta 2024) | Core | Modality-specific parameters, shared attention |
| BAGEL (ByteDance 2025) | Landmark | MoT + interleaved data + "thinking" before generation |
| MetaQuery (2025); BLIP3-o (2025) | Core | Frozen MLLM + learnable queries + diffusion head |
| OmniGen2; UniWorld-V1 (2025) | Strong | Decoupled understanding/generation paths |
| HunyuanImage 3.0 (2025) | Core | Native multimodal MoE generator |
| Qwen-Image / Qwen-Image-Edit (2025) | Core | VLM encoder + MMDiT: "unified" only at the conditioning pathway |
| MMaDA; Muddit; LLaDA-V; LLaDA-Image (**verify**) | Emerging | Unification through masked diffusion |
| UniFluid (Google 2025); Harmon; Tar / TokLIP; X-Omni | Emerging | Continuous-token or text-aligned-tokenizer unification |
| GPT-4o image; Nano Banana Pro | Watchlist | Closed but define the target |

### 4.7 Medical generative imaging (evidence-first)

| Entry | Tier | Evidence type |
|---|---|---|
| Kazerouni et al. 2023 survey (MedIA) | Core (reference) | Map of the space |
| RoentGen (Stanford 2022) | Landmark | First strong domain-adapted T2I for CXR; downstream utility |
| MAISI (NVIDIA 2024) | Core | 3D CT latent diffusion with anatomy control |
| MINIM (Nature Medicine 2025) | Core | Multi-modality generative model with clinical-task evidence |
| Ktena et al., Nature Medicine 2024 "Generative models improve fairness under distribution shift" | Landmark | Real synthetic-data evidence |
| Pinaya 2022 brain-MRI LDM; MONAI Generative | Core | 3D synthesis baseline + tooling |
| Score-based MRI recon (Chung & Ye 2022; Jalal 2021); DPS (Chung 2023); PSLD | Core | Reconstruction via diffusion priors |
| SynDiff (2023); SynthRAD challenge | Core | Modality translation with clinical metrics |
| RadEdit (Microsoft 2024) | Core | Masked editing for stress-testing models |
| Causal counterfactuals (Pawlowski 2020 bg → Ribeiro 2023 → diffusion counterfactuals) | Core | Counterfactual generation with causal validity |
| Pathology FMs (UNI, Virchow, Prov-GigaPath, CONCH 2024) + diffusion virtual staining (2024) | Core | Representation substrate + generation in pathology |
| Med-Gemini (2024); MedGemma (2025); MAIRA-2; LLaVA-Med; Lingshu (2025) | Core | Multimodal medical models |
| Memorization/privacy in medical diffusion (Dar 2023; Fernandez 2023) | Core | Risk evidence |
| Fréchet Radiomics Distance and task-based evaluation (verify) | Emerging (eval) | Beyond FID |

The PubMed MCP tool is available for this section's verification.

---

## 5. Website structure and visual approach

### Stack (**Decision D002**)
- **Astro 5** (static, content collections with Zod-typed schemas, MDX, islands for interactivity). Reasons: best static output for a content-heavy site, typed data loading from YAML/JSON, tiny JS by default, first-class GitHub Pages deploy.
- **Math**: remark-math + rehype-katex.
- **Search**: Pagefind (static, zero backend, indexes built HTML).
- **Graph**: D3 (SVG) inside one React or Svelte island, with a *custom lane-timeline layout* (x = time, y = family lane, edge color = relation type). Node count is deliberately kept under ~300, so WebGL (Sigma) is unnecessary. Filters: by relation type, section, tier, year range; click → side panel with summary and links; "focus mode" shows a node's 2-hop neighborhood.
- **Diagrams**: hand-authored SVG for architecture diagrams; Mermaid for pipelines/flowcharts.
- **Styling**: plain CSS with design tokens (no Tailwind — keeps typography under control). Fonts: Inter (body) + Newsreader or Source Serif (headings) + JetBrains Mono. Max text width 70ch.
- **Theme**: light/dark via CSS variables, `prefers-color-scheme` plus toggle.
- **Deploy**: GitHub Actions → GitHub Pages (needs your approval when we publish).

Rejected: Next.js (heavier, no benefit for static content), Docusaurus (docs look, hard to make beautiful), Hugo (weak component islands for the graph), Quarto (academic but inflexible).

### Site map
```
/                     Home: one-screen "design space" map, 4 entry points, recent updates
/axes/{representation|objective|architecture|conditioning|training-signal|inference}
/sections/{generation|rae|editing|unified|vfm|vlm|medical}
/transitions/{slug}   Narrative pages: "From VAE latents to representation latents", etc.
/graph                Full interactive research graph
/papers/{id}  /concepts/{id}  /systems/{id}  /problems/{id}  /benchmarks/{id}
/compare              Data-driven tables: T2I systems; unified "what is unified" matrix;
                      editing models; tokenizers; medical models
/paths                Learning paths (e.g. "DiT → RAE in 12 papers", "Editing on flow
                      transformers", "Unified models", "Medical GenAI, evidence first")
/problems             Open-problem ledger, each linked to the papers attacking it
/updates              Changelog feed + candidate queue status
```

### Paper page template (from your list)
Before · Problem · Core idea · Representation · Architecture · Objective · Conditioning · Training · Inference · Results · Ablations · Limitations · Builds on · Built on by · Why it matters. Sections that are background concepts render as a link chip to the concept page, not repeated text. Landmark/Core get the full template; Strong gets a short form; Emerging/Watchlist get metadata + 3-sentence summary.

### Color identity
Neutral base (off-white / near-black), one hue per section applied only to headings, badges, graph edges, and the left border of cards.

| Section | Hue |
|---|---|
| Generation | slate blue |
| RAE / representation | violet |
| Editing | teal |
| Unified | amber |
| VFM | green |
| VLM | steel gray |
| Medical | rose |

---

## 6. Knowledge/data schema (**Decision D003**)

One YAML file per entity under `data/`, validated by JSON Schema in CI, compiled to a single `graph.json` at build. Long-form explanations live in MDX under `content/` and are referenced by id.

Entity types: `concept`, `paper`, `system` (model family with releases), `relation`, `problem`, `benchmark`, `result`, `transition`, `path`, `update_event`. Organizations/people are plain string fields, not entities.

```yaml
# data/papers/rae-2025.yaml
id: rae-2025
type: paper
title: Diffusion Transformers with Representation Autoencoders
short: RAE
arxiv: "2510.11690"
date: 2025-10
venue: { name: arXiv, status: preprint }        # monitor updates this
orgs: [NYU]
authors: [Boyang Zheng, Nanye Ma, Shengbang Tong, Saining Xie]
tier: landmark
sections: [rae, generation]
axes:
  representation: [semantic-latent, frozen-encoder]
  objective: [flow-matching]
  architecture: [dit, dit-dh]
problems: [vae-latent-semantics, high-dim-latent-diffusion]
links: { code: ..., weights: ..., project: ... }
status:
  code: released          # none | announced | released
  weights: released
  verified: false         # flipped only after abstract/PDF was fetched in-session
  verified_on: null
  verified_by: null
summary: >-
  One paragraph.
explanation: content/papers/rae-2025.mdx
```

```yaml
# data/relations/rae.yaml  (one file per section cluster)
- from: rae-2025
  to: repa-2024
  type: builds_on            # builds_on | improves | challenges | replaces | combines |
                             # competes_with | uses_representation_from | uses_objective_from |
                             # uses_architecture_from | evaluates_on | addresses | enables
  evidence: "Sec. 1: REPA showed alignment helps; RAE asks why not generate in that space."
  confidence: high           # high | medium | low
  added_by: fable            # human | fable | sonnet | pipeline
  status: verified           # candidate | verified
```

Other schemas, in brief:
- `concept`: id, axis (or `background`), name, one-line, options it belongs to, `explains` (MDX), `introduced_by` (paper ids).
- `system`: id, family name, org, releases `[ {version, date, arxiv|report, open: true/false, notes} ]`, axes, sections.
- `problem`: id, statement, why-it-matters, `attacked_by` (paper ids), `status` (open | partially-solved | solved-by), candidate approaches.
- `benchmark` / `result`: benchmark id, metric, paper id, value, setting, source (page/table), so comparison tables are generated, not hand-typed.
- `transition`: id, from-option, to-option, era, driver (which axis became the bottleneck), cost (what was lost), key papers, narrative MDX.
- `path`: id, title, audience, ordered list of `{id, why}` steps.
- `update_event`: date, kind (new_paper | code_release | weights | acceptance | revision | followup | reproduction), target id, source URL, pipeline run id.

Validation: `scripts/validate.py` (Python, `jsonschema` + referential integrity: every id referenced must exist; every relation endpoint exists; no orphan MDX). `scripts/build_graph.py` emits `site/src/data/graph.json`.

---

## 7. GitHub structure

```
genai-atlas/
  README.md                 What this is, how to run, how to contribute
  CLAUDE.md                 Session bootstrap: "read PROJECT_STATE.md first", rules, model policy
  PROJECT_STATE.md          Phase, done, decisions, files, papers reviewed, open questions,
                            failed approaches, exact next tasks
  CHANGELOG.md              Human-readable log; pipeline appends under "Unreleased"
  DECISIONS.md              ADR-style log (D001…)
  docs/                     blueprint.md (this file), taxonomy.md, style-guide.md, pipeline.md
  schema/                   *.schema.json
  data/
    concepts/  papers/  systems/  problems/  benchmarks/  results/  transitions/  paths/
    relations/              one YAML per cluster
    monitor/                state.json (last-checked per paper), candidates/ (pending YAML)
  content/                  MDX long-form: papers/ concepts/ transitions/ sections/
  site/                     Astro project (src/, public/, astro.config.mjs)
  pipeline/                 Python package: discover/ filter/ dedup/ relate/ monitor/ report/
  scripts/                  validate.py, build_graph.py, new_entity.py, verify_paper.py
  tests/                    schema tests, graph integrity tests, pipeline unit tests
  .github/workflows/        ci.yml (validate + build), deploy.yml, update.yml (cron */3 days)
```

`CLAUDE.md` will contain the resume protocol: (1) read `PROJECT_STATE.md`, (2) read last 30 lines of `CHANGELOG.md`, (3) run `scripts/validate.py`, (4) continue from "Exact next tasks", (5) after each unit of work update state + changelog before anything else.

---

## 8. Three-day update architecture

```
discover → relevance filter → quality filter → duplicate check → relationship analysis
        → candidate (YAML + PR) → verification → merge → rebuild → CHANGELOG + /updates
```

| Stage | Mechanism | Cost |
|---|---|---|
| Discover | arXiv API (cs.CV, cs.LG, cs.AI; keyword sets per section); Semantic Scholar API (citations of atlas papers, new papers citing Landmark nodes); Hugging Face daily papers; org watchlists | Deterministic, free |
| Relevance filter | Rules first (keyword score, author/org whitelist, cites ≥1 atlas node), then Haiku 4.5 classifies against the six axes and seven sections; hard reject if nothing matches | Haiku, cents |
| Quality filter | Rules: org/venue tier, code/weights present, citation velocity from S2, atlas-node citations; Haiku assigns provisional tier (never above Strong Follow-up automatically) | Haiku |
| Duplicate check | arXiv id, DOI, normalized title similarity, S2 corpus id; also detects new *versions* of existing papers | Deterministic |
| Relationship analysis | Sonnet 5 reads abstract + intro, proposes typed relations to existing nodes with evidence quotes and confidence | Sonnet |
| Candidate | Writes `data/monitor/candidates/<id>.yaml` + opens a PR with a summary; nothing enters `data/papers/` automatically | Deterministic |
| Verification | Human or Fable session reviews PR; Landmark/Core tier requires a fetched-PDF read; merge flips `status.verified` | Fable / you |
| Update | Merge → CI validate → build → deploy → CHANGELOG entry → `/updates` feed | Deterministic |

**Monitoring existing papers** (same cron): per paper, S2 for venue change and new citing papers with high velocity (→ "strong follow-up" candidates); arXiv for new versions (diff abstract, flag "important revision" if Haiku judges substantive); GitHub API / HF Hub for code and weights appearance; Papers-with-Code/HF for reproduction results. Emits `update_event` entities; a state file records last-checked timestamps so each run only touches what changed.

**Runner options**: (a) GitHub Actions cron with an Anthropic API key secret for the Haiku/Sonnet stages (paid API, needs your approval); (b) a Claude Code scheduled routine (cloud) that runs the whole pipeline on your subscription; (c) local `claude -p` run you trigger. Recommend starting with (c) during build-out, switching to (a) or (b) at publish time. **Decision D006**: candidates always go through a PR; nothing is auto-merged in the first months.

---

## 9. Model strategy (**Decision D007**)

| Work | Model |
|---|---|
| Taxonomy decisions, transition narratives, RAE deep-dive synthesis, "what is unified" matrix, RAE-editing gap investigation, medical evidence appraisal, conflict resolution between papers, reviewing any Landmark/Core explanation before publish, hard architecture problems | **Fable 5.1** (Opus 5 as the cheaper substitute if Fable budget is tight) |
| Drafting paper explanations for Core/Strong papers from a fetched PDF; site components; schema and validators; pipeline code; tests | **Sonnet 5** |
| Metadata extraction, YAML entry creation, formatting, changelog entries, link checking, batch summaries of Emerging/Watchlist entries | **Haiku 4.5** or Sonnet 5 |
| Pipeline runtime filters | Haiku 4.5 (API) |
| Relationship proposals in pipeline | Sonnet 5 (API) |
| Fetching, dedup, validation, graph build, deploy, monitoring | Deterministic scripts, no LLM |

In-session mechanics: switch with `/model`; for batch drafting use subagents with `model: sonnet` or `haiku`; the pipeline pins model ids in config. I will explicitly say "this step is worth Fable" or "drop to Sonnet for this" at each phase boundary in `PROJECT_STATE.md`.

Never use Fable/Opus for: metadata, formatting, YAML, simple code, repetitive updates.

---

## 10. Implementation phases

| Phase | Deliverable | Model | Sessions |
|---|---|---|---|
| P0 | This blueprint | Fable | done |
| P1 | Repo skeleton, state files, schemas, validators, seed data, Astro scaffold, graph prototype | Sonnet (Fable reviews taxonomy pages only) | 1 |
| P2 | RAE section complete: problem → next chain, 20 verified entries, latent-geometry and transport-path concept pages, open problems; Generation axes pages and 3 transition narratives | Fable for synthesis, Sonnet for entries | 2–3 |
| P3 | Editing section + RAE-editing gap investigation + editing benchmark table | Fable for gap analysis | 2 |
| P4 | Unified section with "what is unified" matrix; VLM/VFM brief pages | Fable for matrix | 2 |
| P5 | Medical section, evidence-first, PubMed-verified | Fable for appraisal, Sonnet for entries | 1–2 |
| P6 | Site polish: full graph, learning paths, compare tables, search, dark mode, diagrams | Sonnet | 2 |
| P7 | Update pipeline + monitoring + first dry run on last 30 days of arXiv | Sonnet; Haiku at runtime | 2 |
| P8 | Publish (your approval), first live 3-day cycle, maintenance loop | — | 1 |

Each phase ends with `PROJECT_STATE.md` + `CHANGELOG.md` updated and a "worth Fable next?" note.

---

## 11. Exact first sprint (P1) — run on Sonnet, one session

Files at end of sprint, all under `/home/exx/Vscode-Sahar/GenAI/` (rename to `genai-atlas` optional):

1. **Governance**: `git init`; `README.md`, `CLAUDE.md` (resume protocol), `PROJECT_STATE.md`, `CHANGELOG.md`, `DECISIONS.md` with D001–D009 from this blueprint; `docs/blueprint.md` (this file copied in), `docs/taxonomy.md`.
2. **Schemas + tooling**: `schema/*.schema.json` for the 10 entity types; `scripts/validate.py` (schema + referential integrity); `scripts/build_graph.py`; `scripts/verify_paper.py` (fetches arXiv abstract by id, writes `verified` fields); `tests/` with 5 tests; Python deps in `pyproject.toml`.
3. **Seed data (RAE spine + generation landmarks, ~30 papers, ~45 relations)**: the 4.2 table in full, plus LDM, DiT, SiT, Flow Matching, Rectified Flow, SD3, FLUX.1, VAR, MAR, JiT from 4.1; 6 axis concept stubs; 7 problem nodes from 4.2; 2 transitions ("pixels → latents → representation latents", "diffusion → flow matching"); 1 path ("DiT to RAE in 12 papers").
4. **Verification pass**: run `verify_paper.py` on all seeds; fetch and read RAE (2510.11690), the RAE T2I scaling paper, LLaDA-Image (2609.03796), and the RAE follow-ups you point me to; **frontier recon**: arXiv search Jan–Sep 2026 for each section's keyword set, output `docs/recon-2026.md` listing candidates for later phases. This step is the one place Fable is worth it in Sprint 1 (reading RAE follow-ups and LLaDA-Image correctly).
5. **Astro scaffold** in `site/`: design tokens, light/dark, home page with the axis map, `/axes/representation`, `/transitions/<one>`, paper page template rendering `rae-2025`, `/graph` D3 prototype reading `graph.json`, Pagefind search, KaTeX working on one equation. No polish beyond a clean base.
6. **State**: `PROJECT_STATE.md` filled with phase=P1-done, files, decisions, papers verified, unresolved (RAE follow-up refs, LLaDA-Image details, hosting approval), exact next tasks for P2.

**Not in Sprint 1**: pipeline, medical, editing, unified content, full paper set, publishing.

### Verification for Sprint 1
```
python scripts/validate.py          # schemas + integrity pass, 0 errors
python scripts/build_graph.py       # emits site/src/data/graph.json with ~30 nodes / ~45 edges
pytest tests/                       # green
cd site && npm run build            # static build succeeds
cd site && npm run preview          # home, /axes/representation, /papers/rae-2025, /graph render;
                                    # search returns "REPA"; dark mode toggles; equation renders
```

---

## The single central organizing idea

**Follow the representation.**

Generative vision is converging on a shared space for seeing, generating, and editing, and every modern branch is a different bet on what that space should be and how to move through it. Objectives and architectures have largely converged (flow-matching transformers, with AR and masked diffusion as the live alternatives), so the questions that now move the field are representational: VAE latent or foundation latent, discrete or continuous, shared with understanding or decoupled, and what pixel fidelity is lost when the latent becomes semantic. That last question is exactly where your RAE work, editing, and unified models meet, so the site's spine is the Representation axis, and every other axis, section, and transition is read in relation to it.

## Open questions for you (non-blocking; answer whenever)
1. Which RAE follow-up papers on latent distributions / transport paths do you mean? Send arXiv ids and I will verify them in Sprint 1.
2. Public or private repo, and under which GitHub account? Needed only at P8.
3. Do you want the pipeline's LLM stages on the paid API or on a Claude Code scheduled routine? Needed only at P7.
