# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    Professional Video Downloader Bot                         ║
# ║                         Makefile                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

.PHONY: help install run dev clean docker-build docker-run docker-stop logs test lint format

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_IMAGE := video-downloader-bot
DOCKER_CONTAINER := vdbot

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help: ## Show this help message
	@echo "╔══════════════════════════════════════════════════════════════════════╗"
	@echo "║          🎬 Video Downloader Bot - Available Commands                ║"
	@echo "╚══════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

install: ## Install dependencies and setup environment
	@echo "📦 Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "📦 Installing dependencies..."
	$(VENV)/bin/pip install --upgrade pip setuptools wheel
	$(VENV)/bin/pip install -r requirements.txt
	@echo "📁 Creating directories..."
	mkdir -p temp downloads cookies logs cache database
	@echo "✅ Installation complete!"

setup-env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file. Please edit it with your settings."; \
	else \
		echo "⚠️  .env already exists. Skipping."; \
	fi

# ═══════════════════════════════════════════════════════════════════════════════
# RUNNING
# ═══════════════════════════════════════════════════════════════════════════════

run: ## Run the bot
	@echo "🚀 Starting bot..."
	$(VENV)/bin/python -u bot.py

dev: ## Run in development mode with auto-reload
	@echo "🔧 Starting in development mode..."
	$(VENV)/bin/python -u bot.py --debug

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t $(DOCKER_IMAGE) .

docker-run: ## Run with Docker
	@echo "🐳 Starting Docker container..."
	docker run -d --name $(DOCKER_CONTAINER) --env-file .env \
		-v $(PWD)/database:/app/database \
		-v $(PWD)/cookies:/app/cookies \
		-v $(PWD)/logs:/app/logs \
		$(DOCKER_IMAGE)

docker-stop: ## Stop Docker container
	@echo "🐳 Stopping Docker container..."
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

docker-compose-up: ## Start with docker-compose
	@echo "🐳 Starting with docker-compose..."
	docker-compose up -d

docker-compose-down: ## Stop docker-compose
	@echo "🐳 Stopping docker-compose..."
	docker-compose down

docker-logs: ## View Docker logs
	docker logs -f $(DOCKER_CONTAINER)

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════════════════

clean: ## Clean temporary files
	@echo "🧹 Cleaning temporary files..."
	rm -rf temp/*
	rm -rf downloads/*
	rm -rf cache/*
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned!"

clean-all: clean ## Clean all generated files (including logs and database)
	@echo "🧹 Cleaning all files..."
	rm -rf logs/*
	rm -rf $(VENV)
	@echo "✅ Cleaned all!"

logs: ## View bot logs
	tail -f logs/bot.log

# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════════════════

lint: ## Run linter
	@echo "🔍 Running linter..."
	$(VENV)/bin/flake8 . --exclude=venv,__pycache__
	$(VENV)/bin/pylint *.py --disable=C0114,C0115,C0116

format: ## Format code
	@echo "✨ Formatting code..."
	$(VENV)/bin/black . --exclude=venv
	$(VENV)/bin/isort . --skip=venv

test: ## Run tests
	@echo "🧪 Running tests..."
	$(VENV)/bin/pytest tests/ -v

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

update-deps: ## Update dependencies
	@echo "📦 Updating dependencies..."
	$(VENV)/bin/pip install --upgrade -r requirements.txt

freeze: ## Freeze current dependencies
	@echo "📦 Freezing dependencies..."
	$(VENV)/bin/pip freeze > requirements.lock.txt

generate-key: ## Generate encryption key
	@$(PYTHON) -c "import secrets; import base64; print('ENCRYPTION_KEY=' + base64.b64encode(secrets.token_bytes(32)).decode())"

check-config: ## Validate configuration
	@echo "🔍 Checking configuration..."
	$(VENV)/bin/python -c "from config import load_config; load_config(); print('✅ Configuration is valid!')"