---
marp: true
theme: kids-review
size: 16:9
paginate: true
title: 'Data products: records, contexts and execution'
footer: 'Data products · contexts and execution · 2026-11-22'
---
<!-- _class: cover -->
<!-- _paginate: false -->

# Data products

<p class="subtitle">Records, structured contexts and execution</p>

From a described measurement to an exact, reusable selection

<!-- The record framework is shared. Raw observations are one domain-specific structured context built with it. -->

---

# A route from records to execution

<div class="cols"><div>

[Products, items and relationships](#3)

[Shared machinery and domain meaning](#4)

[Exact identities and locations](#5)

[Runs, stores and publication](#7)

[Context terminology](#10)

</div><div>

[Dummy measurement context](#11)

[Raw-observation context](#12)

[Build from recorded history](#13)

[Attach an exact model](#14)

[Save and replay run inputs](#16)

</div></div>

<p class="note">Companion: <a href="tolteca-datamodels-input-workflow.html#3">Sources, file tables and data access</a>.</p>

<!-- Use the contents links during review. The sequence starts with records, then moves to publication and structured contexts. -->

---

# A product is a record with relationships

<div class="diagram" data-diagram="product_records"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 320" role="img" aria-labelledby="product_records-title product_records-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:320px">
<title id="product_records-title">Product record relationships</title><desc id="product_records-desc">A product contains items and has associations. Each association targets a product reference.</desc>
<defs><marker id="product_records-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 290 60 H 410" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#product_records-arrow)"/><rect x="302" y="20" width="96" height="28" fill="white"/><text x="350" y="42" text-anchor="middle" fill="#516276" font-size="22">contains</text><path d="M 145 110 V 242 Q 145 250 153 250 H 410" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#product_records-arrow)"/><rect x="172" y="206" width="36" height="28" fill="white"/><text x="190" y="228" text-anchor="middle" fill="#516276" font-size="22">has</text><path d="M 700 250 H 820" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#product_records-arrow)"/><rect x="718" y="208" width="84" height="28" fill="white"/><text x="760" y="230" text-anchor="middle" fill="#516276" font-size="22">targets</text><g><rect x="0" y="10" width="290" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="20" y="48" fill="#17283d" font-size="26" font-weight="600">Product</text>
<text x="20" y="82" fill="#516276" font-size="22">UID + domain metadata</text></g><g><rect x="410" y="10" width="290" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="430" y="48" fill="#17283d" font-size="26" font-weight="600">Item</text>
<text x="430" y="82" fill="#516276" font-size="22">Metadata + source</text></g><g><rect x="410" y="200" width="290" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="430" y="238" fill="#17283d" font-size="26" font-weight="600">Association</text>
<text x="430" y="272" fill="#516276" font-size="22">Type + relation fields</text></g><g><rect x="820" y="200" width="300" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="840" y="238" fill="#17283d" font-size="26" font-weight="600">Product reference</text>
<text x="840" y="272" fill="#516276" font-size="22">UID + namespace</text></g>
</svg></div>

`DataProdIndexBase` packages a product with locations, actors, runs and supporting
product indexes. Its typed subclasses restore the domain's metadata schema.

Items are constituents of a product. Associations target other products.
Neither relationship implies a filesystem directory or database row.

<!-- A product can describe logical data without an artifact. Items describe data sources; associations connect products by exact reference. -->

---

# Infrastructure does not define an instrument

| Shared `core.data_prod` | Instrument or scientific domain |
|---|---|
| Product, item, reference, association, index | Product metadata and domain relationships |
| Named group and version group contracts | Scientific roles and selection constraints |
| Run, namespace, store, versioned publication | Placement and terminal-primary policy |
| ArtifactBinding and RunInputSnapshot | Sweep ownership and consumer readiness |

`dp_obs`, `dp_raw_obs`, quartets and TolTEC calibration history belong to the
LMT/TolTEC product schema. Core treats product UIDs as opaque identifiers.

Dummy products use their own measurement and summary types. Their **observation
reader** follows LMT conventions; their **product schema** does not reuse TolTEC types.

<!-- The core does not define observation numbers or TolTEC product kinds. Dummy products exercise the same shared storage and version machinery. -->

---

# Identity, relationship and location are separate

| Value | Answers |
|---|---|
| Product UID + namespace | Which exact product? |
| Association type | What does the relationship mean? |
| `is_primary` | Which logical entity groups this result for placement? |
| Item metadata | Which constituent, format and producer? |
| `source.location` + `source.path` | Where is this copy stored? |

A copied index can keep the same product identity while its relative artifact
locations resolve under a new directory. Supporting records do not automatically
become context members or primary relationships.

<!-- A reference identifies a record. A location resolves an item path. Relocation must not change product identity. -->

---

# An artifact binding pins a product item

```python
from tolteca_datamodels.core.data_prod import ArtifactBinding

binding = ArtifactBinding(
    product=index.product.reference,
    producer="dummy_instru.summarize_counters",
    name="counter_summary", format="ecsv",
)
item = binding.resolve(index)
uri = index.get_source_uri(item.source)
```

Resolution checks exact product identity, unique selection and producing-run
attribution. It reads no payload and follows no live tag.

Optional `interface`, `scope` and `source` refine the selection.
`resolve_path(index)` additionally verifies a local file and recorded checksum.

<!-- ArtifactBinding now lives in core.data_prod. It selects exactly one item and checks run attribution. A domain binding adds its own ownership checks. -->

---

# Three different meanings of “save”

| Operation | Effect | Requires a producing run? |
|---|---|---|
| `index.write(path)` | Persist records in ordinary index YAML | No |
| `WorkflowRun` + `store.write_run(run)` | Retain an execution and its context | The run itself |
| `store.materialize(index, ...)` | Publish a result realization and version membership | Yes |

Logical acquisitions, named groups and structured contexts can be ordinary
index records. Saving them does not allocate a result version.

A run is an execution. A store run supplies that execution's local directory name.
A namespace identifies the store's scoped product records.

<!-- Keep document persistence, execution lifecycle and publication distinct. Saving YAML alone does not register or publish a result. -->

---

# Version groups select alternative results

<div class="diagram" data-diagram="versions"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 320" role="img" aria-labelledby="versions-title versions-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:320px">
<title id="versions-title">Version-group alternatives</title><desc id="versions-desc">A group has two exact realizations. Its main tag selects realization B.</desc>
<defs><marker id="versions-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 796 250 H 724" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#versions-arrow)"/><rect x="718" y="206" width="84" height="28" fill="white"/><text x="760" y="228" text-anchor="middle" fill="#516276" font-size="22">selects</text><path d="M 304 100 H 396" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#versions-arrow)"/><rect x="314" y="56" width="72" height="28" fill="white"/><text x="350" y="78" text-anchor="middle" fill="#516276" font-size="22">member</text><path d="M 304 128 H 340 Q 348 128 348 136 V 242 Q 348 250 356 250 H 396" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#versions-arrow)"/><rect x="314" y="198" width="72" height="28" fill="white"/><text x="350" y="220" text-anchor="middle" fill="#516276" font-size="22">member</text><g><rect x="0" y="60" width="304" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="20" y="98" fill="#17283d" font-size="26" font-weight="600">Version group</text>
<text x="20" y="132" fill="#516276" font-size="22">Stable logical result</text></g><g><rect x="396" y="50" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="416" y="88" fill="#17283d" font-size="26" font-weight="600">Realization A</text>
<text x="416" y="122" fill="#516276" font-size="22">Exact product + run A</text></g><g><rect x="396" y="200" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="416" y="238" fill="#17283d" font-size="26" font-weight="600">Realization B</text>
<text x="416" y="272" fill="#516276" font-size="22">Exact product + run B</text></g><g><rect x="796" y="200" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="816" y="238" fill="#17283d" font-size="26" font-weight="600">Tag: main</text>
<text x="816" y="272" fill="#516276" font-size="22">Selects realization B</text></g>
</svg></div>

The group has a stable logical identity and a declared member product type.
Each realization has its own exact reference and producing run.

A tag such as `main` selects one member. An exact artifact binding retains the
chosen member even after the tag moves.

<!-- The group identifies a logical result; each member identifies one realization. A tag is a changing choice, while an exact reference is pinned. -->

---

# Publish a prepared dummy result

```python
from tolteca_datamodels.core.data_prod import WorkflowRun
from tolteca_dummy_instru.data_prod import DummyDataProdStore

store = DummyDataProdStore(output / "store", namespace="nightly")
with WorkflowRun.create() as run:
    draft = make_draft(run)  # Prepared summary; stable logical result UID.
    with store.materialize(draft, run_name="first") as result:
        write_summary_artifact(result, result.base_path)
store.write_run(run)
```

The writer runs on an independent staged index. Successful exit installs the
realization, group membership and selected tag. Failure leaves the old selection.

<p class="note">Helper definitions are in the runnable probe and the dummy-instrument example. No analysis is hidden inside materialize().</p>

<!-- This example runs the dummy voltage workflow and publishes a versioned result. Payload units remain in the ECSV artifact. -->

---

# A context is a structured product

| Term | Meaning |
|---|---|
| Context | Product describing selections that belong together |
| Member | One product selection with a declared role |
| Member key | Local name within this context |
| Member selection | Part of a product: interface, block, statistic or artifact |
| Context binding | Relationship between member keys |
| Artifact binding | Selection of one artifact within an exact product |

A context schema constrains the combination. Its associations own product
references and roles. Supporting indexes supply records for resolution.

Context construction is not execution, payload validation or publication.

<!-- A context is itself a product. Membership roles describe its parts; bindings connect those parts by local member key. -->

---

# Dummy: measurement plus selected summary

<div class="diagram small" data-diagram="dummy_context"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 220" role="img" aria-labelledby="dummy_context-title dummy_context-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:220px">
<title id="dummy_context-title">Dummy context binding</title><desc id="dummy_context-desc">The mean summary member names the voltage measurement member it summarizes.</desc>
<defs><marker id="dummy_context-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 700 110 H 420" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#dummy_context-arrow)"/><rect x="500" y="66" width="120" height="28" fill="white"/><text x="560" y="88" text-anchor="middle" fill="#516276" font-size="22">summarizes</text><g><rect x="60" y="60" width="360" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="80" y="98" fill="#17283d" font-size="26" font-weight="600">signal · measurement</text>
<text x="80" y="132" fill="#516276" font-size="22">Acquisition / voltage stream</text></g><g><rect x="700" y="60" width="360" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="720" y="98" fill="#17283d" font-size="26" font-weight="600">mean · summary</text>
<text x="720" y="132" fill="#516276" font-size="22">Result / mean_voltage</text></g>
</svg></div>

The summary member names the voltage measurement it summarizes.

```python
context_path = write_measurement_context(index, output / "context.yaml")
from tolteca_dummy_instru.data_prod import DummyDataProdIndex
restored = DummyDataProdIndex.read(context_path)
products = {i.product.reference: i.product for i in restored.products}
members = restored.product.resolve_context_members(products.__getitem__)
```

The scalar Quantity is available without opening the ECSV artifact.

<!-- The summary member names the measurement member it summarizes. This is a domain rule expressed with shared product relationships. -->

---

# Raw observations: source, sweep and model roles

<div class="diagram" data-diagram="raw_context"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 340" role="img" aria-labelledby="raw_context-title raw_context-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:340px">
<title id="raw_context-title">Raw-observation context bindings</title><desc id="raw_context-desc">The source names a model and a sweep. The model names the same sweep. Labels are local member keys.</desc>
<defs><marker id="raw_context-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 320 70 H 800" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#raw_context-arrow)"/><rect x="506" y="26" width="108" height="28" fill="white"/><text x="560" y="48" text-anchor="middle" fill="#516276" font-size="22">model_key</text><path d="M 160 120 V 262 Q 160 270 168 270 H 400" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#raw_context-arrow)"/><rect x="190" y="226" width="180" height="28" fill="white"/><text x="280" y="248" text-anchor="middle" fill="#516276" font-size="22">calibration_key</text><path d="M 960 120 V 262 Q 960 270 952 270 H 720" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#raw_context-arrow)"/><rect x="750" y="226" width="180" height="28" fill="white"/><text x="840" y="248" text-anchor="middle" fill="#516276" font-size="22">calibration_key</text><g><rect x="0" y="20" width="320" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="20" y="58" fill="#17283d" font-size="26" font-weight="600">signal · source</text>
<text x="20" y="92" fill="#516276" font-size="22">Raw acquisition / block 1</text></g><g><rect x="800" y="20" width="320" height="100" rx="12" fill="#f4f7fa" stroke="#245bc0" stroke-width="2"/>
<text x="820" y="58" fill="#17283d" font-size="26" font-weight="600">fit · model</text>
<text x="820" y="92" fill="#516276" font-size="22">Processed result / artifact</text></g><g><rect x="400" y="220" width="320" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="420" y="258" fill="#17283d" font-size="26" font-weight="600">cal · sweep</text>
<text x="420" y="292" fill="#516276" font-size="22">Raw acquisition / block 0</text></g>
</svg></div>

A source names its recorded calibration sweep and optional fitted model by local
member key. The model names the same sweep. Several sources may share a sweep.

The context UID is separate from the raw-acquisition UID.
Whole-interface selections are for ancillary data; detector inputs select blocks.

<!-- The source and fitted model both name the same calibration sweep. A model may serve several sources, but each source must retain its own recorded lineage. -->

---

# Build the context from recorded history

```python
from tolteca_datamodels.data_prod.context import RawObsContextSourceAssoc
from tolteca_datamodels.data_prod.metadata import RawObsContextMeta
from tolteca_datamodels.raw_obs_context import build_context_product

product = build_context_product(
    [RawObsContextSourceAssoc(
        uid=raw.product.uid, member_key="signal", interface="toltec0", block=1,
    )],
    indexes=indexes, uid="context:review-A",
    meta=RawObsContextMeta(data_prod_type="dp_raw_obs_context", name="Review A"),
)
```

The caller chooses source blocks. Recorded acquisition history determines their
sweeps. The builder validates those relations, changes no input and opens no payload.

<p class="note">Here the acquired history is sweep block 0 followed by timestream block 1. In a file workflow, build_raw_obs_batch supplies the acquisition records.</p>

<!-- The builder follows recorded block history. It does not invent a missing calibration sweep, run a fit or open payload data. -->

---

# Attach a selected fitted model

```python
from tolteca_datamodels.raw_obs_context import (
    KidsModelBinding, bind_context_models,
)

choice = KidsModelBinding(
    product=model_index.product.reference,
    producer="kidscpp.fit", name="model",
)
bound = bind_context_models(product, {"signal": choice}, indexes=indexes)
```

The result is an independent context copy. The source's calibration stays fixed;
its model choice changes. Existing members and unrelated relationships remain.

`KidsModelBinding` validates processed-acquisition and sweep ownership, then uses
the shared `ArtifactBinding` to select the exact ECSV artifact.

<!-- The caller chooses the model product. Binding validates ownership and records the choice without mutating the input context. -->

---

# Model attachment is a selection operation

| This operation establishes | The consumer still establishes |
|---|---|
| Exact product and artifact | Payload can be loaded |
| Producing run | Scientific fit is suitable |
| Model derives from the recorded sweep | Channels and parameter meanings apply |
| Source and model bind the same sweep | Required model coverage is complete |

A source may remain model-free for inspection. A pipeline that needs fitted
models checks its readiness before running.

`bind_context_models()` neither performs a fit nor discovers a “best” model.
It records a choice supplied by the caller.

<!-- Attachment validates records and relationships. The consumer validates the actual scientific payload before use. -->

---

# Persist the context; snapshot a run's choices

```python
from tolteca_datamodels.data_prod import DataProdIndex
from tolteca_datamodels.raw_obs_context import prepare_context_run_inputs

context_index = DataProdIndex(product=bound, products=list(indexes.values()))
context_index.write(output / "raw-context.yaml")
snapshot = prepare_context_run_inputs([context_index])
with WorkflowRun.create(
    context=snapshot.model_dump(mode="json", round_trip=True),
) as run:
    selected_context, = snapshot.selected_indexes
```

The snapshot retains selected context references and supporting indexes, including
producing runs. Relative location roots must first be bound to an index directory.

It does not copy payloads or turn supporting records into selected inputs.

<!-- Ordinary context persistence saves the context product and supporting records. A run snapshot retains the choices used for one execution. -->

---

# Readback restores choices; consumers resolve them

```python
from tolteca_datamodels.core.data_prod import RunInputSnapshot
from tolteca_datamodels.raw_obs_context import resolve_context_members

saved_run = WorkflowRun.model_validate_json(run.model_dump_json(round_trip=True))
saved = RunInputSnapshot[DataProdIndex].from_run(saved_run)
selected_context, = saved.selected_indexes
members = resolve_context_members(selected_context.product, saved.indexes)
```

Readback validates saved records. Explicit member resolution checks context
relationships; the consumer opens selected data and performs its own readiness checks.

Moving a live tag later does not replace the model recorded in this snapshot.

<!-- Readback reconstructs selections. Opening data and applying scientific models belong to consumers with live resource lifetimes. -->

---

# Current boundaries and further integration

<div class="cols"><div>

### Implemented product path

Build source/sweep context products.

Attach exact model artifacts.

Save ordinary indexes and run snapshots.

Resolve saved members independently of payload I/O.

</div><div>

### Existing consumer context

The older nested `RawObsContext` still serves consumers with representation,
stub, APT, pointing and photometry choices.

Those roles are not yet all expressed by the source/sweep/model product schema.

</div></div>

<p class="note">Contracts: tolteca/design/spec/data-products.md. The shared artifact-binding implementation now belongs to core.data_prod; consumer migration remains a separate review.</p>

<!-- The product path is implemented. Existing nested RawObsContext consumers still carry additional roles; their migration remains separate work. -->
