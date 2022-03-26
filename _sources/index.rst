TolTECA Tutorials
=================

`TolTECA <https://github.com/toltec-astro>`__ is the software stack developed to
facilitate the data analysis tasks of the
`TolTEC camera <http://toltec.astro.umass.edu>`__, which is mounted on the
`Large Millimeter Telescope (LMT) <http://www.lmtgtm.org>`__ and provides simultaneous,
polarization-sensitive imaging at wavelengths of 1.1, 1.4 and 2.0 mm through its
7718 Lumped element Kinetic Inductance Detectors (KIDs). For more detailed
description, please check out our recent SPIE papers describing
`TolTEC <https://ui.adsabs.harvard.edu/abs/2020SPIE11453E..02W/abstract>`__ and
`TolTECA <https://ui.adsabs.harvard.edu/abs/2020SPIE11452E..2OM/abstract>`__.

This site includes the learning materials for those who would like to work
on TolTEC data on their own.


Get Started
-----------

The two key components of TolTECA that are related to TolTEC are the Python
package ``tolteca``, and the data reduction engine ``citlali`` written in C++.
Tolteca implements the general data and pipeline management framework that
serves at the highest levels, while ``citlali`` works at the low-level to carry
out the actual KIDs readout signal interpretation, time-ordered data (TOD)
processing, and map-making. All the software source codes can be found in the
`toltec-astro <https://github.com/toltec-astro>`__ Github page.

The tutorials are written in format of Jupyter notebooks. These notebooks are
pre-rendered and can be viewed by clicking the titles listed in the next
section. For those who would like to download and run directly in Jupyter, one
may clone the tolteca_tutorials repository and install the requirements using
``pip``:

.. code:: console

    $ git clone https://github.com/toltec-astro/tolteca_tutorials.git
    $ cd tolteca_tutorials
    $ pip install -r pip-requirements.txt


For more detailed instructions of installing ``tolteca`` and to learn about the
C++ data reduction engine ``citlali``, see their documentations
`tolteca <https://github.com/toltec-astro/tolteca>`__ and
`citlali <https://toltec-astro.github.io/citlali/>`__.


List of Tutorials
-----------------

.. toctree::
   :maxdepth: 1

   tutorials/tolteca_setup/tolteca_setup.ipynb
   tutorials/tolteca_simu/tolteca_simu.ipynb


License
--------

3-Clause BSD.


Acknowledgement
---------------

* The TolTEC project is funded by the National Science Foundation, grant #1636621.
