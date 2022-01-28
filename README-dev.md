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
- Run ``$ make docs`` at the root directory of this package.
  - This also runs ``pytest``.
- Edit ``conf.py`` to change the configurations.
- The following contents are auto-generated (and thus overwritten).
  - ``docs_src/src``
  - ``docs``
- To add a new module to the documentation, go to `docs_src/src`, create one `.rst` file for the module, and fill in the content similarly to the other `.rst` files.
