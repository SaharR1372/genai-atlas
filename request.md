I want to build a **living research website and GitHub knowledge base for modern Generative Vision**, focused mainly on the **2023–2026 frontier**.

I am a PhD student with a computer vision/deep learning background and applied ML internship experience. Recently I worked on image generation and image editing.

My recent path included:

* **Diffusion Transformers with Representation Autoencoders**
  https://arxiv.org/abs/2510.11690
* text-conditioned RAE work such as **Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders**
* follow-up RAE work improving latent distributions, transport paths, training, and baselines
* practical image editing with models such as **FLUX.2** and **Qwen-Image-Edit-2511**
* newer unified multimodal work such as **LLaDA-Image**
  https://arxiv.org/pdf/2609.03796

My problem is that the field is growing quickly and I do not have one clear mental map of all the important modern directions.

# Goal

Build a high-quality research atlas that explains:

> **Why the field moved from one approach to another, what the important branches are today, where they are converging, and what important problems remain open.**

Do NOT organize the project as a giant paper list.

Organize papers around:

* representations;
* generative objectives;
* architectures;
* conditioning mechanisms;
* capabilities;
* important research transitions.

Challenge my taxonomy if there is a better one.

# Scope

Focus strongly on **modern active research**.

Do NOT spend much time on outdated areas such as GANs, early VAEs, or early diffusion. Mention them briefly only when needed to understand a modern method.

The main research areas should include:

1. **Modern Image Generation**

   * latent diffusion
   * DiT
   * flow matching / rectified flow
   * modern text-to-image systems
   * autoregressive / discrete-token generation
   * masked/discrete diffusion
   * important emerging alternatives

2. **Representation-Space / RAE Generation**
   This is particularly important to me.
   Cover:

   * limitations of VAE latents
   * vision foundation representations
   * CLIP/DINO/SigLIP/etc. when relevant
   * RAE
   * decoder/reconstruction issues
   * latent dimensionality and geometry
   * Gaussian vs mixture distributions
   * transport paths
   * diffusion/flow behavior
   * conditioning
   * scaling
   * major improvements and competing approaches

   Show this research line as:
   **problem → idea → method → evidence → limitation → next work**

3. **Modern Image Editing**

   * instruction editing
   * reference-based editing
   * identity/subject preservation
   * local/global editing
   * structural control
   * inversion
   * attention manipulation
   * training-free vs trained editing
   * native editing in unified models

   Specifically investigate whether **RAE / foundation-representation image editing is still underexplored**, or whether I am missing important work.

4. **Vision Foundation Models relevant to generation**

5. **Modern VLM architecture families**

6. **Unified Understanding + Generation**
   Cover important architectures combining some of:

   * language
   * visual understanding
   * reasoning
   * image generation
   * image editing

   Include important families such as Chameleon, Emu, Janus, Show-o, BAGEL, Qwen-related systems, LLaDA-Image, and other major current work.

   For each, explain what is actually unified:

   * representation?
   * tokenizer?
   * backbone?
   * parameters?
   * objective?
   * understanding/generation pathways?

7. **Generative AI for Medical Imaging**
   Have a separate section covering important work in synthesis, reconstruction, modality translation, medical editing, pathology, multimodal medical models, synthetic data, and counterfactual generation.

   Prioritize work with real technical/clinical evidence, not just better FID/SSIM.

# Paper Selection

Do NOT include everything.

Prioritize:

* landmark and highly influential papers;
* top universities;
* major AI labs and companies;
* top CV/ML venues;
* papers that clearly influence later models;
* strong and widely used open-source systems.

Prefer work from groups such as Google/DeepMind, Meta, OpenAI, Microsoft, NVIDIA, Adobe, Alibaba/Qwen, ByteDance, Tencent, and leading universities.

However, do not exclude a less-famous group if the work is clearly important.

Classify papers as:

* Landmark
* Core
* Strong Follow-up
* Emerging
* Watchlist

# Paper Explanations

Important papers should explain:

* what existed before;
* problem;
* core idea;
* representation;
* architecture;
* objective;
* conditioning;
* training;
* inference;
* results;
* ablations;
* limitations;
* what it builds on;
* what builds on it;
* why it matters.

If a background concept is already explained elsewhere, link to it instead of repeating it.

# Research Graph

One of the most important parts of the site should be a visual research graph showing relationships such as:

* builds on
* improves
* challenges
* replaces
* combines
* competes with
* uses representation from
* uses objective from

I want to clearly see how major research branches evolve and converge.

# Website

The website should be **simple, modern, clean, and beautiful**.

Use:

* minimal professional design;
* good typography;
* whitespace;
* clear navigation;
* readable equations;
* diagrams;
* comparison tables;
* search;
* learning paths;
* research graph;
* recent updates;
* optional light/dark mode.

Give each major research section its own **subtle color identity**, while keeping the whole site visually consistent and not colorful or cluttered.

Recommend the best technical stack.

# GitHub + Structured Knowledge

Everything should live in a clean GitHub repository.

Do not store everything only as Markdown.

Create structured data for concepts, papers, model families, relationships, benchmarks, and open research questions so the website and automation can query them.

# Living Update System

The site should check for important new research approximately **every 3 days**.

The pipeline should roughly be:

**discover → relevance filter → quality filter → duplicate check → relationship analysis → candidate → verification → update**

Do NOT automatically add every arXiv paper.

Also monitor existing papers for:

* code release;
* weights release;
* conference acceptance;
* important revisions;
* strong follow-up work;
* reproduction results.

# Persistent Project State

This project will span multiple sessions.

Never rely only on chat history.

Maintain:

* `PROJECT_STATE.md`
* `CHANGELOG.md`

After every meaningful unit of work, record:

* current phase;
* completed work;
* important decisions;
* files created/changed;
* papers already reviewed;
* conclusions;
* unresolved questions;
* failed approaches that should not be repeated;
* exact next tasks.

At the start of every new session, first read the project state and resume from there.

The repository must contain enough information that a new Claude session with **zero previous chat context** can continue correctly.

# Autonomy

You have full authority to manage this project within its scope.

Do not repeatedly ask me for permission for normal research, coding, organization, refactoring, website, schema, testing, or technical decisions.

You may:

* research;
* create/edit/reorganize files;
* choose libraries;
* write/refactor code;
* run tests;
* fix errors;
* improve the architecture;
* revise earlier decisions;
* design automation.

Make the best reasonable decision and log important decisions.

Only stop for genuinely high-impact external actions such as credentials/secrets, paid services, destructive external actions, or public publishing that requires my approval.

# Model / Credit Strategy

I am currently using **Fable 5.1 in Plan Mode**.

Right now, stay focused on **planning**.

Do not start heavy implementation or process a huge literature set yet.

I want to conserve credits.

Use cheaper/faster models for routine work.

Clearly tell me when it is worth switching to **Opus**, especially for:

* deep reading of difficult papers;
* synthesis across many papers;
* resolving conflicting research;
* important taxonomy decisions;
* major architecture decisions;
* reviewing critical research content;
* difficult implementation problems.

Do NOT use Opus for routine metadata extraction, simple searches, formatting, repetitive updates, or easy code.

# What I Want From You Now


For this first response, produce the project blueprint only:

1. scope: in / brief background / out;
2. best taxonomy;
3. major modern research families;
4. initial high-value paper/model map;
5. website structure and visual approach;
6. knowledge/data schema;
7. GitHub structure;
8. 3-day update architecture;
9. model strategy: Fable vs Opus vs deterministic scripts;
10. implementation phases;
11. exact first sprint.

Do not start building the full project yet.

Do not give me hundreds of papers.

Start with the **smallest high-quality backbone of the field**.

The central rule for this project is:

> **Do not organize the field around papers. Organize papers around the ideas, representations, objectives, architectures, capabilities, and problems that caused the field to evolve.**

At the end, tell me what you think should be the **single central organizing idea of the website**.



