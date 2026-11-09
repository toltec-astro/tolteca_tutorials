"""Check configuration and definition examples in the architecture decks.

Run with the development location's Python from the workspace root. This
validates requests and builds Dagster Definitions without connecting to
inventories or submitting compute jobs. The deployment deck's execution
examples are checked by its own probe.
"""

import json
import re
from pathlib import Path

import dagster as dg
import yaml
from tollan.config import RuntimeContext
from tolteca_datamodels.data_prod_run import RunRequest
from tolteca_db.config import DataProdConfig
from tolteca_db.kids_workflow import make_definitions
from tolteca_kids.cli import app
from tolteca_kids.config import KidsConfig
from typer.testing import CliRunner

WORKSPACE = Path(__file__).resolve().parents[3]
ARCHITECTURE = WORKSPACE / "tolteca_tutorials/architecture"


def deck(name):
    """Return the source of one architecture deck."""
    return ARCHITECTURE / name / f"{name}.md"


def sections(path):
    """Return rendered slide content indexed by its heading."""
    result = {}
    for text in re.split(r"^---\s*$", path.read_text(), flags=re.M):
        title = re.search(r"^# (.+)$", text, re.M)
        if title:
            result[title[1]] = text
    return result


def yaml_example(section):
    """Read one displayed YAML configuration."""
    return re.search(r"```yaml\n(.*?)\n```", section, re.S)[1]


def main():
    """Validate current examples without triggering external work."""
    product = sections(deck("toltec-data-products"))
    publication = yaml.safe_load(yaml_example(product["Run allocation and tags"]))
    config = KidsConfig.model_validate(publication["kids"])
    assert isinstance(config.output.run, RunRequest)
    assert config.output.run.name.generator == "counter"
    assert config.output.tag == "ql-main"

    assoc = sections(deck("toltec-associations-and-inventories"))
    merging = yaml.safe_load(yaml_example(assoc["Selection labels across inventories"]))
    policy = DataProdConfig.model_validate(merging["data_prod"])
    assert policy.unify.tag_selections == {"main": "unity:main"}
    assert len(policy.unify.sources) == 2

    runtime = RuntimeContext(config_sources={"kids": {"output": {"enabled": True}}})
    definitions = make_definitions(runtime)
    dg.Definitions.validate_loadable(definitions)
    assert definitions.resolve_asset_graph().get_all_asset_keys() == {
        dg.AssetKey("raw_obs_available"),
        dg.AssetKey("raw_obs_discovered"),
        dg.AssetKey("kids_quicklook"),
    }
    cli = CliRunner().invoke(app, ["--help"])
    assert cli.exit_code == 0 and "config_paths" in cli.output
    for path in sorted(ARCHITECTURE.glob("*/*.md")):
        if "marp: true" not in path.read_text():
            continue
        for i, snippet in enumerate(
            re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S)
        ):
            compile(snippet, f"{path.name}:{i}", "exec")
    print(
        json.dumps(
            {
                "publication": "valid",
                "unify": "valid",
                "asset_definitions": "loadable",
                "python_snippets": "compiled",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
