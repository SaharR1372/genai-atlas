"""
Tests for the living-update pipeline's filtering logic. No network calls: every test
feeds synthetic candidates through the scorer.

The precision of this filter is the whole value of the pipeline — without the core-topic
gate, LLM and perception papers flood the review queue, which is exactly what happened
on the first live run.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.discover import Candidate  # noqa: E402
from pipeline.score import assess, load_atlas_index, _norm_title  # noqa: E402


@pytest.fixture(scope="module")
def atlas():
    return load_atlas_index()


def cand(title, abstract="", authors=None, arxiv="2699.99999", upvotes=None):
    return Candidate(
        arxiv=arxiv, title=title, abstract=abstract, authors=authors or [],
        published="2026-09-01", hf_upvotes=upvotes,
    )


def test_image_generation_paper_is_admitted(atlas):
    a = assess(
        cand(
            "Scaling Text-to-Image Diffusion Transformers with Better Latents",
            "We train a diffusion transformer for text-to-image generation. Code is available at github.com/x.",
            authors=["Saining Xie"],
        ),
        atlas,
    )
    assert a.excluded_by is None
    assert "generation" in a.sections
    assert a.admitted


def test_llm_agent_paper_is_rejected(atlas):
    """The failure mode from the first live run: agent/LLM work shares the vocabulary."""
    a = assess(
        cand(
            "NeoHorse-1: Recursive Self-Improvement via Agentic Post-Training",
            "We present a generative model trained with a post-training recipe for agentic reasoning.",
        ),
        atlas,
    )
    assert not a.admitted
    assert a.excluded_by is not None


def test_depth_estimation_paper_is_rejected(atlas):
    a = assess(
        cand(
            "Marigold V2: Revisiting Diffusion Transformers for Monocular Depth Estimation",
            "We adapt a latent diffusion model for depth estimation from a single image.",
        ),
        atlas,
    )
    assert not a.admitted
    assert a.excluded_by == "depth estimation"


def test_video_paper_is_rejected_per_d005(atlas):
    a = assess(
        cand(
            "A Flow Matching Approach to Text-to-Video Generation",
            "We extend rectified flow to video generation.",
        ),
        atlas,
    )
    assert not a.admitted
    assert a.excluded_by is not None


def test_paper_without_core_topic_is_rejected(atlas):
    """Mentioning 'latent space' or 'generative model' alone is not enough."""
    a = assess(
        cand(
            "On the Geometry of Latent Spaces in Contrastive Learning",
            "We study the latent space of a generative model for representation learning.",
        ),
        atlas,
    )
    assert not a.admitted
    assert a.excluded_by == "no core image-generation term"


def test_core_topic_in_title_scores_higher_than_in_abstract_only(atlas):
    in_title = assess(
        cand("Image Editing with Better Priors", "We do things."), atlas
    )
    in_abstract = assess(
        cand("Better Priors", "We study image editing with better priors."), atlas
    )
    assert in_title.score > in_abstract.score


def test_paper_already_in_atlas_is_flagged_duplicate(atlas):
    """RAE is in the atlas at 2510.11690; rediscovering it must not create a candidate."""
    a = assess(
        cand("Diffusion Transformers with Representation Autoencoders",
             "...", arxiv="2510.11690"),
        atlas,
    )
    assert a.duplicate_of is not None
    assert not a.admitted


def test_duplicate_detected_by_title_when_arxiv_id_differs(atlas):
    a = assess(
        cand("Diffusion Transformers with Representation Autoencoders",
             "...", arxiv="2699.00001"),
        atlas,
    )
    assert a.duplicate_of == "title match"


def test_hf_upvotes_raise_the_score(atlas):
    quiet = assess(cand("Image Generation with X", "text-to-image diffusion model"), atlas)
    loud = assess(cand("Image Generation with X", "text-to-image diffusion model", upvotes=200), atlas)
    assert loud.score > quiet.score


def test_title_normalisation_ignores_punctuation_and_case():
    assert _norm_title("Foo-Bar: A Study!") == _norm_title("foo bar a study")
