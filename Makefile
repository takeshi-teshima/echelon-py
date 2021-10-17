.PHONY: docs

test:
	pytest

docs:
	sphinx-apidoc -e -f -o ./docs/src .
	sphinx-build ./docs/ ./docs/_build/html
	cd docs/_build/html; xdg-open index.html
