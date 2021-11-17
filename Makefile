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

define FIXES
import os
from pathlib import Path
from torrentfileQt.version import _version

distpath =  Path(__file__).resolve().parent / "dist"
for item in distpath.iterdir():
    if item.name == "torrentfileQt.exe":
        os.rename(item, distpath / f"torrentfileQt-v{_version}.exe")
    elif item.name == "torrentfileQt.zip":
        os.rename(item, distpath / f"torrentfileQt-v{_version}-Winx64.zip")
endef
export FIXES


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
	rm -rfv tests/TESTINGDIR

lint: environment ## run linters on codebase
	isort torrentfileQt tests
	pyroma .
	prospector torrentfileQt
	prospector tests

test: lint ## run tests quickly with the default Python
	pytest tests --cov=torrentfileQt --cov=tests --pylint
	coverage report
	coverage xml -o coverage.xml

push: clean test ## push changes to remote
	git add .
	git commit -m "$m"
	git push
	bash codacy.sh report -r coverage.xml

altpush: clean test ## push changes to remote
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

install: ## install app in eedit mode
	pip install --upgrade -rrequirements.txt
	pip install -e .

build:  clean install
	python setup.py sdist bdist_wheel bdist_egg
	rm -rfv ../runner
	mkdir ../runner
	touch ../runner/exe
	cp ./assets/torrentfile.ico ../runner/torrentfile.ico
	cp -rvf ./assets ../runner/assets
	@echo "import torrentfileQt" >> ../runner/exe
	@echo "torrentfileQt.start()" >> ../runner/exe
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-F -n torrentfileQt -w -i ../runner/torrentfile.ico \
		--specpath ../runner/ ../runner/exe --log-level DEBUG \
		--add-data "./assets;./assets"
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-D -n torrentfileQt -w -i ../runner/torrentfile.ico \
		--specpath ../runner/ ../runner/exe --log-level DEBUG \
		--add-data "./assets/*;./assets/"
	cp -rfv ../runner/dist/* ./dist/
	tar -va -c -f ./dist/torrentfileQt.zip ./dist/torrentfileQt
	@python -c "$$FIXES"
