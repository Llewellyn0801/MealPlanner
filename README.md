# Meal Planner

A simple FastAPI app that generates a random daily meal plan (breakfast, lunch, and dinner) from a seeded SQLite database.

## Features

- FastAPI backend with server-rendered HTML
- Random meal plan generation
- `/plan` JSON endpoint for fetching a fresh plan
- SQLite + SQLAlchemy data layer
- Automatic database table creation and seed data on startup
- Docker support

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Jinja2 templates
- Uvicorn
- Poetry

## Project Structure

```
.
├── src/
│   └── meal_planner/
│       ├── main.py
│       ├── routes/
│       │   └── plan.py
│       ├── models/
│       │   └── meal.py
│       ├── database/
│       │   ├── session.py
│       │   ├── base.py
│       │   └── seed.py
│       └── templates/
│           └── index.html
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Prerequisites

- Python 3.12+
- Poetry
- (Optional) Docker + Docker Compose

## Local Setup

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Run the app:

   ```bash
   poetry run python -m uvicorn meal_planner.main:app --app-dir src --reload
   ```

3. Open in your browser:

- App UI: [http://localhost:8000](http://localhost:8000)
- JSON endpoint: [http://localhost:8000/plan](http://localhost:8000/plan)
- OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Run With Docker

```bash
docker compose up --build
```

Then open [http://localhost:8000](http://localhost:8000).

## How It Works

- On startup, the app creates database tables and seeds meals if the database is empty.
- The root route (`/`) renders the current random meal plan in `src/meal_planner/templates/index.html`.
- Clicking **Generate New Plan** calls `/plan` and refreshes breakfast/lunch/dinner in the page.

## Notes

- The database file is stored locally as `meal_planner.db`.
- Seeding is idempotent and only runs when there are no existing meals.
