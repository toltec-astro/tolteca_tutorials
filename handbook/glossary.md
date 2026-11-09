# TolTEC workflow terminology

Use this reference to distinguish the observing units, detector measurements and
scientific results encountered across TolTEC software. Definitions describe
scientific meaning; the linked guides explain supported operations and inputs.

Software terms are introduced in the
[TolTECA domain guides](https://toltec.lmtgtm.org/dr/science/docs/tolteca/terminology.html).
For example, the observation-data guide explains sources, model tables and data
accessors; the product guide explains indexes, references and publication.

One observation can contain a Tune acquisition and a subsequent science
acquisition. Each acquisition can have several readout files. A new reduction
produces a new result from those measurements; it does not create a new
acquisition. Copying a result to another host changes its availability, not the
identity of the measured observation.

## Observations, acquisition, and readout

```{glossary}
Observation
  Observing activity identified by an observation number within an acquisition-master context. It can contain several acquisitions and interfaces. `obsnum`; `tcs-156755`. [Observation selection](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html).

Acquisition / raw observation
  One recorded acquisition identified by master, observation number, subobservation number and scan number. It groups participating interfaces; their samples need not be time aligned. `tcs-156755-0-1`. [Acquisition selection](https://toltec.lmtgtm.org/dr/science/docs/tolteca/raw-obs-context.html).

Acquisition master
  Controller context for an acquisition-number sequence. Observation numbers from different masters are not interchangeable. `master`; labels include `tcs`, `ics`, `clip`. An identifier without a master is context relative. [Selectors](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html).

Subobservation
  Recorded subdivision selected by `subobsnum` within an observation. Its operational meaning depends on the observing program. `subobs`; the drive-fit sequence 145484 uses subobservations 1–7 for different attenuation settings. [Drive fitting](https://toltec.lmtgtm.org/dr/science/docs/tolteca/drive-fit.html).

Scan
  Qualify the meaning: an **acquisition scan number** identifies an acquisition; a **Citlali processing scan** is a sample interval processed within an observation; a **scan pattern** describes telescope motion. Do not infer a processing scan count from `scannum`. [Acquisition selectors](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html); [Citlali reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html).

Subscan
  A subdivision of a scan in a named observing or processing convention. Retain that convention when interpreting the value. Do not substitute `subobsnum`, a KIDs block or a Citlali scan without establishing the correspondence.

Exposure
  A context-dependent observing interval, not an established replacement for the TolTEC acquisition quartet. An exposure duration, integration time, and archive identity answer different questions. Retain this term when explaining another mission's data. For TolTEC file selection use observation/acquisition identifiers. [Selectors](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html).

Acquisition file / interface
  A file records one producing interface's contribution to an acquisition. An interface can be a detector readout, telescope, or half-wave-plate readout. `toltec7`, `tel`, `hwpr`; file identity adds the interface to the acquisition identity. [Input selection](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-inputs.html).

Network
  One TolTEC detector-readout network; network-local channel numbering needs acquisition context. It is not an observing band or an IP network in this usage. `nw`, ROACH, numbered interface; network 7 is `toltec7`. Use “readout network” on first use. [KIDs inputs](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-inputs.html).

Array / band
  A detector array and its associated nominal observing wavelength. An array contains detectors served by multiple readout networks. `a1100`, `a1400`, `a2000`; 1.1, 1.4, 2.0 mm. A network is not an array. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Detector / KID
  A physical kinetic inductance detector. Its identity is independent of the channel number assigned during one acquisition. KID = kinetic inductance detector; plural KIDs. Cross-acquisition matching is needed to establish correspondence. [Drive fitting and matching](https://toltec.lmtgtm.org/dr/science/docs/tolteca/drive-fit.html).

Channel
  One readout channel within a particular acquisition and interface. Subsetting retains its original identity. Equal numbers in different acquisitions do not prove a detector match. `chan`; distinguish a readout channel from another instrument's spectral channel or photometric band. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Tone / frequency comb
  A readout excitation at a selected frequency; the comb is the set of tones with their amplitudes, phases, and masks. A proposed tone need not yet be uploaded or matched to a physical detector. “Probe tone” when interrogating a resonator. Specify RF or LO-relative baseband frequency and units. [Detector power setup](https://toltec.lmtgtm.org/dr/science/docs/tolteca/detector-power-setup.html).

Block
  A coherent interval identified within an acquisition, with applicable channels, probe settings, and recorded model context. It is smaller than the acquisition and is not a scheduler job. “Acquisition block” or “sweep block.” A Tune can contain multiple blocks. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Probe interval / sample
  A probe interval collects samples at one recorded sweep setting. A sample is one recorded readout measurement. Repeated visits to the same frequency remain distinct intervals. A probe axis is not a new detector population. Allocated slots do not prove samples were acquired. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

```

The retained example `toltec7_156755_000_0001_2026_05_16_12_32_26_tune.nc` has
observation 156755, subobservation 0, scan 1, and readout network 7. Its sibling
nominal file has scan 2. These are two acquisitions within the same observation,
not two versions of one reduction.

## Detector tuning and models

```{glossary}
Sweep
  Measurements of complex detector response across probe frequencies. A raw sweep contains recorded samples; a reduced sweep summarizes the acquired intervals. **VNA sweep** searches a broad frequency region; **target sweep** measures the existing target comb. `VnaSweep`, `TargSweep` are LMT Observing Tool actions. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Tune
  The LMT Observing Tool and Tlaloc operation that performs one tone-placement refinement, with two sweeps and two fits separated by an internal placement update. Distinct from one fit or one raw sweep. [Detector setup](https://toltec.lmtgtm.org/dr/science/docs/tolteca/detector-setup.html).

Tone-placement refinement iteration
  One update of the tone placement based on a measured response. A standalone Tune counts as one; an explicit target sweep/reduce/load sequence also counts as one. Initial VNA-to-target placement establishes the starting comb. Reloading unchanged frequencies to apply amplitudes is not another placement iteration.

Resonance finding
  Detecting candidate resonances and relating them to measured input probes. It can change the proposed tone population. “Finding”; distinct from fitting the response of every existing channel. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Resonator fitting / model parameters
  Estimating a specified complex-response model from a sweep. The parameter values require the model family/version, names, units, channel identity, and normalization to be interpretable. “KIDs fit”; native gainlintrend fitting is distinct from drive-fit nonlinear phase fitting. [KIDs artifacts](https://toltec.lmtgtm.org/dr/science/docs/tolteca/workflow-artifacts.html).

Recorded model / newly fitted model
  The recorded model is the model stored with the acquired block. A newly fitted model is estimated by a later fit. A selected external model has its own source block and an application to a target block. “Header model,” “fit report,” and KMP (KIDs model parameters) occur in existing workflows. A recorded model is not evidence that the present reduction fitted it.

Tone matching
  Establishing correspondence between channels/probes or detections across acquisitions. Matching preserves both sides' identities. A same-number channel match is not sufficient. [Drive fitting](https://toltec.lmtgtm.org/dr/science/docs/tolteca/drive-fit.html).

Drive fit
  Estimating useful resonator driving levels from a sequence of sweeps at different attenuations. Produces reusable fit results. “Detector power setup” names the larger operational procedure. [Drive-fit guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/drive-fit.html).

Drive-fit commit
  Applying a saved drive-fit result to a selected target comb to prepare tone amplitudes and drive attenuation. `drive_fit_commit`; “commit” here is neither a Git commit nor hardware application. File preparation, waveform load, and attenuation application are separate actions. [Power setup](https://toltec.lmtgtm.org/dr/science/docs/tolteca/detector-power-setup.html).

```

## Calibration preparation

```{glossary}
Calibration
  A measurement, model, correction, or operation used to interpret instrument response, positions, or fluxes. Qualify which one: calibration observation, calibration artifact, calibration selection, or calibration application. A selected calibration has not necessarily been applied. [Reduction preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html).

Recorded calibration relationship
  The relationship from a detector timestream block to the acquired sweep that characterizes its detector settings. Identified from recorded calibration headers and acquired block order. In the current model, tone placement, channel correspondence and power settings must agree. [Raw-observation contexts](https://toltec.lmtgtm.org/dr/science/docs/tolteca/raw-obs-context.html).

Setup lineage
  The sequence linking a sweep to its preceding sweep as detector settings are refined or verified. Tone placement or power can change along this sequence. It does not itself establish a sweep-to-timestream calibration. [Detector setup](https://toltec.lmtgtm.org/dr/science/docs/tolteca/detector-setup.html).

Calibrator
  A source or observation used to estimate a calibration. Its role depends on the measurement and scientific model. Pointing/flux calibrator; a catalog flux and the flux recovered from a reduction are different quantities. [Reduction preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html).

Reference data
  Data retained for a specified comparison, interpretation, or calibration purpose. State that purpose and version. `tolteca_ref_data` supplies testing/reference acquisitions; it does not mean all those files are calibration corrections. [Reference-data example](https://toltec.lmtgtm.org/dr/science/docs/tolteca/read-acquisition.html).

Ancillary data
  Supporting information needed for a stated interpretation, such as telescope pointing, timestamps, or HWPR state. “Ancillary” does not mean optional. “Auxiliary data” is an accepted descriptive alias when the same role is intended. Calibration data can be separately classified even though they also support interpretation.

APT — array property table
  Detector-associated properties used to interpret an array, including applicable geometry, flags and calibration quantities. Detector/channel correspondence and provenance matter. Spell out **TolTEC array property table** on first use. [APT preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/apt-workflow.html) describes supported inputs and outputs.

APT seed / matched APT / flux-calibrated APT
  A seed provides baseline properties; matching transfers them to a selected observation's detector readout; flux calibration adds or updates the photometric scale. These are distinct scientific states. [Prepare an APT](https://toltec.lmtgtm.org/dr/science/docs/tolteca/apt-workflow.html); [select calibrations for reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html).

Pointing calibration
  Determining or applying offsets needed to relate measured positions to sky/telescope coordinates. Axes, signs, units and applicability must be specified. [Pointing preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html) selects and applies corrections.

PPT / pointing table
  A table of measured pointing offsets and supporting information used to prepare a correction for a selected observation. Candidate tables and the effective correction are different objects. [Pointing preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html) retains the contributing references.

Photometric / flux calibration
  Determining or applying the scale relating measured response to a specified flux quantity. State units, reference source/model and applicable observation/array. Flux calibration does not by itself establish pointing or beam calibration.

Calibration item
  A selected calibration artifact or resolved correction with a stated application scope. [Raw-observation contexts](https://toltec.lmtgtm.org/dr/science/docs/tolteca/raw-obs-context.html) bind selected models; [reduction preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html) selects model, APT and pointing inputs.

```

A completeness claim needs a declared use: for example, interpreting detector
signals or preparing calibrated sky data. Check required interfaces, sample
coverage, units, model identity, detector correspondence, and calibration
applicability for that use. Exact references can describe a complete selection
without placing every payload in one directory. Host availability, applied
calibration state, and reproducibility of an execution are separate checks. The
[context guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/raw-obs-context.html)
explains selecting exact inputs; the
[reduction guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html)
describes their use in a workflow.

## Data representations and reduction

```{glossary}
Raw data
  Measurements as recorded by acquisition, interpreted with their recorded metadata. Raw TolTEC I/Q is different from a Citlali map saved in a directory named `raw`. An acquisition-scoped product can refer to processed representations without changing acquisition identity.

Reduced / processed data
  Data transformed by specified processing operations. The word alone does not state flux units, calibration completeness, or scientific readiness. Reduced sweep means interval-averaged I/Q with retained frequencies and statistics. State the transformation when it matters. [KIDs reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html).

Calibrated data
  Data to which identified calibration operations have been applied. State which calibrations, units, and validity limits. “Calibration-ready” or “calibration-bound” input is not synonymous with calibrated output.

Timestream / TOD
  Measurements ordered in time with the time, detector, and supporting information needed to interpret them. TOD = time-ordered data. Qualify **raw I/Q**, **solved detector signal**, or **calibrated TOD**; time ordering alone does not imply a calibration level. [KIDs artifacts](https://toltec.lmtgtm.org/dr/science/docs/tolteca/workflow-artifacts.html).

Map / mapmaking
  A spatial representation estimated from observations / the operation producing it. Specify coordinates, pixelization, units, weights, masks and processing choices. [Citlali reduction](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html) describes the supported mapmaking workflow.

Coadd
  A combined map/result from multiple contributing inputs. Its meaning includes the selected contributors and combination/weighting method. “Coadded map.” Neither an observation identity nor a particular file format. Native Citlali uses `coadded/`.

Beammap
  Depending on context, an observing mode that measures detector beams, the reduction of that measurement, or its resulting beam/property products. Qualify **beammap observation**, **detector beam map**, or **beammap APT**. A beammap APT is not an image of a beam. [Reduction preparation](https://toltec.lmtgtm.org/dr/science/docs/tolteca/reduction-workdir.html).

Unfiltered / filtered map
  Distinguishes map products before and after the specified output filtering operation. It does not assert that earlier timestream processing was absent. Native Citlali `raw/` and `filtered/` are encountered output labels. Describe the former as an unfiltered map when that is the actual product.

Simulation / source injection
  Simulation constructs modeled measurements; source injection adds a specified synthetic signal to existing data to test recovery or processing. State the injection stage and retain the simulated truth when interpreting recovery.

Quicklook
  A workflow/result intended for prompt observing feedback. It describes purpose and latency, not a universally defined calibration or quality level. `ql`; KIDs diagnostics and map quicklooks are different outputs. [KIDs artifacts](https://toltec.lmtgtm.org/dr/science/docs/tolteca/workflow-artifacts.html).

```
