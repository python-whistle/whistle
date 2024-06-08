PACKAGE ?= whistle
PYTHON ?= $(shell which python || echo python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_DIRNAME ?= $(shell dirname $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
PYTHON_REQUIREMENTS_INLINE ?=
PYTHON_REQUIREMENTS_DEV_FILE ?= requirements-dev.txt
PYTHON_REQUIREMENTS_DEV_INLINE ?=
QUICK ?=
PIP ?= $(PYTHON) -m pip
PIP_INSTALL_OPTIONS ?=
POETRY ?= $(shell which poetry || echo poetry)
VERSION ?= $(shell git describe 2>/dev/null || git rev-parse --short HEAD)
PYTEST_OPTIONS ?= --capture=no --cov=$(PACKAGE) --cov-report html
SPHINX_BUILD ?= $(PYTHON_DIRNAME)/sphinx-build
SPHINX_OPTIONS ?=
SPHINX_SOURCEDIR ?= docs
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build
YAPF ?= $(PYTHON) -m yapf
YAPF_OPTIONS ?= -rip

.PHONY: $(SPHINX_SOURCEDIR) clean format help install install-dev release test benchmarks qa

install:  ## Installs the project.
	$(POETRY) install --only main

install-dev:  ## Installs the project (with dev dependencies).
	$(POETRY) install

clean:   ## Cleans up the working copy.
	rm -rf build dist *.egg-info .cache/install .cache/install-dev
	find . -name __pycache__ -type d | xargs rm -rf

test: install-dev  ## Runs the test suite.
	$(POETRY) run pytest $(PYTEST_OPTIONS) --benchmark-disable tests

benchmarks: install-dev  ## Runs the benchmark suite.
	$(PYTEST) $(PYTEST_OPTIONS) --benchmark-only tests

qa: clean format test benchmarks

$(SPHINX_SOURCEDIR): install-dev  ##
	$(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTIONS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html

format: install-dev  ## Reformats the whole python codebase using isort and black.
	isort whistle tests
	black whistle tests

help:   ## Shows available commands.
	@echo "Available commands:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?##[\s]?.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "    make \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo
