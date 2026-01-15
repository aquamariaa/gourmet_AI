# Makefile
PYTHON := python3
PIP := pip
VENV := venv
BIN := $(VENV)/bin

.PHONY: all setup install clean run reset dashboard

all: run

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/$(PIP) install --upgrade pip

install: $(VENV)/bin/activate requirements.txt
	@echo "📦 Installing dependencies..."
	$(BIN)/$(PIP) install -r requirements.txt

run: install
	@echo "🚀 Launching Gourmet AI Pipeline..."
	@$(BIN)/$(PYTHON) scripts/main.py

# NEW COMMAND
dashboard: install
	@echo "📊 Starting Dashboard..."
	@$(BIN)/streamlit run scripts/dashboard.py

clean:
	@echo "🧹 Cleaning up generated files..."
	rm -rf data/raw/*.csv
	rm -rf data/staged/*.csv
	rm -rf data/results/*.csv
	rm -rf __pycache__
	rm -rf scripts/__pycache__

reset: clean
	@echo "🗑️  Removing virtual environment..."
	rm -rf $(VENV)