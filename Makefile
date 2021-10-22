.PHONY: docs

test:
	pytest

docs:
	sphinx-apidoc -e -f -o ./docs/src .
	cd docs; make
	cd docs/_build/html; xdg-open index.html
