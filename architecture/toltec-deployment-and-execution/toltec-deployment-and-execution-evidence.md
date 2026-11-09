# Deployment and execution — current presentation evidence

> Moved on 2026-11-07 from `tolteca_deploy/design/` to `tolteca_tutorials/architecture/toltec-deployment-and-execution/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-deployment-and-execution/probes/` and build from `slides/`.

Date: 2026-10-19. Scope: requested architecture deck split and current API updates.
The deck contains 14 main slides and 0 appendix/reference slides.

## Contract and implementation

The specifications remain authoritative. This update changes slide sources,
build/preview tooling and presentation probes only. Relevant working trees contain
substantial pre-existing changes; HEAD alone does not identify the inspected code.

HEAD revisions: `tolteca` `486244a`, `tolteca_db` `c29e3b6`, `tolteca_web` `9db03d8`, `tollan` `72d90f5`, `tolteca_deploy` `5e7997c`.

Inspected current sources:

- [tolteca_deploy/src/tolteca_deploy/execution.py](../../../tolteca_deploy/src/tolteca_deploy/execution.py)
- [tolteca_deploy/examples/docker/slurm/definitions.py](../../../tolteca_deploy/examples/docker/slurm/definitions.py)
- [tolteca_deploy/examples/docker/slurm/policy.py](../../../tolteca_deploy/examples/docker/slurm/policy.py)
- [tolteca_deploy/examples/docker/slurm/slurm_client.py](../../../tolteca_deploy/examples/docker/slurm/slurm_client.py)
- [tolteca_deploy/docs/execution.md](../../../tolteca_deploy/docs/execution.md)
- [tolteca/design/unity-slurm-execution.md](../../../tolteca/design/unity-slurm-execution.md)

## Executed examples and scope

The displayed target/profile YAML validates against ExecutionConfig. The Python example resolves the retained QA profile, checks allowed node/CPU overrides and round-trips SlurmRequest. Docker lifecycle/admission evidence is in slurm-execution-profiles-20261019.md. No Unity submission or production deployment is claimed.

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


## Application integration update

The package adapter and normal KIDs asset factory now share the Slurm execution
path. The deck's adapter/status wording reflects this promotion. Current workflow,
CLI, recovery and Web verification is recorded in
[Slurm application integration](../../../tolteca_deploy/design/slurm-workflow-integration-20261019.md). The
original presentation-only audit above describes the preceding deck split.

## Execution update (2026-11-08)

Slides 3, 5 and 7–14 now present `tollan.execution`, which replaced the
`tolteca_deploy` execution adapter shown above (targets, profile priorities,
overrides, `SlurmExecution`, attempt directories). Slides 4 and 6 are unchanged.

| Slides | Contract or implementation source |
| --- | --- |
| 3, 5, 7 | Tollan spec, "External execution" (ownership); `tolteca_deploy` handoff H1 (deployment supplies `execution.profiles`) |
| 8–9 | Tollan guide `docs/execution.md`, "Declare execution profiles" and "Resolve a job spec"; `tollan.execution.policy` |
| 10 | Tollan spec, "Orchestration integration" (pools; Slurm enforces capacity) |
| 11–12 | Tollan spec, "Job records and schedulers" and "Supervision"; guide "Run a job" |
| 13 | Tollan guide, "Run jobs from Dagster"; `tollan.execution.dagster.PipesJobClient` |
| 14 | `tolteca/src/tolteca_reduce/jobs.py` (job records with a local profile); `tolteca_db/src/tolteca_db/kids_slurm.py` still imports `tolteca_deploy.execution` (Codex lane, handoff H2) |

Inspected state: tollan `v3.x` HEAD `e054081` with uncommitted audit changes;
`tollan.execution` itself is committed (`45d901b`). No Unity submission is
claimed.

Checks:

- `probes/deployment_execution.py` validates the displayed profiles, runs the
  displayed resolution (profile, CPUs, node narrowing, thread environment,
  YAML round trip), checks the first-match and maximum-resource rules, and
  compiles the Dagster example. It passes with the development location's
  Python.
- The cross-deck probe (`../probes/architecture_decks.py`) no longer refers to
  this deck's execution examples. It still fails on
  `tolteca_datamodels.data_prod_run`, which Codex's data-product refactor
  removed (unrelated to this update).
