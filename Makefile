PYTHON ?= python3
VENV ?= .venv
VENV_BIN = $(VENV)/bin
PIP_UPGRADE ?= 0

.PHONY: venv deps test clean

venv:
	$(PYTHON) -m venv $(VENV)
ifneq ($(PIP_UPGRADE),0)
	$(VENV_BIN)/python -m pip install --upgrade pip
endif

deps: venv
	$(VENV_BIN)/pip install -r requirements-dev.txt

test: venv
	$(VENV_BIN)/python -m unittest discover -s tests

clean:
	rm -rf $(VENV)
