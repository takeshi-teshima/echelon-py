# echelon-py: Echelon analysis in Python

## Install
`$ pip install echelon-py`

## Functionalities
- Echelon analysis
- Echelon dendrogram plot
- Echelon scan (detection of spatial clusters)

## Quick Start
Check out some [examples (echelon-py-examples)](https://takeshi-teshima.github.io/echelon-py-examples/)!

## How to Use
Check out the [documentation](https://takeshi-teshima.github.io/echelon-py/).

## Note for Developers
- ``$ pip install -r requirements-dev.txt``

### Testing
- ``$ make test``.

### Deploying
- ``$ make test``.
- Bump version in `echelon/__init__.py`,
- File the changes in `docs_src/CHANGELOG.rst`,
- and run `$ make docs`.
- Make sure that ``$ python setup.py sdist bdist_wheel`` runs without an error.
- Create a Release on GitHub (the deployment procedure is configured by `.github/workflows/python-publish.yml`).

### Documenting
- ``$ make docs``
  - This also runs ``pytest``.
- Edit ``conf.py`` to change the configurations.
- The following contents are auto-generated (and thus overwritten).
  - ``docs_src/src``
  - ``docs``

## References
- R Package [‘echelon’](https://cran.r-project.org/web/packages/echelon/echelon.pdf)
