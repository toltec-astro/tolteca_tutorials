# Inspect a reference telescope file

Verify that your notebook environment can read the exact reference data used by
an example. This starter checks one LMT telescope file, reads its observation
identifiers and native array metadata, and writes a provenance report. It does
not perform scientific reduction or validate a full TolTECA pipeline.

## Run

1. Complete the repository [quick start](../../README.md) and
   [reference-data setup](../../datasets/README.md).
2. Open [the notebook](inspect_reference_data.ipynb) in JupyterLab and run all
   cells, or execute it from the repository root:

   ```sh
   uv run --locked jupyter execute workflows/inspect-reference-data/inspect_reference_data.ipynb --timeout=120
   ```

The notebook uses the environment in `uv.lock` and the data identity in
`datasets/reference.toml`. Set `TOLTECA_DATA_LMT` if your inputs are outside the
default sibling checkout.

## Expected result

`_build/inspect-reference-data/summary.json` records the data hash and upstream
revision, tutorial environment lock hash, Python and library versions,
observation `145609`, sub-observation `0`, scan `1`, and `2837` time samples.
Time, azimuth, and elevation variables should share that sample count and have
native units `sec`, `rad`, and `rad`. All checks must pass before the report is
written. Inputs remain unchanged.

See [validation](validation.md) for the exercised environment and limits.
