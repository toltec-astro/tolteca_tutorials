# Input discovery and data access — current presentation evidence

> Moved on 2026-11-07 from `tolteca/design/` to `tolteca_tutorials/architecture/tolteca-datamodels-input-workflow/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/tolteca-datamodels-input-workflow/probes/` and build from `slides/`.

Date: 2026-10-19. Scope: requested architecture deck split and current API updates.
The deck contains 14 main slides and 22 appendix/reference slides.

## Contract and implementation

The specifications remain authoritative. This update changes slide sources,
build/preview tooling and presentation probes only. Relevant working trees contain
substantial pre-existing changes; HEAD alone does not identify the inspected code.

HEAD revisions: `tolteca` `486244a`, `tolteca_db` `c29e3b6`, `tolteca_web` `9db03d8`, `tollan` `72d90f5`, `tolteca_deploy` `5e7997c`.

Inspected current sources:

- [tolteca/src/tolteca_datamodels/data_model.py](../../../tolteca/src/tolteca_datamodels/data_model.py)
- [tolteca/src/tolteca_datamodels/core/data_model.py](../../../tolteca/src/tolteca_datamodels/core/data_model.py)
- [tolteca/src/tolteca_datamodels/core/file/accessor.py](../../../tolteca/src/tolteca_datamodels/core/file/accessor.py)
- [tolteca/src/tolteca_datamodels/core/input_discovery/config.py](../../../tolteca/src/tolteca_datamodels/core/input_discovery/config.py)

## Executed examples and scope

The retained reader probe passed against the reference telescope, KIDs and HWPR files. It executes displayed Python examples in dependency order and exercises the no-op CLI. DataModelSet and explicit metadata-refresh examples replace superseded interfaces.

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

# Datamodels input-workflow presentation — current evidence

## 2026-10-14 coherence review update

Current review artifacts are the [34-slide source](tolteca-datamodels-input-workflow.md)
and [rebuilt HTML](../../_build/slides/architecture/tolteca-datamodels-input-workflow.html). This update supersedes
the outstanding assembly correction below and the older reader/lifecycle API
descriptions. The PDF is still the previous export: **it has not been regenerated
for this update**.

Compared the deck against the current pending implementation at Tolteca `e2cefe9`,
using the workflow-contract-audit, architecture-review-slides and presentation
skills. The related review is
[the input-workflow follow-up](../../../tolteca/design/datamodels-contract-audit-20261014.md#follow-up-input-workflow-review-readiness).

Corrected slides 5–7, 9–10, 13, 22–23, 25 and 33:

- Data-model definition classes identify the declaring accessor;
  `data_models` remains the per-row list of compatible models.
- Component imports are neutral; explicit `data_model.py` imports construct
  definitions, and root workflow imports register the built-ins.
- Concrete filepath result classes are public for type checks; parsing remains
  universal and separate from accessor scope.
- Reader rules belong to each data model and use current values; opening stays
  format-based. Shared physical readers bind/read once; ambiguity raises.
- `open()` stops at identification; `open(update_from_metadata=True)` also
  enriches. `accessor_obj` and `io_obj` exist only inside the open scope.
- `update_from_source_metadata()` skips completed rows unless forced. Metadata
  and classification publish only after successful preparation.
- `source_trace`, `SourceTraceEntry`, `find_unresolved_source_issues()` and
  `source_trace_summary()` replace the obsolete error-only diagnostic examples.

Verification:

| Check | Result |
| --- | --- |
| Executable slide Python | All 14 blocks pass |
| Configured CLI examples | `--show_inputs` and `--dry_run` exit 0 |
| Mixed reference workflow | 16 reference files; 19 mixed rows with temporary dummy files and an unrecognized remote location; five TolTEC sweeps and one dummy count file selected |
| Scientific examples | Telescope time/coordinate assertions, exact block bounds and axes, HWPR packet subset all pass |
| HTML build | Existing Marp command succeeds; 34 sections; obsolete reader identifiers absent |
| Visual/interaction QA | Blocked by browser local-URL policy; not claimed |
| PDF | Previous export retained unchanged; not a current review artifact |

No browser workaround was attempted after the policy rejection. Markdown/HTML
can be reviewed now, but the updated layout still needs a permitted visual check.
No source, dependency, slide theme or reference fixture was changed for the deck.
Logs and snapshots: `/tmp/datamodels-review-ready.us825r/`.

## 2026-10-14 assembly boundary correction

The pending implementation at `e2cefe9` now keeps data-model construction out of
instrument package initializers and component imports. Definitions live in each
instrument's `data_model.py`; root workflow entry points register the built-ins.
The filename entry point only enables parsers. Dummy registration remains
explicit. `lmt/file_store.py` now defines the complete `LmtFileStore`; the private
telescope-store subclass and module are removed. This supersedes the package
assembly descriptions in slides 5 and 9–11 of the current deck. The deck exports
have not been regenerated for this correction.

Verification: 333 focused discovery/import tests and 1,321 instrument/store tests
passed. The 22 skipped tests require an independently configured v2 interpreter.
The eight strengthened explicit-definition and entry-point cases passed again.
All 34 guide Python blocks and six CLI/deployment examples passed; Ruff, changed
production-file type checks and strict Sphinx HTML passed. The generated guide
HTML contains the new import paths. Browser inspection was blocked by the local
file-URL policy. The pre-change snapshot and verification logs are at
`/tmp/datamodel-assembly.gF9noc`; this is the turn baseline, not Git HEAD.

## 2026-10-13 update

The current deck has **34 slides**. It covers input preparation through
pipeline-owned selection, including the core/entry-point split, registrations,
data-model contexts, stores, ObsSpec, flat tables and native readers. Explicit
KIDs block/axis inspection is a separate reader capability. The maintained
[specification](../../../tolteca/design/spec.md#observation-data) owns the contract.

Inspected the live pending TolTECA tree at `67e1ae5` on
`codex/overnight-kids-slice-20260922`, with clean Tollan `v3.x` at `c0836dd`.
This update changes only the deck's Markdown/HTML/PDF, this evidence note and
`probes/datamodels_input_workflow.py`. Application code, shared slide tooling,
other decks and reference files are unchanged. No commit was requested.

Current artifacts:

- [Editable source](tolteca-datamodels-input-workflow.md)
- [HTML](../../_build/slides/architecture/tolteca-datamodels-input-workflow.html)
- [PDF](../../_build/slides/architecture/tolteca-datamodels-input-workflow.pdf)
- [Executable examples](probes/datamodels_input_workflow.py)

### Contract corrections and ownership

This update supersedes the older presentation's single mixed `data_kind` column,
accessor fallback registration, scoped filename factories,
`find_candidates(instru=...)`, common-backend opening restriction, TolTEC-only
discovery wiring and pending integer-kind migration. Those are not current APIs.
The [core reorganization review](../../../tolteca/design/datamodels-core-reorganization-20261013.md)
records the implementation decisions; the deck does not change them.

| Slides | Current implementation evidence, relative to `src/tolteca_datamodels` |
| --- | --- |
| 2–6, 9–11 | Root `file`, `filepath`, `data_model`, `input_discovery`; `core/data_model.py`, `core/_data_model.py`; instrument `data_model.py` |
| 7, 12, 19 | `core/filepath.py`, `lmt_base/filepath.py`, instrument `filepath.py` and `types.py` |
| 8, 16 | `core/obs_spec/`, `lmt_base/obs_spec.py`, private instrument contexts |
| 13, 18, 21–23 | `core/file/{accessor,_handlers}.py` and instrument `file.py` |
| 14, 24–28 | `core/source.py`, `lmt/tel.py`, `lmt_base/metadata.py`, `toltec/{metadata,hwpr}.py`, `toltec/kids/core.py` |
| 15 | `core/file_store/`, `lmt/file_store.py`, `toltec/file_store.py` |
| 11, 17 | `core/data_model.py`, `core/input_discovery/`, `lmt_base/input_discovery.py`, instrument `input_discovery.py` |
| 20 | Tollan `src/tollan/accessor/pandas/{model_table,mapper}.py` |
| 29–30 | `toltec/kids/blocks.py`, `toltec/axes.py`, `toltec/hwpr.py`; KIDs `block_identify.py` |
| 31–34 | `tolteca_kids/{input,cli,config,noop}.py`, `tolteca_dummy_instru/` and the above extension points |

The diagrams and examples now distinguish these boundaries:

- Universal filename parsing uses all available registrations, independent of
  table-handling scope. Concrete factories retain all supplied rows.
- `instru` names the producer; non-exclusive `data_models` memberships describe
  applicable handling support. Telescope companions can belong to LMT and TolTEC.
- Each enabled classifier has its own named integer column and unknown flag.
  There is no combined kind column.
- DataModelContext selects handlers and store requirements. Requirements do not
  enable extra handlers. Config selections only narrow the task's available set.
- Returned DataFrames do not carry a context wrapper; slide 11 notes explain
  maintaining the selected handling scope when constructing a later accessor.
- Format opening is separate from paired identification/metadata reading.
  Ambiguity raises; a metadata failure is not an identification miss.
- Stores apply value constraints using their local context; the table accessor
  applies the complete ObsSpec, including positional selection.

### Current executable checks

From the Python workspace root:

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/datamodels-slides-20261013.jrOA22/mpl \
  toltec_astro_dev/.venv/bin/python \
  tolteca/design/probes/datamodels_input_workflow.py
```

All **14 displayed Python blocks** pass. The two YAML blocks are combined and
passed to the actual `--show_inputs` and `--dry_run` callbacks, both exiting 0.
The probe provides shared imports/path variables and substitutes only local
example locations. No reduction, publication or service runs.

The cumulative reference set remains 16 read-only files: seven telescope files,
four TolTEC 0 acquisitions and five TolTEC 7/11/HWPR files for observation 156755.
Temporary dummy counts and `tel_dummy_instru` companion files plus one unidentified
remote filename exercise the mixed case without fixture or network writes.

- Mixed tables retain all 19 rows. Universal parsing supplies obsnums for 18,
  including through the concrete LMT factory.
- Separate flag queries select five TolTEC sweeps and one dummy counts file,
  despite overlapping numeric bits. The remote row gets each unknown flag.
- Dummy telescope metadata retains producer `lmt` and memberships
  `["lmt", "dummy_instru"]`. TolTEC membership selects 16 rows.
- The scoped context prepares 16 rows without adding the dummy classifier.
  Store/ObsSpec selection returns four files for observation 145609.
- Three telescope records match pointing/lissajous. The coordinate query selects
  `tcs-145609-0-2`, with 60.3 s integration and 68.5 s elapsed time.
- The full table has five raw sweeps and eight raw KIDs files. The pipeline input
  selection returns five sweeps within the open scope.
- Source/source_loc identity separation and io_obj cleanup pass. Needed array
  values are loaded before their resource scope closes.
- TolTEC 7 tune bounds remain `[0,1770)` and `[1770,3540)`, with 1,114 collection
  channel rows and 354 probe rows. HWPR has readout code 13, 131 packets and a
  five-packet encoder subset of shape `(5,500)`.
- Configured entries yield 4, 5 and 7 rows before combination. Probe formatting
  and Ruff E/F/I checks pass.

This is presentation-example verification, not a fresh full-suite, scientific
parity or production-performance certification.

### Current build and visual checks

From `tolteca/design/slides`:

```sh
npm run build -- ../tolteca-datamodels-input-workflow.md
npm run pdf -- ../tolteca-datamodels-input-workflow.md
```

Existing toolchain: Node 24.10.0, Marp CLI 4.5.1, Marp Core 5.0.2. No dependency
installation or upgrade. PDF rendering required approved execution outside the
sandbox after Chrome failed to launch inside it.

- HTML has 34 sections; PDF has 34 pages at 960 × 540 pt.
- Every HTML slide was captured and visually reviewed at 1280 × 720 and
  1024 × 640. Six initial overflow findings were corrected without reducing
  theme font sizes. Final bounds checks report no overflow.
- An isolated offline Chrome session reports no page errors or external HTTP
  requests. Arrow/Home navigation, section links, deep links, overview and
  presenter mode were exercised. Shared theme and standard controls are unchanged.
- All PDF pages were rasterized for visual review. Diagrams, tables and code are
  present; the exported pages do not depend on animation or live services.
- QA captures hide only the transient navigation toolbar; delivery retains it.

Logs, render script, captures, PDF rasters and turn-start snapshots:
`/tmp/datamodels-slides-20261013.jrOA22/`. The focused artifact diff uses that
snapshot, not Git HEAD. The aggregate review is
`/tmp/toltec-python-workspace-review.diff`. Design artifacts remain ignored and
were not force-added to Git.

The deck does not verify DB/Web, Dagster, deployment services, remote staging or
arbitrary ECSV domain metadata. Data-product restructuring remains deferred.

---

# Archived evidence — 2026-10-07

**Historical implementation and checks below are superseded by the 2026-10-13
section above. They are retained as chronology, not current API documentation.**

## Scope and artifacts

The 32-slide deck describes the current registry-driven and scoped APIs,
discovery, ObsSpec, flat model tables, metadata enrichment, typed native readers,
and pipeline-owned input selection. Explicit KIDs block inspection appears as
a separate reader capability, not an input-workflow step.

- [Editable source](tolteca-datamodels-input-workflow.md)
- [HTML](../../_build/slides/architecture/tolteca-datamodels-input-workflow.html)
- [PDF](../../_build/slides/architecture/tolteca-datamodels-input-workflow.pdf)
- [Executable examples](probes/datamodels_input_workflow.py)

The existing Marp toolchain, shared theme and telescope-specific deck are
unchanged. Only this deck's source/exports, evidence and executable probe changed.
No application source, reference fixture, dependency or service was modified.

## Code snapshot

Checked 2026-10-07 against the live working trees, **not only Git HEAD**.

| Repository | HEAD | Scope |
|---|---|---|
| tolteca | `d2796ea`, `codex/overnight-kids-slice-20260922` | Current uncommitted datamodels, registration and KIDs input code |
| tollan | `f9c2b67`, `v3.x` | Shared schema, accessor, config and runtime infrastructure |

Unrelated pending pipeline, DB/Web and documentation work was preserved. The
deployment, DB/Web and Dagster rows retain responsibility boundaries from the
prior audit; this update does not claim those integrations were migrated or run.

Read WORKSPACE.md, the architecture-review-slides workflow, the presentation and
PDF skills, and the shared Marp guidance. Inspected the existing source and all
24 prior rendered slides before editing. The established HTML deck format takes
precedence over generic PPTX defaults.

The implementation checkpoint is in `instrument-discovery-20260929.md`, under
“Generic registered file tables”. Its limitations remain visible: concrete tables
retain integer kinds, configured discovery remains TolTEC-centered, generic
opening requires a common backend, and downstream enum migration is unfinished.
No FileDiscoveryContext API is presented as implemented.

## Claim ownership

Source paths below are relative to the tolteca repository.

| Slides | Implementation evidence |
|---|---|
| 2–4, 12, 16, 20–21 | `src/tolteca_datamodels/file.py`: source/location validation, modes, diagnostics, enrichment and resource ownership |
| 4–6, 9–11 | `_file_registry.py`, `file.py`, `lmt/file.py`, `toltec/file.py`, `src/tolteca_dummy_instru/file.py`: registration, concrete scopes, unique ownership, fallback and mixed flags |
| 7 | `_filepath.py`, `lmt/_filepath.py`, `toltec/_filepath.py`, `src/tolteca_dummy_instru/filepath.py`: model inheritance, pattern registration and scoped factories |
| 10 | `lmt/tel.py`, `lmt/metadata.py`: normalized receiver header independent of current/original filepath |
| 13 | `file_store.py`, `lmt/file_store.py`, `toltec/file_store.py`: store composition, candidate globs and instru scope |
| 8, 14 | `obs_spec.py`, `lmt_base/obs_spec.py`, instrument contexts: layout hooks, context composition, grammar, resolution and positional selection |
| 15 | `input_discovery.py`, `_input_discovery.py`, `lmt/input_discovery.py`, `toltec/input_discovery.py`: configuration registry, globs, rootpath, selection, deduplication and current concrete TolTEC population |
| 17–19 | `_filepath.py`, concrete filepath modules, `model_table.py`, `toltec/file.py`: filename models, projection and query APIs |
| 22–23 | `source.py`, `lmt/tel.py`, `toltec/kids/core.py`, `toltec/hwpr.py`; Tollan accessor/xarray: bindings, recognition and typed readers |
| 24–25 | `core.py`, `lmt_base/metadata.py`, `lmt/metadata.py`, `lmt/tel.py`: strict metadata, inheritance, IDs, times and coordinates |
| 26–27 | `toltec/metadata.py`, `toltec/axes.py`, `toltec/kids/{core,blocks}.py`, `src/tolteca_kids/block_identify.py`: explicit index/axis inspection without BlockCreate |
| 28 | `toltec/hwpr.py`: readout code 13 and native packet arrays |
| 29–30 | `src/tolteca_kids/{input,config,cli,runner,noop}.py`: integer-kind selection, error policy and no-op invocation |
| 31–32 | `src/tolteca_dummy_instru/__init__.py` plus registration/configuration and input code: distinct extension points and remaining integration |

## Executed examples

From the Python workspace root:

```sh
toltec_astro_dev/.venv/bin/python \
  tolteca/design/probes/datamodels_input_workflow.py
```

The probe executes **all 13 displayed Python blocks** and combines both displayed
YAML blocks for the actual CLI callbacks `--show_inputs` and `--dry_run`.
It supplies imports and named example paths, replacing only example locations
with the local reference root. The examples do not reduce or publish products.

Reference root: `toltec_astro_dev/run/data_lmt`. The cumulative set remains 16
files: seven telescope files, four TolTEC 0 acquisitions, and five TolTEC 7/11/HWPR
files for observation 156755. The generic example adds temporary synthetic dummy
counts and telescope companion files plus one unidentified remote filename.
The companion uses `tel_dummy_instru` and an explicit dummy receiver header.
No reference inputs are written.

Results:

- All 16 reference sources parse and provide acquisition metadata.
- Generic population/enrichment retains 19 rows. Queries select five TolTEC
  sweeps and one dummy counts file without cross-matching their shared bit 1.
  The dummy telescope retains its receiver and flag namespace. Only the
  unidentified remote row has a null kind.
- The scoped LMT factory recognizes eight telescope rows without data_kind.
  The scoped TolTEC factory retains integer kinds and leaves the two dummy
  rows plus unidentified path at its unknown flag.
- Store/ObsSpec selection returns four telescope/TolTEC 0 files for 145609.
- Three telescope records match pointing + lissajous. The coordinate query
  selects tcs-145609-0-2 (60.3 s integration, 68.5 s elapsed).
- The concrete table has five raw sweeps and eight raw KIDs files.
- A local-resource/remote-identity example retains the remote FileLoc and reads
  local header metadata. An unidentified remote path needs no network access.
- Open-table scopes remove their temporary io_obj column on exit. Sample arrays
  used afterward are loaded while the scope remains open.
- TolTEC 7 tune blocks span [0, 1770) and [1770, 3540), with 557 channels each,
  1,114 collection channel rows and 354 probe rows.
- HWPR retains readout code 13 and 131 packets. Five encoder packets have shape
  (5, 500).
- Configured discovery entries return 4, 5 and 7 rows before combination.
  The shown sweep query leaves three CLI inputs. Both CLI invocations exit 0;
  dry_run executes only the no-op path.

Log: `/tmp/datamodels-registry-slides.Juxs48/probe.log`.

## Regression checks

Ran registered-file-accessor, flag-column, mapper-reuse, source-diagnostic,
source-reader, raw-block and dummy-workflow tests: **232 passed in 22.40 s**.
Internet is disabled by the test environment. This is not a full-suite,
cross-version scientific parity or production-performance claim.

Log: `/tmp/datamodels-registry-slides.Juxs48/tests.log`.

The probe passes Ruff formatting and E,F,I checks. No application lint settings
or ignores were changed for this design artifact.

## Build and visual verification

From `tolteca/design/slides`:

```sh
npm run build -- ../tolteca-datamodels-input-workflow.md
npm run pdf -- ../tolteca-datamodels-input-workflow.md
```

Existing toolchain: Node 24.10.0, Marp CLI 4.5.1, Marp Core 5.0.2. No installation
or upgrade. The initial sandboxed PDF export could not launch Chrome; the same
local renderer succeeded with approved escalation.

- HTML has 28 sections. PDF has 28 pages at 960 × 540 pt (16:9).
- Every HTML slide was captured at 1280 × 720 in an isolated offline Chrome
  session and visually reviewed. The API-scope and flag-query notes were
  shortened after checking footer clearance. Shared styling is unchanged.
- Browser QA exercises ArrowRight, Home, the section jump to slide 19, overview,
  presenter mode and a 1024 × 640 viewport. No page errors were reported. The
  final bounds check found no slide overflow, and no external runtime assets
  appeared in the delivered document.
- The delivered HTML embeds its diagrams and runtime assets. The offline browser
  successfully opens it without a local server. Temporary QA screenshots hide
  only the transient navigation toolbar; the delivered deck retains its controls.
- All 28 PDF pages were rasterized separately and visually inspected.
- The automated browser uses a fresh profile, not the user's existing session.

QA script and captures: `/tmp/datamodels-registry-slides.Juxs48/`.
The pre-turn deck/probe/evidence snapshots are in the same directory.

Remaining capability boundaries are visible on slides 15, 29 and 32. No commit
was requested or made. The workspace review is the aggregate
`/tmp/toltec-python-workspace-review.diff`, not a focused slide diff; ignored
design artifacts are delivered directly and were not force-added to Git.

## Receiver header correction (2026-10-07)

Slide 6 and the guide now use `Header.Dcs.Receiver`, matching the shared telescope
schema. All seven reference telescope files contain this header with value
`Toltec`. Receiver metadata and constrained identification read only this receiver
header; backend values do not override it or act as a fallback. The temporary
dummy companion fixture/probe now needs only the DCS receiver header.

Re-ran the full 12-example and two-YAML CLI probe successfully. LMT, registered
accessor, TolTEC metadata-read, dummy-instrument and mapper-reuse tests report
365 passed and 14 skipped (cross-environment v2 interpreter not configured).
Scoped Ruff/ty and the strict Sphinx build passed.

Rebuilt both exports with the existing toolchain. Slide 6 was checked offline at
1280 × 720 and 1024 × 640, with keyboard navigation and no page errors, and its
PDF page was rasterized and visually checked. No layout changes; the PDF remains
28 pages. Other slides retain the prior full-deck verification above. This turn's
snapshots and captures are under `/tmp/dcs-receiver.CrvuM4/`.

## Registration and customization diagrams (2026-10-07)

Expanded the former registration slide into slides 5–9, preserving the existing
registration example and adding editable Mermaid graphs for the shared entry
points, class inheritance, and ObsSpec interpretation. The remaining slides shift
by four; section links, speaker-note references and the evidence index above now
use the 32-slide numbering.

The diagrams distinguish three contracts verified against current code:

- FileAccessor explicitly registers concrete provider classes. The generic
  instance snapshots their declarations; direct subclasses retain their own
  scope. Its customization table groups filename acceptance, projections,
  openers/readers, computed values, flag types and query context.
- FilepathInfo automatically registers each subclass's declared patterns and
  ordered parsers. Its factory restricts candidate classes before parsing and
  returns a validated instance of the matched class. Filepath-model registration
  alone does not register a table provider.
- ObsSpecBase supplies grammar and the shared lmt_base.ObsSpec supplies field
  layout and constraints. Instrument modules construct ObsSpecContext values.
  Accessors and stores supply/compose them at resolution time; no instrument
  parser registry exists. Numeric interpretations do not restrict literal labels.

The probe now executes all 13 displayed Python blocks and both YAML blocks. It
also checks the concrete LMT factory rejects a TolTEC filename, the generic
filename factory returns LmtFilepathInfo for a telescope path, and one parsed
`*/1` resolves to no telescope labels, `toltec1`, `chan01`, or both according to
the supplied contexts. The full 16-reference/19-mixed-row and CLI no-op probe
still passes.

Registration, ObsSpec-context/layout, dummy-filepath and dummy-workflow tests:
**197 passed in 14.00 s**. Probe Ruff E,F,I and formatting checks passed. No
runtime implementation, public guide, shared theme, reference data or dependency
was changed. An intermediate probe missed the FilepathInfo name in its execution
namespace; adding the imported class to that namespace fixed the harness without
changing the application or example behavior.

Both HTML and PDF were rebuilt with the existing Marp toolchain. Reviewed all
32 rendered HTML slides and PDF pages, with enlarged checks of the new diagrams.
The new section was also captured at 1024 × 640. Shortening the FilepathInfo note
removed its initial footer overlap. The final automated bounds check reports no
overflow; offline loading, ArrowRight/Home, the updated reader section link and
presenter mode work with no page errors. The PDF has 32 pages at 960 × 540 pt.

Incremental baseline (pre-turn dirty artifacts, not Git HEAD), probe/test logs,
browser script and captures: `/tmp/datamodels-registration.aRE6BJ/`.
No commit was requested or made. The workspace review remains the aggregate
`/tmp/toltec-python-workspace-review.diff`, including unrelated pending work.

## Reader metadata correction (2026-10-08)

The [reader metadata cleanup](../../../tolteca/design/reader-metadata-contract-20261008.md) removes the
unsupported fresh-header reader API. Slide 23 now lists `.meta` alone as validated
acquisition metadata cached on the reader. Table-level metadata population remains
supported. This correction does not revalidate the other slides against subsequent
registry changes; the full-deck results above remain historical.

Rebuilt HTML and PDF using the existing Marp commands. Compared the changed HTML
slide with its pre-turn render at 1280 × 720, inspected it at 1024 × 640, and
rendered PDF page 23 for visual inspection. No clipping or layout changes; the
deck still has 32 slides. Offline browser loading and ArrowRight from slide 23
to 24 pass without page errors. No dependency or theme changes.

Captures: `/tmp/metadata-contract.G3rLNV/slide-before.png`,
`slide-after-1280.png`, `slide-after-1024.png`, and `pdf-23.png`.
The full slide execution probe was not rerun. The current guide probe stops at
the independently reproduced config-source mismatch described in the cleanup
note; no current full CLI/deck-workflow success is claimed.
