# TolTEC Data Handbook

**Observations, reduction, and analysis**

This handbook explains how TolTEC measurements become astronomical data and how
to use those data for science. It connects the instrument and observing process
to the meaning of a map, the effects of calibration and reduction, and the
interpretation of a scientific result.

**26 October 2026 draft for review.** The opening chapter and initial product,
quality, and reduction guidance are available. The detailed calibration chapters
and worked scientific analyses are still in preparation. See
[coverage and updates](coverage.md) for the chapter plan and available material.

## Reading the handbook

Begin with [TolTEC observations and measurements](observations.md) for the
physical picture: the three bands, scanning, detector signals, atmospheric
background, and the construction of a map. Then read
[understanding the products](products.md) to connect that picture to the data
you receive.

If you already have prepared products, you can enter at the product chapter and
continue to [assessing quality and limitations](quality.md). For an independent
reduction, [preparing a reduction](reduction.md) connects input selection and
calibration choices to the supported software workflows.

The reference section provides raw-file details, an analysis-record checklist,
and instrument papers. The [shared glossary](glossary.md) defines terms used
throughout the book.

## Working alongside the book

Package guides linked from the chapters explain installation, commands, and APIs
for the software version you use. The
[TolTECA tutorials](https://github.com/toltec-astro/tolteca_tutorials/tree/v3.x)
provide runnable material with a separate `tolteca_ref_data` checkout. The
current v3 tutorial collection supplies a reference-data setup starter; complete
science recipes are being prepared.

For measurements on a particular release, use its accompanying calibration,
quality, access, and citation information alongside this handbook.

```{toctree}
:maxdepth: 2
:caption: Observations and data

observations
products
```

```{toctree}
:maxdepth: 2
:caption: Working with the data

quality
reduction
```

```{toctree}
:maxdepth: 1
:caption: Reference

glossary
raw-observations
provenance
references
coverage
```
