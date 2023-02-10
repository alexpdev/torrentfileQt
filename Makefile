.PHONY: clean 

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -frv build/
	rm -frv dist/
	rm -frv .eggs/
	rm -frv .tox/
	rm -fv .coverage
	rm -frv htmlcov/
	rm -frv bin/dist
	rm -frv bin/build
	rm -frv bin/*.zip
	rm -frv htmlcov
	rm -frv coverage.xml
	rm -rfv */__pycache__
	rm -fv corbertura.xml
	rm -frv .pytest_cache
	rm -rfv *.egg-info

test: clean ## run tests quickly with the default Python
	tox

unittest: ## only run unit tests
	tox -e py

push: test ## push changes to remote
	git add .
	git commit -m "$m"
	git push

start: ## start program
	torrentfileQt

release: clean test ## release to pypi
	py -m build .
	twine upload dist/*

build: clean test ## build executable file
	py -m build .
	pip install -e .
	pyinstaller app.spec

install: ## Fresh install from PyPi
	python -m pip install --upgrade --force-reinstall --no-cache torrentfileQt
