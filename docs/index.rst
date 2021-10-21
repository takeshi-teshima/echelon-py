.. echelon-py documentation master file, created by
   sphinx-quickstart on Sun Oct 17 15:07:04 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to echelon-py's documentation!
======================================

..
   Installation
   Introduction
   Overview
   Basics
   API
   Tricks
   Documentation
   GitHub
   PyPI
   Changelog
   Issues
   Contributors
   Feel free to share info about your anytree project.



The API modules
--------
The implemented methods can be accessed via the interface classes:

.. toctree::
   :maxdepth: 4

   src/echelon.api

The API classes are also intended to serve as *examples* of how the methods in the following modules can be combined.

The module contents
--------

Algorithms

.. toctree::
   :maxdepth: 4

   src/echelon.algorithms.find_foundation_echelons
   src/echelon.algorithms.find_peak_echelons
   src/echelon.algorithms.find_echelon_clusters
   src/echelon.algorithms.find_echelon_hierarchy

Oracles abstract the access to the data.
For custom input data structures, one can implement a new oracle (inheriting ``EchelonOracleBase``)
using the implemented classes such as ``DataFrameEchelonOracle`` as examples.

.. toctree::
   :maxdepth: 4

   src/echelon.oracle


Supplementary Documents
-----------------------
   :doc:`Algorithms Explained<algorithms>`


Links
-----------------------
If you enjoy anytree: |buymeacoffee|

.. |buymeacoffee| image:: https://cdn.buymeacoffee.com/buttons/default-orange.png
    :height: 2em
    :target: https://www.buymeacoffee.com/diadochos


Indices and tables
==================

:ref:`modindex`
