# From OT script to quicklook — evidence

> Moved on 2026-11-07 from `tolteca/design/` to `tolteca_tutorials/architecture/toltec-ot-reduction-workflow/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/toltec-ot-reduction-workflow/probes/` and build from `slides/`.

Deck: `toltec-ot-reduction-workflow.md` (HTML export beside it). Draft,
2026-11-03, for a group meeting on how v3 operates TolTEC during observing.
Requested by the user [claude 11-02] as the presentation counterpart of the
findings deck `toltec-instrument-operations-findings.md`.
The deck presents the v3 workflow; it changes no specification or software.
Revision 2026-11-03 [claude 11-03]: the labels "intended" and "now"/"current" became
"v3" and "v3 previous"; the status slide ("What runs today, what is intended") was
removed (its content stays in the Status table below); part 2, detector power
setup, follows slide 12. Slides 14–19 present the detector setup specification
and are labelled "v3 previous"; slides 20–22 present the power-setting contract
agreed on 2026-10-27, labelled "v3", as slide 11 does for quicklook [claude 11-03].

## Inspected revisions

| Source | Revision |
| --- | --- |
| Tlaloc | `cpp/tlaloc` `main` `e967166` (`src/ToltecRoachManager.cc`) |
| OT scripts | `toltec_astro/taco_recipes` `main` `c9e7364` (`observing_scripts/00_detector_setup/10_toltec_detector_init_coarse.lmtot`, `12_toltec_tune_3_iters.lmtot`, `01_general_scripts/01_standard_pointing.lmtot`); untracked `00_detector_setup/v3/` variants differ only by a sample-rate action |
| v3 hook and worker | `python/taco_recipes` `v3` plus uncommitted changes (`src/taco_recipes/kids.py`: `run_hook`, `run_worker`, `_run_native`) |
| Reference data | `tolteca_ref_data` `test_fixtures/toltecdb_slice.sqlite`, `lmtmc_slice.csv`; `toltec0` and `tel` files of 145605–145612 under `toltec_astro_dev/run/data_lmt` |
| Measurements | `python/run/v2v3-overhead-20261102/` (`README.md`, `comparison-3way.md`); `python/run/inline-full-20261102/` (T5: one inline request per network); `python/run/pointing-reduction-20261102/` |
| Power setup (part 2) | `tolteca/design/detector-setup-spec.md` revision 1.0 (accepted design; production qualification incomplete), §2, §5–§8; detector power setup specification revision 1.1 (`python/run/detector-power-setup-20261022/specification.md`); `roach-tone-preparation-review-20261030.md`; `drive-fit-normalization-20261021.md` (Table 2) |
| Power products | `python/run/detector-power-setup-20261022/replayed-example/dataprod_toltec/scratch/`: `dp_drivefit` of 145484-1-1 and `dp_drive_fit_commit` of 145485-0-1, network 0 (`results.json`: 632 channels, 506 accepted, A⋆ 8.348090 dB, written 8.25 dB) |
| v3 power contract | Group-chat discussion of 2026-10-27, pasted by the user [claude 11-03]: another agent's proposal for Tlaloc (explicit, validated waveform normalization; waveform and drive attenuation applied together inside Tune; one tone configuration with an identifier, applied state recorded, no silent substitutions) and the user's replies (largely agreed; the Tune change is the minimal change; drive-fit artifacts anchor detector power in dBm; TonePrep prepares the settings that realize it; the ROACH power-chain config is versioned and persisted). The proposal's document code names are another agent's and are not in this workspace |
| Power OT profiles | `toltec_astro/taco_recipes` untracked `observing_scripts/00_detector_setup/v3/21_…`, `13_…` (authored, offline checks only); site scripts at `c9e7364` |

## Figures

All figures are inline SVG written by `probes/render_ot_reduction_workflow.py`.
The probe reads the reference data read-only and replaces each
`<svg id="fig-…">` block in the deck source. Docker durations are constants
in the probe, cited to `comparison-3way.md` and the README.

| Slide | Figure | Source of each value |
| --- | --- | --- |
| 2 | `workflows` | User framing of the three workflows [claude 11-02] |
| 3 | `night` | Starts: ToltecDB `Date`/`Time` (RoachIndex 0). Ends: `toltec0` `ObsEndTime` (145605, 145606, 145609 scans 1–2); `tel` `TelTime` maximum (145608, 145610/145611 scan 2). Estimated: 145607 (145606 duration), Tune scans of 145610–145612 (next scan start − 3 s, as 145609), 145612 Lissajous (145609 duration). Reduce markers inside Tunes without a `toltec0` file use the 145609 block offsets. |
| 5 | `sweep-cycle` | OT script node order; `reduce_do` L1203, `targ_load_from_file` L1275, `targ_read_file` L1885 |
| 6 | `tune-sequence` | `exec_tune` L2347–2396; durations from the 145609 `toltec0` `RecvTime` blocks and `ObsEndTime` |
| 7 | `pointing` | 145609 `toltec0` headers and `RecvTime`. `reduce.sh`: slowest of the 10 recorded networks started at once, clip side included, no SSH (`python/run/inline-full-20261102`, `summary.json` burst; v3 without saving a version). Tune quicklook: Docker, Valid → MC (v2 52.7 s, v3 13.3 s). Pointing map: run start 6.8 s (Docker Tune quicklook) + `python/run/pointing-reduction-20261102/152434` (preparation 15.2 s, input projection 2.2 s, Citlali 23.6 s) |
| 8 | `inline-steps` | `kids.py` hook/worker split; user rule on TonePrep and TlalocOutput; inline saves the high-level tables as a version, no block Zarr (Q1) [claude 11-02] |
| 9 | `inline-time` | `python/run/inline-full-20261102` (T5, burst): 10 networks of a block at once; bar = slowest network; light = clip side (v2 native `kids` and v3 hook + native fit, measured apart from the burst), dark = Taca side; v3 is the inline request with its tables staged (`burst-stage`); the note's version cost is `collect` (fresh DPDB) |
| 10 | `ql-sequence` | toltecpipe readiness rule; Dagster `MIN_INTERVAL_LOOP_TIME` = 5 s; direct-trigger experiment `v3-direct` |
| 11 | `ql-time` | v2 composition (README); v3 previous and v3 stage times (`comparison-3way.md`) |
| 15 | `power-toneprep` | Schematic of spec §7.1–7.2 (no data). Matched tones keep their probe's amplitude; ambiguous matches take the probe's amplitude or, opt-in, the scaled LUT fill; one common normalization; attenuation unchanged |
| 16 | `power-fit` | `dp_drivefit` of 145484, network 0, channel 450: reduced I/Q magnitude per attenuation relative to the first sample, and `a` per attenuation; selection 9.76 dB (a = 0.183 at 10 dB, 0.326 at 8 dB). Channel 450 replaces the spec's worked channel 596 on the slide because 596's window holds a second resonance; 596 is cited in the notes |
| 17 | `power-commit` | `dp_drive_fit_commit` of 145485, network 0: policy attenuation per tone (457 fitted, 49 raised to the 6 dB cutoff, 126 filled with the 8.79 dB median), input and committed amplitudes |
| 18 | `power-lifecycle` | Spec §2.3–2.9 script sequences; Tlaloc LUT/FILE amplitude selection (L686–745) and `attens_set_drive_from_file` (L3361); user [01a15a02 10-20 22:01, 22:15] on calibration groups and commit reuse |
| 20 | `power-v3-flow` | v3 contract: owners and data flow (drive fit dBm targets, TonePrep, tone configuration, Tlaloc, acquisition metadata; power-chain config shared with SweepCheck readout power) |
| 21 | `power-v3-tune` | v3 contract: coordinated application inside Tune between block 0 and block 1 |
| 25 (A2) | `ql-versions` | User description of curated quicklook [claude 11-02]; `dp_quicklook` [kids 10-31 16:55]; moved to the appendix because the first slice matches v2's quicklook (Q3) |

## Status

| Item | Contract | Implementation | Verification |
| --- | --- | --- | --- |
| OT node → Tlaloc action, `exec_tune` order | Tlaloc `main` | Production | Code inspection; headers of 145609 |
| Inline steps for every sweep, native fit for the model | User rule | VNA only; Target/Tune install the fit's `f_out` | Code inspection |
| Inline version of the high-level tables, registered | User answer Q1 [claude 11-02] | Not implemented; existing `Kids.output` always writes block `array.zarr` | T5 harness, Docker |
| Quicklook from inline results, registration in the same run | Proposal | Not implemented | Docker, one run, byte-identical plots |
| Readiness sensor requests runs directly | User record [kids 10-16 15:50] | Not implemented | Docker, one run |
| Pointing map quicklook (v2 parity, Q3) | v2 `reduce_pointing.sh` via toltecpipe | `tolteca_reduce` rejects `reduction_type: pointing` | Citlali on the driver's prepared inputs, 152434 |
| Obsnum and lineage quicklook versions | User description; after the v2-parity slice (Q3) | Not implemented | None |
| TonePrep amplitudes at fixed attenuation, default v2 values | Detector setup spec §7 | `tolteca_kids.tone_prep` (uncommitted, kids lane) | Eight production-v2 comparisons exact (review 2026-10-30) |
| TonePrep scaled-LUT fill, crest-factor search | Spec §7.2; user [01a15a02 10-23] | Implemented, opt-in | Controller/LUT probe; real VNA, target, Tune blocks |
| Drive fit and commit workflows, summed-power normalization | Spec §5–§6 | `tolteca_kids.drive_fit`, `drive_fit_commit` (uncommitted, kids lane) | Network 0 example, nine-trial perturbation replay, 64 focused tests (power spec §6) |
| v3 OT power profiles (`21_…`, `13_…`) | Spec §2.7–2.8 | Authored, untracked in site `taco_recipes` | Offline action/order checks; not run at the site |
| v3 power contract: dBm targets, attenuation prepared per Tune and applied with the comb | User agreement 2026-10-27 | Not implemented; needs the Tlaloc Tune change; `detector-setup-spec.md` §7.3 and TonePrep's fixed-attenuation rule [kids 10-30 19:28] still describe v3 previous | None |
| v3 Tlaloc interface: one tone configuration, validation-only normalization, applied state recorded | User agreement 2026-10-27 (simplifications) | Not implemented | None |
| `reduce.sh` routing of `drivefit_reduce`, `drivefit_commit` | Spec §9.2 | Not in the v3 hook (`python/taco_recipes/src/taco_recipes/kids.py` has no drive-fit route) | None |

## Limitations

- The deck's Mermaid renderer (beautiful-mermaid 1.1.3 in Marp Core 5.0.2)
  supports flowchart, state, sequence, class, ER and XY charts, not Gantt or
  timeline diagrams, and renders labels at a fixed size near 13 px. Diagrams are
  therefore generated SVG at 18–23 px.
- Quicklook durations come from one run per variant on a 12-CPU VM with 13
  networks; the recording has 10 networks. Inline durations (slides 7, 9) come
  from T5: one burst per block, 10 networks, one run; no SSH; clip-side times
  measured apart from the burst. The v2 burst (9.0 s for Tune block 1) is within
  the recorded 9.6 s, which includes SSH.
- The one-version-per-acquisition layout is measured as staging in each inline
  call plus one `collect` after `Valid`; who runs `collect` is open (Q1a). Saving a
  version in every call was measured and rejected: its cost grows with stored
  versions (F10) and 2 of 70 concurrent registrations failed (F12).
- v2's pointing map quicklook (toltecpipe `dispatch_reduction.sh` →
  `reduce_pointing.sh`) is not measured.
- The pointing map was measured on a different obsnum (152434, 2026-02-19, 11
  networks, 60 s Lissajous) on the local host with 12 threads, because 145609
  has only `toltec0` locally. `tolteca_reduce` rejects `reduction_type: pointing`
  (`tolteca_reduce.prepare.native_config`: "This slice materializes science
  maps"), so `run_pointing_native.py` repeated the adapter's `read_preparation`
  and `project_inputs` steps and ran the same Citlali build in pointing mode. The
  Citlali settings are v2's production pointing settings. The APT matched 3,865
  of 5,518 channels against the 137389 beammap. Fit values are not validated
  against v2. 149100, the reduce thread's pointing obsnum, has only 6 of 11
  networks locally.
- The probe is not lint-clean under the tolteca Ruff configuration (style rules
  such as docstrings, argument counts and line length); other probes also carry
  findings.
- Part 2 figures read the replayed products under `python/run/`, local and
  untracked. The power example is computed from recorded sweeps; no settings were
  applied to hardware. Recorded 2025-10-31 network 0: 145485 and 145486 ran in FILE
  mode at 7.25 dB with LUT-range amplitudes (maximum 0.469; a committed amplitude
  file peaks at 1), so the production commit's amplitudes were not in effect there.
  This is cited in the notes of slide 19 only.
- MathJax in Marp Core 5.0.2 cannot load its dynamic font for `\ell`; slides use
  the Unicode `ℓ` outside math.
- Registered in `slides/build-all.mjs`, `slides/preview.py`, `slides/index.html` and
  `slides/README.md` with the findings deck (2026-11-02).

## Build and check

```sh
cd python
toltec_astro_dev/.venv/bin/python tolteca/design/probes/render_ot_reduction_workflow.py
cd tolteca/design/slides
npm run build -- ../toltec-ot-reduction-workflow.md
```

Checked 2026-11-03 after the v3 power slides: all 25 slides at 1280×720 keep
content within the frame (lowest edge 662 px, slide 5; no element past the right
margin); slides 11, 14–22 inspected at 1280×720, slides 18 and 22 at 1024×640; no
console errors. `npm run pdf -- --allow-local-files` produced 25 pages; pages
13–22 inspected as page images with every figure and formula rendered. The Marp
build sometimes stalls on its first run after an edit; rerun it. The findings deck: 18 slides
within the frame at 1024×640 (lowest edge 647 px), PDF 18 pages.
