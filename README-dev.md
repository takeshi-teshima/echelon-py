# Notes for Contributors

### Environment Setup
- ``$ pip install -r requirements-dev.txt``

### Testing
- ``$ make test``.

### Deploying
- ``$ make test``.
- Bump version in `echelon/__init__.py`,
- File the changes in `docs_src/CHANGELOG.rst`,
- and run `$ make docs`.
- Make sure that ``$ make test-build`` runs without an error. Try ``$ pip install dist/echelon-py-<version>.tar.gz`` if you need.
- Create a Release on GitHub (the deployment procedure is configured by `.github/workflows/python-publish.yml`).

### Documenting
- ``$ make docs``
  - This also runs ``pytest``.
- Edit ``conf.py`` to change the configurations.
- The following contents are auto-generated (and thus overwritten).
  - ``docs_src/src``
  - ``docs``
