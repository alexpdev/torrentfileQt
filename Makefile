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
from torrentfileQt.version import __version__

distpath =  Path(os.getcwd()).resolve() / "dist"
for item in distpath.iterdir():
    if item.name == "torrentfileQt.exe":
        os.rename(item, distpath / f"torrentfileQt-v{__version__}.exe")
    elif item.name == "torrentfileQt.zip":
        os.rename(item, distpath / f"torrentfileQt-v{__version__}-Winx64.zip")
endef
export FIXES

define UNIXES
import os
from pathlib import Path
from torrentfileQt.version import __version__

distpath =  Path(os.getcwd()).resolve() / "dist"
for item in distpath.iterdir():
    if item.name == "torrentfileQt.exe":
        os.rename(item, distpath / f"torrentfileQt-v{__version__}-linux")
    elif item.name == "torrentfileQt.zip":
        os.rename(item, distpath / f"torrentfileQt-v{__version__}-linux.zip")
endef
export FIXES


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

coverage: ## run coverage on project
	pytest tests --cov=torrentfileQt --cov tests
	coverage report
	coverage xml -o coverage.xml
	bash codacy.sh report -r coverage.xml

test: ## run tests quickly with the default Python
	pip install --upgrade --force-reinstall --no-cache -rrequirements.txt
	pytest tests --cov=torrentfileQt --cov=tests

push: clean lint coverage test ## push changes to remote
	git add .
	git commit -m "$m"
	git push

release: clean test lint ## release to pypi
	python setup.py sdist bdist_wheel bdist_egg
	twine upload dist/*

build:  clean
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
	@python -c "$$FIXES"

full: clean test push release build
