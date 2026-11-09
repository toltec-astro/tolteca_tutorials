(product-inspection)=

# Understand and inspect products

Before making a measurement, identify what the supplied values represent and
which processing has already been applied. A filename or a successful download
alone does not establish a product's calibration or scientific suitability.

## Identify the dataset

Record the release or delivery identifier, target, contributing observations,
product identifiers, and the accompanying documentation. For products you
generated yourself, also record the reduction run and its inputs.

An {term}`observation` describes measured data; a processing run describes what
was done to those data. Reprocessing an observation can produce different
products without changing the original observation identity. An
{term}`acquisition` identifies one recorded acquisition within that observation.

(inspection-checklist)=

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
the product documentation defines that conversion. A {term}`calibration item`
has an application scope; record that scope as well as its identity.

## Inspect before measuring

1. Check that the target and coordinate coverage match your intended analysis.
2. Inspect the science data together with the available uncertainty, coverage,
   masks, and diagnostic information.
3. Compare any unusual structure with the documented limitations and processing
   choices for this product.
4. Record the region, band, and measurements you intend to use.

For detector diagnostics, @@VIEWER_LINK@@ describes the available views. These
diagnostics do not by themselves establish the suitability of a final science
map.

## Reading an uncertainty plot

The following schematic uses dimensionless illustration data. It is not a TolTEC
observation, sensitivity prediction, or recommended estimation method. It
exercises the figure, equation, and cross-reference rendering used by the
handbook.

```{figure} uncertainty.png
:name: uncertainty-example
:alt: Five illustrative measurements with vertical standard-uncertainty bars.
:width: 90%

Illustrative measurements and their standard uncertainties. These are synthetic
values for this publishing comparison only.
```

If a product explicitly defines its variance as $v$, its standard uncertainty is
related by {eq}`variance-relation`. This relationship alone does not account for
correlations between samples.

```{math}
:label: variance-relation
\sigma = \sqrt{v}
```

Compare {ref}`the illustrated measurements <uncertainty-example>` with the
checks in {ref}`inspection-checklist` before interpreting a product.
