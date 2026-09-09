"""
Loads the scripts/*.py modules by path (scripts/ is not a package) so tests can
import their functions directly instead of shelling out to subprocess for every
case. Shared fixtures live here.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def validate_mod():
    return _load_module("scripts_validate", "validate.py")


@pytest.fixture(scope="session")
def build_graph_mod():
    return _load_module("scripts_build_graph", "build_graph.py")


@pytest.fixture(scope="session")
def verify_paper_mod():
    return _load_module("scripts_verify_paper", "verify_paper.py")


@pytest.fixture
def sample_data_dir(tmp_path, monkeypatch):
    """
    A minimal, self-consistent data/ tree (one concept, one paper, one relation)
    that tests can mutate to check specific failure modes, without touching the
    real repo data.
    """
    data = tmp_path / "data"
    for sub in ("concepts", "papers", "systems", "problems", "benchmarks",
                "results", "transitions", "paths", "updates", "relations"):
        (data / sub).mkdir(parents=True)

    (data / "concepts" / "flow-matching.yaml").write_text(
        "id: flow-matching\n"
        "type: concept\n"
        "name: Flow matching\n"
        "axis: objective\n"
        "one_line: Regress a straight-line velocity field between noise and data.\n"
    )
    (data / "papers" / "sd3-2024.yaml").write_text(
        "id: sd3-2024\n"
        "type: paper\n"
        "title: Scaling Rectified Flow Transformers for High-Resolution Image Synthesis\n"
        "date: '2024-03'\n"
        "tier: landmark\n"
        "sections: [generation]\n"
        "axes:\n"
        "  objective: [flow-matching]\n"
        "status: {code: released, weights: released, verified: false}\n"
        "summary: Placeholder.\n"
    )
    (data / "relations" / "generation.yaml").write_text(
        "- from: sd3-2024\n"
        "  to: flow-matching\n"
        "  type: uses_objective_from\n"
        "  evidence: SD3 trains with the rectified-flow objective.\n"
        "  confidence: high\n"
        "  added_by: sonnet\n"
        "  status: verified\n"
    )
    return data
