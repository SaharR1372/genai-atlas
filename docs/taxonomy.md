# Taxonomy rationale

Full text in `blueprint.md` §2. Summary:

- **Layer A — Design axes.** Representation · Objective · Architecture · Conditioning & control ·
  Training signal · Inference. Every system is a point in this space; the field moves when one axis
  becomes the binding constraint.
- **Layer B — Sections.** generation · rae · editing · unified · vfm · vlm · medical. Capability
  domains with a subtle color identity each; they cut across the axes.
- **Layer C — Evolution.** Transitions (why the field moved, what it cost), Open problems (where it
  is going), Timeline graph (how branches converge).

Why not the user's original flat list: "capabilities" (what a system is for) and "transitions"
(history) are different kinds of thing from design choices, and two decisive axes (training signal,
inference) were missing. Evaluation is not an axis but is first-class via `benchmark` and `result`
entities.

Central organizing idea: **Follow the representation.**
