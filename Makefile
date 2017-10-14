.PHONY: check-venv test pep8 clean coverage

# Clean out potentially stale pyc files
clean:
	find . -name "*.pyc" -exec rm {} \;

# Check that virtualenv is enabled
check-venv:
ifndef VIRTUAL_ENV
	$(error VIRTUAL_ENV is undefined, try "workon" command)
endif

# Install pip requirements.txt file
reqs: check-venv
	pip install --upgrade -r requirements.txt

PEP8_OPTS=--repeat --exclude=static,migrations,js,doc --show-source

pep8:
	pep8 $(PEP8_OPTS) .

FLAKE8_OPTS=--exclude=static,migrations,js,doc
flake8:
	flake8 $(FLAKE8_OPTS) .

#
# Unit tests
#

test: check-venv clean
	python ./manage.py test --keepdb -v 2

travis-tests: check-venv
	@echo "travis_fold:start:flake8"
	make flake8
	@echo "travis_fold:end:flake8"

	@echo "travis_fold:start:pip_freeze"
	pip freeze -l
	@echo "travis_fold:end:pip_freeze"

	coverage erase
	@echo "travis_fold:start:test"
	coverage run $(COVERAGE_ARGS) ./manage.py test --keepdb -v 2
	@echo "travis_fold:end:test"

	@echo "travis_fold:start:coverage"
	coverage report
	coverage html
	@echo "travis_fold:end:coverage"

#
# Run a django instance with a test project for the current app
#

.PHONY: run
run: check-venv clean
	python ./manage.py runserver

#
# Code coverage
#

COVERAGE_ARGS=--source=selenium_testcase --omit=/tests

coverage: check-venv
	coverage erase
	coverage run $(COVERAGE_ARGS) ./manage.py test --keepdb -v 2
	coverage report
	coverage html
	@echo "See ./htmlcov/index.html for coverage report"

develop-%: check-venv
	cd ../$*; python setup.py develop -N

