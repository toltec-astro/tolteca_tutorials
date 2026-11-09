"""Execute the Python fragments in the Tollan architecture deck with guide setup.

The deck and guide fragments use names they do not import; ``main`` runs them
in this module's namespace, so the imports marked F401 are used through ``exec``.
The guide examples import from the Tollan checkout after its path is added.
"""

import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Annotated  # noqa: F401

import numpy as np
import typer  # noqa: F401
from sqlalchemy import text  # noqa: F401
from tollan.accessor.pandas import ModelTableAccessor  # noqa: F401
from tollan.accessor.pandas.model_table import ModelColumn  # noqa: F401
from tollan.db import SqlaDB  # noqa: F401
from tollan.pipeline import ArtifactContext  # noqa: F401
from tollan.utils.typer import MultiOption, create_cli  # noqa: F401
from typer.testing import CliRunner

DECK_DIR = Path(__file__).resolve().parents[1]
REPO = DECK_DIR.parents[2] / "tollan"
sys.path.insert(0, str(REPO / "docs/examples"))
from artifact_example import SignalViz  # noqa: E402, F401
from pipeline_example import Scale, ScaleConfig, ScaleContext  # noqa: E402


def guide_blocks(name, language):
    content = (REPO / "docs" / name).read_text()
    return re.findall(r"```" + re.escape(language) + r"\n(.*?)\n```", content, re.S)


def main():
    namespace = dict(globals())
    for code in guide_blocks("schema-mapping-accessors.md", "{testcode}")[:3]:
        exec(code, namespace)
    exec(guide_blocks("configuration.md", "python")[0], namespace)
    exec(guide_blocks("analyses.md", "{testcode}")[0], namespace)
    exec(guide_blocks("artifacts.md", "{testcode}")[0], namespace)
    namespace["samples"] = [
        SimpleNamespace(channel=1, reading=SimpleNamespace(amplitude=2.5)),
        SimpleNamespace(channel=2),
    ]
    namespace["values"] = np.array([1.0, 2.0, 3.0])
    source = (DECK_DIR / "tollan-architecture-and-workflows.md").read_text()
    body = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
    slides = re.split(r"\n---\n", body)
    executed = []
    with TemporaryDirectory(prefix="tollan-deck-examples-") as directory:
        for number, slide in enumerate(slides, start=1):
            for code in re.findall(r"```python\n(.*?)\n```", slide, re.S):
                namespace["destination"] = Path(directory) / f"slide-{number}"
                exec(compile(code, f"slide-{number}", "exec"), namespace)
                executed.append(number)
            if number == 3:
                assert namespace["signal"].values.tolist() == [2.0, 4.0]
            elif number == 5:
                assert namespace["selected"].channel.tolist() == [1]
            elif number == 6:
                handler = namespace["handler"]
                runtime = namespace["rc"]
                runtime.update_default_config({"search": {"pattern": "warning"}})
                assert handler.config.pattern == "error"
                assert namespace["SearchHandler"](runtime).config.pattern == "warning"
            elif number == 7:
                result = CliRunner().invoke(
                    namespace["app"],
                    ["show_files", "--file_names", "first.txt", "second.txt"],
                )
                assert result.exit_code == 0, result.output
                assert result.stdout.splitlines() == ["first.txt", "second.txt"]
            elif number == 9:
                scope = namespace["scope"]
                assert not scope.dims and not scope.coords
                assert set(scope.children) == {"example.mean"}
                assert set(scope["example.mean"].children) == {"mean"}
                analysis = namespace["analysis"]
                values = namespace["values"]
                assert analysis.make_mean(values) == 2.0
                assert namespace["MeanAnalysis"].compute_mean(values, axis=0) == 2.0
            elif number == 10:
                assert namespace["context"].data.signal.values.tolist() == [3.0, 6.0]
                working = namespace["tree"].copy(deep=False)
                context = ScaleContext(step_cls=Scale, config=ScaleConfig(factor=4.0))
                Scale.run(working, context)
                assert not context.completed
                assert context.data.signal.values.tolist() == [4.0, 8.0]
                values = namespace["values"]
                np.testing.assert_array_equal(
                    Scale.compute_scaled(values, factor=3.0), [3.0, 6.0, 9.0]
                )
                np.testing.assert_array_equal(values, [1.0, 2.0, 3.0])
            elif number == 12:
                entry = namespace["entry"]
                assert entry.data is namespace["selected"]
                assert json.loads(namespace["files"][0].path.read_text()) == {
                    "accepted": 12,
                    "rejected": 2,
                }
            elif number == 13:
                assert namespace["entry"].data is namespace["figure"]
                assert all(receipt.path.is_file() for receipt in namespace["files"])
                assert namespace["files"][0].format == "html"
            elif number == 14:
                assert namespace["value"] == 42
    assert len(slides) == 16
    assert executed == [3, 5, 6, 7, 9, 10, 12, 13, 14]
    print(
        json.dumps(
            {
                "slides": len(slides),
                "executed_python_slides": executed,
                "cli": "passed",
                "api_levels": "passed",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
