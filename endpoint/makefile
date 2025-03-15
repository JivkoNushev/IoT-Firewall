ifeq ($(OS),Windows_NT)
	OS_DETECTED := Windows
else
	OS_DETECTED := $(shell uname -s)
endif

ifeq ($(OS_DETECTED),Windows)
	PYTHON := python
	VENV_ACTIVATE := .venv\Scripts\activate.bat
	CLEAR_CMD := cls
else
	PYTHON := .venv/bin/python3
	VENV_ACTIVATE := .venv/bin/activate
	CLEAR_CMD := clear
endif

all: run

run:
	$(PYTHON) src/app.py

venv:
	python3 -m venv .venv
	chmod +x $(VENV_ACTIVATE)
	$(VENV_ACTIVATE)
	.venv/bin/pip install -r requirements.txt

deps:
	.venv/bin/pip install -r requirements.txt
