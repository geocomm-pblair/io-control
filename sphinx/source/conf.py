# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# Import the target project.
from iocontrol import meta

# Get project metadata.
this = meta.this()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = this.name
author = this.author
release = str(this.version)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxcontrib.apidoc",
    "sphinxcontrib.confluencebuilder",
]
templates_path = ["_templates"]
exclude_patterns = []
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for API doc generation ------------------------------------------
apidoc_module_dir = f"../../{this.name}"
apidoc_output_dir = "apidoc"
apidoc_excluded_paths = []
apidoc_separate_modules = True
