"""Check that notebook sources are valid and contain no saved execution state."""

from pathlib import Path

import nbformat

root = Path(__file__).resolve().parents[1]
notebooks = [
    path
    for folder in ("workflows", "presentations", "workshops")
    for path in sorted((root / folder).rglob("*.ipynb"))
    if ".ipynb_checkpoints" not in path.parts
]
for path in notebooks:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code" and (
            cell.execution_count is not None or cell.outputs
        ):
            raise ValueError(f"Clear execution state before committing: {path}")
    print(f"Valid clean source: {path.relative_to(root)}")
