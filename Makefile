PYTHON ?= python3
UV ?= uv

.PHONY: install dev test docker-up docker-down format lint typecheck check precommit-install precommit-run

install:
	$(UV) sync

dev:
	$(UV) run $(PYTHON) -m uvicorn meal_planner.main:app --app-dir src --reload

test:
	$(UV) run pytest

docker-up:
	docker compose up --build

docker-down:
	docker compose down

format:
	$(UV) run black src tests

lint:
	$(UV) run ruff check src tests --fix
	$(UV) run flake8 src tests --max-line-length=88 --extend-ignore=E203,W503,E501

typecheck:
	$(UV) run mypy src --ignore-missing-imports

check: lint typecheck test

precommit-install:
	$(UV) run pre-commit install

precommit-run:
	$(UV) run pre-commit run --all-files
