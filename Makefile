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

clean: clean-build ## remove all build, test, coverage and Python artifacts

upgrade: clean  ## upgrade all dependencies
	python -m pip install --upgrade pip
	pip install --upgrade --pre -rrequirements.txt

environment:
	.\env\Scripts\activate.bat

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -rfv */__pycache__
	rm -f corbertura.xml
	rm -fr .pytest_cache
	rm -rf *.egg-info

test: environment ## run tests quickly with the default Python
	pytest tests --cov=torrentfileQt --cov=tests
	coverage report
	coverage xml -o coverage.xml

push: clean test ## push changes to remote
	git add .
	git commit -m "$m"
	git push -u origin dev
	bash codacy.sh report -r coverage.xml

branch: ## create dev git branch
	git stash
	git checkout main
	git pull
	git branch -d dev
	git branch dev
	git push -u origin dev
	git stash pop

release: clean test ## release to pypi
	python setup.py sdist bdist_wheel bdist_egg
	twine upload dist/*

build: clean ## building app
	pip install --force-reinstall --upgrade -rrequirements.txt


full: clean test checkout
