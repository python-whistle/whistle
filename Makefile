# This file has been auto-generated.
# All manual changes may be lost, see Projectfile.
#
# Date: 2016-02-14 16:17:29.663484

PYTHON ?= $(shell which python)
PYTHON_BASENAME ?= $(shell basename $(PYTHON))
PYTHON_REQUIREMENTS_FILE ?= requirements.txt
QUICK ?= 
VIRTUALENV_PATH ?= .virtualenv-$(PYTHON_BASENAME)
WHEELHOUSE ?= .wheels
PIP ?= $(VIRTUALENV_PATH)/bin/pip
PYTEST_OPTIONS ?= --capture=no --cov=edgy/event --cov-report html
SPHINX_OPTS ?= 
SPHINX_BUILD ?= $(VIRTUALENV_PATH)/bin/sphinx-build
SPHINX_SOURCEDIR ?= doc
SPHINX_BUILDDIR ?= $(SPHINX_SOURCEDIR)/_build

.PHONY: $(WHEELHOUSE) clean doc install install-dev lint test

# Installs the local project dependencies.
install: $(VIRTUALENV_PATH) $(WHEELHOUSE)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ue "file://`pwd`#egg=edgy.event[dev]"; \
	fi

# Setup the local virtualenv.
$(VIRTUALENV_PATH):
	virtualenv -p $(PYTHON) $(VIRTUALENV_PATH)
	$(PIP) install -U pip\>=8.0,\<9.0 wheel\>=0.24,\<1.0
	ln -fs $(VIRTUALENV_PATH)/bin/activate activate-$(PYTHON_BASENAME)

# Setup the local python wheel-house.
$(WHEELHOUSE): $(VIRTUALENV_PATH)
	$(PIP) install -U pip\>=8.0,\<9.0 wheel\>=0.24,\<1.0
	$(PIP) wheel --wheel-dir=$@ -e "file://`pwd`#egg=edgy.event[dev]"

clean:
	rm -rf $(VIRTUALENV_PATH) $(WHEELHOUSE)

lint: install-dev
	$(VIRTUALENV_PATH)/bin/pylint --py3k edgy.event -f html > pylint.html

test: install-dev
	$(VIRTUALENV_PATH)/bin/py.test $(PYTEST_OPTIONS) tests

install-dev: $(VIRTUALENV_PATH) $(WHEELHOUSE)
	if [ -z "$(QUICK)" ]; then \
	    $(PIP) install -Ue "file://`pwd`#egg=edgy.event[dev]"; \
	fi

doc: install
	$(SPHINX_BUILD) -b html -D latex_paper_size=a4 $(SPHINX_OPTS) $(SPHINX_SOURCEDIR) $(SPHINX_BUILDDIR)/html
