---
marp: true
theme: kids-review
size: 16:9
paginate: true
title: 'Data models: from sources to selected inputs'
footer: 'Data models · input workflow · 2026-11-22'
---
<!-- _class: cover -->
<!-- _paginate: false -->

# Data models

<p class="subtitle">From sources to selected inputs</p>

Files, tables, capabilities and live data access

<!-- This deck stops at prepared pipeline inputs. Use the product deck for persistent identities, contexts and execution records. -->

---

# A route through the APIs

<div class="cols"><div>

[Three different records](#3)

[Shared and domain responsibilities](#4)

[Sources and filename information](#5)

[File tables and preparation modes](#6)

[Stores and observation selection](#8)

</div><div>

[Selecting data-model capabilities](#10)

[Concrete and composite workflows](#11)

[Opening and reading metadata](#12)

[Units and resource lifetime](#14)

[Configured input discovery](#15)

</div></div>

<p class="note">Companion: <a href="toltec-data-products.html#3">Products, contexts and run inputs</a>.</p>

<!-- The contents links divide the workflow by API responsibility. Review the direct Python path before the configured discovery path. -->

---

# Three records serve different purposes

| Record | Represents | Typical next operation |
|---|---|---|
| File table | Sources and the best information available about them | Query rows; open selected data |
| Product index | Product metadata, relationships, items and locations | Resolve references; save or reopen |
| Context product | Selected product members and their relationships | Resolve members; record a run's inputs |

A file table prepares a selection. A product index describes and retains records.
A context makes the intended combination of product selections explicit.

<!-- A file table describes available sources. A product index persists records and relationships. A context product records a purposeful selection. -->

---

# Shared machinery; domain-defined meaning

<div class="diagram" data-diagram="owners"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 280" role="img" aria-labelledby="owners-title owners-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:280px">
<title id="owners-title">Domain modules depend on shared machinery</title><desc id="owners-desc">LMT, TolTEC and dummy each depend on core; root entry points assemble their registrations.</desc>
<defs><marker id="owners-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 162 100 V 160" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#owners-arrow)"/><rect x="173" y="114" width="48" height="28" fill="white"/><text x="197" y="136" text-anchor="middle" fill="#516276" font-size="22">uses</text><path d="M 560 100 V 160" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#owners-arrow)"/><rect x="571" y="114" width="48" height="28" fill="white"/><text x="595" y="136" text-anchor="middle" fill="#516276" font-size="22">uses</text><path d="M 958 100 V 160" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#owners-arrow)"/><rect x="969" y="114" width="48" height="28" fill="white"/><text x="993" y="136" text-anchor="middle" fill="#516276" font-size="22">uses</text><g><rect x="0" y="0" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="20" y="38" fill="#17283d" font-size="26" font-weight="600">LMT</text>
<text x="20" y="72" fill="#516276" font-size="22">Telescope conventions</text></g><g><rect x="398" y="0" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="418" y="38" fill="#17283d" font-size="26" font-weight="600">TolTEC</text>
<text x="418" y="72" fill="#516276" font-size="22">KIDs and HWPR layouts</text></g><g><rect x="796" y="0" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="816" y="38" fill="#17283d" font-size="26" font-weight="600">Dummy instrument</text>
<text x="816" y="72" fill="#516276" font-size="22">Reference extension</text></g><g><rect x="0" y="160" width="1120" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="20" y="198" fill="#17283d" font-size="26" font-weight="600">core + Tollan</text>
<text x="20" y="232" fill="#516276" font-size="22">Shared validation, projection, dispatch, stores and query machinery</text></g>
</svg></div>

| Level | Owns |
|---|---|
| `core` | Source validation, filename dispatch, table workflow, stores, ObsSpec DSL |
| LMT / TolTEC / dummy | Layouts, metadata, readers, derived columns, query interpretation |
| Root entry points | Built-in assembly and registered extension capabilities |

<p class="note">Core imports are neutral. Core factories still use registrations already loaded.</p>

<!-- Core imports are neutral; they consume available registrations. Root entry points assemble first-party support, and extensions register explicitly. -->

---

# A source and its location can differ

```python
from tolteca_datamodels.source import SourceSourceLoc

source = SourceSourceLoc(source=tel_path)
info = source.filepath_info
assert info is not None
assert "lmt" in info.data_models
```

`source` identifies or supplies the resource. `source_loc` supplies location
information when the resource itself cannot, such as for a borrowed data object.

Universal `FilepathInfo.from_source()` uses the most specialized registered
parser. The base fallback supplies a suffix and empty data-model memberships.

<p class="note">A single SourceSourceLoc raises on invalid input. Batch preparation records per-row failures by default.</p>

<!-- source is the resource to open; source_loc supplies naming and location evidence when the resource itself does not. Universal filepath parsing stays independent of data-model selection. -->

---

# Construct an accessor; use its table

```python
from tolteca_datamodels.file import FileAccessor

file_accessor = FileAccessor.from_sources(paths, mode="guess")
table = file_accessor.table
```



| Column family | Meaning |
|---|---|
| `source`, `source_loc`, `filepath_info` | Resource, location and parsed filename object |
| `file_*` | Original filename evidence |
| Current metadata fields | Best available values used for queries and routing |
| `source_trace` | Issues retained per row, latest entry per kind |

<!-- from_sources returns an accessor. Its table holds source evidence, current metadata and traces. Failed rows remain inspectable. -->

---

# Choose how much information to acquire

| Filename information | `guess` | `guess_or_read` | `read` |
|---|---|---|---|
| Recognized; selected workflow matches | Keep guess | Keep guess | Read metadata |
| Recognized; outside selected capabilities | Keep guess | Keep guess | Keep guess |
| Unidentified | Keep available filename facts | Attempt read | Attempt read |

Metadata replaces current values; `file_*` remains filename evidence.
An unsupported opener or reader leaves an inspectable row and trace.

`on_error="record"` keeps source failures in the table. Use `"raise"` to stop.
Invalid batch arguments still raise.

<!-- Guess is cheap evidence from names. Read obtains metadata for matching or unidentified sources; recognized foreign sources are not read by that workflow. -->

---

# A store finds candidates; a table makes the query

```python
from tolteca_datamodels.lmt.file_store import LmtFileStore
from tolteca_datamodels.lmt_base.obs_spec import ObsSpec
from tolteca_datamodels.toltec.file import ToltecFileAccessor

store = LmtFileStore(data_lmt_path)
S = type(store)
search = store.partial(S.tel, S.toltec)
spec = ObsSpec.parse("145609/{tel,0}")
paths = search.glob_obs_spec(spec)
file_accessor = ToltecFileAccessor.from_sources(paths)
selected = file_accessor.query_obs_spec(spec)
```

`iter_glob_patterns(spec)` exposes the search patterns. Store paths and substores
are declared; a partial view restricts them without changing the store.

<!-- Store selection chooses declared search locations. The complete ObsSpec query is evaluated on the model table after candidate collection. -->

---

# ObsSpec is a context-free query language

| Actor | Interprets the same parsed specification |
|---|---|
| File store | Renders candidate patterns for its own locations |
| Child store | Uses its own interface/range interpretation |
| File workflow | Applies the full table query, including positions |

`*` or `{}` selects all field values; `()` is numeric-only.
Literal sets and numeric ranges are syntax, independent of the instrument.

A store does not combine child query contexts. Composite table queries combine
the contexts of the selected workflows and apply positional selection once.

<!-- Parsing does not choose an instrument. The store and accessor interpret the query with their own field knowledge. -->

---

# DataModelSet selects capabilities

```python
from tolteca_datamodels.data_model import DataModelSet, data_models
from tolteca_datamodels.input_discovery import query_file_store

models = DataModelSet.from_select(["toltec"])
assert data_models.toltec.info_cls.name == "toltec"
selected = query_file_store(store, spec, data_models=models)
```

| Entity | Purpose |
|---|---|
| `DataModelInfo` | Name and descriptive identity of a data model |
| `DataModelSpec` | Its file-accessor class and relevant store types |
| `DataModelSet` | Immutable collection of selected specifications/capabilities |

`data_models` on a **row** is a compatibility set. A TolTEC telescope file can
support both `lmt` and `toltec`; this does not duplicate the row.

<!-- DataModelInfo names a model. DataModelSpec assembles capabilities. DataModelSet selects a set of those capabilities above the file and store machinery. -->

---

# Composition chooses one workflow per row

```python
file_accessor = FileAccessor.from_sources(paths, mode="guess")
partial = file_accessor.partial(accessor_types=(ToltecFileAccessor,))
selected = partial.query_obs_spec(spec)
```

| Component | Responsibility |
|---|---|
| `FileAccessorBase` | Source validation, universal filename projection, table API |
| `FileAccessorWorkflow` | One domain's matching, derivation, readers and queries |
| `CompositeFileWorkflow` | Components, precedence and disjoint row assignment |
| Partial view | Restrict available accessor types; retain the same handling |

TolTEC takes precedence over LMT for a shared TolTEC telescope row.
The dummy composite exercises child workflows without changing the base.

<!-- Composite matching partitions rows among workflows using declared precedence. partial is an instance view that narrows available accessor types. -->

---

# Open resources; read metadata explicitly

```python
from tolteca_datamodels.lmt.file import LmtFileAccessor

file_accessor = LmtFileAccessor.from_sources([tel_path])
with file_accessor.open(on_error="raise") as opened:
    data_accessor = opened.accessor_obj.iloc[0]
    file_accessor.read_metadata(on_error="raise")
    metadata = data_accessor.meta
assert "io_obj" not in file_accessor.table
```

`open()` provides live `io_obj` and `accessor_obj` columns for its lifetime.
`read_metadata()` reads and projects metadata; it can reuse those live accessors.
Called outside `open()`, it manages its own resource lifetime.

No metadata-read cache flag: a requested metadata read runs again.

<!-- open exposes live resource and data-accessor objects. read_metadata updates table columns and uses the same resource handling. -->

---

# Opening and reader selection have distinct jobs

<div class="diagram" data-diagram="open_read"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 200" role="img" aria-labelledby="open_read-title open_read-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:200px">
<title id="open_read-title">Resource and data access</title><desc id="open_read-desc">Source; io_obj; accessor_obj</desc>
<defs><marker id="open_read-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#516276"/></marker></defs>
<path d="M 324 100 H 396" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#open_read-arrow)"/><rect x="336" y="50" width="48" height="28" fill="white"/><text x="360" y="72" text-anchor="middle" fill="#516276" font-size="22">open</text><path d="M 724 100 H 796" fill="none" stroke="#516276" stroke-width="2" marker-end="url(#open_read-arrow)"/><rect x="736" y="50" width="48" height="28" fill="white"/><text x="760" y="72" text-anchor="middle" fill="#516276" font-size="22">bind</text><g><rect x="0" y="50" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="20" y="88" fill="#17283d" font-size="26" font-weight="600">Source</text>
<text x="20" y="122" fill="#516276" font-size="22">Path or borrowed resource</text></g><g><rect x="400" y="50" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="420" y="88" fill="#17283d" font-size="26" font-weight="600">io_obj</text>
<text x="420" y="122" fill="#516276" font-size="22">Format-specific container</text></g><g><rect x="796" y="50" width="324" height="100" rx="12" fill="#f4f7fa" stroke="#007c83" stroke-width="2"/>
<text x="816" y="88" fill="#17283d" font-size="26" font-weight="600">accessor_obj</text>
<text x="816" y="122" fill="#516276" font-size="22">Domain-specific data view</text></g>
</svg></div>

| Operation | Uses | Provides |
|---|---|---|
| Opener selection | Current row values and format | An opened I/O object |
| Reader selection | Row rules, then content inspection if needed | A validated data accessor |
| Metadata read | The live accessor's `.meta` | A model projected into current columns |

Source openers and reader rules use Tollan's rule machinery. Domain readers
supply scientific meaning; core orchestration manages rows and resources.

<!-- The opener handles the resource format. The reader selects and binds a domain accessor. Metadata projection is a subsequent operation. -->

---

# Units survive mapped access and calculation

```python
import astropy.units as u
from tolteca_datamodels.lmt import open_lmt_tel

with open_lmt_tel(tel_path) as dataset:
    tel = dataset.lmt_tel
    az = tel.az.isel(time=slice(0, 100)).u.to(u.deg).load().u.quantity
    alt = tel.alt.isel(time=slice(0, 100)).u.to(u.deg).load().u.quantity
assert az.unit == alt.unit == u.deg
```

`.u.to()` converts from the mapped unit. `.u.quantity` retains physical units.
Load required values while the resource is open.

The dummy measurement uses the same pattern: **mV samples → V → mean-voltage
Quantity → product metadata and ECSV**.

<!-- Mapped arrays carry unit metadata. Convert through the unit accessor before calculation or plotting; do not attach guessed units afterward. -->

---

# Configured discovery assembles these operations

```yaml
input_discovery:
  data_model_select: [toltec]
  inputs:
    - data_lmt_path: /data_lmt
      obs_spec: "145609/{tel,0}"
      mode: read
```

Each entry finds candidates, prepares its table and applies its selection.
Global and entry-level capability selections narrow the available workflows.
The handler combines the resulting records for the next stage.

The outcome is a selected model table. Input discovery does not run a reduction
or publish a product. Pipelines consume the prepared selection.

<!-- Each configured entry discovers candidates and builds a table. Entry results merge for the task to select its inputs. -->

---

# Extension points follow the same ownership

| Extension declares | Consumed by |
|---|---|
| Filename subclass and parser | Universal filename factory |
| Metadata models and data readers | Domain workflow |
| Workflow class and concrete accessor | Direct Python use or composition |
| Store paths / substores | Candidate discovery |
| DataModelSpec | Root capability selection |

```python
from tolteca_dummy_instru import register
register()
models = DataModelSet.from_select(["dummy_instru"])
```

Root imports assemble built-ins; extensions register explicitly.

<!-- Dummy instrument is a small extension that exercises these registration boundaries. It uses the same shared machinery as first-party modules. -->

---

# Where input preparation ends

<div class="cols"><div>

### Data model

Describe acquired files and metadata.

Identify available blocks for selection.

Return queryable input records and typed data access.

</div><div>

### Pipeline / product workflow

Create working blocks and perform analysis.

Choose scientific inputs and calibration models.

Describe results, contexts and publication.

</div></div>

<p class="note">Contracts: tolteca/design/spec/observation-data.md and index.md.
Next: <a href="toltec-data-products.html#3">Product records and structured contexts</a>.</p>

<!-- Input preparation makes metadata available for selection. Block construction, reduction and product publication belong to the next workflow. -->
