# Meal Planner

A FastAPI meal-planning app that generates daily or multi-day plans, supports recipe management, pantry-aware groceries, and keeps a small collection of restaurant-style meal entries and Indian curry recipes seeded into SQLite.

## Features

- FastAPI backend with server-rendered Jinja templates
- Random 1-day meal plans plus multi-day generation for 1, 3, and 7 days
- Dedicated weekly workspace at `/weekly` for generating and naming a 7-day plan
- Choose the start date for a weekly plan, with the date range restored when it is reopened
- Open any saved day from the weekly workspace in the main planner UI
- Drag meals between days, swap recipes within a meal slot, and build one weekly grocery list
- Meal rerolls and swap-candidate matching for a specific meal slot
- Search by recipe name or tag
- Recipe manager UI for creating, updating, favoriting, rating, and deleting meals
- Pantry inventory tracking with stock-aware grocery subtraction
- Aggregated, categorized grocery list export and WhatsApp text generation
- Saved plans support for later retrieval
- Light/dark mode with browser persistence
- SQLite + SQLAlchemy + Alembic based data layer
- Support for external image URLs and self-hosted images in the static assets folder
- Restaurant-style metadata such as prep/cook time, servings, ratings, and prep-step detail
- CI workflow for linting + tests on pull requests and pushes

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Jinja2
- Uvicorn
- uv
- pytest / black / flake8 / ruff / mypy / pre-commit

## Project Structure

```text
.
├── src/
│   └── meal_planner/
│       ├── main.py
│       ├── models/
│       │   └── meal.py
│       ├── routes/
│       │   ├── pantry.py
│       │   ├── plan.py
│       │   └── recipes.py
│       ├── services/
│       │   ├── grocery.py
│       │   └── meal_engine.py
│       ├── database/
│       │   ├── base.py
│       │   ├── session.py
│       │   └── seed.py
│       ├── static/
│       │   └── images/
│       └── templates/
│           ├── index.html
│           ├── manage_recipes.html
│           └── search.html
├── alembic/
│   ├── env.py
│   └── versions/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── uv.lock
├── README.md
├── tests/
│   └── test_generate_meal_plan.py
└── meal_planner.db
```

## Prerequisites

- Python 3.12+
- uv
- Docker + Docker Compose (optional)

## Local Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Apply database migrations:

   ```bash
   uv run alembic upgrade head
   ```

3. Run the app:

   ```bash
   uv run python -m uvicorn meal_planner.main:app --app-dir src --reload
   ```

4. Open the app:

- Home planner: http://localhost:8000
- Recipe manager: http://localhost:8000/recipes/manage
- Search: http://localhost:8000/search?q=chicken
- OpenAPI docs: http://localhost:8000/docs

## Useful Commands

```bash
make test
make lint
make typecheck
make precommit-run
make check
```

## Run With Docker

```bash
docker compose up --build
```

Then open http://localhost:8000.

## Database Migrations

Schema changes are managed with Alembic and should be reviewed before applying:

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

To roll back the most recent migration:

```bash
uv run alembic downgrade -1
```

## Recipe and Image Notes

Each meal can use either an external image URL or a file in `src/meal_planner/static/images/`.

1. Save a photo that matches the actual recipe.
2. Put it in `src/meal_planner/static/images/`.
3. Set the `image_url` in `src/meal_planner/database/seed.py` to the matching file path.
4. Restart the app so seed data is reloaded.

Recommended free-stock sources:

- Unsplash
- Pexels
- Pixabay

## Pantry and Grocery Flow

The pantry API stores stock levels and categories. The grocery generator subtracts pantry-owned items from the shopping list and creates a categorized export for the week or selected plan.

## CI

The repository includes a GitHub Actions workflow in `.github/workflows/ci.yml` that runs the same repo checks on pull requests and pushes to `main`/`master`:

- pre-commit hooks
- mypy / lint checks
- pytest suite

## How It Works

- On startup, the app seeds meals into SQLite if the DB is empty or missing enough seeded records.
- The planner selects breakfast, lunch, and dinner meals while de-prioritizing recent meals.
- Each meal can include core ingredients, family additions, and user alternatives.
- Grocery generation consolidates them by category and strips already-owned pantry items.
- `/recipes/manage` provides CRUD for recipe data and is the place to manage favorites, tags, and meal metadata.
- `/weekly` generates a named 7-day workspace plan; saving it lets users open any selected day in the main planner UI.
- Saved plans can also be stored and retrieved via the plan routes.

## Notes

- `meal_planner.db` is local state and not intended for version control.
- For production, use a persistent volume or move the app to a managed database.
