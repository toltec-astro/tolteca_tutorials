# Pair tutorials with reference data

Keep the repositories separate. A convenient layout is:

```text
learning/
├── tolteca_tutorials/       # notebooks, environments, teaching material
└── tolteca_ref_data/        # versioned input files, using Git LFS
    └── data_lmt/
```

[reference.toml](reference.toml) identifies the data repository revision and the
one file needed by the first workflow. Its size is 1,157,288 bytes (about 1.1 MiB).
The SHA-256 and byte count come from the upstream Git LFS pointer at that
revision; the remaining fields are the expected observation and array shape.

## Retrieve the starter dataset

After the sibling clone shown in the [quick start](../README.md), run these
commands from `tolteca_tutorials`:

```sh
git -C ../tolteca_ref_data lfs install --local
GIT_LFS_SKIP_SMUDGE=1 git -C ../tolteca_ref_data checkout 99711bde64f96d0df042e3c44a1e174ab68dcb4c
git -C ../tolteca_ref_data lfs pull --include="data_lmt/tel/tel_toltec_2025-10-31_145609_00_0001.nc" --exclude=""
```

These commands apply to the newly cloned data checkout. If you already have
reference data, leave that checkout at its current revision and point the
tutorial at its `data_lmt` directory instead. The notebook verifies the exact
file bytes against the manifest before reading them.

## Use data stored elsewhere

The default is the sibling `tolteca_ref_data/data_lmt` directory. Override it
with an absolute path when the data live elsewhere:

```sh
export TOLTECA_DATA_LMT=/path/to/tolteca_ref_data/data_lmt
uv run --locked jupyter lab
```

In PowerShell, set `$env:TOLTECA_DATA_LMT` to that directory before starting
JupyterLab. In an existing TolTECA deployment, point it at the location's
`run/data_lmt` directory. The tutorial writes results under its own `_build/`
directory and opens reference inputs read-only.

A Git LFS pointer is not a NetCDF file. A missing or mismatched payload fails the
checksum check; retrieve the specified LFS file before continuing. The manifest
pins this example's input bytes, independently of the tutorial environment's
software versions. It is a reference acquisition, not an archive science release.
