.PHONY: setup run app clean reset

PYTHON := venv/bin/python

run:
	@ $(PYTHON) scripts/main.py

setup:
	python3 -m venv venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

app:
	$(PYTHON) app/server.py

clean:
	rm -rf data/raw/* data/staged/* data/results/*
	rm -rf **/__pycache__

reset: clean
	@ echo "Reset complete"
