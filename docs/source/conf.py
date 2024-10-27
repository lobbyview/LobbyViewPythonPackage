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

extensions = [
    'sphinx.ext.autodoc',
    'nbsphinx',  # Add support for Jupyter notebooks
    'sphinx.ext.mathjax',  # For math rendering in notebooks
]

# NBSphinx settings
nbsphinx_execute = 'never'  # Don't execute notebooks during build
nbsphinx_allow_errors = True  # Continue building even if there are errors

templates_path = ['_templates']
exclude_patterns = ['_build', '**.ipynb_checkpoints']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add the path to your Python package source code
sys.path.insert(0, os.path.abspath('../../src/lobbyview'))