---
marp: true
theme: tolteca-overview
size: 16:9
paginate: true
title: TolTECA v3 — from acquisition to usable products
description: TolTEC data lifecycle, workflows, execution, product provenance and user support.
footer: TolTECA v3 · October 2026
---

<!-- _class: cover -->

<div class="kicker">Status · October 2026</div>

# TolTECA v3

<div class="sub">From acquisition to usable products</div>

<img class="diagram" src="assets/cover.svg" alt="Acquire, process, publish and explore" />

<div class="date">Data · workflows · operations · user support</div>

<!--
0:30. Working components and exercised workflows, with remaining science and deployment work. The full v2 science pipeline has not yet migrated.
-->

---

<!-- _header: Data lifecycle -->

# From observation to the next reduction

<img class="diagram" src="assets/lifecycle.svg" alt="Acquisition, processing, publication, inspection and reprocessing connected through the product database" />

<!--
1:30. The observation planner supports preparation before acquisition. Raw files and acquisition records enter through discovery. The product database records identities, relationships and locations. Artifacts are actual arrays and figures. Inspection can lead to another run. The helpdesk connects this broader user journey.
-->

---

<!-- _header: Run modes -->

# One workflow, several ways to run it

<img class="diagram" src="assets/modes.svg" alt="Python, CLI and Dagster invoke the same configured workflow and can write artifacts and register them" />

<!--
1:00. Python supports exploration and reusable computations. CLI supports manual processing and QA. Dagster supplies scheduling and run supervision. Configuration and scientific workflow stay in the application packages. Writing a product does not require a database; registration is a configurable output action.
-->

---

<!-- _header: Data structure -->

# Observation → acquisition → interface → block

<img class="diagram" src="assets/hierarchy.svg" alt="Observation hierarchy with acquisition files and separate KIDs blocks" />

<!--
1:15. An observation number may contain multiple acquisitions, identified by subobservation and scan. Each acquisition has interface files. KIDs files can hold multiple blocks. File-level readers provide metadata and explicit block identification; the KIDs runner iterates the blocks. Telescope and HWPR readers exist, while the processed-product integration currently exercises KIDs.
-->

---

<!-- _header: Scientific processing -->

# A block owns its data and analyses

<img class="diagram" src="assets/blocks.svg" alt="Sweep and timestream processing branches produce datasets and optional analyses within a block" />

<!--
1:30. SweepReduce averages repeated samples at each sweep step, retaining I/Q uncertainties. SweepCheck ports the v2 core checks, despiking and D21 diagnostics. Timestream processing provides time-domain data and configurable PSD analysis. These are selectable operations, not a requirement to run every analysis. The runner owns acquisitions and interfaces; steps operate on a block. Detector finding and full model solving are not part of this demonstrated slice.
-->

---

<!-- _header: Saved data → interactive inspection -->

# Open a product. Select a block and channel.

<div class="image-layout">
<div>
<p><span class="number">2</span><br>tune blocks</p>
<p><span class="number">632</span><br>channels per block</p>
<p>Selection reads<br>the saved Zarr.</p>
</div>
<img src="assets/processed-viewer.jpg" alt="Actual processed KIDs viewer showing two tune blocks and channel I and Q curves" />
</div>

<div class="caption">Reference acquisition 145609 · toltec0 · block 1</div>

<!--
1:00. This is the working viewer reading the published Docker reference result. The user selects a product location, interface, block and channel. The viewer does not run SweepCheck again. Saved diagnostic views and exported figures share the same configurable visualization machinery.
-->

---

<!-- _header: Live observing workflow -->

# Telescope acquisition → observer feedback

<img class="diagram" src="assets/operations.svg" alt="Telescope records and raw files feed Dagster readiness and independent raw-ingestion and quicklook workflows. Registered feedback serves MC and observers through the quicklook HTTP API." />

<div class="caption">Processing runs while the telescope continues its next exposure.</div>

<!--
1:15. The external acquisition system writes raw files and ToltecDB records. Dagster observes record discovery and file readiness; Valid and local-file availability gate live KIDs processing. Raw ingestion and quicklook computation are independent workflows. Product registration joins the available raw records and published feedback, making the result queryable in DPDB. MC asks the separate HTTP service for feedback and displays the returned images to the observer. Inspection informs the observing team's decisions; the API does not control the telescope. These application workflows also run through CLI without Dagster. Unity inventory, transfer and reprocessing operate independently of this site quicklook path.
-->

---

<!-- _header: Observatory integration · MC HTTP interface -->

# Quicklook API: state and prepared plot URLs

<div class="ql-api">
<div class="ql-request"><span class="label">MC request · one observation number</span><code>GET /api/ql?obs_spec=145609</code></div>
<div class="ql-contract">
<div><h2>JSON response</h2><p>Acquisition / run identity<br /><code>kids_summary</code> · <code>pointing</code></p></div>
<div><h2>Explicit readiness</h2><p><code>ready</code> · <code>pending</code><br /><code>unavailable</code> · <code>unknown</code></p></div>
</div>
<img class="plot" src="assets/quicklook-summary.png" alt="Actual prepared sweep-check summary returned for acquisition 145609; MC follows the returned plot URL to display it" />
</div>

<div class="caption">MC fetches the returned URL · requests never launch or wait for reduction</div>

<!--
1:00. The public contract is GET /api/ql?obs_spec=145609, with named KIDs summary and pointing collections carrying result identity, status and plot URLs. The same endpoint accepts GET /api/ql?obs_spec=tcs-145609-0-1 and broader ObsSpec selections. One obsnum may cover several scans; each is identified in the response. MC currently sends one obsnum at a time, including consecutive requests for grouped observing sequences. Follow the plot URL in the relevant sweep block or pointing array to fetch the image. Ready feedback uses DPDB and a cached immutable descriptor without contacting Dagster. Missing feedback can use a bounded optional Dagster status lookup; its default 100 ms deadline is not a total response-time guarantee. The FastAPI service is separate from the Dash portal. KIDs blocks contain sweep checks and detector-finding summaries; pointing arrays contain fitted offsets and optional figures. Host and port are deployment settings, not part of the endpoint contract.
-->

---

<!-- _header: Product provenance -->

# Preserve the run. Choose what to present.

<img class="diagram" src="assets/products.svg" alt="A published run holds arrays, figures, configuration and records; a version group retains runs and a main tag selects one" />

<!--
1:30. A run has a stable UUID and a readable name. The effective configuration is saved after resolving defaults and overrides. Step records and analysis configuration snapshots remain with the data. A version group links realizations, and a tag such as main selects a run. Changing the tag does not rewrite the old arrays. Replay also needs the same inputs and software environment; saved configuration is necessary, not a promise of bitwise reproducibility. Diagram groups stored information conceptually: index and Zarr carry different parts.
-->

---

<!-- _header: Calibration and lineage -->

# Calibration follows the interfaces

<img class="diagram" src="assets/lineage.svg" alt="An illustrative acquisition uses two VNA ancestors; interface references reduce to acquisition links and a connected calibration group" />

<!--
1:15. Arrows in the upper graph point from an acquisition to its calibration. Readout interfaces need not be synchronized to the same VNA. Persistent per-interface facts preserve that information; acquisition associations and calibration groups are derived from them. Live updates touch affected records rather than rebuild all history. Unknown references remain visible instead of inventing a master. This diagram is illustrative, not a claim about the screenshot acquisition.
-->

---

<!-- _header: Site and archive -->

# Independent inventories, one combined view

<img class="diagram" src="assets/sites.svg" alt="Taco live, transferred Taco data on Unity and native Unity processing retain independent inventories feeding a combined inventory and viewer" />

<!--
1:30. Taco records live operations. A transferred artifact tree has its own inventory and can remain unchanged while Taco advances. Unity reductions create their own results. The unified inventory combines compatible records and locations without taking over the source databases. Incremental transport follows committed database updates, including CLI work. Namespace records processing context; locations specify how to read an artifact. Remote and local availability are not inferred from a namespace string.
-->

---

<!-- _header: Deployment and execution -->

# Services supervise. Compute nodes reduce.

<img class="diagram" src="assets/execution.svg" alt="Dagster and web services remain in the service container; Slurm workers and interactive QA allocations access shared storage" />

<div class="caption">Unity execution design · exercised with service and compute containers in Docker</div>

<!--
1:30. A deployment location supplies the software and configured service profiles. Code locations register workflows in Dagster. Submission policies select the permitted Slurm target, resources and concurrency limits. Slurm owns allocations; manual QA can use an interactive allocation and the same CLI. PostgreSQL serves database clients; shared storage holds inputs, products and execution records. Real Unity authentication, accounts, permissions and enforcement still require site validation.
-->

---

<!-- _header: Run supervision -->

# The reduction has a visible execution history

<img class="image-full run" src="assets/dagster-run.jpg" alt="Actual Dagster success screen with Slurm pending, running and completed states for a compute1 reduction" />

<div class="strip"><span>Submit & track</span><span>Bounded retry</span><span>Cancel</span><span>Recover a known attempt</span></div>

<!--
1:00. This is a completed reference run, with Slurm transitions and the compute host in the event log. The adapter retains scheduler and product identities. Retry is explicit and bounded. A known allocation can be reattached after supervisor failure; ambiguous submission is not blindly retried. Separate registration can be retried using the published output without recomputing the scientific result.
-->

---

<!-- _header: User support · work in progress -->

# tolteca_helpdesk: guidance and AI assistance

<div class="helpdesk-example">
<div>
<h2>Task guidance</h2>
<img class="portal" src="assets/helpdesk-science.jpg" alt="Live TolTEC Science Portal with workflow guidance and observation planner resources" />
<p><strong>Science</strong><br />Plan · analyze · reduce</p>
<p><strong>Operations</strong><br />Observe · curate · QA</p>
</div>
<div>
<h2>AI answer excerpt</h2>
<div class="answer-crop"><img src="assets/helpdesk-answer-wip.png" alt="Unverified AI-generated answer excerpt proposing a CLI command for local DPDB ingestion" /></div>
<div class="excerpt-label">Linked source guide</div>
<div class="citation-crop"><img src="assets/helpdesk-answer-wip.png" alt="Source citation in the same answer: Publish and register product indexes" /></div>
</div>
</div>

<div class="caption wip"><strong>Work-in-progress example — answer accuracy needs improvement.</strong></div>

<!--
1:30. The companion tolteca_dr portal organizes guidance around tasks and links to the planner, software guides and tutorials. Science and operations have separate navigation and retrieval scopes. The operations observer supports a live shift; proposal planning belongs to science. The answer and citation are two crops from the user's Operations Portal screenshot, taken on 2026-10-19. This is a work-in-progress example, not a verified recipe. The complete answer incorrectly describes index publication in its Python example as ingestion. Source links help review an answer; they do not establish correctness. Answer accuracy needs improvement. The portals provide guidance, not instrument control, live monitoring or QA approval.
-->

---

<!-- _header: Helpdesk and software assistants · work in progress -->

# Shared sources, distinct ways to get help

<img class="diagram short" src="assets/helpdesk.svg" alt="Authored sources support task guidance, optional source-grounded AI answers and independent offline, HTTP or MCP access for software assistants" />

<div class="caption">AI answers are reviewable drafts; answer accuracy remains under validation.</div>

<!--
1:00. tolteca_helpdesk grounds human answers in selected authored sources and attaches citations. The AI provider is a separate service, including for local development. The portal host does not run inference. Answer accuracy remains under validation. tolteca_agent exposes the authored documents directly through offline, HTTP and MCP access, without using the human model. Generated answers do not become reference material. Tutorial recipes remain in tolteca_tutorials; package guides remain owned by their packages.
-->

---

<!-- _header: Current scope -->

# Working foundations; science and site rollout ahead

<div class="status-grid">
<div class="status">
<h2>Working now</h2>
<p>Read → reduce → inspect<span class="detail">Block data, sweep checks, PSD, Zarr views</span></p>
<p>Publish → trace → combine<span class="detail">Runs, tags, calibration links, inventories</span></p>
<p>Schedule → supervise<span class="detail">CLI and Dagster; Slurm integration in Docker</span></p>
<p>Find guidance<span class="detail">Science and operations portals; authored sources</span></p>
</div>
<div class="status next">
<h2>Still in progress</h2>
<p>Broader science workflows<span class="detail">Detector finding, solving and further interface integration</span></p>
<p>Unity operational rollout<span class="detail">Site policy, authentication, resource and load validation</span></p>
<p>Helpdesk and learning workflows<span class="detail">Answer accuracy and complete recipes</span></p>
<p>Formal QA and release workflow<span class="detail">Review process and dashboard</span></p>
</div>
</div>

<div class="nav"><a href="#2">Lifecycle</a> · <a href="#5">Processing</a> · <a href="#7">Observing</a> · <a href="#9">Products</a> · <a href="#11">Taco–Unity</a> · <a href="#12">Execution</a> · <a href="#14">Helpdesk</a></div>

<!--
1:15. Distinguish the exercised processing and infrastructure slice from the complete science pipeline and observatory rollout. The current systems provide a common basis for the next science operations, human review and end-user guidance. Processing success does not mean QA acceptance or a science release. The detailed architecture decks provide API-level material for questions.
-->
