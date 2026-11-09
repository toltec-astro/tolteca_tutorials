# Handbook primary-source evidence — 26 October 2026

> Moved on 2026-11-08 from `tolteca_helpdesk/design/` with the handbook.
> Recorded commands keep their earlier paths as history.

## Scope and inspected state

This audit supplies the first recorded-data examples for
[Understand a raw observation](../raw-observations.md). It does not
validate a science reduction, characterize instrument performance, or establish
an archive release policy. The user supplied Tlaloc, Unity's raw store, and six
SPIE papers as primary sources.

- Helpdesk baseline: `d7dd2c8d3e55296c38dae2c756d94a4997f72cbd`. The pending
  `src/tolteca_agent/data/learning.md` edit belongs to the terminology work and
  remains separate.
- Tlaloc checkout: `../cpp/tlaloc` relative to the Python workspace; inspected
  absolute path `/Users/ma/Codes/toltec/dev_toltec/cpp/tlaloc`. Committed source
  revision: `e930bcc28baa7e4eabec22a635075233a2ca35ea`. The checkout has
  uncommitted writer, manager, command, build, and documentation changes. Source
  claims below use `git show HEAD:src/ToltecRoachWriterNetcdf.cc`, not those
  development changes.
- Committed writer blob: `88dbcbfb40f61b40278679a4eb6fe8e3b8dca3e1`. Working
  writer blob when inspected: `df1fa6396deac16fcf5823e10e17aba7be8a1d02`. The
  deployed writer revision that produced the sampled files was not established.
  Agreement with these fields does not prove revision identity.
- Recorded data: nine explicit files under
  `unity-toltec4:/nese/toltec/data_lmt`, opened read-only using the existing
  helpdesk environment's netCDF4 1.7.5. No service configuration or data
  changed. No signal arrays, source names, positions, project identifiers, or
  operator details were read by the collector.

## Recorded data and writer contracts

The [header capture](../probes/handbook-sources/unity-headers-20261026.json)
contains the exact relative filenames, sizes, selected scalar values, variable
shapes, units, and labels. Missing variables are listed explicitly. This is a
selected sample from two observing dates, not a survey of all acquisition types
or epochs.

Line numbers below refer to the committed `src/ToltecRoachWriterNetcdf.cc`.

| Fact                                                                                  | Writer evidence                                | Recorded evidence and handbook use                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Acquisition identity includes controller and observation/sub-observation/scan numbers | Lines 148–161                                  | Observation 145609 has separate scan-1 and scan-2 files for the same interface. Preserve the full identity and interface when selecting inputs.                                                                                                          |
| File acquisition type and per-sample type are different enums                         | Lines 137–139 and 247–250                      | Files contain the enum labels as attributes. `ObsType=0` means Nominal; `SampleType=0` means Timestream. Do not use one label table for both. No sample-type payload was read in this audit.                                                             |
| Readout sampling depends on settings                                                  | Lines 175–187                                  | Six readout files satisfy `SampleFreq = FpgaFreq / AccumLen`. Tune files record 488.28125 Hz; following nominal files record 122.0703125 Hz. These values are examples, not universal specifications.                                                    |
| Raw I/Q arrays use time and readout-channel dimensions                                | Lines 233–241                                  | Integer `Is`/`Qs` arrays have `(time, iqlen)` dimensions. Observation 156755 scan 2 has 557 channels on toltec7 and 474 on toltec11. These are stored channel counts, not validated detector yields.                                                     |
| Raw timing contains several clocks/counters and receiver timestamps                   | Lines 293–309                                  | `Ts` has six columns and `RecvTime` has seconds units. The collector records their descriptions, not their values. Timing validity, packet loss, clock alignment, and usable integration time were not measured.                                         |
| Companion streams need independent timing interpretation                              | HWP layout at lines 255–288                    | Observation 145609 scan 2 has 7802 toltec0 rows and 3427 telescope rows. Observation 156755 scan 2 has 8012 rows on each sampled readout and 131 HWP rows, with an encoder array shaped `(131, 500)`. Equal row indices are not evidence of equal times. |
| Recorded target-sweep references describe readout state                               | Lines 164–172, which write `last_targ_sweep_*` | Nominal scan 2 points to scan 1 of the same observation in both sampled observations. Tune scan 1 points to the preceding observation's scan 1. Preserve these references; this audit does not validate calibration suitability.                         |
| Tone-table dimensionality varies with acquisition type                                | Lines 314–345                                  | Sampled Tune files have two `numSweeps` rows; nominal files have one. Do not describe every tone table as a one-dimensional vector. This detail remains in the evidence record, outside the introductory chapter.                                        |

The HWP file also has a `Header.Toltec.SampleFreq` value of 2.0 Hz. Its FPGA and
accumulation headers do not yield that value via the readout formula. The HWP
writer branch has separate encoder arrays. This audit therefore does not label
2.0 Hz as the encoder sampling rate or infer a rotor speed from that field. The
published 2 revolutions/s rotator description is a different physical quantity.

## Paper source register

All six user-supplied files exist in `/Users/ma/Downloads`. macOS refused
content reads with `Operation not permitted`, including an approved escalated
read. Their full texts and file hashes were not inspected. Bibliographic
identity was checked against the linked publisher, institutional, or author
records below. The [public reading list](../references.md) links the
identified papers; listing a paper does not assert that its full text has been
reviewed here.

| Supplied file                        | Identified paper                                                                                                                                        | Evidence read and intended use                                                                                                                                                                                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `18_toltec_hwp_121901O.pdf`          | Lee et al. 2022, _The TolTEC camera: polarimetric commissioning and performance of the continuously rotating half-wave plate_, DOI `10.1117/12.2627725` | [Cardiff author repository](https://orca.cardiff.ac.uk/id/eprint/157094/) metadata and abstract. Supports the 2022 description of polarization modulation and the rotator; full-text timing and performance details remain pending. The public PDF could not be retrieved reliably.  |
| `18_toltec_optical_1219016.pdf`      | Lunde et al. 2022, _The TolTEC camera: optical alignment and characterization_, DOI `10.1117/12.2630340`                                                | [ASU author publication record](https://asu.elsevierpure.com/en/publications/the-toltec-camera-optical-alignment-and-characterization/) metadata and abstract. Future use: optical path and alignment context, with the epoch stated.                                                |
| `18_toltec_citlali_121891H.pdf`      | McCrackan et al. 2022, _The TolTEC camera: the citlali data reduction pipeline engine_, DOI `10.1117/12.2629095`                                        | [Publisher record](https://doi.org/10.1117/12.2629095) and indexed abstract. Future use: reduction principles and terminology; supported v3 commands and algorithms still require current code and tests.                                                                            |
| `18_toltec_optical_2020_114534A.pdf` | Lunde et al. 2020, _The optical design and performance of TolTEC: a millimeter-wave imaging polarimeter_, DOI `10.1117/12.2562798`                      | [Sapienza institutional record](https://iris.uniroma1.it/handle/11573/1487690) metadata and abstract. Its angular-resolution unit needs verification against the paper before reuse. No beam value was adopted from this record.                                                     |
| `18_toltec_lab2020_1145302.pdf`      | Wilson et al. 2020, _The TolTEC camera: an overview of the instrument and in-lab testing results_, DOI `10.1117/12.2562331`                             | [ASU author publication record](https://asu.elsevierpure.com/en/publications/the-toltec-camera-an-overview-of-the-instrument-and-in-lab-testin/) metadata and abstract. Future use: design and laboratory specifications, distinguished from on-sky or release-specific performance. |
| `18_toltec_tolteca_114522O.pdf`      | Ma et al. 2020, _The TolTEC data analysis pipeline and software stack_, DOI `10.1117/12.2560735`                                                        | [Coauthor bibliography](https://dlee.xyz/assets/pdf/dennislee_cv.pdf) identifies the 2020 proceeding. Bibliography only; the same-titled 2023 American Astronomical Society abstract is a separate publication. Future use: historical software responsibilities and motivation.     |

An additional accessible source is the workspace manuscript
`refs/zma_spie2026_v2.pdf`, _Software Framework for TolTEC Operation and Data
Automation_, Ma et al. The PDF has eight pages and a creation timestamp of
2026-06-30; its publication status was not established. SHA-256:
`6f801b4ddf65a20271432a74a14a2d14cba17e38dcd4d96db3fb7fe13333964a`. Sections 1–2
and Figure 1 (PDF page 3, visually inspected) describe site acquisition, timely
analysis, Unity storage/processing, visualization, and archive handoff. Use this
as an architectural account to check against current `tolteca_db`/`tolteca_web`
behavior. It does not establish completed automation, QA policy, or deployed
schema merely by describing them.

## Reproduce and extend the evidence

From the helpdesk checkout, using the existing authorized Unity SSH alias:

```sh
ssh unity-toltec4 '$HOME/opt/toltec_astro/helpdesk/.venv/bin/python - /nese/toltec/data_lmt' \
  < design/probes/handbook-sources/collect_headers.py \
  > ../run/handbook-sources-20261026/unity-headers-repeat.json
```

The [collector](../probes/handbook-sources/collect_headers.py) has an explicit file
list and metadata allowlist. It opens files in read mode and emits JSON to
stdout. From the workspace development environment, pass
`../toltec_astro_dev/run/data_lmt` to inspect the corresponding reference
copies. All nine selected file sizes and captured metadata matched those
reference copies. This is not a byte-for-byte file comparison.

Next source work: make the six PDF contents accessible within the workspace;
extract section/page-specific physical specifications; distinguish design,
laboratory, on-sky, and release measurements; and check timing and calibration
claims against their readers and validated reductions. Expand the raw sample to
other acquisition types and epochs before declaring a complete file-format
reference. No calibration thresholds or release performance guarantees are
established by the present sample.

## Publication boundary and checks

The handbook gains an input-inspection chapter, links from reduction preparation
and the contents page, a paper reading list, and updated coverage. The
framework, glossary ownership, model retrieval corpus, and deployed services are
unchanged. The chapter supports user selection and interpretation; the detailed
writer audit and access limitations stay in this design record.

Header collection succeeded for all nine files. All six readout sample-frequency
ratios matched their stored values. The strict Sphinx handbook build passed
without warnings. All 225 local handbook links and anchors resolved within the
assembled preview, including package references. Browser inspection verified the
raw-observation chapter, example table, and reading-list navigation at
`http://127.0.0.1:8056/science/docs/handbook/raw-observations.html`. Repository
hooks, including type and docstring checks for the collector, passed. The
workspace review diff was regenerated; no runtime behavior changed and no new
runtime tests were added.
