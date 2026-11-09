# Operational workflows — current presentation evidence

> Moved on 2026-11-07 from `tolteca/design/` to `tolteca_tutorials/architecture/toltec-operational-workflows/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-operational-workflows/probes/` and build from `slides/`.

Date: 2026-10-19. Scope: requested architecture deck split and current API updates.
The deck contains 14 main slides and 0 appendix/reference slides.

## Contract and implementation

The specifications remain authoritative. This update changes slide sources,
build/preview tooling and presentation probes only. Relevant working trees contain
substantial pre-existing changes; HEAD alone does not identify the inspected code.

HEAD revisions: `tolteca` `486244a`, `tolteca_db` `c29e3b6`, `tolteca_web` `9db03d8`, `tollan` `72d90f5`, `tolteca_deploy` `5e7997c`.

Inspected current sources:

- [tolteca_db/src/tolteca_db/kids_workflow.py](../../../tolteca_db/src/tolteca_db/kids_workflow.py)
- [tolteca_db/src/tolteca_db/inventory_workflow.py](../../../tolteca_db/src/tolteca_db/inventory_workflow.py)
- [tolteca/src/tolteca_kids/runner.py](../../../tolteca/src/tolteca_kids/runner.py)
- [tolteca_web/src/tolteca_web/quicklook.py](../../../tolteca_web/src/tolteca_web/quicklook.py)
- [tolteca_web/src/tolteca_web/data/location/run/tolteca_web.default/just.d/00_default.just](../../../tolteca_web/src/tolteca_web/data/location/run/tolteca_web.default/just.d/00_default.just)

## Executed examples and scope

The current kids_workflow factory creates loadable Dagster Definitions in the configuration probe. The active package-owned code location imports that factory; the older tolteca_db.dagster experiments are not the presented entry point. The KIDs runner/publication snippets execute independently of Dagster. Docker lifecycle tests were not rerun for this slide update.

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
