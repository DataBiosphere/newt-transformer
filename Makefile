
include common.mk
MODULES=newt tests

all: test

lint:
	flake8 $(MODULES)

mypy:
	mypy --ignore-missing-imports $(MODULES)

check_readme:
	python setup.py check -r -s

tests:=$(wildcard tests/test_*.py)

# A pattern rule that runs a single test module, for example:
#   make tests/test_gen3_input_json.py

$(tests): %.py : mypy lint check_readme
	python -m unittest --verbose $*.py

test: $(tests)

develop:
	pip install -e .
	pip install -r requirements-dev.txt

undevelop:
	python setup.py develop --uninstall
	pip uninstall -y -r requirements-dev.txt

release: test
	python release.py $(VERSION)

.PHONY: all lint mypy test
