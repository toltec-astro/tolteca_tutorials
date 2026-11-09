# TolTEC observations and measurements

A TolTEC map brings together measurements made by many detectors as the
telescope moves across the sky. Understanding that connection helps explain the
coverage of a map, the structure of its noise, and the processing choices that
affect a scientific measurement.

This chapter follows the signal from the sky to a map. The next chapter turns to
[the data products you will use](products.md).

## Three views of the millimetre sky

TolTEC is a continuum imaging polarimeter on the 50-m Large Millimeter Telescope
(LMT). It observes simultaneously in three wavelength bands, conventionally
called **1.1, 1.4, and 2.0 mm**.[^instrument] Each band has its own detector
array.[^detectors] A band measures radiation over a range of wavelengths; its
nominal wavelength is a label for that spectral response.

Each detector views a small region of sky through the telescope's beam. The beam
describes the angular response to a compact source. A source much smaller than
the beam therefore appears spread over an angular area in a map. The map's pixel
size determines how that image is sampled; it is a separate quantity from the
angular resolution.

The three bands provide complementary measurements of the same field. To compare
their brightnesses, the analysis must account for each product's beam,
calibration, and spatial coverage. Choosing identical pixel sizes alone does not
make two maps measure the same angular structure.

## Scanning turns a sky image into time series

During a scan, each detector's line of sight moves across the field. Imagine a
compact source passing through its beam: the source contribution rises as the
beam approaches, reaches a maximum, and falls as the beam moves away. A second
detector encounters the source at a different time because it occupies a
different position in the focal plane.

The recorded signals are consequently ordered in time. Reconstructing an image
requires the telescope pointing, detector positions, and timing that connect
each measurement to a position on the sky. Repeated visits provide additional
measurements of a region. The scan pattern and data selection determine how
those measurements are distributed across the map.

```{figure} figures/measurement-to-map.svg
:alt: A telescope scan produces detector time series. Timing, pointing, and calibration connect those signals to a reconstructed sky map.
:name: measurement-to-map

From an observation to an image. The drawing is schematic; the curves and map
do not represent a measured dataset or a particular reduction algorithm.
```

The scan speed also connects temporal and angular scales: a given angular
feature is crossed more quickly during a faster scan. This matters because
atmospheric variations and instrumental drifts also contribute to the recorded
time series. Scan strategy and time-domain processing therefore affect the noise
and sky structure recovered in a map.[^scanning]

## What the detectors record

TolTEC uses kinetic inductance detectors (KIDs), superconducting resonators
whose response changes when they absorb radiation. Microwave readout tones probe
that response, allowing many detectors to share a readout system. Changes in the
resonator response carry information about the incident power.[^detectors]

The raw readout records the two components of a complex signal, conventionally
called I and Q. Detector processing interprets those signals using measurements
of the resonator response. These electronic I/Q components describe a different
quantity from the Stokes parameters used for astronomical polarization. The
[raw-file reference](raw-observations.md) shows where the readout signals and
supporting metadata appear in recorded files.

Detector tuning establishes a useful operating point for this measurement.
Converting the response into astronomical brightness requires further
calibration. Detector response, telescope pointing, and flux calibration each
address a different part of the connection between a recorded signal and the
sky.

## Recovering the astronomical signal

A ground-based detector receives emission from the atmosphere as well as from
the astronomical field. The recorded signal also contains instrumental
variations and noise. Reduction uses the detector measurements and supporting
information to estimate the sky contribution, assign it to sky coordinates, and
combine the usable measurements into a map. Citlali is the TolTEC reduction
engine developed for processing time-ordered data and producing maps.[^citlali]

Separating these contributions is particularly consequential for extended
emission: slowly varying sky structure can be difficult to distinguish from
background variations. Processing choices can change the response to different
angular scales. A map is therefore interpreted together with its calibration,
noise information, and processing history. These become central questions when
[assessing a product's suitability for a measurement](quality.md).

For polarization measurements, TolTEC's rotating half-wave plate modulates the
polarized signal. Its recorded orientation supplies additional information for
recovering polarization.[^polarization] Such an analysis needs the applicable
polarization calibration and processing procedure as well as the intensity
measurement described here.

With this measurement picture in place, continue to
[understanding the supplied products](products.md): which stage they represent,
what their values mean, and which accompanying information is needed for your
analysis.

[^instrument]:
    Lunde et al. (2022),
    [optical alignment and characterization](https://doi.org/10.1117/12.2630340).

[^scanning]:
    Thiel (2023),
    [master's thesis, §3.1.1](https://toltec.astro.umass.edu/papers/Thiel_Felix_M_202309_MSC.pdf),
    discusses TolTEC scan patterns and the relationship between temporal and
    angular scales.

[^detectors]:
    Austermann et al. (2018),
    [TolTEC detector development](https://arxiv.org/abs/1803.03280); Bisigello
    et al. (2016),
    [KID readout response and calibration](https://arxiv.org/abs/1602.00442).

[^citlali]:
    McCrackan et al. (2022),
    [the Citlali data reduction engine](https://doi.org/10.1117/12.2629095).

[^polarization]:
    Lee et al. (2022),
    [half-wave-plate commissioning and performance](https://doi.org/10.1117/12.2627725).
