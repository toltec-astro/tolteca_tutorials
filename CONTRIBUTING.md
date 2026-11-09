# Contribute learning material

Organize each contribution around a complete user task. Put each item in the
folder for its kind:

| Folder | Holds |
| --- | --- |
| `workflows/<task>/` | Runnable workflows |
| `presentations/<topic>/` | Standalone teaching decks |
| `workshops/<topic>/` | Workshop slides and exercises together |
| `architecture/<deck>/` | Developer architecture decks, each with an evidence note and probes ([architecture decks](architecture/README.md)) |
| `handbook/` | The TolTEC Data Handbook sources; build with `just handbook` |
| `slides/` | The shared slide toolchain that builds every deck ([slide toolchain](slides/README.md)) |

Each item needs a goal, prerequisites, an executable sequence, expected outputs,
and checks. Record applicable software versions, data identities, validation
date and platform, and limitations. Distinguish a draft from an executed example.
Link package guides for software details. Architecture specifications stay in
the owning software repository; the decks that review them go in
`architecture/`.

## Environment and data

Use the committed `pyproject.toml` and `uv.lock`. Add dependencies deliberately
with `uv add`, then rerun the affected workflows. Do not install packages from
notebook cells. If a future recipe needs a separate reduction deployment, link
the package-owned deployment instructions and record the tested revisions and
configuration. A local editable development checkout does not establish that a
fresh remote clone can run the recipe.

Pair examples with the separate `tolteca_ref_data` repository or a documented
archive dataset. Record revision, file paths, byte counts, and checksums in a
data manifest. Keep input files read-only and generated results under `_build/`
or another ignored output directory. Do not add nested data repositories,
submodules, or copied reference payloads to this repository.

## Notebook sources and validation

Commit notebooks with stable cell IDs and no execution counts or outputs.
Use relative project paths and a configurable data root, never a developer's
absolute path. Keep actual workflow operations visible in the notebook.

From the repository root:

```sh
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python scripts/check_notebooks.py
uv run --locked jupyter execute workflows/inspect-reference-data/inspect_reference_data.ipynb --timeout=120
```

The `just check` and `just execute` recipes run these checks. Execute new
workflows from a clean kernel against their documented inputs. Keep errors
fatal. Record results beside the workflow, with the data and environment
identities. Build/preview instructions accompany slide sources; generated
exports go under `_build/` until published with their source revision.

Update the relevant collection README and `llms.txt` so the landing page,
helpdesk, and agents can discover the material without duplicating it.
