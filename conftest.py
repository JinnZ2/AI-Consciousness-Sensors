import sys
import os

# Ensure the repo root is on sys.path so that top-level packages
# (sensors, explainability, drift, ethics, etc.) can be imported.
sys.path.insert(0, os.path.dirname(__file__))
