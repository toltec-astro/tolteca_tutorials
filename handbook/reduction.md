# Prepare a reduction

Start with a stated scientific outcome: for example, inspect detector response,
produce a map, or compare a new processing choice with an existing result.
Choose a workflow that documents support for that input and outcome.

## Assemble the inputs

For recorded inputs, consult the [raw-file reference](raw-observations.md) to
check acquisition identities, readout contents, timing, and tuning references.

Record the observation and acquisition identifiers, the data representation you
will process, and the supporting calibration and telescope information required
by the chosen workflow. The
[TolTECA input guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-inputs.html)
and
[observation selectors](https://toltec.lmtgtm.org/dr/science/docs/tolteca/obs_spec.html)
explain how to identify and select files.

A calibration candidate is not yet a selected calibration. Record the exact
artifact or correction used and its application scope. Detector-response,
pointing, and flux calibration address different parts of the measurement;
completion of one does not establish completion of the others. Use the
[calibration glossary](glossary.md#calibration-preparation) when interpreting
these terms.

## Choose and record the software environment

Follow the
[deployment guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca_deploy/) to
create a location on the workstation or compute site you intend to use. Match
the recipe's package versions, calibration inputs, storage requirements, and
configuration before starting a large run.

The current
[KIDs reduction guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca/kids-reduction.html)
lists supported stages and their limitations. A detector-processing example is
not a complete calibrated-map recipe. Check the selected workflow's stated
inputs and outputs before extending it to a different purpose.

## Establish a reproducible starting result

1. Select a documented example compatible with your software and data.
2. Inspect its selected inputs and effective configuration using the workflow's
   documented inspection commands.
3. Run the example and compare its outputs with the example's expected results.
4. Retain the configuration, exact inputs, calibration choices, logs, and output
   identities as described in [the analysis record](provenance.md).
5. Apply the [quality checks](quality.md) before treating the result as suitable
   for science.

The v3 tutorial collection has not yet supplied a complete validated science
reduction example. Until a recipe for your intended output is available, use the
supported package guides and seek guidance from the TolTEC team for the
remaining stages.

## Compare a changed reduction

Keep the starting result and change one scientifically meaningful choice at a
time. Compare like-for-like inputs, regions, units, and measurements. Record
which outputs changed and whether the difference addresses your original
scientific question. A newer software version alone is not evidence that a
particular measurement is more reliable.
