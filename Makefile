PACKAGE ?= whistle
UV ?= $(shell which uv || echo uv)
UVX ?= $(shell which uvx || echo uvx)
VERSION ?= $(shell git describe 2>/dev/null || git rev-parse --short HEAD)
PYTEST_OPTIONS ?= --capture=no --cov=$(PACKAGE) --cov-report html
SPHINX_BUILD ?= sphinx-build
SPHINX_OPTIONS ?=
SPHINX_SOURCEDIR ?= docs
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build

.PHONY: $(SPHINX_SOURCEDIR) clean clean-dist apidoc format help install install-dev release test benchmarks qa

install:  ## Installs the project.
	$(UV) sync --no-dev

install-dev:  ## Installs the project (with dev dependencies).
	$(UV) sync --all-groups

wheel:
	mkdir -p dist
	bin/sandbox "$(MAKE) install-dev; $(UV) build; cp dist/* $(PWD)/dist"

clean: clean-dist  ## Cleans up the working copy.
	find . -name __pycache__ -type d | xargs rm -rf

clean-dist:  ## Cleans up the distribution files (wheels...)
	rm -rf build dist *.egg-info

apidoc:  ## Generate api doc
	rm -rf docs/reference;
	$(UV) run bin/generate_apidoc

test: install-dev  ## Runs the test suite.
	$(UV) run pytest $(PYTEST_OPTIONS) --benchmark-disable tests

benchmarks: install-dev  ## Runs the benchmark suite.
	$(UV) run pytest $(PYTEST_OPTIONS) --benchmark-only tests

qa: clean apidoc format test benchmarks

$(SPHINX_SOURCEDIR): install-dev  ##
	$(UV) run $(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTIONS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html

format: install-dev  ## Reformats the whole python codebase using ruff.
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

help:   ## Shows available commands.
	@echo "Available commands:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?##[\s]?.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "    make \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo
