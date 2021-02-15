# -- Project information -----------------------------------------------------

project = 'Symengine'
copyright = '2021, Symengine Development Team'
author = 'Symengine Development Team'

# The full version, including alpha/beta/rc tags
release = 'latest'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # Consumes docstrings
    "sphinx.ext.napoleon",  # Allows for Google Style Docs
    "sphinx.ext.viewcode",  # Links to source code
    "sphinx.ext.intersphinx",  # Connects to other documentation
    "sphinx.ext.todo",  # Show TODO details
    "sphinx.ext.imgconverter",  # Handle svg images
    "sphinx.ext.duration",  # Shows times in the processing pipeline
    "sphinx.ext.mathjax",  # Need math support
    "sphinx.ext.githubpages",  # Puts the .nojekyll and CNAME files
    "sphinx_proof",  # Future proofing
    "sphinx_copybutton",  # Let there be plagiarism!
    "sphinxcontrib.bibtex", # References!
    "sphinx_sitemap", # Sitemaps are not part of the theme
    "sphinx_dust", # Review documentation
    "sphinx_togglebutton",  # Toggles reduce clutter
    "myst_nb" # All the myst we need
]

# Allowed Files
source_suffix = ['.md', '.rst']

# Sitemap Config
html_baseurl = "https://symengine.org/"
html_extra_path = ['robots.txt']

# MathJax Configuration
mathjax_config = {
    "extensions": ["tex2jax.js"],
    "jax": ["input/TeX", "output/HTML-CSS"],
}

# Intersphinx Config
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'cpp_api': ('https://symengine.org/api-docs/',None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Bibtex
bibtex_bibfiles = ["references.bib"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['*.ipynb']

# -- Library Theme Settings ------------------------------------------
# Sidebars
html_sidebars = {
    "**": [
        "about.html",  # Project name, description, etc.
        "searchbox.html",  # Search.
        "extralinks.html",  # Links specified in theme options.
        "globaltoc.html",  # Global table of contents.
        "localtoc.html",  # Contents of the current page.
        "readingmodes.html",  # Light/sepia/dark color schemes.
        "sponsors.html",  # Fancy sponsor links.
    ]
}

html_theme_options = {
    "show_breadcrumbs": True,
    "reading_mode": "sepia",
    "typography": "book",
    "extra_links": {
        "Github": "https://github.com/Symengine/symengine.github.io",
    },
}
# -- MyST --------------------------------------------------------------
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]
myst_url_schemes = ("http", "https", "mailto")

# Options for HTML output -------------------------------------------------
html_context = dict(
    display_github=True,
    github_user="Symengine",
    github_repo="symengine.github.io",
    github_version="sources",
    conf_py_path="docs/",
    script_files=[
        "//cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
    ],
)

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'library'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "monokai"
