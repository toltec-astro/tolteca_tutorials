"""Execute the data-product deck's Python, YAML and CLI examples.

Run with the workspace Python. Input references remain read-only; numerical
products and a local SQLite graph are created in a temporary directory.
"""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path
from tempfile import TemporaryDirectory

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from tollan.config import RuntimeContext
from tollan.utils.yaml import yaml_load
from tolteca_datamodels.data_prod import DataProdIndex
from tolteca_datamodels.data_prod_store import DataProdStore
from tolteca_db.db import populate_registry_tables
from tolteca_db.models.orm import Base, DataProd
from tolteca_db.product_index import (
    collect_obs_product,
    ingest_data_prod_index,
    write_obs_index,
)
from tolteca_kids.cli import app
from tolteca_kids.product import open_sweep_product, read_product_provenance
from tolteca_kids.runner import run_source
from typer.testing import CliRunner

DESIGN = Path(__file__).resolve().parents[1]
WORKSPACE = DESIGN.parents[2]
DECK = DESIGN / "toltec-data-products.md"
source = (
    WORKSPACE
    / "toltec_astro_dev/run/data_lmt/toltec/tcs/toltec0/toltec0_145609_000_0001_2025_10_31_09_26_59_tune.nc"
)
sections = re.split(r"^---\s*$", DECK.read_text(), flags=re.M)
examples = {}
for section in sections:
    heading = re.search(r"^# (.+)$", section, re.M)
    if heading:
        examples[heading[1]] = re.findall(r"```python\n(.*?)\n```", section, re.S)
report = {"input": str(source), "examples": []}


def run(title, env):
    for n, code in enumerate(examples[title], 1):
        exec(compile(code, f"{DECK.name}:{title}:{n}", "exec"), env)
        report["examples"].append(f"{title}:{n}")


with TemporaryDirectory(prefix="toltec-data-products-") as directory:
    root = Path(directory).resolve()
    env = dict(
        RuntimeContext=RuntimeContext,
        DataProdIndex=DataProdIndex,
        run_source=run_source,
        read_product_provenance=read_product_provenance,
        open_sweep_product=open_sweep_product,
        output_root=root / "products",
        source=source,
    )
    run("Python publication and reopening", env)
    index = env["index"]
    path = env["product_path"]
    assert path == root / "products/scratch/145609-0-1/dp_raw_obs_proc/0000-nightly"
    assert env["signal"].shape == (632, 177)
    raw = DataProdIndex(
        uid="tcs-145609-0-1",
        meta={
            "tag": "raw_obs",
            "data_prod_type": "dp_raw_obs",
            "name": "raw",
            "master": "tcs",
            "obsnum": 145609,
            "subobsnum": 0,
            "scannum": 1,
        },
    )
    products = {raw.reference: raw, index.reference: index}
    engine = create_engine(f"sqlite:///{root / 'dpdb.sqlite'}")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        populate_registry_tables(session)
        ingest_data_prod_index(session, raw)
        ingest_data_prod_index(session, index)
        session.commit()
        product = session.scalar(select(DataProd).where(DataProd.uid == index.uid))
        run("Primary access", dict(env, products=products, product=product))
        assert product.primary.uid == raw.uid
        run(
            "Observation inventory",
            dict(
                env,
                session=session,
                collect_obs_product=collect_obs_product,
                write_obs_index=write_obs_index,
            ),
        )
        obs_index = DataProdIndex.read(root / "products/scratch/145609/dp_obs.yaml")
        assert [assoc.uid for assoc in obs_index.assocs] == [raw.uid]
        report["observation_inventory"] = "passed"
    engine.dispose()
    for code in re.findall(r"```yaml\n(.*?)\n```", DECK.read_text(), re.S):
        assert yaml_load(code)["assocs"][0] == {
            "uid": raw.uid,
            "data_prod_assoc_type": "dpa_raw_obs_proc_raw_obs",
            "is_primary": True,
            "context": {},
        }
    store = DataProdStore(root / "products")
    assert store.get_product_path(raw.uid, "dp_raw_obs_proc") == path.parent
    assert (
        store.get_index_path(raw.uid, "dp_raw_obs_proc", run_name="0000-nightly")
        == path / "index.yaml"
    )
    snapshot = store.set_tag(raw.uid, "dp_raw_obs_proc", "0000-nightly", tag="copy")
    assert DataProdIndex.read(snapshot) == index
    report["store_api"] = "passed"
    code = re.findall(r"```console\n(.*?)\n```", DECK.read_text(), re.S)[0]
    argv = shlex.split(code.replace("\\\n", ""))
    assert argv.pop(0) == "tolteca_kids"
    argv = [
        str(root / "cli")
        if value == "dataprod_toltec"
        else str(source)
        if value == "tune.nc"
        else value
        for value in argv
    ]
    result = CliRunner().invoke(app, argv)
    assert result.exit_code == 0, (result.output, result.exception)
    assert (root / "cli/ql/145609-0-1/dp_raw_obs_proc/0000-check-a/index.yaml").exists()
    report["cli"] = "passed"
    with open_sweep_product(path) as tree:
        report["tree"] = {
            node.path: {
                "dims": dict(node.sizes),
                "vars": list(node.data_vars),
                "attrs": list(node.attrs),
            }
            for node in tree.subtree
        }
        assert "raw" not in tree
        assert tree["blocks/index"].has_data
        assert tree["blocks/chan"].has_data
        assert tree["blocks/probe"].has_data
    report["yaml"] = "passed"
print(json.dumps(report, indent=2))
