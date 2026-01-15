# ==========================================
# 🎨 GOURMET AI PIPELINE MAKEFILE
# ==========================================

# Python Configuration
PYTHON := python3
VENV := venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PY := $(BIN)/python
STREAMLIT := $(BIN)/streamlit

# Sentinel file to track installation state
INSTALLED_FLAG := $(VENV)/.installed

# Colors for decoration
BOLD := \033[1m
GREEN := \033[32m
BLUE := \033[34m
CYAN := \033[36m
RESET := \033[0m

.PHONY: all setup install clean run reset dashboard

all: run

# 1. Create Virtual Env (only if missing)
$(VENV)/bin/activate:
	@echo "$(BLUE)🔧 Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

# 2. Install Dependencies (Only runs if requirements.txt changes)
$(INSTALLED_FLAG): requirements.txt $(VENV)/bin/activate
	@echo "$(CYAN)📦 Installing dependencies... (This happens only once)$(RESET)"
	$(PIP) install -r requirements.txt
	@touch $(INSTALLED_FLAG)

install: $(INSTALLED_FLAG)

# 3. Run Pipeline
run: install
	@echo "$(GREEN)🚀 Launching Gourmet AI Pipeline...$(RESET)"
	@$(PY) scripts/main.py
	@echo "$(BOLD)$(GREEN)📊 Starting Interactive Dashboard...$(RESET)"
	@$(STREAMLIT) run scripts/dashboard.py

# 4. Maintenance
clean:
	@echo "$(BLUE)🧹 Cleaning up generated files...$(RESET)"
	@rm -rf data/raw/*.csv data/staged/*.csv data/results/*.csv
	@rm -rf __pycache__ scripts/__pycache__

reset: clean
	@echo "$(BOLD)🗑️  Removing virtual environment...$(RESET)"
	@rm -rf $(VENV)