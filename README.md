# echelon-py: Echelon analysis in Python

## Functionalities
- Echelon analysis
- Echelon dendrogram plot
- Echelon scan (detection of spatial clusters)

## Quick Start
```python
from echelon import EchelonScan

model = EchelonScan()
model.fit()
model.plot()
pred = model.predict()
```
## Optional Dependencies
- ``scipy`` to enable dendrogram.
- ``anytree`` to store and visualize the echelon hierarchical structure.

## Development
- ``$ pip install -r requirements-dev.txt``

### Documentation
- ``$ make docs``
  - This also runs ``pytest``.
- Edit ``conf.py`` to change the configurations.
- The contents of ``docs/src`` are auto-generated from the Docstrings (and thus often overwritten).

### Testing
- ``$ make test``.

## Links
- [Documentation](#)
- [Examples (echelon-py-examples)](#)

## References
- R Package [‘echelon’](https://cran.r-project.org/web/packages/echelon/echelon.pdf)
- [Myers et al. (1997) <doi:10.1023/A:1018518327329>](#): Echelon Analysis
- [Kurihara (2003) <doi:10.20551/jscswabun.15.2_171>](#): Echelon Scan
- [Project structure](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application)
- [Project template](https://github.com/pypa/sampleproject)
