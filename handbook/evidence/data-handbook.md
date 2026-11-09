# TolTEC Data Handbook: editorial and publication record

> Moved on 2026-11-08 from `tolteca_helpdesk/design/` with the handbook.
> Recorded commands keep their earlier paths as history.

The implementation below records the initial prototype. The later
[framework comparison](../probes/handbook-frameworks/README.md) evaluates the
publishing framework and proposes handbook ownership of the shared glossary. The
framework experiment did not migrate content. The shared definitions now live in
the [handbook glossary](../glossary.md).

The [primary-source audit](handbook-source-evidence-20261026.md) adds recorded
raw-observation examples and a six-paper reading list. Its evidence
distinguishes recorded headers, committed writer behavior, and published
descriptions.

## Accepted reading structure — 26 October 2026

The user accepted a scientific progression after reviewing the first draft's
file-inspection emphasis. This replaces the initial task-checklist organization
as the book's main outline. File inspection remains supporting reference
material. The revised subtitle is **Observations, reduction, and analysis**. The
[chapter plan](../coverage.md#chapter-plan) records the six intended
chapters and distinguishes existing draft material from unwritten chapters.

The narrative begins with the measurement, then develops product interpretation,
calibration and mapmaking, quality, scientific analysis, and independent
reprocessing. Prepared-product users can enter at product interpretation;
understanding raw storage is not a prerequisite for their analysis. Operations
procedures remain in the operations material. Package guides and tutorials
retain their existing responsibilities.

The specific precedents are the
[WFC3 handbook structure](https://hst-docs.stsci.edu/wfc3dhb/preface/handbook-structure),
the
[SCUBA-2 overview](https://starlink.eao.hawaii.edu/docs/sc21.htx/sc21ch2.html)
and
[scientific examples](https://starlink.eao.hawaii.edu/docs/sc21.htx/sc21ch7.html),
and the
[JWST data introduction](https://jwst-docs.stsci.edu/getting-started-with-jwst-data).
WFC3 connects data structure to calibration, error sources, and analysis.
SCUBA-2 develops the measurement and mapmaking concepts before illustrated
reductions. JWST gives archive-product users an entry before optional
reprocessing. These inform the reading sequence, not TolTEC numerical values or
supported algorithms.

Against helpdesk baseline `d3b0f1c`, this revision adds one representative
opening chapter and an authored SVG schematic. The existing product, quality,
and reduction text remains initial material for later expansion. It does not
create placeholder calibration or science-analysis pages. Raw-file inspection
moves into the reference navigation at its existing URL. Its measured facts and
source record remain intact. The publishing framework and glossary ownership are
unchanged.

### Opening-chapter evidence

| Topic                                                         | Evidence used and limits                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LMT aperture, simultaneous bands, polarization-sensitive KIDs | [Lunde et al. 2022 institutional abstract](https://asu.elsevierpure.com/en/publications/the-toltec-camera-optical-alignment-and-characterization/). No beam width, sensitivity, or calibration accuracy is adopted.                                                                           |
| Separate band arrays and detector context                     | [Austermann et al. 2018 author abstract](https://arxiv.org/abs/1803.03280). Historical detector development informs physical explanation, not current usable detector counts.                                                                                                                 |
| Resonator response and readout interpretation                 | [Bisigello et al. 2016 author abstract](https://arxiv.org/abs/1602.00442), plus the recorded I/Q arrays in the existing source audit. The chapter explains the measurement; it does not prescribe that paper's calibration algorithm for TolTEC.                                              |
| Scan speed, atmosphere, and temporal/spatial scales           | Indexed text of [Thiel 2023 thesis §3.1.1](https://toltec.astro.umass.edu/papers/Thiel_Felix_M_202309_MSC.pdf), printed page 23. Direct PDF retrieval returned HTTP 502; no complete-paper or figure review is claimed. No scan-speed recommendation or numerical filtering scale is adopted. |
| Time-ordered reduction and maps                               | McCrackan et al. 2022 abstract, registered in the [source audit](handbook-source-evidence-20261026.md). Citlali's role is distinguished from the currently limited Python KIDs pipeline described in `tolteca/docs/kids-reduction.md`.                                                        |
| Polarization modulation                                       | [Lee et al. 2022 institutional abstract](https://orca.cardiff.ac.uk/id/eprint/157094/). The chapter explains the role of the modulator and angle record without claiming a released polarization recipe.                                                                                      |

The source audit's six local-PDF access limitations still apply. The opening
chapter adds general measurement explanations and a conceptual diagram; it does
not fill release-dependent scientific gaps with inferred specifications. The SVG
contains no measured or simulated dataset. Its signal traces and map illustrate
the change of representation, not quantitative recovery quality.

### Reading-structure validation

The strict handbook HTML build passed. All 286 local links and anchors and the
new image resolved in the assembled preview. Browser inspection checked the
opening chapter, the schematic at its displayed size, and the reference
navigation. No theme or stylesheet changes were needed. The preview was
refreshed under `run/data-handbook-20261026/preview`; Unity and the deployment
location's published tree were not changed. The six-chapter plan is accepted;
the new scientific prose remains a draft for review.

## Scope and evidence

Inspected 2026-10-26 against helpdesk HEAD `4223269`. The terminology campaign
in chat `10_toltec_terminology` produced `tolteca/docs/terminology.md` and
`tolteca/design/terminology-audit.md`; it did not produce a complete handbook.
Its pending discovery link in `src/tolteca_agent/data/learning.md` is preserved.

The user requested a user-facing data-handling handbook served by the portal.
The initial title is **TolTEC Data Handbook**, subtitle **Reduction and
analysis**. This covers prepared-product users as well as users performing
reductions. The first edition is a draft, not a release-specific scientific
prescription.

## Observatory precedents

These sources informed organization, not TolTEC scientific parameters. Retrieved
2026-10-26. No equivalence between their data models and TolTEC is asserted.

| Source                                                                                                                                                                    | Observed pattern                                                                                                                     | TolTEC application                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| [HST WFC3 Data Handbook](https://hst-docs.stsci.edu/wfc3dhb)                                                                                                              | Separate instrument/data handbooks; chapters on structure, calibration, errors and analysis; edition history, citation, HTML and PDF | Organize a science handbook with an explicit edition, distinct from package API references                 |
| [JWST data documentation](https://jwst-docs.stsci.edu/table-of-contents-data)                                                                                             | Access, processing, calibration status, known issues and post-pipeline analysis                                                      | Let users enter at prepared products or reprocessing; give caveats a visible home                          |
| [ALMA processing portal](https://almascience.nrao.edu/processing/science-pipeline)                                                                                        | Pipeline-version-matched manuals, product/QA guidance, known issues and provenance                                                   | Record software/calibration applicability and separate reproduction from updated processing                |
| [SCUBA-2 cookbook](https://starlink.eao.hawaii.edu/docs/sc21.htx/sc21.html) and [JCMT tutorials](https://www.eaobservatory.org/jcmt/science/reductionanalysis-tutorials/) | Reduction choices, diagnostics and post-processing paired with runnable tutorials and downloadable datasets                          | Keep conceptual guidance in the handbook; pair tested recipes in tutorials with independent reference data |

## Content ownership

The [specification](../../design/spec.md#handbook) owns the handbook boundary.
The handbook owns shared scientific terminology. Package guides own the terms
used by their software and link to the handbook for scientific definitions. Do
not present proposed API names or internal architecture as instructions for
astronomers. Package guides own supported commands and fields. Tutorials own
runnable sequences and example inputs/outputs.

Each scientific procedure needs: user goal; input and software applicability;
prerequisites; ordered actions; expected outputs; scientific checks;
limitations; and a reproducibility record. Add commands only with a tested
recipe and an identified owner. Do not fill absent archive policies, calibration
values, QA thresholds, or citation instructions with plausible defaults.

## Initial coverage and next scientific slice (prototype record)

The draft contains product inspection, reduction preparation, quality questions,
provenance, and an explicit coverage/edition page. It provides no executable
end-to-end reduction and no release-specific certification.

The next recommended slice is **one identified prepared map through inspection
and one defined measurement**. Required evidence: distributable input products;
file/units/uncertainty definitions; known calibration and processing
limitations; a runnable tutorial; expected figures and numerical checks; and
scientific review. Then extend to reproducing that map from its documented
inputs. This order gives archive users a useful result before covering every
reduction branch.

Before a reviewed edition, identify a scientific owner for each chapter and
record the reviewed software/data scope. Preserve an edition history. Publish
immutable, citable editions and a matching PDF when a stable reviewed edition
exists; neither version selection nor a PDF export is implemented by this draft.

## Publication and assistant boundary

The handbook uses the existing Sphinx/MyST and book theme dependencies, with its
own reader navigation and no API imports. `build_docs` stages its source, runs a
strict build, rewrites package-document links to the same publication, and only
then switches the existing `current` publication. `/handbook/` redirects to the
book within that published tree; existing path containment protects its files.
No new service or Apache rule is needed.

The book exposes the original Markdown through Sphinx's source links. Draft
chapters are not added to the Llama or agent retrieval manifest in this change.
After review, select the same authored chapters for the existing source catalog
with explicit use-case assignments; do not create a generated-answer copy.

## Initial prototype validation

- Strict handbook HTML build: passed without warnings.
- Helpdesk package HTML: passed with online dependency inventories and the
  locally published Tollan inventory. The sandboxed attempt could not fetch
  inventories; no warning filters were relaxed.
- Package tests: 80 passed, including a failed handbook build preserving the
  previous complete publication and handbook entry paths for both audiences.
- Guide doctests: two tests passed. Ruff and type checks passed.
- Checked 165 local links in rendered handbook pages, including chapter anchors
  and linked package documentation, against the assembled preview.
- Browser visual inspection was blocked by the app's browser security policy. No
  screenshot or visual approval is claimed.

The preview at `http://127.0.0.1:8056/science/handbook/` uses an isolated tree
under `run/data-handbook-20261026/preview`: the previous local package
publication, the terminology campaign's rendered draft, and the new handbook. It
does not replace the location's published `current` tree or update Unity. A full
fresh build of all sibling packages and scientific review remain outside this
initial draft's validation. The glossary is still unpublished.
