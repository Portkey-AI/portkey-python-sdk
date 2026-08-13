GIT_ROOT ?= $(shell git rev-parse --show-toplevel)
help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: format lint hooks
# Same scope as mypy's `files` in pyproject.toml. Passing `.` would also pick up
# untracked scratch files in the repo root, so `make lint` would fail locally
# while CI passes on the identical commit.
LINT_PATHS = portkey_ai examples

format: ## Run code formatter: ruff
	ruff check $(LINT_PATHS) --fix
	ruff format $(LINT_PATHS)
lint: ## Run linters: mypy, ruff
	mypy
	ruff format $(LINT_PATHS) --check
	ruff check $(LINT_PATHS)
hooks: ## Install the git pre-commit hooks (run once per clone)
	pre-commit install
	pre-commit run --all-files
test: ## Run tests
	pytest tests
watch-docs: ## Build and watch documentation
	sphinx-autobuild docs/ docs/_build/html --open-browser --watch $(GIT_ROOT)/llama_index/

build:
	mypy
	ruff format $(LINT_PATHS) --check
	ruff check $(LINT_PATHS)
	rm -rf dist/ build/
	python -m pip install build
	python -m build .

upload:
	python -m pip install twine
	python -m twine upload dist/portkey_ai-*
	rm -rf dist

sandbox:
	python -m pip install twine
	python -m twine upload --repository testpypi dist/portkey_ai-*
	rm -rf dist

dev:
	pip install -e ".[dev]"

langchain_callback:
	pip install -e ".[langchain_callback]"

llama_index_callback:
	pip install -e ".[llama_index_callback]"

instrumentation:
	pip install -e ".[instrumentation]"
