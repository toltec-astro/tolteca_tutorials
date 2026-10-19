# TolTECA tutorials

Clone this repository to run TolTEC learning workflows on your own machine.
It brings together runnable examples, teaching presentations, and workshops
across the TolTECA software packages.

This branch starts the v3 collection afresh. The previous collection remains
on the archive branch, currently `main`. Its notebooks and build system are
outside this branch's environment and content.

## Get started

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and
[Git LFS](https://git-lfs.com/). Clone the two repositories as siblings:

```sh
git clone --branch codex/v3-learning-materials https://github.com/toltec-astro/tolteca_tutorials.git
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/toltec-astro/tolteca_ref_data.git
cd tolteca_tutorials
uv sync --locked
```

The tutorial branch must be published before the clone command can be used
remotely. In a local checkout, start with `uv sync --locked`.

Follow [reference-data setup](datasets/README.md) to retrieve the small pinned
dataset for the first example. Then open JupyterLab:

```sh
uv run --locked jupyter lab
```

Open [Inspect reference data](workflows/inspect-reference-data/inspect_reference_data.ipynb)
and run its cells in order. It verifies one telescope file's checksum, reads
its observation identifiers, and saves a small provenance report under `_build/`.
The data files are opened read-only.

To run the same notebook without a browser:

```sh
uv run --locked jupyter execute workflows/inspect-reference-data/inspect_reference_data.ipynb --timeout=120
```

The committed `uv.lock` fixes the environment's package versions. The first
sync and data retrieval need network access; the installed notebook runs
offline. The first workflow uses NetCDF inspection to verify the environment
and data pairing. Full TolTECA observation-planning, archive-analysis, and
reduction recipes are still to be added with their own tested software versions.

## Find learning material

| Collection | Purpose |
| --- | --- |
| [Workflows](workflows/README.md) | Complete tasks with inputs, executable steps, outputs, and checks |
| [Presentations](presentations/README.md) | Ecosystem introductions and workflow teaching decks |
| [Workshops](workshops/README.md) | Teaching sequences with slides and exercises together |
| [Reference data](datasets/README.md) | Pair this checkout with versioned data from `tolteca_ref_data` |
| [Agent index](llms.txt) | Authored discovery material and compatibility status |

Package documentation owns software usage and API details. Maintained software
specifications and architecture review decks stay in each owning repository's
`design/` directory. The TolTEC landing page and helpdesk link to this collection
for complete learning workflows.

See [Contributing](CONTRIBUTING.md) to add material, and
[the project design](design/spec.md) for ownership and reproducibility decisions.
