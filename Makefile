.PHONY: docs

test:
	pytest

docs: build-coverage-badge
	sphinx-apidoc -e -f -o ./docs_src/src .
	cd docs_src; make
	rsync -av ./docs_src/_build/html/ docs
	touch ./docs/.nojekyll
	cd docs; xdg-open index.html

build-coverage-badge:
	docstr-coverage src --failunder=0 --skipmagic --exclude=".*/__init__.py" --skipfiledoc --badge ./docs_src/coverage_badge.svg  2>&1 | tee docs_src/docstr-coverage-output.txt

test-build:
	python setup.py sdist bdist_wheel
