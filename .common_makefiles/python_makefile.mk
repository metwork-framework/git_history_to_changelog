include .common_makefiles/common_makefile.mk

.PHONY: venv devvenv reformat _check_app_dirs refresh_venv lint reformat tests coverage_console coverage_html coverage_xml

VENV_DIR=venv
PIP=pip3 --disable-pip-version-check
PYTHON=python3
PIP_FREEZE=$(PIP) freeze --all |(grep -v ^pip== ||true) |(grep -v ^setuptools== ||true)
PIP_INDEX_URL=
PIP_EXTRA_INDEX_URL=
_PIP_INDEX_URL_OPT=$(if $(PIP_INDEX_URL),--index-url $(PIP_INDEX_URL),)
_PIP_EXTRA_INDEX_URL_OPT=$(if $(PIP_EXTRA_INDEX_URL),--extra-index-url $(PIP_EXTRA_INDEX_URL),)
PIP_TRUSTED_HOSTS=pypi.org files.pythonhosted.org pypi.fury.io
_PIP_TRUSTED_OPT=$(addprefix --trusted-host ,$(PIP_TRUSTED_HOSTS))
PIP_INSTALL=$(PIP) install $(_PIP_INDEX_URL_OPT) $(_PIP_EXTRA_INDEX_URL_OPT) $(_PIP_TRUSTED_OPT)
MAX_LINE_LENGTH=89
MAX_LINE_LENGTH_MINUS_1=$(shell echo $$(($(MAX_LINE_LENGTH) - 1)))
BLACK=black
BLACK_REFORMAT_OPTIONS=--line-length=$(MAX_LINE_LENGTH_MINUS_1)
BLACK_LINT_OPTIONS=$(BLACK_REFORMAT_OPTIONS) --quiet
FLAKE8=flake8
FLAKE8_LINT_OPTIONS=--ignore=W503,E501 --max-line-length=$(MAX_LINE_LENGTH)
MYPY=mypy
MYPY_LINT_OPTIONS=--ignore-missing-imports
ISORT=isort
ISORT_REFORMAT_OPTIONS=--profile=black --lines-after-imports=2 --virtual-env=$(VENV_DIR)
ISORT_LINT_OPTIONS=$(ISORT_REFORMAT_OPTIONS) --check-only
LINTIMPORTS=lint-imports
BANDIT=bandit
BANDIT_LINT_OPTIONS=-ll -r
SAFETY=safety
SAFETY_CHECK_OPTIONS=
PYLINT=pylint
PYLINT_LINT_OPTIONS=--errors-only --extension-pkg-whitelist=pydantic,_ldap
PYTEST=pytest
TWINE=twine
TWINE_REPOSITORY?=
TWINE_USERNAME?=
TWINE_PASSWORD?=
MAKE_VIRTUALENV=$(PYTHON) -m venv
ENTER_TEMP_VENV=. $(VENV_DIR).temp/bin/activate && unset PYTHONPATH
ENTER_VENV=. $(VENV_DIR)/bin/activate && unset PYTHONPATH
SETUP_DEVELOP=$(PYTHON) setup.py develop

APP_DIRS=
TEST_DIRS=
_APP_AND_TEST_DIRS=$(APP_DIRS) $(TEST_DIRS) $(wildcard setup.py)

PREREQ=
PREDEVREQ=
ifneq ($(wildcard prerequirements-notfreezed.txt),)
	PREREQ+=prerequirements.txt
endif
ifneq ($(wildcard forced-requirements.txt),)
	PREREQ+=forced-requirements.txt
endif
ifneq ($(wildcard predevrequirements-notfreezed.txt),)
	PREDEVREQ+=predevrequirements.txt
endif

all:: venv $(wildcard $(VENV_DIR)/.dev)

clean::
	rm -Rf $(VENV_DIR) $(VENV_DIR).temp htmlcov *.egg-info .mypy_cache .pytest_cache build dist coverage.xml .coverage
	find . -type d -name __pycache__ -exec rm -Rf {} \; >/dev/null 2>&1 || true

requirements.txt: requirements-notfreezed.txt $(PREREQ)
	rm -Rf $(VENV_DIR).temp
	$(MAKE_VIRTUALENV) $(VENV_DIR).temp
	if test -f prerequirements.txt; then $(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r prerequirements.txt; fi
	$(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r $< && $(PIP_FREEZE) |$(PYTHON) $(ROOT_DIR)/python_forced_requirements_filter.py forced-requirements.txt >$@
	rm -Rf $(VENV_DIR).temp

venv:: $(VENV_DIR)/.run ## Make the (runtime) virtualenv

$(VENV_DIR)/.run: requirements.txt
	rm -Rf $(VENV_DIR)
	$(MAKE_VIRTUALENV) $(VENV_DIR)
	if test -f prerequirements.txt; then $(ENTER_VENV) && $(PIP_INSTALL) -r prerequirements.txt; fi
	$(ENTER_VENV) && $(PIP_INSTALL) -r $<
	@mkdir -p $(VENV_DIR) ; touch $@

prerequirements.txt: prerequirements-notfreezed.txt 
	rm -Rf $(VENV_DIR).temp
	$(MAKE_VIRTUALENV) $(VENV_DIR).temp
	$(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r $< && $(PIP_FREEZE) >$@
	rm -Rf $(VENV_DIR).temp

predevrequirements.txt: predevrequirements-notfreezed.txt 
	rm -Rf $(VENV_DIR).temp
	$(MAKE_VIRTUALENV) $(VENV_DIR).temp
	$(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r $< && $(PIP_FREEZE) >$@
	rm -Rf $(VENV_DIR).temp

devrequirements.txt: devrequirements-notfreezed.txt requirements.txt $(PREDEVREQ)
	rm -Rf $(VENV_DIR).temp
	$(MAKE_VIRTUALENV) $(VENV_DIR).temp
	if test -f predevrequirements.txt; then $(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r predevrequirements.txt; fi
	$(ENTER_TEMP_VENV) && $(PIP_INSTALL) -r $< && $(PIP_FREEZE) |$(PYTHON) $(ROOT_DIR)/python_forced_requirements_filter.py forced-requirements.txt >$@
	rm -Rf $(VENV_DIR).temp

devrequirements-notfreezed.txt:
	echo "-r requirements.txt" >$@

requirements-notfreezed.txt:
	touch $@

refresh:: refresh_venv

refresh_venv: ## Update the virtualenv from (dev)requirements-notfreezed.txt
	rm -f requirements.txt
	$(MAKE) venv
	rm -f devrequirements.txt
	$(MAKE) devvenv

devvenv:: $(VENV_DIR)/.dev $(VENV_DIR)/.setup_develop ## Make the (dev) virtualenv (with devtools)

$(VENV_DIR)/.setup_develop: $(wildcard setup.py)
	if test "$(SETUP_DEVELOP)" != "" -a -f setup.py; then $(ENTER_VENV) && $(SETUP_DEVELOP); fi
	@mkdir -p $(VENV_DIR) ; touch $@

$(VENV_DIR)/.dev: devrequirements.txt
	rm -Rf $(VENV_DIR)
	$(MAKE_VIRTUALENV) $(VENV_DIR)
	if test -f predevrequirements.txt; then $(ENTER_VENV) && $(PIP_INSTALL) -r predevrequirements.txt; fi
	$(ENTER_VENV) && $(PIP_INSTALL) -r $<
	@mkdir -p $(VENV_DIR) ; touch $@ $(VENV_DIR)/.run

_check_app_dirs:
	@if test "$(APP_DIRS)" = ""; then echo "ERROR: override APP_DIRS variable in your Makefile" && exit 1; fi

lint: devvenv _check_app_dirs ## Lint the code
	@$(ENTER_VENV) && $(ISORT) --help >/dev/null 2>&1 || exit 0 ; echo "Linting with isort..." && $(ISORT) $(ISORT_LINT_OPTIONS) $(_APP_AND_TEST_DIRS) || ( echo "ERROR: lint errors with isort => maybe you can try 'make reformat' to fix this" ; exit 1)
	@$(ENTER_VENV) && $(BLACK) --help >/dev/null 2>&1 || exit 0 ; echo "Linting with black..." && $(BLACK) $(BLACK_LINT_OPTIONS) $(_APP_AND_TEST_DIRS) || ( echo "ERROR: lint errors with black => maybe you can try 'make reformat' to fix this" ; exit 1)
	@$(ENTER_VENV) && $(FLAKE8) --help >/dev/null 2>&1 || exit 0 ; echo "Linting with flake8..." && $(FLAKE8) $(FLAKE8_LINT_OPTIONS) $(_APP_AND_TEST_DIRS)
	@$(ENTER_VENV) && $(PYLINT) --help >/dev/null 2>&1 || exit 0  ; echo "Linting with pylint..." && $(PYLINT) $(PYLINT_LINT_OPTIONS) $(_APP_AND_TEST_DIRS)
	@$(ENTER_VENV) && $(MYPY) --help >/dev/null 2>&1 || exit 0  ; echo "Linting with mypy..." && $(MYPY) $(MYPY_LINT_OPTIONS) $(_APP_AND_TEST_DIRS)
	@$(ENTER_VENV) && $(LINTIMPORTS) --help >/dev/null 2>&1 || exit 0  ; if test -f .importlinter; then echo "Linting with lint-imports..."; $(LINTIMPORTS); fi
	@$(ENTER_VENV) && $(BANDIT) --help >/dev/null 2>&1 || exit 0  ; echo "Linting with bandit..." && $(BANDIT) $(BANDIT_LINT_OPTIONS) $(APP_DIRS)

reformat: devvenv _check_app_dirs ## Reformat sources and tests
	$(ENTER_VENV) && $(ISORT) --help >/dev/null 2>&1 || exit 0 ; $(ISORT) $(ISORT_REFORMAT_OPTIONS) $(_APP_AND_TEST_DIRS)
	$(ENTER_VENV) && $(BLACK) --help >/dev/null 2>&1 || exit 0 ; $(BLACK) $(BLACK_REFORMAT_OPTIONS) $(_APP_AND_TEST_DIRS)

safety: devvenv ## Check safety of dependencies
	@$(ENTER_VENV) && $(SAFETY) --help >/dev/null 2>&1 || (echo "safety is not installed in you virtualenv"; exit 1)
	@$(ENTER_VENV) && echo "Testing runtime dependencies..." && $(SAFETY) check $(SAFETY_CHECK_OPTIONS) -r requirements.txt
	@$(ENTER_VENV) && echo "Testing dev dependencies..." && $(SAFETY) check $(SAFETY_CHECK_OPTIONS) -r devrequirements.txt

tests: devvenv ## Execute unit-tests
	$(ENTER_VENV) && $(PYTEST) --help >/dev/null 2>&1 || exit 0 ; export PYTHONPATH="." && $(PYTEST) $(TEST_DIRS)

coverage_console: devvenv # Execute unit-tests and show coverage in console
	@$(ENTER_VENV) && $(PYTEST) --help >/dev/null 2>&1 || (echo "pytest is not installed in your virtualenv"; exit 1)
	$(ENTER_VENV) && export PYTHONPATH="." && $(PYTEST) --cov=$(APP_DIRS) $(TEST_DIRS)

coverage_xml: devvenv # Execute unit-tests and compute coverage.xml file
	@$(ENTER_VENV) && $(PYTEST) --help >/dev/null 2>&1 || (echo "pytest is not installed in your virtualenv"; exit 1)
	$(ENTER_VENV) && export PYTHONPATH="." && $(PYTEST) --cov-report=xml --cov=$(APP_DIRS) $(TEST_DIRS)

coverage_html: devvenv # Execute unit-tests and show coverage in html
	@$(ENTER_VENV) && $(PYTEST) --help >/dev/null 2>&1 || (echo "pytest is not installed in your virtualenv"; exit 1)
	$(ENTER_VENV) && export PYTHONPATH="." && $(PYTEST) --cov-report=html --cov=$(APP_DIRS) $(TEST_DIRS)

prewheel:

presdist:

wheel: devvenv prewheel ## Build wheel (packaging)
	$(ENTER_VENV) && python setup.py bdist_wheel

sdist: devvenv presdist ## Build sdist (packaging)
	$(ENTER_VENV) && python setup.py sdist

upload: devvenv sdist  ## Upload to Pypi
	@if test "$(TWINE_USERNAME)" = ""; then echo "TWINE_USERNAME is empty"; exit 1; fi
	@if test "$(TWINE_PASSWORD)" = ""; then echo "TWINE_PASSWORD is empty"; exit 1; fi
	@if test "$(TWINE_REPOSITORY)" = ""; then echo "TWINE_REPOSITORY is empty"; exit 1; fi
	$(ENTER_VENV) && twine upload --repository-url "$(TWINE_REPOSITORY)" --username "$(TWINE_USERNAME)" --password "$(TWINE_PASSWORD)" dist/*
	

