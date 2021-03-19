TolTECA
=======

`TolTECA <https://github.com/toltec-astro>`_ is the software stack developed to
facilitate the data analysis tasks of the
`TolTEC camera <http://toltec.astro.umass.edu>`_, which is to be mounted on the
`Large Millimeter Telescope (LMT) <http://www.lmtgtm.org>`_ and provides simultaneous,
polarization-sensitive imaging at wavelengths of 1.1, 1.4 and 2.0mm through its
7718 Lumped element Kinetic Inductance Detectors (KIDs). For more detailed
description, please check out our recent SPIE papers
`TolTEC <https://ui.adsabs.harvard.edu/abs/2020SPIE11453E..02W/abstract>`_
and `TolTECA <https://ui.adsabs.harvard.edu/abs/2020SPIE11452E..2OM/abstract>`_.

This site hosts a wide range of learning materials and documentations for those
who would like to working with TolTEC data. The site is equipped with a search
box that allows you to filter tutorials by keywords, search for filters, and
make search queries in tutorials and documentation simultaneously.


Installing TolTECA
------------------

The two key components of TolTECA are the Python package ``tolteca``, and the
fast data reduction engine ``citlali`` written in C++. Tolteca implements the
general data and pipeline management framework that serves at the highest
levels, while ``citlali`` works at the low-level to carry out the actual KIDs
readout signal interpretation, time-ordered data (TOD) processing, and
map-making. All the software source codes can be found in the
`toltec-astro <https://github.com/toltec-astro>`_ Github page.

.. tip::

    As of March 2021, the repositories are only available to `toltec-astro`
    organization members. please send email to zhiyuanma (at) umass (dot) edu
    if you would like to have access.


To download and run the Jupyter notebook tutorials, one need to install the
Python package ``tolteca`` and its dependencies, which can be done as follows:

.. code::

    $ git clone https://github.com/toltec-astro/tolteca_tutorials.git
    $ cd tolteca_tutorials
    $ pip install -r pip-requirements.txt


For more detailed instructions of installing ``tolteca`` and to learn about the
C++ data reduction engine ``citlali``, see their documentations
`tolteca <https://github.com/toltec-astro/tolteca>`_ and
`citlali <https://toltec-astro.github.io/citlali/>`_.


For contributors
----------------

Feedback, improvements, and new tutorial content are highly appreciated
via the `TolTECA tutorials repository <https://github.com/toltec-astro/tolteca_tutorials>`_  on
GitHub. Please feel free to open issues or submit pull requests.

For more information, please see the contributing documentation:

.. raw:: html

    <a href="contributing.html"><button id="binder" style="background-color: #fa743b; border-color: #fa743b; margin-bottom: 1rem; cursor: pointer">How to contribute</button></a>


Acknowledgement
---------------

* The TolTEC project is funded by the National Science Foundation, grant #1636621.

* This site uses the HTML templates and infrastructure developed by `Learn Astropy <https://learn.astropy.org>`_.

