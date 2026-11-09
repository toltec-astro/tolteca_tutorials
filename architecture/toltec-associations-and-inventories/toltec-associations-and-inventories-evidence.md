# Associations and inventories — current presentation evidence

> Moved on 2026-11-07 from `tolteca_db/design/` to `tolteca_tutorials/architecture/toltec-associations-and-inventories/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-associations-and-inventories/probes/` and build from `slides/`.

## Optional inventory roles implemented — 2026-10-24

Scope: separate default write attribution from journal publishing. Reviewed
working trees include substantial earlier changes at `tolteca_db` HEAD `c29e3b6`,
`tolteca_web` HEAD `9db03d8` and `tolteca` HEAD `2613923`. This update does not
modify Unity, running deployments or the separate accessor refactor.

Implementation and caller changes:

- Setup config selects the optional default and publisher independently. The
  default is a database-local inventory role; portable records do not import it.
- Registry population no longer initializes ownership or a journal. Test and
  probe fixtures requiring operational setup now use `create_db_and_tables`.
- Pure unified imports preserve supplied ownership without either destination
  role. Derived tags use explicit `tag_inventory` or the configured default.
- `local_inventory` callers now use `default_inventory`; no alias is retained.
- Existing publishing identity/history cannot be removed or reassigned by setup.
  Operational defaults still create one inventory for both roles.

QA:

- 60 focused DPDB tests passed, including pure-destination bootstrap, incremental
  import, concurrency, rollback, attribution, typed config and publication.
- Six capture tests passed, including bounded work with growing observation
  membership, unrelated history and version-group membership.
- One HTTP journal transport test passed with a pure destination.
- Changed Python files passed Ruff and syntax checks; changed implementation
  modules passed `ty`. The unified YAML example passed typed validation.
- The publication example registered seven products, two runs and three
  publications, with two journal entries in a fresh temporary output.
- Focused strict Sphinx build passed with no warnings. The ownership guide was
  inspected in the browser. Deck HTML/PDF were rebuilt. Browser inspection found
  footer overlap on slide 12; compact YAML removed it. Slides 12 and 20 were
  inspected after the fix; DOM checks found no section overflow on all 20 slides.

Limits: CLI/handler, broader association-ingestion and Web integration suites
cannot collect because `ingest/file_scanner.py` still imports the removed
`tolteca_datamodels.toltec.file` module. This is the separate accessor caller port.
PostgreSQL execution, Docker, Unity and full documentation builds were not rerun.
No migration is supplied for existing test databases.

Review artifacts: `/tmp/inventory-roles-turn.diff` compares this turn against its
saved starting files, not Git HEAD. `just review` refreshes the complete pending
workspace diff at `/tmp/toltec-python-workspace-review.diff`.


## Inventory and journal terminology alignment — 2026-10-24

Reviewed working trees: `tolteca_db` HEAD `c29e3b6` and `tolteca` HEAD `2613923`,
including pending model and journal changes. The deck now has 14 main slides and
6 appendix/reference slides.

The deck distinguishes logical inventory identity, inventory-specific namespace
paths and artifact locations. The added reference slide separates `DataProdBatch`,
`DataProdJournal`, `DataProdJournalEntry` and `DataProdImportState`. The limits slide
marks optional default inventory ownership as agreed but not yet implemented.

Sources: [inventory ORM](../../../tolteca_db/src/tolteca_db/models/orm/inventory.py),
[journal API](../../../tolteca_db/src/tolteca_db/journal.py), and the
[registration guide](../../../tolteca_db/docs/publish-product-example.md#inspect-the-journal).

HTML and PDF rebuilt with the pinned Marp toolchain. All 20 PDF pages were rendered
and inspected as contact sheets; browser checks found no section overflow and the
new journal slide was inspected at full size. The publication example and focused
strict Sphinx build passed; details are in the
[product evidence](../toltec-data-products/toltec-data-products-evidence.md).
No graph-scaling, Docker, remote-journal or Unity acceptance was rerun for this
documentation update. Presenter/offline and smaller-viewport checks were not repeated.

## Earlier presentation evidence — 2026-10-19

Date: 2026-10-19. Scope: requested architecture deck split and current API updates.
The deck contains 14 main slides and 5 appendix/reference slides.

## Contract and implementation

The specifications remain authoritative. This update changes slide sources,
build/preview tooling and presentation probes only. Relevant working trees contain
substantial pre-existing changes; HEAD alone does not identify the inspected code.

HEAD revisions: `tolteca` `486244a`, `tolteca_db` `c29e3b6`, `tolteca_web` `9db03d8`, `tollan` `72d90f5`, `tolteca_deploy` `5e7997c`.

Inspected current sources:

- [tolteca_db/src/tolteca_db/associations/rules.py](../../../tolteca_db/src/tolteca_db/associations/rules.py)
- [tolteca_db/src/tolteca_db/associations/generator.py](../../../tolteca_db/src/tolteca_db/associations/generator.py)
- [tolteca_db/src/tolteca_db/associations/pool.py](../../../tolteca_db/src/tolteca_db/associations/pool.py)
- [tolteca_db/src/tolteca_db/product_index.py](../../../tolteca_db/src/tolteca_db/product_index.py)
- [tolteca_db/src/tolteca_db/inventory_workflow.py](../../../tolteca_db/src/tolteca_db/inventory_workflow.py)
- [tolteca_db/docs/product-indexes.md](../../../tolteca_db/docs/product-indexes.md)

## Executed examples and scope

The displayed unify configuration validates against DataProdConfig. Source review traces both ingestion and portable import to AssocPool/AssocRules/AssocGenerator. Recorded calibration examples retain their previous reference-slice evidence. This update does not rerun graph-scaling or remote-journal integration tests.

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
