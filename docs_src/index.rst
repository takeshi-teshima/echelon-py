.. echelon-py documentation master file, created by
   sphinx-quickstart on Sun Oct 17 15:07:04 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to echelon-py's documentation!
======================================

..
   Overview
   Basics
   Tricks
   Documentation
   GitHub
   PyPI
   Issues
   Contributors
   Feel free to share info about your anytree project.

Installation
------------
::

  $ pip install echelon-py

Usage
-----
Various examples are implemented in the `echelon-py-examples <https://takeshi-teshima.github.io/echelon-py-examples/>`_ repository.


The API modules
---------------

* :doc:`src/echelon.api.dataframe_api`
* :doc:`src/echelon.api.ndarray_api`

The API modules provide easy interface to access the integrated functionalities of the package.

In case these APIs do not match your needs, you can also combine the algorithms separately.
To learn how to combine the different modules in this package, you can look into the API code.

Some of the functionalities that are common to the APIs are implemented in the base module (:doc:`src/echelon.api.base`).

..
   All functionalities are accessible from the API classes.
   They are also *examples* of how the algorithms and other codes can be combined to serve the analysis.

The Contributed modules
---------------
The "contributed" modules provide utility functionalities to handle external packages, various data types, etc.
Currently, the following modules are available:

* :doc:`src/echelon.contrib.geo`


The module contents
--------
These modules are called from the API modules.

* **Algorithms**:
  implemented in the following modules.

  .. toctree::
    :maxdepth: 4

    src/echelon.algorithms.find_peak_echelons
    src/echelon.algorithms.find_foundation_echelons
    src/echelon.algorithms.find_echelon_clusters
    src/echelon.algorithms.find_echelon_hierarchy
    src/echelon.algorithms.find_echelon_hotspots

* **Oracles**:
  abstract the access to the data.
  For custom input data structures, you can implement a new oracle (inheriting ``EchelonOracleBase``)
  using the implemented classes such as ``DataFrameEchelonOracle`` as examples.

  .. toctree::
    :maxdepth: 4

    src/echelon.oracle
    src/echelon.scan_oracle

* **Typing**:
  Some types for type hinting are defined in the following module:

    :doc:`src/echelon.typing`


Supplementary Documents
-----------------------
* :doc:`Algorithms Explained <algorithms>`
* :doc:`Changelog <CHANGELOG>`


Optional Dependencies
-----------------------
- ``scipy`` to enable dendrogram.
- ``anytree`` to store and visualize the echelon hierarchical structure.


Call for Contributions
-----------------------
The algorithms have not been optimized for efficiency (sorry),
and there are probably obvious ways to improve the performance.

* If you encounter a performance issue, please file it on GitHub.
* If you notice an edge case, please file a ``test case`` issue on GitHub.
* If you are kind enough to refactor the algorithms for efficiency, please feel free to open an issue and submit a pull request on GitHub.


Links
-----------------------
If you enjoy this package: |buymeacoffee|

.. |buymeacoffee| image:: https://cdn.buymeacoffee.com/buttons/default-orange.png
    :height: 2em
    :target: https://www.buymeacoffee.com/diadochos


Indices and tables
==================

:ref:`modindex`
