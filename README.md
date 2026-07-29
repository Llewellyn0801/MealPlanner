# Meal Planner

A FastAPI app that generates a random daily meal plan (breakfast, lunch, and dinner) from a seeded SQLite database, with a modular "core base / family side / user alternative" structure for each meal and an aggregated grocery list.

## Features

- FastAPI backend with server-rendered HTML
- Random meal plan generation with 48-hour repeat avoidance
- Reroll individual meals without regenerating the whole plan
- Search meals by name or tag
- Aggregated, categorized grocery list generation
- Light/dark mode with system-preference detection and persistence
- SQLite + SQLAlchemy data layer
- Alembic-managed schema migrations
- Self-hosted image support (in addition to external URLs)
- Docker support

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Jinja2 templates
- Uvicorn
- uv

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
│       ├── services/
│       │   ├── meal_engine.py
│       │   └── grocery.py
│       ├── database/
│       │   ├── session.py
│       │   ├── base.py
│       │   └── seed.py
│       ├── static/
│       │   └── images/        # place self-hosted meal photos here
│       └── templates/
│           ├── index.html
│           └── search.html
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prerequisites

- Python 3.12+
- uv
- (Optional) Docker + Docker Compose

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

4. Open in your browser:

- App UI: [http://localhost:8000](http://localhost:8000)
- Search: [http://localhost:8000/search?q=chicken](http://localhost:8000/search?q=chicken)
- JSON endpoint: [http://localhost:8000/plan](http://localhost:8000/plan)
- OpenAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Run With Docker

```bash
docker compose up --build
```

Then open [http://localhost:8000](http://localhost:8000). The container runs `alembic upgrade head` automatically before starting the server.

## Database Migrations

Schema changes are managed with Alembic — the app no longer creates or alters tables on startup.

Whenever you change a model in `src/meal_planner/models/`:

```bash
uv run alembic revision --autogenerate -m "describe the change"
# review the generated file in alembic/versions/ before applying
uv run alembic upgrade head
```

To roll back the most recent migration: `uv run alembic downgrade -1`

## Meal Images

Each meal can use either an external `image_url` (e.g. a hotlinked Unsplash photo) or a self-hosted image:

1. Download a photo that actually matches the meal (see recommended sources below)
2. Save it to `src/meal_planner/static/images/`
3. Set that meal's `image_url` in `src/meal_planner/database/seed.py` to `/static/images/your-file.jpg`
4. Delete `meal_planner.db` and restart so the seed data reloads

**Recommended free-stock sources** (search for the specific dish, don't grab generic "healthy food" shots):
- [Unsplash](https://unsplash.com)
- [Pexels](https://www.pexels.com)
- [Pixabay](https://pixabay.com)

Avoid pulling images from recipe blogs or general image search — those are typically copyrighted and not reliably hotlinkable.

## Dark Mode

Toggle via the 🌙/☀️ button in the header on both the home and search pages. The choice is saved in the browser (`localStorage`) and defaults to your OS-level light/dark preference on first visit.

## How It Works

- On startup, the app seeds meals into the database if none exist (idempotent — safe to restart repeatedly).
- The root route (`/`) renders a random meal plan in `src/meal_planner/templates/index.html`, structured into a shared core base, a family-only side, and a user-only alternative per meal.
- **Generate New Daily Plan** calls `/plan` for a fresh plan; recently-served meals (last 48h) are deprioritized to reduce repeats.
- **Next** on an individual meal card calls `/reroll-meal` to swap just that meal.
- **Generate Aggregated Grocery List** calls `/grocery-list`, which categorizes and deduplicates ingredients across all three meals.
- `/search?q=...` finds meals by name or tag.

## Notes

- The database file is stored locally as `meal_planner.db` and is not committed to version control.
- For production, mount a persistent volume for `meal_planner.db` (or move to Postgres) so meal history survives container restarts — see the Docker/production notes in project discussions for details.
