# Makefile para facilitar o desenvolvimento local do Serviço de IA.

PYTHON = python

.DEFAULT_GOAL := help

# --- Comandos Principais ---

.PHONY: help setup install venv run clean
help: ## Mostra esta mensagem de ajuda com todos os comandos disponíveis.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: install ## (Comando principal) Prepara o ambiente completo do serviço de IA.
	@echo "\nAmbiente do Serviço de IA pronto!"
	@echo "Use 'make run' para iniciar o worker."

venv: ## Cria o ambiente virtual, se não existir.
	@if [ ! -d "venv" ]; then \
		echo "Criando ambiente virtual para o Serviço de IA..."; \
		$(PYTHON) -m venv venv; \
	else \
		echo "Ambiente virtual já existe."; \
	fi

install: venv ## Instala as dependências Python para o serviço de IA.
	@echo "Instalando dependências do Serviço de IA..."
	@. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run: ## Inicia o worker do serviço de IA.
	@echo "Iniciando o worker do Serviço de IA..."
	@. venv/bin/activate && $(PYTHON) -m src

clean: ## Remove o ambiente virtual e arquivos de cache.
	@echo "Limpando ambiente virtual e arquivos de cache do Serviço de IA..."
	@rm -rf venv
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Limpeza concluída."

.PHONY: freeze
freeze: venv ## Atualiza o requirements.txt com as dependências do ambiente virtual.
	@echo "Gerando requirements.txt para o Serviço de IA..."
	@. venv/bin/activate && pip freeze > requirements.txt