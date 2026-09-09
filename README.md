# Generative Vision Atlas

A living research atlas of modern generative vision (2023–2026): a website and structured knowledge
base organized around ideas, representations, objectives, architectures, and open problems — not a
paper list. See [`docs/blueprint.md`](docs/blueprint.md) for the full project design.

**Starting a new session? Read [`CLAUDE.md`](CLAUDE.md) first, then
[`PROJECT_STATE.md`](PROJECT_STATE.md).**

## Central organizing idea

**Follow the representation.** Objectives and architectures have largely converged on flow-matching
transformers; what now moves the field is representational — what latent space a model generates in,
and what gets traded away to get there. See `docs/blueprint.md` for the full taxonomy.

## Repository layout

```
docs/            blueprint, taxonomy rationale, frontier recon notes
schema/          JSON Schema for every entity type (paper, concept, system, relation, ...)
data/            one YAML file per entity — the structured knowledge base
content/         long-form MDX narratives, referenced by id from data/
site/            the Astro website
scripts/         validate.py, build_graph.py, verify_paper.py
tests/           pytest suite for the scripts above
pipeline/        the 3-day living-update pipeline (not built yet — see PROJECT_STATE.md)
```

## Working with the data

```bash
python3 -m venv .venv && .venv/bin/pip install PyYAML jsonschema requests pytest   # first time only
.venv/bin/python scripts/validate.py                        # schema + referential integrity
.venv/bin/python scripts/build_graph.py                     # data/**/*.yaml -> site/{src/data,public}/graph.json
.venv/bin/python -m pytest                                   # test suite
.venv/bin/python scripts/verify_paper.py <paper-id>          # fetch arXiv metadata, flip status.verified
```

Never hand-edit `site/src/data/graph.json` or `site/public/graph.json` — both are generated from
`data/` and gitignored. Every explanatory claim about a paper should follow a fetch: see Decision
D004 in [`DECISIONS.md`](DECISIONS.md).

## Running the site

```bash
cd site
npm install
npm run dev      # regenerates graph.json, then starts the dev server
npm run build    # regenerates graph.json, builds static output, indexes it with Pagefind
npm run preview  # serve the built site locally
```

## Status

Sprint 1 (repo skeleton, schemas, RAE-spine seed data, Astro scaffold) — see `PROJECT_STATE.md` for
exactly what's done and what's next.
