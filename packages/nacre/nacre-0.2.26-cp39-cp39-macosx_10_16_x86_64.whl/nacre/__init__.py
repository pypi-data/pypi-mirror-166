"""
The top-level package contains all sub-packages needed for NautilusTrader.
"""

import os

import toml


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYPROJECT_PATH = os.path.join(PACKAGE_ROOT, "pyproject.toml")

try:
    __version__ = toml.load(PYPROJECT_PATH)["tool"]["poetry"]["version"]
except FileNotFoundError:  # pragma: no cover
    __version__ = "latest"
