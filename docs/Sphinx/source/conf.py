# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# -- Python Bindings
sys.path.insert(0, os.path.abspath('../../../projects/bindings/python/build'))


# -- Project information -----------------------------------------------------

project = 'Symengine'
copyright = '2020, SymEngine Development Team'
author = 'SymEngine Development Team'
master_doc = "index"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'breathe',
    # 'exhale',
    'myst_nb',
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinx_thebe",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/3.x", None),
}
nitpick_ignore = [
    ("py:class", "docutils.nodes.document"),
    ("py:class", "docutils.parsers.rst.directives.body.Sidebar"),
]

numfig = True

# MyST and MyST-NB configuration ---------------------------------------------------

myst_dmath_enable = True
myst_dmath_allow_labels = True
myst_dmath_allow_space = True
myst_dmath_allow_digits = True
myst_deflist_enable = True
# Non-default
myst_amsmath_enable = True
myst_admonition_enable = True
myst_url_schemes = ("http", "https", "mailto")
panels_add_bootstrap_css = False
# NB stuff
jupyter_cache = "./jupCache"

# -- Exhale configuration ---------------------------------------------------
# Setup the breathe extension
# breathe_projects = {
#     "Symengine XML": "./../../Doxygen/gen_docs/xml"
# }
# breathe_default_project = "Symengine XML"

#  # Setup the exhale extension
# exhale_args = {
#     # These arguments are required
#     "containmentFolder":     "./api",
#     "rootFileName":          "library_root.rst",
#     "rootFileTitle":         "Library API",
#     "doxygenStripFromPath":  "..",
#     # Suggested optional arguments
#     "createTreeView":        True,
#     # TIP: if using the sphinx-bootstrap-theme, you need
#     # "treeViewIsBootstrap": True,
# }

# Tell sphinx what the primary language being documented is.
primary_domain = 'cpp'

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'cpp'

# -- Doxyrest Settings -------------------------------------------------
sys.path.insert(1, os.path.abspath('../../doxyrest/sphinx'))
extensions += ['doxyrest', 'cpplexer']
exclude_patterns += ['page_index.rst']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'nervproject'
# html_theme = 'pyramid'
html_theme = 'sphinx_book_theme'
# -- Sphinx Book Theme Settings
html_theme_options = {
    "repository_url": "https://github.com/symengine/symengine.github.io",
    "use_issues_button": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

