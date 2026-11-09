# Operating TolTEC in v3: findings — evidence

> Moved on 2026-11-07 from `tolteca/design/` to `tolteca_tutorials/architecture/toltec-instrument-operations-findings/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-instrument-operations-findings/probes/` and build from `slides/`.

Deck: `toltec-instrument-operations-findings.md` (HTML export beside it). Draft,
2026-11-02: the handoff of the pipeline-overhead findings and input to an updated
detector setup spec. Requested by the user [claude 11-02]. The group-meeting
presentation is `toltec-ot-reduction-workflow.md`. The deck presents findings and
proposals; it does not change `detector-setup-spec.md` or any software.

## Inspected revisions

| Source | Revision |
| --- | --- |
| Tlaloc | `cpp/tlaloc` `main` `e967166` (`src/ToltecRoachManager.cc`, `src/ToltecRoachCommander.cc`) |
| v2 OT scripts and reduction | `toltec_astro/taco_recipes` `main` `c9e7364` |
| v2 toltecpipe | `toltec_astro/toltecpipe` `clipy_no_rsync` `fbf7cf8` |
| v3 hook | `python/taco_recipes` `v3` `c9e7364` plus uncommitted changes (`src/taco_recipes/kids.py`) |
| v3 KIDs, quicklook | `python/tolteca` `8bbf013` plus uncommitted changes (`tolteca_kids/fit_prepare.py`, `tolteca_quicklook/`) |
| v3 Dagster adapter | `python/tolteca_db` `c29e3b6` plus uncommitted changes (`kids_workflow.py`, `readiness.py`) |
| Detector setup spec | `python/tolteca/design/detector-setup-spec.md` (untracked) |
| Reference data | `tolteca_ref_data` `toltecdb_slice.sqlite`, `lmtmc_slice.csv`, `toltec0` 145605/145606/145609 files |
| Dagster | 1.6.6 (v2 image), 1.13.20 (dev location) |

## Claims and sources

| Slide | Claim | Source |
| --- | --- | --- |
| 3 | Sequence ↔ OT scripts | ToltecDB `ObsType`/`Date`/`Time`; LMTMC `ObsPgm`/`ObsGoal`; script contents in `observing_scripts/00_detector_setup`, `01_general_scripts/01_standard_pointing.lmtot` |
| 4 | OT node ↔ `RoachCmd` ↔ Tlaloc action | `-RoachCmd` values in the scripts; `COMMAND(...)` table in `ToltecRoachCommander.cc`; dispatch loop and functions in `ToltecRoachManager.cc` (L1203, L1275, L1307, L1623, L1815, L1885, L2347, ~L3018–3066). Cal-mode dispatch from LMT to Tlaloc is outside inspected code. |
| 5 | `exec_tune` order and state | `exec_tune` L2347–2396; `reduce_do` reads the report for VNA/TARG types without loading |
| 6 | 145609 timeline | `Header.Toltec.ObsStartTime/ObsEndTime`, `Data.Toltec.RecvTime` of both `toltec0` files |
| 7 | v2 and v3 `reduce.sh` paths | v2 `scripts/tlaloc/bin/reduce.sh`, `dispatch_tlaloc.py`, `scripts/kids/dispatch_tolteca_kids.py`; v3 `kids.py` (`run_hook`, `run_worker`, `_run_native`) |
| 8 | v3 installs native-fit `f_out` as tones | `fit_prepare.py:47` (`f_centered = f_out - lo`); `kids.py::_run_native`; spec §2.1, §9.2, §10.1. Rule from the user [claude 11-02]. |
| 9 | Inline costs | `python/run/pipeline-overhead-20261102/README.md`; `python/run/v2v3-overhead-20261102/README.md`; `python/run/inline-full-20261102/README.md` (burst rows, T5) |
| 10–12 | Quicklook timings and attribution | `python/run/v2v3-overhead-20261102/` (`v2-run1`, `v3-base`, `v3-reuse2`, `comparison-3way.md`) |
| 13, 16 | Proposed flow and spec changes | User answers to Q1–Q3 [claude 11-02]: inline saves its high-level tables as a version, no block Zarr; inline run request pending a Dagster concurrency check; first slice matches v2's quicklook |
| 14 | Curated quicklook contexts | User [claude 11-02]; `dp_quicklook` decision [kids 10-31 16:55]; after the v2-parity slice (Q3) |
| 15 | 5 s sensor floor; direct trigger | `dagster/_daemon/sensor.py` `MIN_INTERVAL_LOOP_TIME`; `_evaluate_sensor` order; `v3-direct` run |

## Status

| Item | Contract | Implementation | Verification |
| --- | --- | --- | --- |
| Tone preparation by TonePrep for every sweep | User rule; spec disagrees (F1) | v3 Target/Tune uses native `f_out` | Code inspection |
| Inline export without DPDB | Spec §11 (collector), proposal | Not implemented | Experiment harness only |
| Quicklook from inline tables, in-run registration | Proposal | Not implemented | Docker experiment, byte-identical artifacts |
| Direct sensor trigger | User record [kids 10-16 15:50] | Not implemented | Docker experiment, one run |
| Curated obsnum/lineage quicklook | User description, proposal | Not implemented | None |

## Limitations

- Docker VM (12 CPUs, 7.75 GB) is slower than production; one run per variant.
- v3 inline in Docker used Codex's Python-finding actor, without the clip-side
  hook or native fit; SSH, NFS and hardware upload are not measured.
- The deck is not yet registered in `slides/build-all.mjs` or `slides/index.html`
  (shared files in Codex's lane). No PDF was produced.

## Build and preview

```sh
cd python/tolteca/design/slides
npm run build -- ../toltec-instrument-operations-findings.md
```

Marp CLI 4.5.1, Marp Core 5.0.2 (pinned in `slides/package.json`). Checked all 18
slides at 1280×720 in the browser: no content overflow (lowest content edge
624 px), diagrams readable after simplification, keyboard navigation working.
