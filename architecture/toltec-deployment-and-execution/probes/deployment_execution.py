"""Check the deployment deck's execution examples.

Run with the development location's Python. The displayed profiles validate
and resolve; the Dagster example compiles. No scheduler is contacted.
"""

import re
from pathlib import Path

from tollan.config import RuntimeContext
from tollan.execution import ExecutionPolicy, ExecutionRequest, JobSpec
from tollan.utils.yaml import yaml_loads

DECK = Path(__file__).resolve().parents[1] / "toltec-deployment-and-execution.md"


def examples(language):
    """Return the deck's code blocks in one language."""
    return re.findall(rf"```{language}\n(.*?)\n```", DECK.read_text(), re.S)


def main():
    """Validate the displayed configuration and run the displayed resolution."""
    (profiles,) = examples("yaml")
    runtime = RuntimeContext()
    runtime.update_default_config(yaml_loads(profiles))
    resolution, dagster = examples("python")
    namespace = {"runtime": runtime}
    exec(compile(resolution, f"{DECK.name}:resolution", "exec"), namespace)  # noqa: S102
    spec = namespace["spec"]
    assert spec.profile.name == "compute"
    assert spec.resources.cpus == 1
    assert spec.profile.select_nodes(spec.request, ["compute1", "compute2"]) == [
        "compute2"
    ]
    assert namespace["environ"]["OMP_NUM_THREADS"] == "1"
    assert JobSpec.model_validate_yaml(namespace["kept"]) == spec
    local = ExecutionPolicy(runtime).resolve(ExecutionRequest(workload="ingest"))
    assert local.profile.name == "local"
    for workload in ("kids_quicklook", "ingest"):
        try:
            ExecutionPolicy(runtime).resolve(
                ExecutionRequest(workload=workload, resources={"cpus": 4})
            )
        except ValueError:
            continue
        raise AssertionError(workload)
    compile(dagster, f"{DECK.name}:dagster", "exec")
    print("profiles: valid; resolution: as displayed; dagster example: compiled")


if __name__ == "__main__":
    main()
