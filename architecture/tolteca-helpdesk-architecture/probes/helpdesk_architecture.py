#!/usr/bin/env python3
"""Execute the architecture deck's API and configuration examples offline."""

from __future__ import annotations

import re
import shlex
import sys
from http import HTTPStatus
from pathlib import Path

import yaml
from tollan.config import RuntimeContext
from tolteca_agent.cli import app
from tolteca_agent.material import use_cases
from tolteca_dr.config import Dr
from tolteca_dr.web import create_app
from tolteca_helpdesk.config import Helpdesk
from typer.testing import CliRunner


def _require(*, condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _example(text: str, language: str) -> str:
    match = re.search(rf"```{language}\n(.*?)\n```", text, re.DOTALL)
    if match is None:
        message = f"Missing {language} example"
        raise ValueError(message)
    return match[1]


def main() -> None:
    """Run the displayed snippets without contacting an inference provider."""
    source = Path(__file__).resolve().parents[1] / "tolteca-helpdesk-architecture.md"
    text = source.read_text()
    namespace = {}
    # Execute the maintained, local example exactly as displayed.
    exec(compile(_example(text, "python"), str(source), "exec"), namespace)  # noqa: S102
    question = namespace["question"]
    _require(
        condition=question.case_id == "plan_observation",
        message="Question workflow differs",
    )
    _require(
        condition=question.history == [],
        message="Question starts with unexpected history",
    )

    runtime = RuntimeContext(yaml.safe_load(_example(text, "yaml")))
    _require(
        condition=Dr(runtime).config.test_mode, message="Test mode was not enabled"
    )
    _require(
        condition=Helpdesk(runtime).config.provider_name == "MacBook Pro",
        message="Provider label differs",
    )
    client = create_app(runtime).server.test_client()
    _require(
        condition=client.get("/dr/science/_dash-layout").status_code == HTTPStatus.OK,
        message="Science portal failed",
    )
    _require(
        condition=client.get("/dr/operations/").status_code == HTTPStatus.NOT_FOUND,
        message="Science configuration exposed the operations portal",
    )

    runner = CliRunner()
    results = []
    for line in _example(text, "bash").splitlines():
        executable, *args = shlex.split(line)
        _require(condition=executable == "tolteca_agent", message="Unexpected command")
        result = runner.invoke(app, args)
        _require(condition=result.exit_code == 0, message=result.output)
        results.append(result.output)
    _require(
        condition="# TolTEC workflow guidance" in results[0],
        message="Bootstrap text missing",
    )
    _require(
        condition=tuple(results[1].splitlines()) == use_cases("science"),
        message="Science workflow listing differs",
    )
    _require(
        condition="# Reduce my own TolTEC data" in results[2],
        message="Reduction guide missing",
    )
    sys.stdout.write("Displayed Python, YAML and CLI examples passed.\n")


if __name__ == "__main__":
    main()
