# Configuration file for the Sphinx documentation builder.

import builtins
import os
import sys
from datetime import datetime

builtins.__sphinx__ = True

sys.path.insert(0, os.path.abspath(".."))

project = "Whistle"

first_year, current_year = 2015, datetime.now().year
author = "Romain Dorgueil"
copyright = f"{current_year}, {author}"
if current_year > first_year:
    copyright = str(first_year) + "-" + copyright
version = release = ".".join(__import__("whistle").__version__.split(".")[0:2])


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxcontrib.jquery",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

root_doc = "index"

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "whistle.png",
}
html_js_files = ["js/links-target-blank.js"]
html_css_files = ["css/whistle.css"]
html_baseurl = "https://python-whistle.readthedocs.io/latest/"


todo_include_todos = True
html_show_sphinx = False

autodoc_typehints = "description"
autodoc_member_order = "groupwise"
autodoc_default_flags = ["members", "undoc-members", "show-inheritance"]
autodoc_class_signature = "separated"

autoclass_content = "both"
add_module_names = False
pygments_style = "sphinx"
graphviz_output_format = "svg"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
