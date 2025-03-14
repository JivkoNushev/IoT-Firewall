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
    PYTHON := python3
    VENV_ACTIVATE := source .venv/bin/activate
    CLEAR_CMD := clear
endif

all: run

venv:
	$(PYTHON) -m venv .venv
	$(VENV_ACTIVATE)

run:
	$(PYTHON) src/main.py