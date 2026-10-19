# Starter validation

Executed on 2026-10-19 using the fresh tutorial environment on macOS arm64,
Python 3.13.9, netCDF4 1.7.5. The complete locked environment is in
`uv.lock`. This record covers the working tree on `codex/v3-learning-materials`;
its content identities below avoid treating the uncommitted archive-parent
revision as the tutorial revision.

| Input or source | Identity |
| --- | --- |
| Reference repository revision | `99711bde64f96d0df042e3c44a1e174ab68dcb4c` |
| Input SHA-256 | `285f8d5170a1f54cb94d1272ede3abf9f5e4babd26b453cb87a5254bd28551e0` |
| Notebook source SHA-256 | `b6e48a1658ffd5a2c7a3179a88eb8635808d18e1a0c36fcb662bc71197b3b882` |
| Environment lock SHA-256 | `aa88c4e08894bd60d07853313adf138c3918533041274049599244b47b8b464e` |

The notebook ran from a clean Python kernel through `jupyter execute`, with a
120-second per-cell timeout and errors fatal. Reference inputs were read through
the development location's `run/data_lmt`, selected with `TOLTECA_DATA_LMT`.

Verified: 1,157,288 input bytes; observation 145609, sub-observation 0,
scan 1; 2837 time samples; native time/azimuth/elevation units sec/rad/rad.
The notebook wrote `_build/inspect-reference-data/summary.json` in the tutorial
checkout. The input checksum remained unchanged, and the source notebook kept
empty outputs and execution counts.

A second run used a clean export of the staged branch in a temporary directory
and a newly created virtual environment. `uv sync --locked --offline` installed
from the existing download cache. The notebook used the configured external
data path and produced an identical provenance report. No sibling software
checkout or editable TolTECA installation was required.

This verifies notebook execution and the pairing with the pinned reference
file. It does not validate a complete TolTECA reduction, archive analysis,
proposal workflow, Linux/Windows execution, or remote Git LFS availability.
