mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
project_dir := $(dir $(mkfile_path))

.PHONY: clean clean-test clean-pyc clean-build docs help install install-user install-develop install2 install-user2 install-develop2
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
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

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 src/vpnmenu tests


# pytest naming conventions on Fedora / Arch Linux as of Oct. 2016
# | Version | Fedora    | Arch Linux |
# |---------+-----------+------------|
# | python3 | py.test-3 | py.test    |
# | python2 | py.test-2 | py.test2   |
test: ## run tests for python3
	@echo "----------------------------------------"
	@echo "Running tests for python3"
	@echo "----------------------------------------"
	eval `which py.test-3 || which py.test` "$(project_dir)tests/"
	

test2: ## run tests for python2
	@echo "----------------------------------------"
	@echo "Running tests for python2"
	@echo "----------------------------------------"
	eval `which py.test-2 || which py.test2` "$(project_dir)tests/"
	


docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/vpnmenu.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/vpnmenu
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes (requires python-watchdog)
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
# watchmedo is a program found in python-watchdog

dist: clean ## builds source and wheel package (requires python-wheel)
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages - python3
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu - may need root\n\t `pip3 --version`"
	@echo "----------------------------------------"
	pip3 install $(project_dir)

install2: clean ## install the package to the active Python's site-packages - python2
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu - may need root\n\t `pip2 --version`"
	@echo "----------------------------------------"
	pip2 install $(project_dir)

install-user: ## install the package to the user's home directory - python3
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu for ${USER}\n\t `pip3 --version`"
	@echo "----------------------------------------"
	pip3 install --user $(project_dir)

install-user2: ## install the package to the user's home directory - python2
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu for ${USER}\n\t `pip2 --version`"
	@echo "----------------------------------------"
	pip2 install --user $(project_dir)

install-develop: ## install the package to the user's home directory as symlinks - python3
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu for ${USER}\n\t `pip3 --version`"
	@echo "----------------------------------------"
	pip3 install --user -e $(project_dir)

install-develop2: ## install the package to the user's home directory as symlinks - python2
	@echo "----------------------------------------"
	@echo -e "Installing vpnmenu for ${USER}\n\t `pip2 --version`"
	@echo "----------------------------------------"
	pip2 install --user -e $(project_dir)

uninstall: ## uninstall the package - python3
	@echo "----------------------------------------"
	@echo -e "Uninstalling vpnmenu - may need root\n\t `pip3 --version`"
	@echo "----------------------------------------"
	-pip3 uninstall vpnmenu

uninstall2: ## uninstall the package - python2
	@echo "----------------------------------------"
	@echo -e "Uninstalling vpnmenu - may need root\n\t `pip2 --version`"
	@echo "----------------------------------------"
	-pip2 uninstall vpnmenu


