"""Run the datamodels deck examples against read-only reference acquisitions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import xarray as xr
import yaml
from tollan.accessor.pandas.model_table import ModelColumn, ModelTableAccessor
from tolteca_datamodels.file import FileAccessor
from tolteca_datamodels.filepath import FilepathInfo
from tolteca_datamodels.input_discovery import InputDiscoveryConfig
from tolteca_datamodels.lmt._obs_spec import _obs_spec_context as lmt_context
from tolteca_datamodels.lmt.file import LmtFileAccessor
from tolteca_datamodels.lmt.file_store import LmtFileStore
from tolteca_datamodels.lmt.tel import open_lmt_tel
from tolteca_datamodels.lmt_base.obs_spec import ObsSpec
from tolteca_datamodels.toltec._obs_spec import _obs_spec_context as toltec_context
from tolteca_datamodels.toltec.file import ToltecFileAccessor
from tolteca_datamodels.toltec.hwpr import open_toltec_hwpr
from tolteca_datamodels.toltec.kids import open_toltec_kids
from tolteca_datamodels.toltec.types import ToltecDataKind
from tolteca_dummy_instru._obs_spec import _obs_spec_context as dummy_context
from tolteca_dummy_instru.metadata import DummyInstruMetadata
from tolteca_dummy_instru.testing import make_dataset
from tolteca_dummy_instru.types import DummyInstruDataKind
from tolteca_kids.cli import app
from tolteca_kids.config import InputConfig
from tolteca_kids.input import Input
from typer.testing import CliRunner

DESIGN = Path(__file__).resolve().parents[1]
WORKSPACE = DESIGN.parents[2]
DECK = DESIGN / "tolteca-datamodels-input-workflow.md"
DATA = WORKSPACE / "toltec_astro_dev/run/data_lmt"


def _dummy_paths(temporary: Path, telescope_path: Path) -> list[Path]:
    """Create an explicitly synthetic acquisition and its telescope companion."""
    counts = temporary / "chan01-tcs-1-0-2-20251031T120000.nc"
    metadata = DummyInstruMetadata(
        instru="dummy_instru",
        data_models=["dummy_instru"],
        interface="chan01",
        interface_kind="counter",
        channel=1,
        master="tcs",
        obsnum=1,
        subobsnum=0,
        scannum=2,
        filepath_orig=str(counts),
        t0=1761912000.0,
        t1=1761912003.0,
        t_int="3 s",
    )
    make_dataset(metadata, [1, 2]).to_netcdf(counts)
    companion = temporary / "tel_dummy_instru_2025-10-31_145609_00_0002.nc"
    with xr.open_dataset(telescope_path) as data:
        telescope = data[
            [
                "Header.File.Name",
                "Header.Dcs.ObsNum",
                "Header.Dcs.SubObsNum",
                "Header.Dcs.ScanNum",
                "Header.Dcs.ObsPgm",
                "Header.Dcs.ObsGoal",
                "Header.Dcs.IntegrationTime",
                "Header.Source.Ra",
                "Header.Source.Dec",
                "Header.TelescopeBackend.Master",
                "Data.TelescopeBackend.TelTime",
                "Data.TelescopeBackend.TelAzAct",
            ]
        ]
        telescope.drop_encoding().assign(
            {
                "Header.File.Name": str(companion),
                "Header.Dcs.Receiver": "Dummy_Instru",
            }
        ).to_netcdf(companion)
    return [counts, companion]


def _run(temporary: Path):
    """Execute displayed examples using read-only references and temporary files."""
    markdown = DECK.read_text()
    paths = LmtFileStore(DATA).partial("tel", "toltec").glob_obs_spec("*")
    assert len(paths) == 16
    tel_path = next(
        p for p in paths if "tel_toltec_2025-10-31_145609_00_0002" in p.name
    )
    tune_path = next(
        p for p in paths if p.name.startswith("toltec7_") and "tune" in p.name
    )
    hwpr_path = next(p for p in paths if p.name.startswith("hwpr_"))
    mixed_sources = (
        paths + _dummy_paths(temporary, tel_path) + ["archive:/unidentified.nc"]
    )
    namespace = {
        "FileAccessor": FileAccessor,
        "FilepathInfo": FilepathInfo,
        "LmtFileAccessor": LmtFileAccessor,
        "LmtFileStore": LmtFileStore,
        "ToltecFileAccessor": ToltecFileAccessor,
        "ModelColumn": ModelColumn,
        "ModelTableAccessor": ModelTableAccessor,
        "open_lmt_tel": open_lmt_tel,
        "open_toltec_kids": open_toltec_kids,
        "open_toltec_hwpr": open_toltec_hwpr,
        "Input": Input,
        "InputConfig": InputConfig,
        "data_lmt_path": DATA,
        "tel_path": tel_path,
        "remote_name": f"archive:/data_lmt/tel/{tel_path.name}",
        "tune_path": tune_path,
        "hwpr_path": hwpr_path,
        "all_paths": paths,
        "mixed_sources": mixed_sources,
        "filepath_models": [FilepathInfo.from_source(p) for p in paths],
    }
    snippets = []
    # Execute dependent examples in workflow order, independently of slide order.
    example_order = [
        "Universal filename parsing",
        "Enabling registered support",
        "Data-model context in discovery",
        "Generic table API",
        "Resource and acquisition identity",
        "File stores",
        "Column projection",
        "Querying observations and flags",
        "Source trace and failures",
        "Opening a selected table",
        "Telescope data",
        "KIDs acquisition inspection",
        "HWPR and KIDs identity",
        "Pipeline-owned input selection",
    ]
    sections = re.split(r"^---\s*$", markdown, flags=re.M)
    sections.sort(
        key=lambda section: next(
            (i for i, title in enumerate(example_order) if f"# {title}\n" in section),
            len(example_order),
        )
    )
    for section in sections:
        title = re.search(r"^# (.+)$", section, re.M)
        if title is None:
            continue
        for number, snippet in enumerate(
            re.findall(r"```python\n(.*?)\n```", section, re.S), 1
        ):
            label = f"{DECK.name}:{title[1]}:{number}"
            exec(compile(snippet, label, "exec"), namespace)
            snippets.append(title[1])
    mixed = namespace["mixed"]
    mixed_read = namespace["mixed_read"]
    assert isinstance(namespace["info"], FilepathInfo)
    assert FilepathInfo.from_source(tel_path) == namespace["info"]
    assert FilepathInfo.from_source(tune_path).interface == "toltec7"
    contexts = (
        lmt_context,
        lmt_context | toltec_context,
        lmt_context | dummy_context,
        lmt_context | toltec_context | dummy_context,
    )
    interfaces = list(contexts[-1].field_label_numbers["interface"])
    spec = ObsSpec.parse("*/1")
    assert [
        spec.resolve_values("interface", interfaces, context=context)
        for context in contexts
    ] == [[], ["toltec1"], ["chan01"], ["toltec1", "chan01"]]
    assert len(mixed) == len(mixed_read) == 19
    assert len(namespace["mixed_sweeps"]) == 5
    assert len(namespace["mixed_counts"]) == 1
    assert "data_kind" not in mixed
    assert mixed.data_kind_dummy_instru.iloc[-3] == DummyInstruDataKind.counts.value
    assert mixed.data_kind_dummy_instru.iloc[-2] == DummyInstruDataKind.telescope.value
    assert mixed_read.instru.iloc[-2] == "lmt"
    assert mixed_read.data_models.iloc[-2] == ["lmt", "dummy_instru"]
    assert (
        mixed_read.data_kind_dummy_instru.iloc[-2]
        == DummyInstruDataKind.telescope.value
    )
    assert mixed_read.data_kind_toltec.iloc[-1] == ToltecDataKind.unknown.value
    assert (
        mixed_read.data_kind_dummy_instru.iloc[-1] == DummyInstruDataKind.unknown.value
    )
    assert ToltecDataKind.vnasweep.value == DummyInstruDataKind.counts.value
    assert str(namespace["mixed_sweeps"].data_kind_toltec.dtype) == "Int64"
    assert len(FileAccessor(mixed).query('contains(data_models, "toltec")')) == 16
    lmt = LmtFileAccessor.from_sources(mixed_sources)
    assert lmt.obsnum.notna().sum() == 18
    assert "data_kind" not in lmt
    toltec = ToltecFileAccessor.from_sources(mixed_sources)
    assert str(toltec.data_kind_toltec.dtype) == "Int64"
    assert (
        toltec.data_kind_toltec.iloc[-3:].tolist() == [ToltecDataKind.unknown.value] * 3
    )
    assert namespace["toltec_context"].data_models.keys() == {"toltec"}
    assert len(namespace["scoped_paths"]) == len(namespace["scoped_table"]) == 16
    assert "data_kind_toltec" in namespace["scoped_table"]
    assert "data_kind_dummy_instru" not in namespace["scoped_table"]
    assert len(namespace["selected"]) == 4
    assert len(namespace["full"]) == 16
    assert len(namespace["pointing"]) == 3
    assert namespace["sky"].uid_raw_obs.tolist() == ["tcs-145609-0-2"]
    assert len(namespace["sweeps"]) == 5
    assert len(namespace["science"]) == 8
    assert len(namespace["inputs"]) == 5
    assert "io_obj" not in namespace["opened"]
    assert "io_obj" not in namespace["live"]
    assert namespace["issues"][0].stage == "filepath"
    assert not namespace["cached"].source_loc_is_local.iloc[0]
    assert namespace["cached"].obsnum.iloc[0] == 145609
    assert len(namespace["projected"]) == 16
    meta = namespace["meta"]
    assert meta.obs_goal == "pointing"
    assert meta.obs_pgm == "lissajous"
    assert round(meta.t_int.to_value("s"), 1) == 60.3
    assert round(meta.t_elapsed.to_value("s"), 1) == 68.5
    prepared = namespace["prepared"]
    assert prepared.index.sample_start.values.tolist() == [0, 1770]
    assert prepared.index.sample_end.values.tolist() == [1770, 3540]
    assert len(namespace["channels"]) == 1114
    assert len(namespace["probes"]) == 354
    assert len(namespace["block_rows"]) == 2
    assert namespace["hwpr_meta"].readout_code == 13
    assert namespace["hwpr_meta"].n_times == 131
    assert namespace["encoder"].shape == (5, 500)

    yaml_blocks = re.findall(r"```yaml\n(.*?)\n```", markdown, re.S)
    config = yaml.safe_load(yaml_blocks[0]) | yaml.safe_load(yaml_blocks[1])
    entries = config["input_discovery"]["inputs"]
    entries[0]["data_lmt_path"] = str(DATA)
    entries[1]["data_toltec_path"] = str(DATA / "toltec")
    entries[2]["sources"][0]["glob"] = str(DATA / "tel/*.nc")
    parsed = InputDiscoveryConfig.model_validate(config["input_discovery"])
    assert [len(entry.discover()) for entry in parsed.inputs] == [4, 5, 7]
    config_path = temporary / "inputs.yaml"
    config_path.write_text(yaml.safe_dump(config))
    runner = CliRunner()
    results = {}
    for flag in ("--show_inputs", "--dry_run"):
        result = runner.invoke(app, ["--config_paths", str(config_path), flag])
        assert result.exit_code == 0, (flag, result.output, result.exception)
        results[flag] = result.exit_code
    print(
        json.dumps(
            {
                "python_examples": snippets,
                "reference_files": len(paths),
                "mixed_rows": len(mixed),
                "mixed_counts": len(namespace["mixed_counts"]),
                "mixed_sweeps": len(namespace["mixed_sweeps"]),
                "raw_sweeps": len(namespace["sweeps"]),
                "raw_kids": len(namespace["science"]),
                "pointing_lissajous": len(namespace["pointing"]),
                "block_sample_bounds": [[0, 1770], [1770, 3540]],
                "collection_axes": {
                    "chan_entry": len(namespace["channels"]),
                    "probe": len(namespace["probes"]),
                },
                "hwpr_encoder_subset_shape": list(namespace["encoder"].shape),
                "cli_exit_codes": results,
            },
            indent=2,
        )
    )


def main():
    """Keep synthetic fixtures and CLI configuration outside the reference tree."""
    with TemporaryDirectory(prefix="datamodels-deck-") as temporary:
        _run(Path(temporary))


if __name__ == "__main__":
    main()
