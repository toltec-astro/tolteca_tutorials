# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Astropy documentation build configuration file.

import datetime
import re
import os
import sys

# Load all of the global Astropy configuration
from sphinx_astropy.conf import *
import sphinx_bootstrap_theme

# Get configuration information from setup.cfg
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
conf = ConfigParser()

conf.read([os.path.join(os.path.dirname(__file__), '..', 'metadata.cfg')])
setup_cfg = dict(conf.items('metadata'))


# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.4'  # needed for suppress_warnings

# To perform a Sphinx version check that needs to be more specific than
# major.minor, call `check_sphinx_version("x.y.z")` here.
# check_sphinx_version("1.2.1")

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('**.ipynb_checkpoints')

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog += """
"""

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = setup_cfg['package_name']
author = setup_cfg['author']
copyright = '2013–{0}, {1}'.format(
    datetime.datetime.now().year, setup_cfg['author'])

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version, including alpha/beta/rc tags.
release = setup_cfg['version']
# The short X.Y version.
version = re.match(r'([\d\.]*)(\D*\d?)', setup_cfg['version']).group(1)
if version.endswith('.'): # e.g. "3.0.dev", which splits into groups "3.0." and "dev"
    version = version[:-1]


# -- Options for HTML output --------------------------------------------------

# A NOTE ON HTML THEMES
# The global astropy configuration uses a custom theme, 'bootstrap-astropy',
# which is installed along with astropy. A different theme can be used or
# the options for this theme can be modified by overriding some of the
# variables set in the global configuration. The variables set in the
# global configuration are listed below, commented out.


# Please update these texts to match the name of your package.
html_theme_options = {
    'globaltoc_depth': 2,
    'navbar_fixed_top': "true",
    'bootswatch_theme': "sandstone",
    'bootstrap_version': "3"
}

# html_style = 'custom.css'

# Add any paths that contain custom themes here, relative to this directory.
# To use a different custom theme, add the directory containing the theme.
# html_theme_path = []

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes. To override the custom theme, set this to the
# name of a builtin theme or the name of a custom theme in html_theme_path.
#html_theme = None

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/astropy_favicon.ico"

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# Improve PNG resolution
plot_formats = [('png', 512)]

# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation',
                    author, 'manual')]


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation',
              [author], 1)]


# -- Resolving issue number to links in changelog -----------------------------
github_issues_url = 'https://github.com/{0}/issues/'.format(setup_cfg['github_project'])

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'themes'))]
html_theme = 'tutorials-theme'
html_sidebars = {'tutorials': ['tutorialfilters.html']}

# # Custom style overrides
def setup(app):
    app.add_css_file('bootstrap_sandstone.css')
    app.add_css_file('astropy.css')  # may also be an URL

# -- Run and convert the notebook files to RST --------------------------------

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_scripts_path = os.path.join(_root, 'scripts')
if _scripts_path not in sys.path:
    sys.path.insert(1, _scripts_path)

from convert import process_notebooks
nb_tutorials_path = os.path.join(_root, 'tutorials', 'notebooks')
template_path = os.path.join(_root, 'tutorials', 'astropy.tpl')
rst_output_path = os.path.join(_root, 'tutorials', 'rst-tutorials')

processkwargs = dict(output_path=rst_output_path, template_file=template_path)
if os.environ.get('NBCONVERT_KERNEL'):  # this allows access from "make html"
    processkwargs['kernel_name'] = os.environ.get('NBCONVERT_KERNEL')

if os.environ.get('NBFILE'):  # this allows only building a single tutorial file
    nb_tutorials_path = os.path.abspath(os.environ.get('NBFILE'))

process_notebooks(nb_tutorials_path, **processkwargs)


suppress_warnings = ['image.nonlocal_uri']
html_static_path = ['notebooks', '_static']
html_static_path = [os.path.join(_root, 'tutorials', x)
                    for x in html_static_path] # make absolute paths
