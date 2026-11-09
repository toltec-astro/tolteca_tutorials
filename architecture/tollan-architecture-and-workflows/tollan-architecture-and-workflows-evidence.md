# Tollan deck evidence

> Moved on 2026-11-07 from `tollan/design/` to `tolteca_tutorials/architecture/tollan-architecture-and-workflows/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/tollan-architecture-and-workflows/probes/` and build from `slides/`.

## Scope and baseline

- Date: 2026-10-15.
- Tollan revision: `3c765d4`, `Add artifact and database infrastructure with aligned contracts`.
- Purpose: technical architecture and API overview, approximately 20 minutes.
- Deliverables: 16-slide editable Markdown source and embedded HTML presentation.
- No Tollan-specific deck was found under the repository's ignored design files,
  refs, or inspected Git history. Other domain decks belong to TolTECA.
- The maintained [specification](../../../tollan/design/spec.md) owns the contracts. The deck selects
  those contracts for presentation. It introduces no new package requirements.
- Package source, tests and public documentation source remain unchanged.
  New presentation assets and regenerated documentation are ignored local files.

## Claim sources

| Slides | Contract and implementation evidence |
| --- | --- |
| 1–2 | [Overview and domains](../../../tollan/design/spec.md), [documentation entry paths](../../../tollan/docs/index.md) |
| 3–4 | [Data access contract](../../../tollan/design/spec.md#data-access-and-representation), [mapping examples](../../../tollan/docs/schema-mapping-accessors.md), [adapters](../../../tollan/docs/data-adapters.md), `src/tollan/accessor/` |
| 5 | [Model tables](../../../tollan/design/spec.md#model-tables), [projection and enrichment examples](../../../tollan/docs/model-tables.md), `src/tollan/accessor/pandas/model_table.py` |
| 6–7 | [Configuration contract](../../../tollan/design/spec.md#application-configuration), [runtime examples](../../../tollan/docs/configuration.md), [CLI examples](../../../tollan/docs/cli.md) |
| 8–9 | [API levels](../../../tollan/design/spec.md#concepts-and-responsibilities), [analyses](../../../tollan/docs/analyses.md), `src/tollan/accessor/xarray/analysis.py` |
| 10–11 | [Step contract](../../../tollan/design/spec.md#steps-and-pipelines), [pipeline example](../../../tollan/docs/examples/pipeline_example.py), `src/tollan/pipeline/step.py` |
| 12–13 | [Artifact contract](../../../tollan/design/spec.md#artifacts-and-visualization), [artifact guide](../../../tollan/docs/artifacts.md), [visualization example](../../../tollan/docs/examples/artifact_example.py), `src/tollan/pipeline/artifact.py`, `src/tollan/plot/viz.py`, `src/tollan/plot/plotly.py` |
| 14–15 | [Database contract](../../../tollan/design/spec.md#database-resources), [database guide](../../../tollan/docs/databases.md), `src/tollan/db/`, [supporting utilities](../../../tollan/design/spec.md#supporting-utilities) |
| 16 | Integrated handoffs under the corresponding domains in [the specification](../../../tollan/design/spec.md) |

Actual database consumers inspected include `tolteca_db/src/tolteca_db/core.py`
and `tolteca_web/src/tolteca_web/db.py`. They create owned resources and wrap
borrowed engines respectively. They do not define Tollan's consumer policy.

## Contract and implementation status

- Displayed APIs are implemented at the inspected Tollan revision.
- `ObservationMapper`, `SearchHandler`, `MeanAnalysis`, `MeanView`, `Scale`,
  `RecordSpec` and `SignalViz` are guide example classes. Speaker notes identify
  their definitions; the probe supplies their setup.
- The diagrams describe mapping dependencies and possible workflow transfers.
  They do not prescribe a single mandatory pipeline.
- DAG scheduling is a permitted execution strategy. The deck does not claim
  that Tollan ships a DAG scheduler integration.
- Restored result access is an input contract, not a storage-backend guarantee.
- Context pickle transport is not checkpoint/resume.
- No contract discrepancy requiring a package change was identified in the
  selected presentation scope. This is not a new package-wide audit.

## Executed checks

### Documentation

- Regenerated API stubs and built fresh HTML with nitpicky references,
  warnings-as-errors and keep-going enabled.
- Ran doctests in a separate process against the generated doctrees:
  **90 tests, zero failures**, including setup and cleanup.
- Reused cached external inventories. Live external target URLs were not checked.
- The installed/generated package version still named the preceding commit.
  The local build sets Sphinx `version` and `release` to Git's exact source
  description, `v3.0.0-85-g3c765d4`. It does not change package version machinery.
- Output: `../docs/_build/html/` and `../docs/_build/doctest/`.
- Build runner and command logs are copied into
  `slides/.qa/tollan-architecture-and-workflows/`.
- Inspected the rebuilt index and artifact guide. The browser reported one
  Sphinx-theme message about an empty saved color mode, then reset it to auto.
  The pages rendered normally. No theme-source change was made.

### Runnable examples

- Ran [the probe](probes/tollan_architecture_and_workflows.py).
- Executed all nine displayed Python blocks and the CLI invocation.
- Checked mapper reuse reads the supplied source, projected rows, configuration
  snapshot stability, analysis layout and producing settings, step data identity
  and payload, middle-level context behavior, numerical results and input
  preservation, JSON artifact selection, reference retention, HTML figure export,
  and SQL transaction visibility.
- Output files used temporary directories. No reference input was modified.
- These examples do not establish production performance, distributed execution,
  arbitrary payload picklability or database-dialect coverage.

### Presentation

- Marp CLI 4.5.1, Marp Core 5.0.2; shared dependencies remain pinned in
  `../../tolteca/design/slides/package-lock.json` from the workspace layout.
- HTML contains 16 slides and four inline Mermaid SVG diagrams.
- No external script, stylesheet, image, media or frame assets were found.
  No remote CSS imports remain.
- Inspected all rendered slides at the normal 1280 × 720 viewport. Simplified
  crowded slides and rerendered them without reducing body text.
- Checked all slide bounds at 1024 × 768 and visually inspected the dense tables,
  analysis layout, database example and final diagram. Reset the viewport after QA.
- Arrow-key navigation, overview, topic links and hash deep links work.
- The deck reported no browser console warnings or errors.
- Direct presenter view shows notes and supports navigation. The in-app browser
  did not expose a popup from the `p` shortcut. Cross-window synchronization is
  unverified.
- The browser security policy blocks `file:` URLs. Direct-from-disk and
  network-disabled playback were not verified. Local HTTP playback was verified.
- No PDF or PowerPoint export was requested or produced.

## Build and review

- Build and preview commands: [slides/README.md](README.md).
- Local preview binds only to `127.0.0.1:8872`.
- Workspace review diff: `/tmp/toltec-python-workspace-review.diff`, regenerated
  at handoff. Its baseline is each repository's Git HEAD. Ignored presentation
  files do not appear in that diff.
