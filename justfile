# Optional shortcuts; README.md also gives commands that require only uv.
default:
    @just --list

setup:
    uv sync --locked

lab:
    uv run --locked jupyter lab

check:
    uv run --locked ruff check .
    uv run --locked ruff format --check .
    uv run --locked python scripts/check_notebooks.py

execute:
    uv run --locked jupyter execute workflows/inspect-reference-data/inspect_reference_data.ipynb --timeout=120

# Build the TolTEC Data Handbook into _build/handbook/.
handbook:
    uv run --locked --only-group handbook sphinx-build -W --keep-going -n -E -b html handbook _build/handbook
