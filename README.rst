TolTECA Tutorials
=================

This repository contains tutorials for TolTEC data analysis.

To see the tutorials rendered as static web pages, see the `TolTECA tutorials
site <https://toltec-astro.github.io/tolteca_tutorials/rst-tutorials/basic_obs_data.html>`_.

How to run
----------

To run the tutorials interactively, you'll need to make sure you have `Jupyter
notebook <http://jupyter.org/>`_ installed, then clone or download this
repository. The notebook files themselves live in the ``tutorials`` directory
of this repository, organized by the names of the tutorials.

The tutorials depends on TolTECA python packages and some other supporting
packages. To install those packages, run the following (preferrably in a
dedicated virtual environment):

.. code::

    $ cd tolteca_tutorials
    $ pip install -r pip-requirements.txt


You can also get started quickly using `Binder <http://mybinder.org>`_ to run the tutorials in
your web browser within a remote server:

.. image:: http://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/astropy/astropy-tutorials/master?filepath=tutorials/notebooks


Acknowledgement
---------------

This repo makes use of the astropy-tutorials repo as the template.


Contributing tutorial material
------------------------------

Please see the "`For contributors
<http://www.astropy.org/astropy-tutorials/#for-contributors>`_" section
of the tutorials documentation for information on how to get started.


Tutorial infrastructure
-----------------------

For more information on the infrastructure that builds the tutorials, see the
`infrastructure/developer <http://www.astropy.org/astropy-tutorials/dev.html#dev-page>`_
section of the tutorials documentation.
