"""Execute the KIDs deck examples against a reference tune and numerical series.

Run from the workspace root with toltec_astro_dev/.venv/bin/python.
Reference inputs remain read-only. Publication uses temporary directories.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import xarray as xr
from astropy import units as u
from tollan.accessor.xarray import ensure_datatree
from tollan.config import RuntimeContext
from tolteca_datamodels.toltec import open_toltec_kids
from tolteca_kids import BlockCreate, BlockIdentify
from tolteca_kids.product import read_sweep_context
from tolteca_kids.runner import run_data, run_source
from tolteca_kids.sweep_reduce import SweepReduce
from tolteca_kidsproc.accessors import make_kids_dataset
from tolteca_kidsproc.analysis import D21Analysis, PSDAnalysis

DESIGN = Path(__file__).resolve().parents[1]
WORKSPACE = DESIGN.parents[2]
DECK = DESIGN / "toltec-kids-data-and-analysis.md"
TUNE = WORKSPACE / (
    "toltec_astro_dev/run/data_lmt/toltec/tcs/toltec0/"
    "toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc"
)


def main():
    """Verify displayed examples and per-block context/publication boundaries."""
    examples = {}
    for section in re.split(r"^---\s*$", DECK.read_text(), flags=re.M):
        title = re.search(r"^# (.+)$", section, re.M)
        if title:
            examples[title[1]] = re.findall(r"```python\n(.*?)\n```", section, re.S)
    executed = []

    def run(title, env):
        for i, code in enumerate(examples[title], 1):
            exec(compile(code, f"{DECK.name}:{title}:{i}", "exec"), env)
            executed.append(f"{title}:{i}")

    env = dict(
        np=np,
        xr=xr,
        u=u,
        D21Analysis=D21Analysis,
        PSDAnalysis=PSDAnalysis,
        make_kids_dataset=make_kids_dataset,
        run_data=run_data,
        run_source=run_source,
    )
    with (
        open_toltec_kids(TUNE) as native,
        TemporaryDirectory(prefix="kids-deck-") as tmp,
    ):
        ds = native
        tree = ensure_datatree(ds)
        BlockIdentify()(tree)
        BlockCreate()(tree)
        block = tree["blocks/0"]
        env.update(block=block, tree=tree, scope=block)
        run("Configured block pipelines", env)
        run("Sweep reduction and views", env)
        assert env["sweep"].I.shape == env["sweep"].unc_I.shape
        run("Sweep checks", env)
        assert env["flags"].shape == (632,)
        run("Figures and artifact ownership", env)
        assert len(env["context"].artifacts) == 4
        assert len(env["figure"].data) > 0
        run("D21 analysis", env)
        xr.testing.assert_allclose(env["matched"], env["view"].d21)
        run("Analysis configuration and reuse", env)

        runtime = RuntimeContext(
            config_sources={"kids": {"output": {"enabled": False}}}
        )
        env.update(ds=ds, source_path=TUNE, runtime=runtime)
        run("Runner and output", env)
        assert env["index_path"] is None
        working = env["working"]
        assert all(SweepReduce.has_context(b.tree) for b in working.toltec_kids.blocks)
        assert not SweepReduce.has_context(working)

        # Exercise the interface-root publication contract without a database.
        output_runtime = RuntimeContext(
            config_sources={
                "kids": {
                    "output": {
                        "enabled": True,
                        "registration": False,
                        "path": tmp,
                        "run": {"name": {"generator": "counter", "key": "slides"}},
                    }
                }
            }
        )
        run_data(ds, TUNE, output_runtime)
        stores = list(Path(tmp).rglob("array.zarr"))
        assert len(stores) == 1
        with xr.open_datatree(stores[0], engine="zarr") as saved:
            assert set(saved.children) == {"toltec0"}
            saved_block = saved["toltec0/blocks/0"]
            assert not SweepReduce.has_context(saved_block)
            context = read_sweep_context(saved_block)
            assert context.completed and context.data is None
            assert saved_block.kids.sweep.I.shape == block.kids.sweep.I.shape

    time = np.arange(256) / 128
    signal = np.sin(2 * np.pi * 16 * time)
    values = np.stack([signal, 2 * signal])
    source = make_kids_dataset(values, values, f_smp=128 * u.Hz)
    series = xr.DataArray(signal, dims="sample", name="signal", attrs={"units": "V"})
    env.update(
        source=source,
        series=series,
        I=values,
        Q=values,
        frequency=np.broadcast_to(np.linspace(1e9, 1.1e9, 256), values.shape),
    )
    run("PSD analysis", env)
    assert env["spectra"].signal.u.unit == u.V**2 / u.Hz
    run("Numerical inputs, coordinates and units", env)
    env["tree"] = xr.DataTree.from_dict({"blocks/0/timestream": source})
    run("Analysis destinations", env)
    assert env["result"] is env["tree"]
    assert len(executed) == sum(map(len, examples.values()))
    print(
        json.dumps(
            {"examples": executed, "publication": "interface-root Zarr passed"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
