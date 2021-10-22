.PHONY: docs

test:
	pytest

docs:
	sphinx-apidoc -e -f -o ./docs_src/src .
	cd docs_src; make
	rsync -av ./docs_src/_build/html/ docs
	touch ./docs/.nojekyll
	cd docs; xdg-open index.html

package-test:
	python setup.py sdist bdist_wheel
