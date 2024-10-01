# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import toml

project = 'LobbyView'
copyright = '2024, LobbyView Team'
author = 'LobbyView Team'

# Get the project root dir, which is the parent dir of this
cwd = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(os.path.dirname(cwd))

# Load the pyproject.toml file
pyproject_path = os.path.join(project_root, 'pyproject.toml')
pyproject_data = toml.load(pyproject_path)

# Set the version
version = pyproject_data['project']['version']
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add the path to your Python package source code
import os
import sys
sys.path.insert(0, os.path.abspath('../../src/lobbyview'))

# Enable the autodoc extension
extensions = [
    'sphinx.ext.autodoc',
]