.PHONY: clean help full
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

enviornment:  ## Actiate local python environmant
	env\Scripts\activate.bat

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -frv build/
	rm -frv dist/
	rm -frv .eggs/
	rm -frv .tox/
	rm -fv .coverage
	rm -frv htmlcov/
	rm -rfv */__pycache__
	rm -fv corbertura.xml
	rm -frv .pytest_cache
	rm -rfv *.egg-info
	rm -rfv tests/TESTINGDIR

lint: ## run linters on codebase
	pyroma .
	prospector torrentfileQt
	prospector tests

test: ## run tests quickly with the default Python
	pip install --upgrade --force-reinstall --no-cache torrentfile pyben
	pytest tests --cov=torrentfileQt --cov=tests
	coverage report
	coverage xml -o coverage.xml

push: clean lint test ## push changes to remote
	git add .
	git commit -m "$m"
	git push

start: ## start program
	torrentfileQt

release: clean test lint ## release to pypi
	python setup.py sdist bdist_wheel bdist_egg
	twine upload dist/*

build:  clean
	python -m pip install --upgrade --no-cache --force-reinstall torrentfile pyben pip wheel setuptools
	python setup.py sdist bdist_wheel bdist_egg
	rm -rfv .runner/dist
	rm -rfv .runner/build
	cd .runner && pyinstaller ./exec.spec
	mkdir .runner/dist/torrentfileQt-

full: clean test push release build
