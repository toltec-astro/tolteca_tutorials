# Understand and inspect products

Before making a measurement, identify what the supplied values represent and
which processing has already been applied. A filename or a successful download
alone does not establish a product's calibration or scientific suitability.

## Identify the dataset

Record the release or delivery identifier, target, contributing observations,
product identifiers, and the accompanying documentation. For products you
generated yourself, also record the reduction run and its inputs.

An observation identifier describes measured data; a processing run describes
what was done to those data. Reprocessing an observation can produce different
products without changing the original observation identity. The
[observation and acquisition glossary](glossary.md#observations-acquisition-and-readout)
explains the identifiers encountered in TolTEC workflows.

## Establish the product's meaning

| Check                    | What to establish before using the data                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Data representation      | Is this detector readout, a processed timestream, a map, a combined map, or a diagnostic? Which processing steps produced it?                  |
| Units and calibration    | What quantity is stored? Which calibration was applied, and over what observations, arrays, or detectors is it valid?                          |
| Coordinates and sampling | What coordinate frame, projection, pixel scale, and time convention apply?                                                                     |
| Coverage and selection   | Which observations, bands, detectors, and regions contributed? Were any excluded?                                                              |
| Uncertainty information  | Is an accompanying quantity uncertainty, variance, inverse variance, weight, coverage, or a diagnostic? What is its documented interpretation? |
| Quality information      | What flags, masks, limitations, and review results accompany the product?                                                                      |

Use the delivered product description to answer these questions. In particular,
do not treat a weight or coverage quantity as a measurement uncertainty unless
the product documentation defines that conversion.

## Inspect before measuring

1. Check that the target and coordinate coverage match your intended analysis.
2. Inspect the science data together with the available uncertainty, coverage,
   masks, and diagnostic information.
3. Compare any unusual structure with the documented limitations and processing
   choices for this product.
4. Record the region, band, and measurements you intend to use, then follow
   [the quality checklist](quality.md).

For detector diagnostics, the
[processed KIDs viewer guide](https://toltec.lmtgtm.org/dr/science/docs/tolteca_web/processed-kids.html)
describes the available views. These diagnostics do not by themselves establish
the suitability of a final science map.

## Decide whether to reprocess

First identify the scientific limitation you need to address. Check whether the
release documentation recommends a different product or processing version. If
reprocessing is appropriate, retain the original products for comparison and
continue with [preparing a reduction](reduction.md).
