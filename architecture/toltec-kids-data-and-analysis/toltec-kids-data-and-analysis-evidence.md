# KIDs processing and analysis — current presentation evidence

> Moved on 2026-11-07 from `tolteca/design/` to `tolteca_tutorials/architecture/toltec-kids-data-and-analysis/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-kids-data-and-analysis/probes/` and build from `slides/`.

Date: 2026-10-19. Scope: requested architecture deck split and current API updates.
The deck contains 14 main slides and 6 appendix/reference slides.

## Contract and implementation

The specifications remain authoritative. This update changes slide sources,
build/preview tooling and presentation probes only. Relevant working trees contain
substantial pre-existing changes; HEAD alone does not identify the inspected code.

HEAD revisions: `tolteca` `486244a`, `tolteca_db` `c29e3b6`, `tolteca_web` `9db03d8`, `tollan` `72d90f5`, `tolteca_deploy` `5e7997c`.

Inspected current sources:

- [tolteca/src/tolteca_kids/core.py](../../../tolteca/src/tolteca_kids/core.py)
- [tolteca/src/tolteca_kids/runner.py](../../../tolteca/src/tolteca_kids/runner.py)
- [tolteca/src/tolteca_kids/sweep_check.py](../../../tolteca/src/tolteca_kids/sweep_check.py)
- [tolteca/src/tolteca_kids/sweep_check_viz.py](../../../tolteca/src/tolteca_kids/sweep_check_viz.py)
- [tolteca/src/tolteca_kids/product.py](../../../tolteca/src/tolteca_kids/product.py)
- [tolteca/src/tolteca_kidsproc/analysis/d21.py](../../../tolteca/src/tolteca_kidsproc/analysis/d21.py)
- [tolteca/src/tolteca_kidsproc/analysis/psd.py](../../../tolteca/src/tolteca_kidsproc/analysis/psd.py)

## Executed examples and scope

The updated KIDs probe passed all 13 displayed Python snippets on the 632-channel reference tune and numerical PSD inputs. It checks per-block contexts, figures, analysis views, interface-root Zarr publication and reopened execution records. Narrow channel selections failed the unchanged v2-derived checker baseline algorithm; the example now uses the complete recorded sweep. Algorithm changes are outside this slide update.

Logs and local render artifacts: `run/slides-split-20261019/` in the Python workspace.

## Build and visual review

HTML and PDF exports were rebuilt with Marp CLI 4.5.1 / Marp Core 5.0.2.
The seven-deck set contains 140 pages. All PDF pages were visually inspected;
HTML slide geometry and code clipping were checked at presentation and
1024×768 laptop viewports. Dense reference slides were reformatted without
changing the shared font sizes.

Contents links, numbered deep links, arrow-key navigation and overview were
exercised in the workflow deck. No browser console errors were recorded.
The presenter shortcut was attempted, but the in-app browser did not expose a
presenter window; presenter-popup behavior remains unverified there. Direct
file-URL opening is restricted by that browser, so HTML QA used the allowlisted
localhost preview. Fonts, scripts and diagrams are embedded; a network-disabled
browser run was not performed.

The presentation probes check reader, KIDs, telescope and configuration examples.
Focused Ruff E/F/I checks passed for the changed probes and preview script;
package-wide lint and Docker/Unity execution were outside this slide update.
Shared commands and the current deck index are in
[the slide tooling](../README.md).

## Historical evidence before the split

The following records retain their original dates, slide numbering and verification scope.
They do not describe the current organization.

# Build and verification record

Updated 2026-10-06. The 29-slide deck is a feature/design/API reference. Audience
context, verification narration and build details are deliberately outside the
slides. The reusable guideline records that distinction.

## Sources and baseline

This is the current working tree, including pending reducer integration, rather
than a released feature set:

- Tolteca ownership migration starts from HEAD `d2796ea`, including prior pending work.
- Tollan HEAD: `f9c2b67` (`Restore omitted API documentation and enforce numpydoc parsing`)
- Tolteca has unrelated and relevant pending changes. This deck update follows the reducer-ownership implementation. Reference inputs were read only.

| Slide subjects | Current source |
|---|---|
| Native acquisition, metadata, block tables | `tolteca/src/tolteca_datamodels/toltec/kids/{core,blocks}.py`, `toltec/metadata.py` |
| Block identification/creation, sweep/timestream reduction, export | `tolteca/src/tolteca_kids/{block_identify,block_create,blocks,accessor,sweep_reduce,timestream_reduce}.py` |
| Generic signal views | `tolteca/src/tolteca_kidsproc/accessors/` |
| D21 and PSD | `tolteca/src/tolteca_kidsproc/analysis/{d21,psd}.py` |
| Analysis scopes, ownership and reuse | `tollan/src/tollan/accessor/xarray/analysis.py` |
| Step lifecycle, typed contexts, aliases, failures, serialization | `tollan/src/tollan/pipeline/step.py` |
| Configured execution | `tolteca/src/tolteca_kids/{runner,core,noop,sweep_reduce,timestream_reduce,dataprod_output}.py` |

The kidsproc guides and configured reduction guide match the displayed APIs.
The historical architecture HTML is presentation context, not the behavioral
specification.

## Toolchain and commands

The user explicitly selected the cutting-edge/prerelease Marp channel.

- Marp Core **5.0.2**, using `@marp-team/marp-core/full`
- Marp CLI **4.5.1**
- Beautiful Mermaid **1.1.3**, Shiki **4.0.2**
- Node **24.10.0**, npm **11.6.0**
- Shared theme and build configuration: `slides/`
- Exact dependencies: `slides/package.json` and `slides/package-lock.json`

From `tolteca/design/slides/`:

```sh
npm ci
npm run build -- ../toltec-kids-data-and-analysis.md
npm run pdf -- ../toltec-kids-data-and-analysis.md
npm run preview
```

The PDF command needs a local supported browser. The review server used:

```sh
python3 -m http.server 8871 --bind 127.0.0.1 --directory tolteca/design
```

That server command runs from the workspace root. The HTML also contains its
styles, scripts and SVG diagrams, with no external script/font/image resources.
Network-disabled browsing was not separately emulated.

## Executed examples

From the workspace root:

```sh
toltec_astro_dev/.venv/bin/python tolteca/design/probes/toltec_kids_data_and_analysis.py
```

The check executes all **23 displayed Python snippets** and the CLI example, supplying the imports,
open-source lifetimes and named inputs omitted from the short slide fragments.
It asserts the relevant view properties, metadata/table selections, dimensions,
configuration recovery, numerical high/low-level agreement, PSD peak/units,
DataTree identity, detached-block round trip, compact native export/reopen,
spectra-only export, no-op execution, primary/aliased sweep contexts,
continuation after a recorded publication failure, a file-backed pickle round trip,
and both configured product formats. The CLI example supplies a temporary recipe
directory and a reference sweep filename in place of the displayed placeholders.

Inputs under `toltec_astro_dev/run/data_lmt/toltec/tcs/toltec0`:

- `toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc`
- `toltec0_145609_000_0002_2025_10_31_09_27_57.nc`

Select original channels 0 and 5. The tune contains two blocks. Block 1 reduces
to `iqlen=2, sweep=177`; D21's unified grid has 1169 bins. For the timestream,
select the first 256 samples and use `nperseg=64`; spectra have 33 frequency bins.
The numerical example uses two channels with a 16 Hz tone sampled at 128 Hz.
Stores are created in a temporary directory, not beside reference inputs.
The bounded checks passed. `slides/.qa/toltec-kids-data-and-analysis/` contains
the observed tree paths, dimensions and variables in `example-results.json`
and run output in `examples.log`.

### Dask D21 support

The earlier `Array.to_value` failure is resolved: unified-grid construction now
converts unit-aware frequency arrays to eager Hz values explicitly. The probe
requires the Dask-backed block result to match eager matched/unified arrays,
units and coverage. It no longer catches the old error. D21 remains eager.
Remote query performance, mixed acquisition detection, model solving and
joint telescope analysis are outside this check.

## Artifact verification

- HTML and PDF build successfully; 29 pages, three inline SVG diagrams.
- Every PDF page inspected after rasterization with Poppler; the corrected
  crowded pages were rendered again and inspected. Pipeline tree diagrams and
  dense slides were also inspected in the live browser.
- Final Poppler rasterization completed without diagnostics. Diagrams, text
  and tree glyphs inspected correctly.
- The preceding 28-slide HTML revision was visited for active-layout bounds after layout settled.
  Code, tables and tree paths fit within the slide. Overview and arrow-key
  navigation work.
- Dense slides checked at 1280×720 and 1024×768 browser sizes; temporary viewport
  overrides reset. The browser reported no console errors or warnings.
- Deep links were exercised while checking all slides.
- Presenter shortcut was exercised in the in-app browser; it did not expose a
  separate presenter window there. Presenter popup behavior in an external
  browser remains unverified.
- The source, HTML, PDF and evidence use the shared stem
  `toltec-kids-data-and-analysis` in `tolteca/design/`. Reusable build tooling
  lives in `tolteca/design/slides/`; checks live in `tolteca/design/probes/`.
- `just review` regenerates the workspace review diff. The repository's existing
  `design/` ignore rule also applies to these new artifacts. The reusable
  guideline remains in workspace `refs/`.

Framework sources: [Marp v5 announcement](https://github.com/orgs/marp-team/discussions/625),
[v5 Markdown](https://github.com/marp-team/marp-core/blob/v5.0.0/docs/markdown.md),
[Marp CLI](https://github.com/marp-team/marp-cli).

## Pipeline and step update — 2026-10-05

Slides 17–27 replace the single configured-pipeline overview with distinct API
and data contracts. Slides 1–16 retain the numerical/block workflow, apart from
the component manifest and revision date. The capability table includes the
configured reducer slice and checkpoint support.

| Contract | Evidence |
| --- | --- |
| Fresh context before `run`; normal completion from failures; exceptions re-raised | `tollan/src/tollan/pipeline/step.py`, `Step.__call__` and `SequentialPipeline.__call__` |
| Concrete config/context bindings and instance aliases | Same module, `Step.__init_subclass__`, `StepContext.make_step`, `StepContextDict` |
| Live typed sweep/time views in `context.data` | `tolteca_kids/{sweep_reduce,timestream_reduce}.py` |
| In-place invocation, previous result lifetime, file-backed and aliased pickle | `tests/tolteca_kids/test_reducer_contexts.py`; slide probe for primary pickle and live aliases |
| Output requires a completed live reduction; recorded failures allow later operations | `tolteca_kids/dataprod_output.py`; displayed missing-input/NoOp sequence |
| Runner source ownership and per-input config | `tolteca_kids/{runner,core}.py`; displayed `run_data` / `run_source` sequences |
| Explicit saved-context readers and separate scientific views | `tolteca_kids/product.py`; displayed sweep and timestream round trips |
| Saved contexts do not restore excluded views or attach themselves | Producing step's `load_context`; probe assertions on `data` and live context absence |
| CLI publication and reporting | `tolteca_kids/cli.py`; displayed CLI command exercised with a temporary recipe and real sweep |

Both configured reducers now use the acquisition/block hierarchy. Sweep
processing retains every sweep block and publishes the selected block's view
in its context. Timestream processing acts on the selected block. Slide 22 shows
their common acquisition structure and the distinct per-block result leaves.
The probe records both trees in `example-results.json`. Standalone
`SweepReducer(raw_dataset)` now uses the same block layout. Numerical arrays use
`reduce_samples` with explicit intervals. Details are recorded in the
[remaining-work audit](../../../tolteca/design/kids-block-pipeline-remaining-work-20261005.md).

The working tree's root owns the live context store. The live `tolteca_kids` node
stores source identity and the prepared input row. Product writers select what to
persist: both save context JSON on the exported `tolteca_kids` node and omit the
reserved live context store. Sweep products omit native samples while retaining
block metadata, axes, model parameters and reduced sweeps. Timestream products
retain native samples once. A reopened product has scientific views and explicit
metadata readers, without recreating a live execution.

The initial block migration also updated the configured reducers, product IO,
focused Web consumers, tests and guide. Its validation: 368 reducer/block tests, 10 Web tests,
23 guide examples and 22 deck examples plus its CLI invocation pass. The reducer
tests include four exact production-v2 comparisons. Strict Sphinx, focused Ruff
and explicit development-environment type checks pass. Changed slides 21, 22,
25 and 26 were visually inspected after rendering; the unchanged slides retain
the earlier full-deck audit.

The end-to-end probe also passes four exact v2 comparisons through deployed CLI,
Zarr, database registration, Parquet catalog and Web plots. Its no-op equivalence
and Dash catalog callback checks pass. The report and local test products are in
`/tmp/tolteca-kids-block-slice-final-20261005/`.

The existing Marp versions and shared theme remain unchanged. The PDF build used
the existing local rendering browser outside the process sandbox; it installed
no dependencies. The HTML contains local/embedded styles, scripts and diagrams.
Slides 8 and 9 now include the standalone block reducer/numerical averaging API
and eager D21 computation for NumPy/Dask inputs.

The standalone-reducer/Dask follow-up passed 1,010 regression tests (including
four exact v2 comparisons), 10 Web tests, 24 guide examples and 22 deck examples
plus the CLI invocation. The Dask example now asserts equality with eager D21.
Eight benchmarks and backend read-count assertions passed in a separate focused
run. Strict Sphinx HTML/doctests, public reducer docstring examples, focused Ruff
and explicit type checks passed. Final slides 8 and 9 were visually inspected in
the PDF; configuration fields and the guide were checked in rendered HTML.
Commands, scope and log locations are recorded in the remaining-work audit.

## Reducer ownership update (2026-10-05)

- Native Dataset `.toltec_kids`: acquisition metadata, mapped native arrays and
  explicit `block_index`. The index records scalar block metadata, bounds and
  columnar axes without constructing a processing tree or loading detector arrays.
- `tolteca_kids.prepare_kids_data`: explicit acquisition tree construction from
  the cached index. Dataset input creates a new tree; native tree input keeps
  the supplied container; an already prepared acquisition/block is unchanged.
- `SweepReduce` and `TimestreamReduce` own their result installation and execution
  configuration. No public datamodels reducer remains. Numerical repetition
  averaging is `tolteca_kidsproc.reduction.reduce_sweep_samples`.
- `.toltec_kids` on a processing DataTree exposes blocks/results and compact
  scientific export. It omits live pipeline contexts; product writers explicitly
  save portable execution metadata through Tollan's context protocol.
- Removed the nested `reducer` config object. Scientific controls belong directly
  to `kids.sweep_reduce` and `kids.timestream_reduce`; spectral configuration
  remains the reusable `PSDAnalysis` at `kids.timestream_reduce.psd`.
- Guide: all 24 Python blocks execute. Deck: all 22 Python snippets and its CLI
  example execute. Dask D21 matches eager results. Web consumers: 10 tests pass.
- Strict Sphinx HTML build and the D21/PSD/repetition-averaging docstrings pass.
  Changed processing modules pass Ruff and `ty`; broad legacy scientific-module
  type errors remain outside this ownership extraction.
- Final KIDs, kidsproc and TolTEC native-reader run: 1,214 tests pass, including
  the production-v2 comparisons. Four additional native-axis bounds cases pass.
- All 28 rendered slide pages were checked; the updated ownership, preparation
  and step slides were also inspected at full resolution in the browser.

Earlier sections retain their dated checkpoint descriptions and may use the
former datamodels reducer class names.

## Block identification step (2026-10-06)

- `BlockIdentify` replaces `prepare_kids_data`. Callers use Tollan's
  `ensure_datatree(ds)` and invoke the step on that working tree. The supplied
  tree is updated in place; native arrays remain lazy under `raw`.
- Both configured reducer pipelines begin with `BlockIdentify`. Standalone
  reducers invoke it when block structure is absent. No-op execution does not
  identify blocks. Existing acquisition, collection and block structures are
  reused, including reopened products without a live context.
- `BlockIdentifyContext.data` carries the live collection or selected-block
  view. The root retains the live context store; scientific export omits it.
  JSON context serialization excludes the live view.
- Native opening and acquisition metadata remain independent of identification.
  Explicit `.block_index` inspects the recorded structure. Identification uses
  the working tree's native accessor cache and installs the index, shared axes
  and per-block scopes without reading detector samples.
- Active callers, tests, guide, API reference and deck now use `BlockIdentify`.
  The native opener is `open_toltec_kids`, following the concurrent datamodels
  update. Numerical reduction code is unchanged.

Validation:

- The broad KIDs/kidsproc/native-reader run passed 1,240 tests, including the
  production-v2 comparisons. Its three failures were stale expectations of a
  datamodels log message. After updating that expectation, all 24 no-op tests
  passed, including a check that no-op execution never invokes identification.
- All 71 focused block/lifecycle/metadata/export checks passed. The guide's 24
  Python blocks and deck's 22 snippets plus CLI example passed; Dask D21 matched
  eager output. Nine BlockIdentify/Kids docstring examples passed.
- Strict Sphinx HTML build, focused source Ruff/type checks and diff whitespace
  checks passed. Existing lint findings in the native accessor test module are
  outside this change.
- HTML and PDF rebuilt with the existing toolchain. All 28 PDF pages were
  inspected after rasterization; the changed native-block and configured-pipeline
  slides were also inspected in the browser. The pipeline slide's crowded note
  was removed and the final slide checked again.

Logs: `/tmp/kids-identify-{final-tests,noop-final,focused,guide,slides,docs-final}.log`.
The focused change was reviewed against the pre-change working snapshot in
`/tmp/kids-block-extract-before/tolteca.tar`, separately from the workspace's
Git-HEAD review diff.

### Slide and next-work refresh (2026-10-06)

Slides 5, 21 and 28 now consistently name block identification, include its live
context view and identify `SweepCheck`/`KidsFind` integration as pending work.
The native example inspects and identifies blocks through the same working-tree
accessor. All 22 snippets and the CLI example pass again, including the new
context-view assertion (`/tmp/kids-identify-slide-refresh.log`). HTML and PDF
were rebuilt; all three changed HTML slides and the expanded context table in
the PDF were visually checked. Unchanged pages retain the preceding full-deck
audit. No runtime source changed in this refresh.

The [remaining-work record](../../../tolteca/design/kids-block-pipeline-remaining-work-20261005.md)
now starts with the current ownership contract and a proposed next slice:
`SweepCheck` on reduced blocks, followed by `KidsFind`/plotting consumers and
integration through the configured Python/CLI entry point. This recommendation
is based on current `core.Kids`, `pipeline.KidsPipeline` and the direct
`SweepCheck` context dependency in `KidsFind.run`.

## Identification and creation split (2026-10-06)

This supersedes the combined `BlockIdentify` behavior in the dated entries above.
The configured sequence is now `BlockIdentify → BlockCreate → SweepReduce` or
`TimestreamReduce`, followed by `DataProdOutput`.

| Step | Live context payload | Working-tree effect |
| --- | --- | --- |
| `BlockIdentify` | `ToltecBlockIndex`: index, axes and scalar metadata | Native variables and children stay in place |
| `BlockCreate` | Collection or selected-block view | Native variables under `raw`; index/axes and block scopes under `blocks` |

Standalone creation identifies first if no live index is available. Standalone
reducers create the block structure when needed. An existing acquisition,
collection or block processing tree is reused without rescanning: identification
has no new payload in this case, and creation publishes its existing view.
No-op execution invokes neither step. Detector samples remain lazy; numerical
reduction and native-reader code are unchanged.

The identification payload uses Pydantic `InstanceOf[ToltecBlockIndex]` because
it is a live native dataclass instance. This avoids rebuilding that dataclass's
type annotations as a Pydantic model. Both live payloads are excluded from JSON.
A pickle checkpoint after identification preserves the index for subsequent
creation without invoking identification again.

Validation:

- KIDs, kidsproc and native-reader regression: **1,233 passed, 12 skipped**.
  The skipped production-v2 tests were then enabled separately: **4 reducer and
  8 axis/model comparisons passed**.
- The **8 focused boundary tests** cover native-layout preservation, lazy I/O,
  cached and checkpointed index reuse, reopened scopes, collisions and pipeline
  ordering. No-op and standalone-reducer behavior pass in the broad suite.
- All **24 guide blocks**, **23 slide snippets plus CLI**, and **15 public
  docstring examples** pass. Dask D21 agrees with eager results.
- Strict Sphinx HTML, focused Ruff and explicit development-environment type
  checks pass. Pre-existing lint findings in the native accessor test module
  remain outside this change.
- HTML and PDF rebuilt as **29 slides**. Every PDF page was inspected after
  rasterization. The new creation slide and expanded pipeline table initially
  crowded their footers; both were adjusted and inspected again in HTML and
  the final PDF. The rendered API reference includes both steps and contexts.
  Navigation and resize checks remain those of the earlier full-deck audit.

Logs: `/tmp/kids-block-create-{regression,v2,v2-axes,boundary,guide,slides,docs-final}.log`.
The focused diff uses the pre-change working snapshot
`/tmp/kids-block-create-before/tolteca.tar`; the workspace review uses Git HEAD.

## Product/export metadata review (2026-10-06)

Slides 16 and 28 now show acquisition/block metadata and the shared block index,
channel and probe leaves explicitly. The direct exporter creates no product
manifest; configured writers place `manifest.json` beside `arrays.zarr`.
The distinction and the v1/v2/Citlali, DPDB and DV pipeline source trail are in
[the product-contract audit](../../../tolteca/design/data-products-dpdb-and-archive-20261006.md).

The bounded local export probe compared the persisted acquisition/block metadata
and all three shared tables with their working-tree counterparts for both
product writers and direct standalone scientific export. These checks passed.
Direct export of the configured runner tree exposed a separate non-JSON `Path`
in its live input row; this is recorded as an open finding, not silently fixed.
Evidence and the stored inventories are under
`/tmp/kids-product-contract-20261006/`. No runtime or database schema changed.
All 23 slide snippets and the CLI example pass after the update. Both changed
slides fit in the rendered HTML and rebuilt PDF. Unchanged slides retain the
preceding full-deck checks. Audit source links resolve; the focused documentation
diff was reviewed and `just review` regenerated the workspace diff.

## Run-index provenance update, 2026-10-12

The current deck replaces the manifest artifact with run-index provenance.
The data-product deck includes per-input workflow settings, result snapshots and
replay limits. HTML was rebuilt with the installed Marp toolchain. Earlier
manifest descriptions and rendering checks above are historical; no new visual
browser audit is claimed. See the [implementation and QA record](../../../tolteca/design/product-provenance-audit-20261012.md).
