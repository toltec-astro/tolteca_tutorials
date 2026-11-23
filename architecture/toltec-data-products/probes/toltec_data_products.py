"""Execute product-deck examples, including dummy artifacts and raw contexts.

The raw records below describe an acquired sweep followed by a timestream.
The model record describes a selected artifact; this probe does not fit or
create that model payload. Dummy artifact examples perform actual ECSV I/O.
"""

import importlib.util
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

import astropy.units as u
from tolteca_datamodels.core.data_prod import WorkflowRun
from tolteca_datamodels.data_prod import (
    DataProd,
    DataProdAssoc,
    DataProdCalRef,
    DataProdIndex,
    DataProdItem,
    DataProdSource,
    Location,
    RawObsBlockHistory,
    RawObsFileCalObsFileMeta,
    RawObsHistoryBlock,
)
from tolteca_datamodels.data_prod.metadata import RawObsMeta, RawObsProcMeta
from tolteca_dummy_instru.analysis import CounterSummary
from tolteca_dummy_instru.data_prod import (
    DummyCounterSummaryMeta,
    DummyDataProd,
    DummyDataProdIndex,
    DummySummaryAcquisitionAssoc,
)

DECK = Path(__file__).resolve().parents[1] / "toltec-data-products.md"
WORKSPACE = Path(__file__).resolve().parents[4]


def make_draft(run):
    return DummyDataProdIndex(
        product=DummyDataProd(
            uid="counter-summary",
            meta=DummyCounterSummaryMeta(
                data_prod_type="dummy_counter_summary",
                summary=CounterSummary(4, 15),
                mean_voltage=3750 * u.mV,
            ),
            assocs=[
                DummySummaryAcquisitionAssoc(uid="dummy:measurement-A", is_primary=True)
            ],
        ),
        run=run,
    )


def acquisition_and_model_records():
    raw = DataProdIndex(
        product=DataProd(
            uid="tcs-145609-0-2",
            meta=RawObsMeta(
                data_prod_type="dp_raw_obs",
                name="Acquired blocks",
                master="tcs",
                obsnum=145609,
                subobsnum=0,
                scannum=2,
            ),
            cal_refs=[
                DataProdCalRef(
                    interface="toltec0",
                    meta=RawObsFileCalObsFileMeta(
                        block_history=RawObsBlockHistory(
                            initial="root",
                            blocks=(
                                RawObsHistoryBlock(kind="sweep"),
                                RawObsHistoryBlock(kind="timestream"),
                            ),
                        ),
                    ),
                )
            ],
        )
    )
    with WorkflowRun.create() as fit_run:
        pass
    model = DataProdIndex(
        product=DataProd(
            uid=f"{raw.product.uid}_proc/{fit_run.uid}",
            namespace_uid=uuid4(),
            meta=RawObsProcMeta(
                data_prod_type="dp_raw_obs_proc",
                name="Selected sweep fit",
                master="tcs",
                obsnum=145609,
                subobsnum=0,
                scannum=2,
            ),
            assocs=[
                DataProdAssoc(
                    data_prod_assoc_type="dpa_raw_obs_proc_raw_obs",
                    uid=raw.product.uid,
                    is_primary=True,
                )
            ],
            data_items=[
                DataProdItem(
                    meta={
                        "type": "artifact",
                        "format": "ecsv",
                        "interface": "toltec0",
                        "scope": "blocks/0",
                        "producer": "kidscpp.fit",
                        "name": "model",
                        "run_uid": str(fit_run.uid),
                    },
                    source=DataProdSource.model_validate(
                        {"location": "models", "path": "fit.ecsv"}
                    ),
                )
            ],
        ),
        run=fit_run,
        locations={"models": Location(root="/recorded/models")},
    )
    return raw, model


def main():
    spec = importlib.util.spec_from_file_location(
        "dummy_example", WORKSPACE / "tolteca/examples/dummy_instru_products.py"
    )
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    raw, model = acquisition_and_model_records()
    with TemporaryDirectory(prefix="datamodel-product-deck-") as directory:
        output = Path(directory).resolve()
        index = DummyDataProdIndex.read(example.run_example(output / "dummy"))
        scope = dict(
            index=index,
            output=output,
            raw=raw,
            model_index=model,
            indexes={i.product.reference: i for i in (raw, model)},
            make_draft=make_draft,
            write_summary_artifact=example.write_summary_artifact,
            write_measurement_context=example.write_measurement_context,
        )
        blocks = re.findall(r"^```python\n(.*?)^```", DECK.read_text(), re.M | re.S)
        for number, code in enumerate(blocks, 1):
            exec(compile(code, f"{DECK}:example-{number}", "exec"), scope)
        assert scope["members"]["signal"].product.reference == raw.product.reference
        assert scope["saved"].inputs == (scope["bound"].reference,)
        print(
            f"{len(blocks)} Python examples passed; exact model and run-input readback verified"
        )


if __name__ == "__main__":
    main()
