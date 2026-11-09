# Architecture decks

Open the [deck index](../slides/index.html) for HTML, PDF, source and evidence links.
Each domain architecture deck has 14 main slides. Detailed API and structure references follow in
appendices where needed. The telescope deck remains a focused instrument example.

Audience: developers reviewing architecture, APIs and operational boundaries.
Status: maintained descriptions of the current implementation, reviewed 2026-10-19;
verification and deployment limits are recorded in each companion evidence file.
These are developer design resources, not end-user operational instructions.

The [TolTECA v3 overview](../presentations/tolteca-v3-overview/README.md)
is a separate 16-slide, 20-minute presentation for the TolTEC group. It uses
lifecycle diagrams and actual interface captures, including the developing
science and operations helpdesk. It is under `presentations/`.

Each deck sits in its own folder, `<deck>/<deck>.md`, with its companion
`<deck>-evidence.md` and, where present, `probes/` that execute the deck's
examples or render its figures. `probes/architecture_decks.py` checks examples
across decks. Dated outlines, such as the KIDs deck's 2026-10-04
outline, sit beside their deck. The [slide toolchain](../slides/README.md)
builds every deck. The owning repository keeps the specification each deck explains.

| Domain | Maintained source | Owner | Evidence |
| --- | --- | --- | --- |
| Input discovery and data access | [Reader deck](tolteca-datamodels-input-workflow/tolteca-datamodels-input-workflow.md) | tolteca | [Evidence](tolteca-datamodels-input-workflow/tolteca-datamodels-input-workflow-evidence.md) |
| KIDs processing and analysis | [KIDs deck](toltec-kids-data-and-analysis/toltec-kids-data-and-analysis.md) | tolteca | [Evidence](toltec-kids-data-and-analysis/toltec-kids-data-and-analysis-evidence.md) |
| Data products and publication | [Product deck](toltec-data-products/toltec-data-products.md) | tolteca | [Evidence](toltec-data-products/toltec-data-products-evidence.md) |
| Associations and inventories | [Inventory deck](toltec-associations-and-inventories/toltec-associations-and-inventories.md) | tolteca_db | [Evidence](toltec-associations-and-inventories/toltec-associations-and-inventories-evidence.md) |
| Operational workflows | [Workflow deck](toltec-operational-workflows/toltec-operational-workflows.md) | tolteca | [Evidence](toltec-operational-workflows/toltec-operational-workflows-evidence.md) |
| Deployment and execution | [Deployment deck](toltec-deployment-and-execution/toltec-deployment-and-execution.md) | tolteca_deploy | [Evidence](toltec-deployment-and-execution/toltec-deployment-and-execution-evidence.md) |
| LMT telescope files | [Telescope deck](lmt-telescope-file-workflow/lmt-telescope-file-workflow.md) | tolteca | [Evidence](lmt-telescope-file-workflow/lmt-telescope-file-workflow-evidence.md) |
| TolTEC operation (group meeting) | [OT and reduction deck](toltec-ot-reduction-workflow/toltec-ot-reduction-workflow.md) | tolteca | [Evidence](toltec-ot-reduction-workflow/toltec-ot-reduction-workflow-evidence.md) |
| TolTEC operation (findings) | [Findings deck](toltec-instrument-operations-findings/toltec-instrument-operations-findings.md) | tolteca | [Evidence](toltec-instrument-operations-findings/toltec-instrument-operations-findings-evidence.md) |
| Helpdesk and user resources | [Helpdesk deck](tolteca-helpdesk-architecture/tolteca-helpdesk-architecture.md) | tolteca_helpdesk | [Evidence](tolteca-helpdesk-architecture/tolteca-helpdesk-architecture-evidence.md) |
| Tollan infrastructure | [Tollan deck](tollan-architecture-and-workflows/tollan-architecture-and-workflows.md) | tollan | [Evidence](tollan-architecture-and-workflows/tollan-architecture-and-workflows-evidence.md) |

Workflow configuration owns inputs, operations and publication actions. Deployment
configuration owns environments, services and execution policy. Inventory slides
own association generation, transfer identity and unified metadata. Product slides
own product identity, storage and provenance. Teaching presentations are in
`../presentations/` and workshops in `../workshops/`.

The specifications own intended contracts. Companion `<stem>-evidence.md` records
list inspected implementations, executed checks and outstanding limitations.
Decks describe the current implementation without changing those contracts.

## Build and preview

The shared Marp toolchain is in [`../slides/`](../slides/). From that directory:

```sh
npm ci
npm run build:all
npm run pdf:all
npm run preview:all
```

`build:all` builds every deck in this folder, the teaching presentations and
the deck index ([`../slides/index.html`](../slides/index.html)) into
`../_build/slides/`, which Git ignores; `pdf:all` adds PDFs beside the HTML.
Rebuild before sharing; an existing export can predate its source.

`preview:all` serves the build at <http://127.0.0.1:8951/index.html>. HTML
bundles include diagrams and navigation and can also be opened directly. In a
deployment, `tolteca_dr build_docs` builds the same HTML into the published
documentation, and the operations portal links the deck index.

For one deck, from `../slides/`:

```sh
npm run build -- ../architecture/toltec-kids-data-and-analysis/toltec-kids-data-and-analysis.md \
  -o ../_build/slides/architecture/toltec-kids-data-and-analysis.html
```

Evidence files link to sources and working notes in the sibling repositories of
the development workspace; those links resolve only in that layout.

Content and verification follow the `architecture-review-slides` skill.
