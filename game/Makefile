SHELL=/bin/bash

deps:
	python3 -m venv .venv && source .venv/bin/activate && pip3 install --upgrade -r requirements.txt

run:
	source .venv/bin/activate && uvicorn main:app --reload --port 9009 --host 0.0.0.0

run-debug:
	source .venv/bin/activate && uvicorn main:app --reload --port 9009 --host 0.0.0.0 --log-level trace