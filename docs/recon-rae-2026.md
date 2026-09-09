# RAE follow-up recon (fetched 2026-09-09, Fable session 1)

Source: arXiv API query `all:"representation autoencoder"` (40 newest) + web search. Every id below
was returned by arXiv; the one-line summaries come from the fetched abstracts. Nothing has been read
in full yet; `verified` in data files stays false until the PDF is read.

## Anchor papers (user's path)
| arXiv | Date | Title | Note |
|---|---|---|---|
| 2510.11690 | 2025-10 | Diffusion Transformers with Representation Autoencoders (Zheng, Ma, Tong, Xie; NYU) | RAE. Landmark. code: github.com/bytetriper/RAE |
| 2601.16208 | 2026-01 | Scaling Text-to-Image Diffusion Transformers with RAEs (Tong, Zheng, Wang, ..., LeCun, Xie) | Scale-RAE. SigLIP-2 encoder; decoder scaled on web/synthetic/text-rendering data; VAE models overfit at 64 ep, RAE stable to 256 ep. code: github.com/ZitengWangNYU/Scale-RAE; page: rae-dit.github.io/scale-rae |
| 2605.18324 | 2026-05 | Improved Baselines with Representation Autoencoders (Singh et al.) = **RAEv2** | Multilayer representation aggregation; RAE+REPA complementary; DiT output re-parameterization fixes CFG; gFID 1.06 in 80 ep, 10x faster. page: raev2.github.io. **This is the "training + baselines" follow-up.** |
| 2609.03796 | 2026-09-03 | LLaDA-Image: Building Strong Image Generators with Fully Open Training Recipes (Chen et al., 30 authors) | 6B DiT from scratch + frozen LLaDA2.0-Mini diffusion-LM understanding module; 220M samples; image-only pretraining first; 2–4 step distilled; SOTA open on EN/CN tracks. NOT an RAE paper — belongs to unified/generation sections. |

## Follow-ups by theme (candidate tiers in parentheses)

### Latent distribution / geometry / transport paths
| arXiv | Date | Title | One-line |
|---|---|---|---|
| 2606.15553 | 2026-06 | Distilling Drifting Transformers with RAEs (Zhang) | RAE latents are severely anisotropic per-token; isotropic Gaussian → anisotropic target forces curved trajectories; drifting-field distillation, FID 1.48 in 16 ep. (strong-followup) |
| 2512.00684 | 2025-11 | Cosine-Similarity Methods for Efficient Training and Sampling in High-Dim Latent Spaces (Duan) | Directional regularities in high-dim latents; cosine-based couplings give cleaner velocity fields. (emerging) |
| 2604.01545 | 2026-04 | RAE-AR: Taming Autoregressive Models with RAEs (Yu) | Distribution normalization of tokens + Gaussian noise injection to close train/inference gap for AR on RAE latents. (strong-followup) |
| 2605.05206 | 2026-05 | Taming Outlier Tokens in Diffusion Transformers (Wu) | High-norm outlier tokens in encoder and denoiser; dual-stage registers. (emerging) |
| 2608.01306 | 2026-08 | SPAE: Spectrally Guided Autoencoder for Pretrained Visual Latents (Huang) | Spectral mismatch (high-freq) between encoder latents and DiT-generated latents; bottleneck suppresses bad frequencies. (emerging) |
| 2608.00626 | 2026-08 | Where Does Generative Difficulty Reside? (Plocher) | Empirical: pixels vs SD-VAE vs DINOv2 vs MAE targets redistribute difficulty across context modeling, per-token denoising, inference control; compression/rFID do not predict gFID. (core for the representation axis) |
| 2512.18184 | 2025-12 | Is There a Better Source Distribution than Gaussian? Exploring Source Distributions for Image Flow Matching | **Gaussian vs alternative source** question directly. (verify; not RAE-specific) |
| CVPR 2026 | 2026 | Flow Matching for Multimodal Distributions (Luo) — MM-FM | GMM source + mode-dependent coupling. (verify; not RAE-specific) |
| 2605.07676 | 2026-05 | Structured Coupling for Flow Matching | Learned structured source for stochastic interpolants. (verify) |

### Decoder / reconstruction
| arXiv | Date | Title | One-line |
|---|---|---|---|
| 2602.08620 | 2026-02 | Improving Reconstruction of Representation Autoencoder (Liu) — LV-RAE | Semantic features lack color/texture; add low-level info + decoder robustness finetune + noise injection. (strong-followup) |
| 2605.22777 | 2026-05 | DecQ: Detail-Condensing Queries for RAEs (Wang) | Lightweight queries pull fine detail from intermediate VFM layers for the decoder; PSNR 19.13→22.76, FID 1.05 w/ guidance. (strong-followup) |
| 2602.04873 | 2026-02 | Laminating RAEs for Efficient Diffusion (Calvo-González) — FlatDINO | Compress DINOv2 grid to 32 1-D tokens; gFID 1.80 at 8x fewer FLOPs. (strong-followup) |

### Discrete / unified RAE
| arXiv | Date | Title | One-line |
|---|---|---|---|
| 2511.23386 | 2025-11 | VQRAE (Du) | Continuous semantic + discrete tokens via high-dim quantization for understanding+generation+reconstruction. (emerging) |
| 2606.11096 | 2026-06 | IDEAL: In-Depth Alignment Makes a Discrete RAE (Chen) | Align quantized tokens to shallow+deep VFM features; rFID 0.61, gFID 1.89 AR. (emerging) |
| 2607.22148 | 2026-07 | dRAE: RAE with Hyper-Spherical Codes (Ma) | Euclidean VQ collapses on anisotropic features; angular routing, 100% codebook use at 131k. (emerging) |
| 2605.10780 | 2026-05 | Beyond the Last Layer: Multi-Layer Representation Fusion for Visual Tokenization (Zhu) | (verify) |

### Objective / sampling on RAE
| arXiv | Date | Title | One-line |
|---|---|---|---|
| 2511.13019 | 2025-11 | MeanFlow Transformers with RAEs (Hu) | One-step on RAE latents; 1-step FID 2.03. (strong-followup) |
| 2606.14700 | 2026-06 | RepFusion (Pan) | MLLM repurposed as noisy representation encoder conditioning a DiT; denoising in representation space for T2I. (emerging; also unified section) |

### Competing line (VFM latents without the RAE recipe)
| arXiv | Date | Title | One-line |
|---|---|---|---|
| 2512.11749 | 2025-12 | SVG-T2I (Shi) | T2I directly in VFM feature space; GenEval 0.75, DPG 85.78; fully open. (core competitor to Scale-RAE) |
| 2510.18457 | 2025-10 | VFM-VAE: Vision Foundation Models Can Be Good Tokenizers for LDMs | (verify) |
| 2603.03276 | 2026-03 | Beyond Language Modeling: An Exploration of Multimodal Pretraining (Tong) | Transfusion-style controlled study; vision more data-hungry than language; MoE helps. (core for unified section) |

### Out-of-scope pointers (video/3D/world models on RAE) — record only
2608.13556 V-RAE · 2607.14088 VideoRAE · 2607.05352 Multiplayer world models w/ RAE · 2603.09241 RAE-NWM ·
2603.16099 OneWorld · 2604.11331 3D scene 1K tokens · 2607.29180 MoRAE (motion).

## RAE-editing gap: first-pass result
A targeted search for image editing in RAE / VFM latent space returned **no dedicated paper**.
Adjacent only: RepFusion (MLLM-conditioned denoising in representation space), LV-RAE / DecQ (detail
recovery, which is the prerequisite for edit-region preservation), UniEdit-I (training-free editing
for unified VLMs, not RAE). The hypothesis "RAE editing is underexplored" survives the first pass;
Phase 3 must do a deeper search (Semantic Scholar citations of 2510.11690 and 2601.16208 filtered
by "edit") before concluding.
