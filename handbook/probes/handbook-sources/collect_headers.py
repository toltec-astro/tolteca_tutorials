"""Capture selected raw-file metadata for the handbook's dated evidence record.

Run with a data_lmt root as the sole argument. This reads scalar headers and
array descriptions, never signal arrays, target names, or project identifiers.
It requires netCDF4 in the selected environment and writes JSON to stdout.
"""

# Standalone evidence collector, not an importable package.
# ruff: noqa: INP001

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import netCDF4

SAMPLES = (
    "toltec/tcs/toltec0/toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc",
    "toltec/tcs/toltec0/toltec0_145609_000_0002_2025_10_31_09_27_57.nc",
    "toltec/tcs/toltec7/toltec7_156755_000_0001_2026_05_16_12_32_26_tune.nc",
    "toltec/tcs/toltec7/toltec7_156755_000_0002_2026_05_16_12_33_28.nc",
    "toltec/tcs/toltec11/toltec11_156755_000_0001_2026_05_16_12_32_26_tune.nc",
    "toltec/tcs/toltec11/toltec11_156755_000_0002_2026_05_16_12_33_28.nc",
    "toltec/tcs/hwpr/hwpr_156755_000_0002_2026_05_16_12_33_28.nc",
    "tel/tel_toltec_2025-10-31_145609_00_0001.nc",
    "tel/tel_toltec_2025-10-31_145609_00_0002.nc",
)
HEADERS = tuple(
    f"Header.Toltec.{name}"
    for name in (
        "Master",
        "ObsNum",
        "SubObsNum",
        "ScanNum",
        "ObsType",
        "RoachIndex",
        "SampleFreq",
        "FpgaFreq",
        "AccumLen",
        "NumKidsActual",
        "TargSweepObsNum",
        "TargSweepSubObsNum",
        "TargSweepScanNum",
    )
) + tuple(f"Header.Dcs.{name}" for name in ("ObsNum", "SubObsNum", "ScanNum"))
ARRAYS = (
    "Data.Toltec.Is",
    "Data.Toltec.Qs",
    "Data.Toltec.SampleType",
    "Data.Toltec.Ts",
    "Data.Toltec.RecvTime",
    "Header.Toltec.ToneFreq",
    "Header.Toltec.TonePhase",
    "Data.Toltec.HwprEncVal",
    "Data.Toltec.HwprEncTs",
    "Data.Toltec.HwprEncUts",
    "Data.TelescopeBackend.TelTime",
)


def collect(root: Path) -> dict[str, object]:
    """Read the fixed sample; absent variables are reported, not defaulted.

    Parameters
    ----------
    root : pathlib.Path
        Readable data_lmt tree containing the explicitly listed sample files.

    Returns
    -------
    dict
        Capture timestamp, root, reader version, and selected file metadata.
    """
    records = []
    for relative in SAMPLES:
        path = root / relative
        stat = path.stat()
        record = {"path": relative, "size_bytes": stat.st_size, "variables": {}}
        with netCDF4.Dataset(path, "r") as dataset:
            record["dimensions"] = {k: len(v) for k, v in dataset.dimensions.items()}
            record["absent_variables"] = []
            for name in HEADERS + ARRAYS:
                if name not in dataset.variables:
                    record["absent_variables"].append(name)
                    continue
                variable = dataset.variables[name]
                description = {
                    "dtype": str(variable.dtype),
                    "dimensions": variable.dimensions,
                    "shape": variable.shape,
                    "attributes": {
                        k: str(variable.getncattr(k))
                        for k in ("units", "long_name")
                        if k in variable.ncattrs()
                    },
                }
                if name in HEADERS:
                    description["value"] = variable[...].item()
                record["variables"][name] = description
        records.append(record)
    return {
        "captured_utc": datetime.now(UTC).isoformat(),
        "root": str(root),
        "netcdf4_version": netCDF4.__version__,
        "files": records,
    }


if __name__ == "__main__":
    sys.stdout.write(json.dumps(collect(Path(sys.argv[1])), indent=2) + "\n")
