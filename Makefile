PYTHON = uv run python
ARGS ?= --help

install:
	@uv sync

install-vllm:
	@mkdir -p data/raw && wget -O /tmp/vllm.zip "https://github.com/69Nesta/42-RAG-Against-The-Machine/raw/refs/heads/main/vllm-0.10.1.zip" && unzip -o /tmp/vllm.zip -d data/raw/

run:
	@$(PYTHON) -m src $(ARGS)

debug:
	@$(PYTHON) -m pdb -m src $(ARGS)

clean:
	@find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -not -path "./.venv/*" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -not -path "./.venv/*" -exec rm -rf {} +

lint:
	@uv run flake8 --exclude=.venv,data/raw/vllm-0.10.1 .
	@uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --exclude 'data/raw' --exclude '.venv' --disable-error-code=attr-defined --disable-error-code=no-untyped-def --disable-error-code=no-any-return --disable-error-code=arg-type --disable-error-code=misc --disable-error-code=assignment --disable-error-code=var-annotated

.PHONY: install run debug clean lint