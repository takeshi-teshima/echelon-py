"""
::

    Sphinx-autodoc can't document typevars properly right now,
    see https://github.com/agronholm/sphinx-autodoc-typehints/issues/39
"""
from typing import List, TypeVar, NewType

IndexType = TypeVar('IndexType')
"""Generic index type."""

EchelonType = NewType('EchelonType', List[IndexType])
"""Abstraction of the type of an echelon.
Each echelon is a list of indices of the original data.
It is implemented as mere list of ``IndexType``.
"""

EchelonsType = NewType('EchelonsType', List[EchelonType])
"""List of echelons."""
