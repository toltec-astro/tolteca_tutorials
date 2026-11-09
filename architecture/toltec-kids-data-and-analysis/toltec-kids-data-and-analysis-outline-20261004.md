# Applying the review to TolTEC KIDs

This is a worked content outline for the first deck, based on the local working
tree on 2026-10-04, including uncommitted reducer integration. Its API names,
layouts, and findings are historical. Recheck them against the maintained
specification, current callers, and executed examples before reuse. This outline
does not establish current requirements or verification.

Use the earlier architecture deck (workspace `refs/TolTEC v3 Data Processing
Architecture.html`) for presentation context and the tolteca guide
`docs/kids-reduction.md` for runnable workflows. The important question is: **what does the object contain
at each stage, and which view gives access to it?**

## Content manifest

1. Data flow: acquisition, block discovery, channel selection, reduction,
   analysis, export and reopening.
2. Show responsibilities: Tollan supplies the general access/analysis machinery;
   `tolteca_datamodels` knows the recorded TolTEC format; `tolteca_kidsproc`
   supplies generic KIDs views and analyses; `tolteca_kids` orchestrates a run.
3. Show the opened native Dataset, then the acquisition tree obtained through
   `.toltec_kids.tree` / `.blocks`. Label the stage at which block discovery occurs.
4. Zoom into a sweep block: reduction creates `sweep`; D21 consumes its sweep
   view and installs its own namespace in the same block scope.
5. Use a separate timestream acquisition example: prepared samples and PSD
   results are siblings. One `.toltec_kids.timestream` view exposes both.
6. Show data in memory versus the compact Zarr export, then reopening and
   selecting one channel. Include detaching a block for independent analysis.
7. Capability scope: supported analyses and explicit extension boundaries.

The maintained [deck source](toltec-kids-data-and-analysis.md)
may contain later revisions of these APIs.
Follow the parent skill's content rules. Record observed defects in the companion
evidence file; show limitations on slides when they qualify a displayed contract.

## Sweep acquisition after block reduction and D21

Paths below describe the recorded example's in-memory DataTree nodes. `[S]` means an attributes-only scope and
`[D]` means a Dataset carrying variables. Array descriptions use semantic names;
obtain literal variable names and dimension sizes from the executed example.

```text
/ [S] acquisition metadata
├── raw [D] native netCDF variables, including recorded I/Q
└── blocks [S] collection metadata
    ├── index [D] one row per block and selection bounds
    ├── chan [D] shared channel columns across blocks
    ├── probe [D] shared probe/step/repetition columns
    ├── 0 [S] complete inherited block metadata
    └── 1 [S] complete inherited block metadata; selected analysis scope
        ├── sweep [D] reduced I/Q, uncertainties, frequencies
        └── tolteca_kidsproc.analysis.d21 [S] producing analysis configuration
            ├── d21 [D] matched derivative result
            └── d21_unified [D] unified derivative result
```

This is a representative tune acquisition with two discovered blocks, reducing
the second one. The diagram is not a requirement that acquisitions have two
blocks. The raw payload and shared axes are not physically repeated under each
block; the block views select them. Scope nodes carry metadata without arrays
whose coordinates would constrain the analysis leaves.

Pair this tree with the tested calls from the guide, including
`SweepReducer()(tree, parent_namespace="blocks/1")` and D21's explicit input view
and output scope. Show the effective source for each accessor/view rather than
drawing every Python property as another stored node.

## Timestream block after reduction and PSD

This is an alternative branch from a timestream acquisition, not evidence that
the current reader already detects arbitrary mixed sweep/timestream files.

```text
blocks/0 [S] complete block metadata; selected analysis scope
├── timestream [D] prepared I/Q on (chan, time); reducer configuration
└── tolteca_kidsproc.analysis.psd [S] producing analysis configuration
    ├── psd [D] channel spectra and frequency-band statistics
    └── psd_common [D] optional channel median/MAD spectra
```

Explain shared axes beside the tree: one `time(time)` coordinate for every
channel, channel spectra on `(chan, f_psd)`, and common spectra on `(f_psd)`.
The native samples remain at the acquisition's `raw` leaf. Views retain original
channel IDs. PSD uses the recorded sampling rate; checking continuity and handling
missing samples belong to the surrounding workflow.

Show `.toltec_kids.timestream` for the combined signal/spectral view and
`.kids.psd` for the shared analysis view. Explain that magnitude and phase spectra
do not imply model solving; optional supplied `r/x` data are not a Python solver.

## Persistence and remaining boundaries

- Contrast the in-memory tree with exported nodes. Compact native export keeps
  raw samples once and retains reduction metadata while omitting reconstructible
  time-sample projections. Reopened TolTEC views rebuild those projections
  lazily; generic xarray reopening alone does not repopulate every view as a node.
- With `include_raw=False`, results and metadata remain, but recorded time
  samples are unavailable. Do not draw virtual samples in that exported tree.
- A detached block carries the local raw selection when requested and the axis
  data it needs. Show the acquisition and detached roots separately so relative
  namespaces and independence are visible.
- The selected-block sweep API and the existing standalone aggregate-sweep
  pipeline still have different layouts. Show this as a current integration
  boundary instead of drawing a unified contract that has not been implemented.
- Mixed-file boundary detection, model solving, and telescope clock alignment
  need their own status/evidence. Supporting a storage layout is not proof that
  discovery or analysis of every future input already works.
- Demonstrate local reopen/selection separately from remote partial-query
  performance. A Zarr diagram does not establish how many chunks are fetched.

## Evidence to inspect when building the deck

The links below locate current inspection targets. They do not update or reverify
the historical examples above.

- Layout and discovery: [core.py](../../../tolteca/src/tolteca_datamodels/toltec/kids/core.py)
  and [blocks.py](../../../tolteca/src/tolteca_datamodels/toltec/kids/blocks.py).
- Reduction and views: [sweep.py](../../../tolteca/src/tolteca_kids/sweep.py)
  and [timestream.py](../../../tolteca/src/tolteca_kids/timestream.py).
- Analysis namespaces: [D21](../../../tolteca/src/tolteca_kidsproc/analysis/d21.py)
  and [PSD](../../../tolteca/src/tolteca_kidsproc/analysis/psd.py).
- Representative behavior: [block tests](../../../tolteca/tests/tolteca_kids/test_block_tree.py),
  [timestream/export tests](../../../tolteca/tests/tolteca_kids/test_timestream_domains.py),
  and [configured pipeline tests](../../../tolteca/tests/tolteca_kids/test_timestream_pipeline.py).

Record the input filenames, selections, configuration, and resulting paths/dims
from the actual run. Use those observations to update the diagrams before
presenting them as verified. Keep measured tree inventories in the companion
evidence file unless the inventory itself is useful API reference material.

## Initial example check — 2026-10-04

The two layouts above were checked against reference files under
`toltec_astro_dev/run/data_lmt/toltec/tcs/toltec0`, selecting original channel IDs
`[0, 5]`. The source was `tolteca` HEAD `29a6ef4` plus the local uncommitted
reducer integration; no reference data were modified.

| Input and operation | Observed result |
| --- | --- |
| `toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc`, default opening, reduce block 1, run default D21 | Two blocks; `sweep` and matched `d21` have `iqlen=2, sweep=177`; unified result has `f_unified=1169` |
| `toltec0_145609_000_0002_2025_10_31_09_27_57.nc`, opened with `chunks={}`, first 256 samples, PSD with `nperseg=64, compute_common=True` | One block; `timestream` has `chan=2, time=256`; `psd` has `chan=2, f_psd=33`; `psd_common` has `f_psd=33` |

An additional sweep probe with `chunks={}` failed in `D21Analysis.make_unified`:
the frequency bound was a Dask Array and `.to_value(u.Hz)` raised `AttributeError`.
The default-opening example succeeded. Treat Dask-backed unified D21 as an open
finding until resolved and rechecked; these tree checks do not establish full
lazy execution or remote performance. This guideline task made no software fix.
