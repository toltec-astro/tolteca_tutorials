# TolTECA v3 overview evidence

Date: 2026-10-19. Deliverable: 16-slide HTML/PDF overview, with 19½ minutes of
speaker notes and brief transitions within a 20-minute slot. Audience: TolTEC
instrument/software developers, observers and data product curators.

## Ownership and inspected state

The ecosystem presentation belongs to `tolteca_tutorials/presentations` under
the workspace documentation rule. Domain specifications retain contract
ownership. This change adds presentation sources, assets, styling, build and
preview integration. It changes no scientific code, database, deployment or
reference input. It runs no new reductions.

Inspected HEADs, plus existing uncommitted v3 work:

| Repository | HEAD |
| --- | --- |
| tolteca_tutorials | `92acaa6` |
| tolteca | `486244a` |
| tolteca_db | `c29e3b6` |
| tolteca_web | `9db03d8` |
| tollan | `72d90f5` |
| tolteca_deploy | `030d3b0` |
| tolteca_helpdesk | `c35fa0a`, plus ongoing documentation and deck work |

The helpdesk implementation was inspected alongside the current **Plan Toltec v3
user resources** chat (`01a15607-1aeb-7ff2-b607-5ed5499c0863`). That work remains
active. The overview deliberately records its stable ownership boundaries and
prototype status, not a claim of validated answer accuracy or completed
deployment integration.

## Claims and source evidence

| Slides | Evidence | Scope |
| --- | --- | --- |
| 2–4 | [Input architecture](../../../tolteca/design/tolteca-datamodels-input-workflow.md), [workflow architecture](../../../tolteca/design/toltec-operational-workflows.md) | File/acquisition selection, accessor use, block scopes, Python/CLI/Dagster ownership |
| 5–6 | [KIDs architecture](../../../tolteca/design/toltec-kids-data-and-analysis.md), [viewer guide](../../../tolteca_web/docs/processed-kids.md), retained Docker reference output | Reduction, optional analyses, Zarr selection |
| 7–8 | [Quicklook API guide](../../../tolteca_web/docs/quicklook.md), [API implementation](../../../tolteca_web/src/tolteca_web/quicklook.py), [KIDs asset workflow](../../../tolteca_db/docs/kids-quicklook.md), [asset definitions](../../../tolteca_db/src/tolteca_db/kids_workflow.py) | Independent ingestion/publication, joined registration, MC ObsSpec request, readiness states and prepared image delivery |
| 9 | [Product architecture](../../../tolteca/design/toltec-data-products.md), [specification](../../../tolteca/design/spec.md) | Run identity, tags, resolved settings, stored arrays and records |
| 10–11 | [Inventory architecture](../../../tolteca_db/design/toltec-associations-and-inventories.md) and its evidence | Per-interface calibration facts, connected groups, independent inventories and unified projection |
| 12–13 | [Execution architecture](../../../tolteca_deploy/design/toltec-deployment-and-execution.md), [Slurm integration report](../../../tolteca_deploy/design/slurm-workflow-integration-20261019.md) | Service/compute separation, supervision, bounded retry, cancellation and exact-attempt recovery; Docker verification, not Unity production acceptance |
| 14–15 | [Helpdesk specification](../../../tolteca_helpdesk/design/spec.md), [README](../../../tolteca_helpdesk/README.md), current companion chat and live public portal | Separate science/operations guidance, package-owned sources, external inference and independent agent access |
| 16 | The preceding sources and their explicit implementation limits | Science migration, site rollout, helpdesk accuracy and formal QA remain incomplete |

The diagrams are selected conceptual views. The calibration example is explicitly
illustrative. The interface hierarchy shows a multi-sweep KIDs file; it does not
claim that a mixed sweep/timestream acquisition writer is deployed. Telescope and
HWPR readers exist; the demonstrated processed product contains KIDs only.

The published-run diagram groups provenance conceptually. The portable index,
step records and analysis attributes remain distinct storage owners. Saved
configuration alone does not guarantee identical results without the same input
data and software environment.

## Captured artifacts

Captures were made on 2026-10-19. Original captures are retained in `assets/`;
they are not mockups. No data values were edited. Agent browser captures use
the browser's normal 1280×720 viewport. The processed-viewer capture scrolls
to the block/channel controls and curves. The run capture filters logs to Slurm
events. The exported quicklook image is the existing workflow artifact.

| Asset | Source |
| --- | --- |
| `processed-viewer.jpg` | `http://127.0.0.1:33006/processed-kids`; acquisition `tcs-145609-0-1`, `toltec0`, block 1, channel 0; published run `a09aacaf-90c0-539e-981e-b1c3e8c80cd7` |
| `quicklook-summary.png` | Local MC API `/api/ql?obs_spec=145609`, then its returned summary artifact URL; same run; two blocks, 632 channels per block |
| `dagster-run.jpg` | `http://127.0.0.1:33004/runs/3ef92102-0198-4d7d-a94a-e08658d7ee74?logs=Slurm`; retained successful Docker run on compute1 |
| `helpdesk-science.jpg` | `https://toltec.lmtgtm.org/dr/science/`; live Science Portal and configured planner link; no inference request issued |
| `helpdesk-answer-wip.png` | User-supplied Operations Portal screenshot, `Screenshot 2026-10-19 at 21.10.05.png`, 1682×2358; original pixels retained |

Slide 14 displays two presentation crops from the supplied answer: the CLI
excerpt and its source citation. The omitted Python section incorrectly calls
index publication ingestion. The slide labels the answer as work in progress
with accuracy needing improvement; its notes record the specific error. The
example demonstrates the UI and citation format, not a validated procedure.

The LMT masthead photograph remains part of the actual portal screenshot. The
portal attributes it to `http://toltec.astro.umass.edu/css/images/banner.jpg`.
The deck does not reuse that photograph as separately authored artwork.

An older association demo exposed an incomplete calibration component for the
selected acquisition. It was not used as a complete-lineage screenshot. Slide 10
uses an explicit conceptual example instead. The initially attempted local
helpdesk preview was stopped; the public portal supplied the screenshot.

## Build and presentation QA

- Shared toolchain: Marp CLI 4.5.1, Marp Core 5.0.2. The overview imports the
  existing renderer and uses a dedicated theme. Python builds editable SVGs;
  source images and SVGs are embedded in the HTML export. All 17 image elements
  loaded; no external scripts or stylesheets are required by the exported deck.
- HTML and PDF both contain 16 slides. PDF pages were rendered with Poppler and
  all inspected. The quicklook graphic was enlarged; execution-slide spacing and
  the final slide's footer collision were corrected after inspection.
- Browser review at 1280×720 and 1024×768 checked labels, images and slide bounds.
  All sections have 1280×720 content bounds without overflow. Contact sheets and
  individual captures remain in ignored `.qa/`.
- Arrow navigation, numbered deep links, native overview and final-slide topic
  links were exercised. Presenter view renders notes at `?view=presenter`.
  The in-app browser did not open the separate window from the native presenter
  shortcut; the README documents the direct URL fallback.
- Browser console inspection returned no errors. HTML asset references were
  inspected for self-containment. Physical network disconnection was not used;
  external further-reading links naturally still require connectivity.
- The SVG generator passed Ruff. Changes passed whitespace checks. The workspace
  review command regenerated `/tmp/toltec-python-workspace-review.diff`; it also
  includes unrelated work already present in other repositories.

The answer-crop update was checked for readable excerpts, source attribution,
visible WIP status and footer clearance. The subsequent operational-workflow
update separates the observing diagram and MC API contract into slides 7–8.
It updates slide numbering, topic links and timing; the helpdesk example is now
slide 14. The MC contract uses a deployment-relative endpoint, not a claimed
production hostname. Ready responses do not contact Dagster; the optional status
lookup deadline does not bound the full HTTP response time.

No application tests were rerun for this presentation-only change. Existing
workflow reports establish the illustrated computations; screenshots establish
the displayed UI state, not general latency, concurrency, science correctness or
production readiness.
