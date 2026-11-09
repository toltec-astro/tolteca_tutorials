# Assess quality and limitations

Assess whether a product supports the measurement you intend to make. A job
finishing successfully, a product appearing in a viewer, and a scientific
quality assessment are different observations.

## Read the applicable caveats

Start with the selected release's quality notes and the recipe's documented
checks. Record which notes apply to the product version, band, region, and
processing settings you use. This draft does not provide release-specific
acceptance thresholds or a substitute for the team's quality review.

## Check the measurement

| Question                                            | Useful evidence                                                                                                           |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Are the intended data present?                      | Input identities, excluded data, coverage, and processing logs                                                            |
| Is the calibration applicable?                      | Selected calibration artifacts, their scope, and documented checks                                                        |
| Are positions and scales interpreted correctly?     | Coordinate metadata, pixel scale, units, and the workflow's reference comparisons                                         |
| Is the uncertainty meaningful for this measurement? | The documented uncertainty or weight definition, masks, and relevant noise checks                                         |
| Could processing affect the feature of interest?    | Recipe settings, documented artifacts and spatial-scale limitations, and comparisons with an appropriate reference result |

For detector-level investigation, use the available
[sweep-product views](https://toltec.lmtgtm.org/dr/science/docs/tolteca_web/sweep-products.html)
and
[processed KIDs views](https://toltec.lmtgtm.org/dr/science/docs/tolteca_web/processed-kids.html).
Interpret each plot according to its guide; a diagnostic score is not a general
quality certificate for downstream products.

## When a result is unexpected

1. Confirm the product identity and processing version.
2. Check the associated logs, masks, calibration choices, and documented known
   limitations.
3. Compare against an appropriate reference or starting reduction while keeping
   the measurement definition fixed.
4. If the discrepancy remains unexplained, retain the evidence and contact the
   [LMT Helpdesk](https://sites.google.com/umass.edu/lmthelpdesk/home).

Include the product and observation identifiers, software versions, relevant
configuration, expected behavior, and a concise description of the discrepancy.
The [analysis record](provenance.md) helps assemble that information.
