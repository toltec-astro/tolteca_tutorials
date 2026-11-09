# Runnable learning workspace

## Purpose and ownership

Users clone tutorials to execute complete learning workflows on their own
machines. This branch starts fresh; the former notebooks, themes, converter,
and requirements remain on `main` as archive material. The branch retains Git
ancestry for provenance; its working tree does not depend on the legacy stack.

Tutorials own the extended materials: executable teaching sequences, end-to-end
examples, teaching presentations, workshops, the TolTEC Data Handbook
(`handbook/`), and the developer architecture review decks with their evidence
and example checks (`architecture/`). They also own the tooling that builds,
runs and previews these materials from a checkout (`slides/` for Marp decks,
`just handbook` for the book, locked notebook execution). Package guides
own software usage, and each software repository owns its specification and
design records; a deck explains selected parts of a specification and names
it. `tolteca_helpdesk` owns the rules for where materials live, the landing
page and helpdesk services, and serving built materials in a deployment;
`tolteca_dr` provides discovery and `tolteca_agent` consumes authored material
independently of human Llama inference.

## Slides

- Decks are Marp Markdown. `slides/` holds the pinned Marp toolchain
  (`package.json`, lock), the shared configuration, the themes and the deck
  index. `build-all` builds every deck under `architecture/`, the teaching
  presentations and the deck index into `_build/slides/`, which Git ignores,
  or into the directory given with `--output`. The index links only to built
  decks and, for sources and evidence, to the repository on GitHub. A
  deployment publishes the HTML build through `tolteca_dr`.
- Each architecture deck is a folder `architecture/<deck>/` with the source,
  its `<deck>-evidence.md` record of inspected revisions and executed checks,
  and `probes/` that execute its examples or render its figures against the
  sibling package checkouts of the development workspace.

## Handbook

- The TolTEC Data Handbook explains the instrument measurement and its
  transformation into scientific data, so astronomers can interpret products,
  assess quality, perform an analysis, and choose when and how to reprocess
  observations. Chapters follow that scientific progression, with entry points
  for prepared-product users and independent reducers.
- File-field details belong in supporting reference material. Package guides
  keep command and API details. Workflows and workshops in this repository keep
  the executable examples; chapters link to them at the step they illustrate.
- The handbook glossary owns the definitions of shared scientific and workflow
  terms. Package guides and other materials link to it.
- Operations procedures and internal architecture stay outside the handbook.
- `handbook/` is one Sphinx book in MyST Markdown, with contents, search, an
  edition and a review status. The first edition is a draft: it does not certify
  release compatibility or complete scientific recipes.
- `handbook/evidence/` holds the editorial record and the primary-source
  evidence; `handbook/probes/` holds the scripts behind them. Neither is part of
  the book.
- `just handbook` builds the book strictly into `_build/handbook/`, which Git
  ignores. Deployments publish it through `tolteca_dr`.

## Reproducible execution

The repository is a uv project without a distributable Python package. Python
3.13 matches the v3 development floor. `pyproject.toml` declares the notebook
environment; committed `uv.lock` resolves it. Users run commands with `--locked`
so a stale environment declaration fails rather than changing the lock.

JupyterLab and its Python kernel share this environment. Notebook validation
uses nbclient with errors fatal and a bounded per-cell timeout. Source notebooks
retain stable cell IDs and no outputs; generated reports and exports use
`_build/`. No CI or hosting service is configured in this scaffold.

The first workflow verifies a pinned reference file and reads native NetCDF
metadata. It proves the notebook/data setup only. Future planning, archive
analysis, and reduction workflows must record their tested TolTECA package
versions and deployment requirements before being marked runnable.

## Pairing with reference data

`tolteca_ref_data` remains a separate repository. There is no nesting, submodule,
vendored payload, or requirement to merge the two repositories. The default
layout uses sibling checkouts; `TOLTECA_DATA_LMT` selects any existing data tree,
including a deployment location's `run/data_lmt`.

Each example identifies its input revision and files. The starter manifest
records the upstream Git LFS byte count and SHA-256, plus expected observation
identity and array shape. The notebook verifies the payload before reading it.
An existing checkout may be at another revision when the required file bytes
match. Inputs remain read-only; the tutorial owns all generated outputs.

The data revision, tutorial revision, environment lock, and any science release
identifier are distinct provenance fields. The starter uses a reference
acquisition, not a science release.

## Tooling references

The setup follows current primary documentation inspected on 2026-10-19:

- [uv project locking](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
- [nbclient execution](https://nbclient.readthedocs.io/en/latest/client.html)
- [Git LFS collaboration](https://docs.github.com/en/repositories/working-with-files/managing-large-files/collaboration-with-git-large-file-storage)
