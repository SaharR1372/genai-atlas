#!/usr/bin/env python3
"""
Build and execute the atlas's runnable notebooks, so the versions committed to the repo
carry real outputs from a real GPU rather than promises.

    python notebooks/build.py                 # build + execute all
    python notebooks/build.py latents         # just one, by stem
    python notebooks/build.py --no-exec       # write the .ipynb without running it

Notebooks are defined in notebooks/specs/*.py, each exposing `TITLE`, `INTRO`, `CREDITS`
and `CELLS` (a list of (kind, source) where kind is "md" or "code"). Keeping the spec as
plain Python rather than raw .ipynb JSON means the sources stay reviewable in a diff.

Every notebook assembles the upstream authors' own material. Each code cell that uses a
released model credits the repository it comes from.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent
SPECS = ROOT / "specs"
OUT = ROOT

# The environment that actually has torch + diffusers on this machine.
KERNEL_PYTHON = "/home/exx/anaconda3/envs/dediffusion/bin/python"


def load_spec(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(mod) -> nbformat.NotebookNode:
    cells = [
        new_markdown_cell(f"# {mod.TITLE}\n\n{mod.INTRO}\n\n---\n\n{mod.CREDITS}")
    ]
    for kind, src in mod.CELLS:
        cells.append(new_markdown_cell(src) if kind == "md" else new_code_cell(src))
    nb = new_notebook(cells=cells)
    nb.metadata.kernelspec = {
        "display_name": "Python 3", "language": "python", "name": "python3",
    }
    nb.metadata.language_info = {"name": "python"}
    return nb


def execute(nb, cwd: Path):
    from nbclient import NotebookClient

    client = NotebookClient(
        nb,
        timeout=1800,
        kernel_name="python3",
        resources={"metadata": {"path": str(cwd)}},
        allow_errors=False,
    )
    client.execute()
    return nb


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    no_exec = "--no-exec" in sys.argv

    specs = sorted(SPECS.glob("*.py"))
    if args:
        specs = [s for s in specs if s.stem in args]
    if not specs:
        print("no matching specs")
        return 1

    for path in specs:
        mod = load_spec(path)
        print(f"\n=== {path.stem}: {mod.TITLE} ===")
        nb = build(mod)
        if not no_exec:
            print("  executing...")
            try:
                nb = execute(nb, ROOT)
            except Exception as e:  # noqa: BLE001
                print(f"  EXECUTION FAILED: {type(e).__name__}: {e}")
                print("  writing the un-executed notebook so the failure is visible in review")
        out = OUT / f"{path.stem}.ipynb"
        nbformat.write(nb, out)
        print(f"  wrote {out.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
