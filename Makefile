PYTHON ?= python3
POETRY ?= poetry

.PHONY: install dev test docker-up docker-down format lint typecheck check precommit-install precommit-run

install:
	$(POETRY) install

dev:
	$(POETRY) run $(PYTHON) -m uvicorn meal_planner.main:app --app-dir src --reload

test:
	$(POETRY) run pytest

docker-up:
	docker compose up --build

docker-down:
	docker compose down

format:
	$(POETRY) run black src tests

lint:
	$(POETRY) run ruff check src tests --fix
	$(POETRY) run flake8 src tests --max-line-length=88 --extend-ignore=E203,W503

typecheck:
	$(POETRY) run mypy src --ignore-missing-imports

check: lint typecheck test

precommit-install:
	$(POETRY) run pre-commit install

precommit-run:
	$(POETRY) run pre-commit run --all-files
