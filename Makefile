GIT_ROOT ?= $(shell git rev-parse --show-toplevel)
EXCLUDE_DIRS := portkey_ai/_vendor,venv
help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: format lint
format: ## Run code formatter: black
	black .
	ruff check . --fix --exclude $(EXCLUDE_DIRS)   
lint: ## Run linters: mypy, black, ruff
	mypy . --exclude portkey_ai/_vendor --exclude venv
	black . --check --exclude portkey_ai/_vendor --exclude venv
	ruff check . --exclude $(EXCLUDE_DIRS)
test: ## Run tests
	pytest tests
watch-docs: ## Build and watch documentation
	sphinx-autobuild docs/ docs/_build/html --open-browser --watch $(GIT_ROOT)/llama_index/

build:
	mypy . --exclude portkey_ai/_vendor --exclude venv
	black . --check --exclude portkey_ai/_vendor --exclude venv
	ruff check . --exclude $(EXCLUDE_DIRS)
	rm -rf dist/ build/
	python -m pip install build
	python -m build .

upload:
	python -m pip install twine
	python -m twine upload dist/portkey_ai-*
	rm -rf dist

dev: 
	pip install -e ".[dev]"