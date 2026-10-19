# Runnable learning workspace

## Purpose and ownership

Users clone tutorials to execute complete learning workflows on their own
machines. This branch starts fresh; the former notebooks, themes, converter,
and requirements remain on `main` as archive material. The branch retains Git
ancestry for provenance; its working tree does not depend on the legacy stack.

Tutorials own executable teaching sequences, end-to-end examples, presentations,
and workshops. Package guides own software usage. Each software repository owns
its maintained architecture specifications and review decks. `tolteca_dr`
provides discovery; helpdesk cases link to the sources. `tolteca_agent` consumes
authored source material independently of human Llama inference.

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
