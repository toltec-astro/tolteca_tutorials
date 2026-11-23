"""Execute the reader deck's Python examples against the read-only reference tree."""

import re
from pathlib import Path

from tollan.config import RuntimeContext
from tolteca_datamodels.input_discovery import InputDiscovery

DECK = Path(__file__).resolve().parents[1] / "tolteca-datamodels-input-workflow.md"
WORKSPACE = Path(__file__).resolve().parents[4]


def main():
    data_lmt_path = WORKSPACE / "toltec_astro_dev/run/data_lmt"
    tel_path = next((data_lmt_path / "tel").glob("*145609*"))
    paths = [tel_path, *list((data_lmt_path / "toltec").glob("*/toltec0/*145609*"))]
    scope = dict(data_lmt_path=data_lmt_path, tel_path=tel_path, paths=paths)
    blocks = re.findall(r"^```python\n(.*?)^```", DECK.read_text(), re.M | re.S)
    for number, code in enumerate(blocks, 1):
        exec(compile(code, f"{DECK}:example-{number}", "exec"), scope)
    config = RuntimeContext(
        {
            "input_discovery": {
                "data_model_select": ["toltec"],
                "inputs": [
                    {
                        "data_lmt_path": str(data_lmt_path),
                        "obs_spec": "145609/{tel,0}",
                        "mode": "read",
                    }
                ],
            }
        }
    )
    table = InputDiscovery(config).discover()
    assert not table.empty
    assert set(table.interface) <= {"tel", "toltec0"}
    print(
        f"{len(blocks)} Python examples and configured discovery passed; {len(table)} selected rows"
    )


if __name__ == "__main__":
    main()
