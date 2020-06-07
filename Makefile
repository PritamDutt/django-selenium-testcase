# You can set these variables from the command line
# arguments for sphinx-apidoc autodoc builds

SPHINXOPTS     ?= -n -W
SPHINXBUILD    ?= sphinx-build
SOURCEDIR      ?= docs
BUILDDIR       ?= public
APIOPTS        ?= -f
APIDOCBUILD    ?= sphinx-apidoc
APISOURCE      ?= selenium_testcase
APIDEST        ?= docs/_modules

# Put it first so that "make" without argument is like "make help".
.PHONY: help
help:
	@echo "*** Help ***"
	@echo "  all           make clean pep8 flake8 test coverage docs"
	@echo "  clean         remove generaed build files"
	@echo "  coverage      run tests with code coverage being computed"
	@echo "  reqs          update your requirements from requirements.txt"
	@echo "  reqs-update   compile requirements.txt from requirements.in"
	@echo "  test          run tests"
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# run a complete test suite
.PHONY: all
all:
	make clean
	make pycodestyle
	make flake8
	make test
	make coverage
	make docs

# make all docs
.PHONY: docs
docs:
	make linkcheck
	make html

# clear the generated files
.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/* $(APIDEST)
	find . -name "__pycache__" -exec rm -rf {} \;

# install requirements using pip
.PHONY: reqs
reqs:
	pip install --require-hashes --upgrade -r requirements.txt

# use pip-compile to lock down requirements
.PHONY: update-reqs reqs-update
update-reqs reqs-update:
	pip-compile --no-index --generate-hashes --allow-unsafe

# pep8
.PHONY: pep8 pycodestyle
PEP8_OPTS ?= --repeat --exclude=static,migrations,js,docs --show-source
pep8 pycodestyle:
	pycodestyle $(PEP8_OPTS) .

# flake8
.PHONY: flake8
FLAKE8_OPTS ?= --exclude=static,migrations,js,docs
flake8:
	flake8 $(FLAKE8_OPTS) .

# test
.PHONY: test
TEST_OPTS ?= -v 2
test:
	python ./manage.py test $(TEST_OPTS)

# run
.PHONY: run
RUN_OPTS ?=
run:
	python ./manage.py $(RUN_OPTS) runserver

# coverage

COVERAGE_ARGS ?= --source=$(APISOURCE) --omit=/tests
COVERAGE_OPTS ?= --keepdb -v 2
COVERAGE_REPORT_OPTS ?= -m
COVERAGE_HTML_OPTS ?= -d public/coverage
coverage:
	coverage erase
	coverage run $(COVERAGE_ARGS) ./manage.py test $(COVERAGE_OPTS)
	coverage report $(COVERAGE_REPORT_OPTS)
	coverage html $(COVERAGE_HTML_OPTS)
	@echo "See ./public/coverage/index.html for coverage report"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
ifdef APISOURCE
	@$(APIDOCBUILD) -o "$(APIDEST)" "$(APISOURCE)" $(APIOPTS)
endif
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
