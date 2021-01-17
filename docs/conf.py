# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import datetime
import os
import sys

import toml

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "DiviK"
copyright = "{0}, Grzegorz Mrukwa".format(datetime.date.today().year)
author = "Grzegorz Mrukwa"

# The full version, including alpha/beta/rc tags
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, '../pyproject.toml')) as f:
    release = toml.load(f)['tool']['poetry']['version']


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
    "numpydoc",  # required for numpy-style docstrings interpretation
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "inherited-members": True,
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# For ReadTheDocs according to https://stackoverflow.com/a/56448499
master_doc = "index"
