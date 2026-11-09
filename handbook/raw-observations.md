# Raw-file reference

Use this reference to identify recorded files and inspect their readout
metadata. For the measurement context, begin with
[TolTEC observations and measurements](observations.md); for processing,
continue to [reduction preparation](reduction.md).

The examples below use recorded acquisitions from 31 October 2025 and 16
May 2026. They illustrate what to check in your files; they do not define the
configuration or quality of every TolTEC observation.

## Identify the acquisition and its streams

Keep the acquisition controller, observation number, sub-observation number,
scan number, and interface with each input. An observation number alone can
refer to several acquisitions and several readout files. Read these identifiers
from the metadata when checking a dataset, especially after files have been
renamed or moved. The
[input selection guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-inputs.html)
explains filename discovery and header-based inspection; the
[observation selector guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html)
explains how to select the intended acquisitions and interfaces.

For example, observation 145609 includes these two files for interface
`toltec0`:

```text
toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc
toltec0_145609_000_0002_2025_10_31_09_27_57.nc
```

Both record the TCS controller and sub-observation 0. Their scan numbers and
recorded acquisition types differ:

| Header quantity            | Scan 1       | Scan 2         |
| -------------------------- | ------------ | -------------- |
| `Header.Toltec.ObsType`    | 4 (`TUNE`)   | 0 (`Nominal`)  |
| `Header.Toltec.SampleFreq` | 488.28125 Hz | 122.0703125 Hz |
| Readout samples (`time`)   | 3540         | 7802           |
| Readout channels (`iqlen`) | 632          | 632            |

The recorded type describes the acquisition. It does not establish the
observation's scientific purpose or whether the data pass quality checks. Use
the observing information and reduction record for those decisions.

## Check the contents before combining files

The sampled readout files store integer arrays `Data.Toltec.Is` and
`Data.Toltec.Qs`, with dimensions `(time, iqlen)`. These are the electronic
readout's I and Q signals. Do not interpret them as calibrated sky intensity or
Stokes polarization maps. Follow the
[KIDs processing guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html)
for supported detector processing, then the recipe for the calibrated product
you intend to make.

Inspect the channel count for each file. For acquisition 156755, sub-observation
0, scan 2, interfaces `toltec7` and `toltec11` contain 557 and 474 channels
respectively. An array's width does not tell you how many detectors will pass
the reduction's selection and quality checks.

Use the sampling metadata for the selected readout. The two rates in the table
come from different settings within one observation; a single assumed
instrument-wide sampling rate would misdescribe this pair. The per-sample
`Data.Toltec.SampleType` also has its own labels, distinct from the file's
`Header.Toltec.ObsType`.

Telescope and half-wave-plate data have separate layouts and timing information.
For scan 2 of observation 145609, the sampled telescope file has 3427 time rows
while the `toltec0` file has 7802. Matching row numbers cannot establish
matching times. Retain the companion streams required by your recipe and use its
timing alignment procedure before combining detector, pointing, or polarization
information.

## Keep the recorded tuning reference

The readout headers include `Header.Toltec.TargSweepObsNum`,
`TargSweepSubObsNum`, and `TargSweepScanNum`. For the `toltec0` scan-2 file
above, these point to 145609, 0, 1. Preserve that reference and the
corresponding readout interface when assembling inputs.

This is a recorded detector-setup relationship, not a complete calibration
prescription. The reference alone does not establish that a candidate is valid
for a particular reduction, or supply pointing and flux calibration. Record the
actual calibration selected by your recipe, as described in
[reduction preparation](reduction.md).

## Before starting a reduction

Check the selected identities, acquisition types, channel counts, sampling
metadata, required companion streams, and recorded tuning references. Resolve
missing or inconsistent inputs before processing a large dataset. Keep these
checks with [your analysis record](provenance.md) so another user can reproduce
the selection.
