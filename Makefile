# -----------------------------------------------------------------------------
# Makefile for Graduation Countdown API Project
# -----------------------------------------------------------------------------

.PHONY: help create_env run

.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
VENV_DIR       := ./venv
REQUIREMENTS   := requirements.txt
PYTHON         := python3
PIP            := $(VENV_DIR)/bin/pip
VENV_PYTHON    := $(VENV_DIR)/bin/python
PORT           := 8000

# Default graduation settings
DATA_FORMATURA := 2025-12-19
HORA_FORMATURA := 10:00

# Detectar sistema operacional para comandos específicos
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    # macOS
    ACTIVATE_CMD := source $(VENV_DIR)/bin/activate
else ifeq ($(UNAME_S),Linux)
    # Linux
    ACTIVATE_CMD := source $(VENV_DIR)/bin/activate
else
    # Windows (assumindo uso de Git Bash ou similar)
    VENV_DIR := ./venv
    PIP := $(VENV_DIR)/Scripts/pip
    VENV_PYTHON := $(VENV_DIR)/Scripts/python
    ACTIVATE_CMD := source $(VENV_DIR)/Scripts/activate
endif

# -----------------------------------------------------------------------------
# Python Environment Targets
# -----------------------------------------------------------------------------

create_env: ## Cria ambiente virtual e instala dependências
	@echo "🐍 Creating Python virtual environment in $(VENV_DIR)..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "⬆️ Upgrading pip..."
	$(PIP) install --upgrade pip
	@echo "📦 Installing dependencies from $(REQUIREMENTS)..."
	$(PIP) install -r $(REQUIREMENTS)
	@echo "✅ Environment created successfully!"
	@echo "To activate manually: $(ACTIVATE_CMD)"


run: ## Executa em modo desenvolvimento com reload automático
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "❌ Virtual environment not found. Run 'make create_env' first."; \
		exit 1; \
	fi
	@echo "🔧 Starting FastAPI server in development mode..."
	@echo "📅 Graduation Date: $(DATA_FORMATURA) at $(HORA_FORMATURA)"
	@DATA_FORMATURA=$(DATA_FORMATURA) HORA_FORMATURA=$(HORA_FORMATURA) \
		$(VENV_PYTHON) -m uvicorn main:app --host 0.0.0.0 --port $(PORT) --reload --log-level debug