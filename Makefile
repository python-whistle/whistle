# This file has been auto-generated.
# All manual changes may be lost, see Projectfile.
#
# Date: 2016-02-15 08:37:10.941935

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
QUICK ?= 
VIRTUAL_ENV ?= .virtualenv-$(PYTHON_BASENAME)
PIP ?= $(VIRTUAL_ENV)/bin/pip
PYTEST_OPTIONS ?= --capture=no --cov=edgy/event --cov-report html
SPHINX_OPTS ?= 
SPHINX_BUILD ?= $(VIRTUAL_ENV)/bin/sphinx-build
SPHINX_SOURCEDIR ?= doc
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build

.PHONY: clean doc install install-dev lint test

# Installs the local project dependencies.
install: $(VIRTUAL_ENV)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ue "file://`pwd`#egg=edgy.event[dev]"; \
	fi

# Setup the local virtualenv.
$(VIRTUAL_ENV):
	virtualenv -p $(PYTHON) $(VIRTUAL_ENV)
	$(PIP) install -U pip\>=8.0,\<9.0 wheel\>=0.24,\<1.0
	ln -fs $(VIRTUAL_ENV)/bin/activate activate-$(PYTHON_BASENAME)

clean:
	rm -rf $(VIRTUAL_ENV)

lint: install-dev
	$(VIRTUAL_ENV)/bin/pylint --py3k edgy.event -f html > pylint.html

test: install-dev
	$(VIRTUAL_ENV)/bin/py.test $(PYTEST_OPTIONS) tests

install-dev: $(VIRTUAL_ENV) $(WHEELHOUSE)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ue "file://`pwd`#egg=edgy.event[dev]"; \
	fi

doc: install
	$(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html
