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

define CHANGE_NAME
import os
from zipfile import ZipFile
from torrentfileQt.version import __version__
zfile = ZipFile(f"./bin/torrentfileQt-v{__version__}-WIN.zip", mode="w")
zfile.write("./bin/dist/torrentfileQt.exe", "torrentfileQt.exe")
zfile.close()
endef
export CHANGE_NAME

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

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

build: install clean test ## build executable file
	py -m build .
	pip install -e .
	cd bin && pyinstaller exec.spec
	python -c "$$CHANGE_NAME"

install: ## Fresh install from PyPi
	python -m pip install --upgrade --force-reinstall --no-cache torrentfileQt
