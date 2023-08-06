"""
org-template-builder:
    Create org-mode templates for work and study.

Usage: 
    python -m orgtemp myprojectname --author

Where:
    project: name of the project. Required.
    --author, -a: name of the author. Optional. Defaults to "".
"""
from . import install
from . import sources
