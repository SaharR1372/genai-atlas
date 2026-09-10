"""
Configuration for the living-update pipeline: what counts as relevant, what counts as
high quality, and where to look. Deliberately data, not logic — tune this file rather
than editing the pipeline stages.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CANDIDATES = DATA / "monitor" / "candidates"
STATE_FILE = DATA / "monitor" / "state.json"

# arXiv categories worth scanning at all.
ARXIV_CATEGORIES = ["cs.CV", "cs.LG", "cs.AI"]

# How far back a normal run looks. The cron runs every 3 days; the extra day is slack
# for a missed or delayed run.
LOOKBACK_DAYS = 4

# ---------------------------------------------------------------------------
# Relevance: a candidate must hit at least one section's terms to survive at all.
# Keys match the `section` enum in schema/common.schema.json.
# ---------------------------------------------------------------------------
SECTION_TERMS: dict[str, list[str]] = {
    "generation": [
        "text-to-image", "image generation", "diffusion transformer", "flow matching",
        "rectified flow", "latent diffusion", "autoregressive image", "masked generative",
        "one-step generation", "few-step", "distillation", "classifier-free guidance",
        "image synthesis", "generative model",
    ],
    "rae": [
        "representation autoencoder", "latent space", "tokenizer", "visual tokenizer",
        "vae", "representation alignment", "semantic latent", "foundation model features",
        "dinov2", "dinov3", "siglip", "latent manifold", "reconstruction", "vq",
    ],
    "editing": [
        "image editing", "instruction-based editing", "inversion", "in-context editing",
        "reference-guided", "identity preservation", "controlnet", "inpainting",
        "attention control", "subject-driven",
    ],
    "unified": [
        "unified multimodal", "understanding and generation", "any-to-any",
        "multimodal llm", "interleaved generation", "native multimodal",
    ],
    "vfm": [
        "self-supervised", "vision foundation model", "visual representation learning",
        "masked autoencoder", "contrastive", "image encoder",
    ],
    "vlm": ["vision-language model", "multimodal understanding", "visual question answering"],
    "medical": [
        "medical image", "radiology", "chest x-ray", "mri", "ct scan", "histopathology",
        "pathology", "clinical", "lesion", "segmentation", "diagnosis", "counterfactual",
    ],
}

# A hard gate. The atlas is about generating and editing IMAGES; a paper must show
# evidence of that, not merely use the word "generative" or "latent". Without this
# gate, LLM post-training and depth-estimation papers dominate the queue, because they
# share most of the vocabulary. Checked against title + abstract.
REQUIRED_CORE_TERMS = [
    "image generation", "image synthesis", "text-to-image", "image editing",
    "image generator", "generate images", "generating images", "generated images",
    "image tokenizer", "visual tokenizer", "latent diffusion", "diffusion transformer",
    "diffusion model", "flow matching", "rectified flow", "autoregressive image",
    "masked image generation", "image inpainting", "subject-driven generation",
    "representation autoencoder", "image reconstruction", "visual generation",
    "unified multimodal", "understanding and generation", "medical image synthesis",
]

# Terms that mean "out of scope for this atlas" even if a section term matched (D005),
# plus adjacent fields that share vocabulary but are not generative vision.
EXCLUDE_TERMS = [
    # other modalities (D005)
    "video generation", "text-to-video", "video diffusion", "image-to-video",
    "3d generation", "nerf", "gaussian splatting", "mesh generation", "point cloud",
    "novel view synthesis", "speech synthesis", "audio generation", "text-to-speech",
    "music generation", "protein", "molecule", "molecular", "motion generation",
    # adjacent vision tasks that are perception, not generation
    "depth estimation", "surface normal", "optical flow estimation", "object detection",
    "semantic segmentation benchmark", "pose estimation", "visual tracking",
    # LLM / agent work that shares generative vocabulary
    "world model", "world-action", "agentic", "agent framework", "tool use",
    "reasoning path", "chain-of-thought reasoning", "post-training recipe",
    "reinforcement learning from human feedback for language",
    "code generation", "math reasoning", "retrieval-augmented",
]

# ---------------------------------------------------------------------------
# Quality signals. None of these alone admits a paper; they produce a score that
# ranks the candidate queue for human/model review (D006: nothing auto-merges).
# ---------------------------------------------------------------------------
STRONG_ORGS = [
    "google", "deepmind", "openai", "meta", "fair", "microsoft", "nvidia", "adobe",
    "apple", "alibaba", "qwen", "bytedance", "seed", "tencent", "hunyuan", "kuaishou",
    "kling", "stability", "black forest", "baai", "deepseek", "stepfun", "moonshot",
    "mit", "stanford", "berkeley", "cmu", "carnegie mellon", "nyu", "princeton",
    "oxford", "cambridge", "eth", "tsinghua", "peking", "hku", "cuhk", "nus", "kaist",
]

# Authors whose involvement is a strong signal in this specific field. Kept short and
# purely as a ranking hint, never as an automatic admit.
NOTABLE_AUTHORS = [
    "Kaiming He", "Saining Xie", "Yaron Lipman", "Tianhong Li", "Song Han",
    "Bjorn Ommer", "Robin Rombach", "Patrick Esser", "Jiaming Song", "Stefano Ermon",
    "Yann LeCun", "Rob Fergus", "Nanye Ma", "Shengbang Tong", "Xinlei Chen",
]

SCORE_WEIGHTS = {
    "section_hit": 2.0,       # per distinct section matched
    "strong_org": 3.0,
    "notable_author": 3.0,
    "cites_atlas_paper": 4.0,  # references something already in the atlas
    "has_code": 2.0,
    "title_signal": 2.0,       # title contains a high-signal phrase
    "core_in_title": 4.0,      # the core image-generation topic is in the title, not just the abstract
}

# Phrases in a title that usually mark a substantive contribution rather than an
# incremental application.
TITLE_SIGNALS = [
    "scaling", "we introduce", "rethinking", "revisiting", "what matters",
    "a systematic study", "towards", "unified", "beyond", "efficient",
]

# Candidates scoring below this are recorded in the run log but not written as
# candidate files, to keep the review queue readable.
MIN_SCORE = 6.0
