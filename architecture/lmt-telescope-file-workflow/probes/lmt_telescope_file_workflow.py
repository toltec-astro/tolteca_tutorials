"""Execute the LMT telescope deck's examples against read-only reference data.

Run from the workspace root with toltec_astro_dev/.venv/bin/python.
The config and SQLite database live in a temporary directory.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
from tollan.config import RuntimeContext
from tolteca_datamodels.input_discovery import InputDiscoveryConfig
from tolteca_datamodels.lmt.file import LmtFileAccessor
from tolteca_datamodels.lmt.tel import open_lmt_tel
from tolteca_db.api import ObsQuery
from tolteca_db.cli.db_commands import db_app
from tolteca_db.cli.ingest_commands import ingest_app
from tolteca_kids.cli import app as kids_app
from tolteca_web.obs.db_catalog import DBCatalogBackend
from tolteca_web.obs.tel_data import load_tel_file
from tolteca_web.portal import create_app
from typer.testing import CliRunner

DESIGN = Path(__file__).resolve().parents[1]
WORKSPACE = DESIGN.parents[2]
DECK = DESIGN / "lmt-telescope-file-workflow.md"
DATA = WORKSPACE / "toltec_astro_dev/run/data_lmt"
PATH = DATA / "tel/tel_toltec_2025-10-31_145609_00_0002.nc"


def run_snippets(title, examples, namespace):
    for index, snippet in enumerate(examples[title], 1):
        exec(compile(snippet, f"{DECK.name}:{title}:{index}", "exec"), namespace)


def run_cli(runner, app, arguments):
    result = runner.invoke(app, arguments)
    assert result.exit_code == 0, (result.output, result.exception)
    return result.output


def main():
    markdown = DECK.read_text()
    examples = {}
    for section in re.split(r"^---\s*$", markdown, flags=re.M):
        title = re.search(r"^# (.+)$", section, re.M)
        if title:
            examples[title[1]] = re.findall(r"```python\n(.*?)\n```", section, re.S)
    paths = list((DATA / "tel").glob("*.nc"))
    assert len(paths) == 7
    namespace = {
        "LmtFileAccessor": LmtFileAccessor,
        "open_lmt_tel": open_lmt_tel,
        "ObsQuery": ObsQuery,
        "path": PATH,
        "paths": paths,
        "cached_path": PATH,
        "acquisition_path": f"archive:/data_lmt/tel/{PATH.name}",
    }
    run_snippets("Resource and acquisition identity", examples, namespace)
    row = next(namespace["table"].itertuples(index=False))
    assert row.uid_raw_obs == "tcs-145609-0-2"
    assert not row.source_loc_is_local
    assert row.source_loc_host == "archive"

    run_snippets("Telescope reader and metadata", examples, namespace)
    meta = namespace["meta"]
    assert namespace["az"].shape == (100,)
    assert meta.obs_goal == "pointing" and meta.obs_pgm == "lissajous"

    run_snippets("Python selection and resource lifetime", examples, namespace)
    assert len(namespace["pointing"]) == 3
    assert namespace["selected"].uid_raw_obs.tolist() == ["tcs-145609-0-2"]
    assert "io_obj" not in namespace["opened"]
    assert namespace["az"].shape == (100,)

    with TemporaryDirectory(prefix="lmt-telescope-slides-") as temporary:
        scratch = Path(temporary)
        config = yaml.safe_load(re.findall(r"```yaml\n(.*?)\n```", markdown, re.S)[0])
        config["input_discovery"]["inputs"][0]["data_lmt_path"] = str(DATA)
        config_path = scratch / "tel-inputs.yaml"
        db_url = f"sqlite:///{scratch / 'products.sqlite'}"
        config.update(
            {
                "db": {
                    "binds": [{"name": "local", "url": db_url}],
                    "setup": {
                        "db_bind": "local",
                        "locations": [{"label": "LMT", "root_uri": str(DATA)}],
                    },
                },
                "data_prod": {"ingest": {"db_bind": "local", "location": "LMT"}},
                "web": {"db_bind": "local"},
            }
        )
        config_path.write_text(yaml.safe_dump(config))
        discovery = InputDiscoveryConfig.model_validate(config["input_discovery"])
        assert len(discovery.inputs[0].discover()) == 2

        db_url = f"sqlite:///{scratch / 'products.sqlite'}"
        runner = CliRunner()
        run_cli(runner, kids_app, ["--config_paths", str(config_path), "--dry_run"])
        run_cli(runner, db_app, ["init", "--config_paths", str(config_path)])
        run_cli(
            runner,
            ingest_app,
            [
                "inputs",
                "--config_paths",
                str(config_path),
            ],
        )
        namespace["db_url"] = db_url
        run_snippets("Query registered files and reopen", examples, namespace)
        spans = namespace["spans"].set_index("uid_raw_obs")
        assert set(spans.index) == {"tcs-145609-0-1", "tcs-145609-0-2"}
        assert (
            spans.loc["tcs-145609-0-2", "t_elapsed_s"]
            > spans.loc["tcs-145609-0-2", "t_int_s"]
        )

        backend = DBCatalogBackend(db_url)
        assert backend.query().height == 2
        path = backend.get_tel_path("tcs-145609-0-2")
        header, arrays = load_tel_file(path, 10)
        assert header["source_name"] == "0449+635"
        assert round(header["ra_deg"], 5) == 72.34713
        assert round(header["dec_deg"], 5) == 63.53595
        assert round(header["t_int_s"], 1) == 60.3
        assert round(header["t_elapsed_s"], 1) == 68.5
        assert len(arrays["tel_time"]) == 342
        app = create_app(RuntimeContext(config_sources=config_path))
        client = app.server.test_client()
        assert client.get("/tel?quartet=tcs-145609-0-2").status_code == 200

    print(
        json.dumps(
            {
                "python_examples": sum(map(len, examples.values())),
                "reference_files": len(paths),
                "configured_inputs": 2,
                "pointing_observations": 3,
                "coordinate_selection": "tcs-145609-0-2",
                "sample_shape": list(namespace["az"].shape),
                "viewer": {
                    key: header[key]
                    for key in (
                        "source_name",
                        "ra_deg",
                        "dec_deg",
                        "t_int_s",
                        "t_elapsed_s",
                    )
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
