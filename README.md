# echelon-py: Echelon analysis in Python

## Install
`$ pip install echelon-py`

## Functionalities
- Echelon analysis
- Echelon dendrogram plot
- Echelon scan (detection of spatial clusters)

## Quick Start
Check out some [Examples (echelon-py-examples)](https://takeshi-teshima.github.io/echelon-py-examples/)!

## How to Use
Check out the [Documentation](https://takeshi-teshima.github.io/echelon-py/).

## Note for Developers
- ``$ pip install -r requirements-dev.txt``

### Testing
- ``$ make test``.

### Build Documentation
- ``$ make docs``
  - This also runs ``pytest``.
- Edit ``conf.py`` to change the configurations.
- The contents of ``docs/src`` are auto-generated from the Docstrings (and thus often overwritten).

## References
- R Package [‘echelon’](https://cran.r-project.org/web/packages/echelon/echelon.pdf)
