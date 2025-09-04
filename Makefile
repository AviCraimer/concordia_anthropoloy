VENV := .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

.PHONY: venv dev_deps build run test lint check

venv:
	python3.13 -m venv $(VENV)
	$(PY) -m pip install -U pip

build:
	$(PIP) install -e .

dev_deps:
	$(PIP) install -e .[dev]



# Run to set up initally.
setup: venv dev_deps

run:
	$(VENV)/bin/concordia-anth

test:
	$(VENV)/bin/pytest -q

types:
	$(VENV)/bin/pyright

lint:
	$(VENV)/bin/ruff check .

check: types test lint