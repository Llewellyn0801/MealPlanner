from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from meal_planner.database.seed import seed_meals
from meal_planner.database.session import SessionLocal
from meal_planner.routes.pantry import router as pantry_router
from meal_planner.routes.plan import router as plan_router
from meal_planner.routes.profile import get_or_create_default_household
from meal_planner.routes.profile import router as profile_router
from meal_planner.routes.recipes import router as recipes_router

app = FastAPI(title="Meal Planner")
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(plan_router)
app.include_router(recipes_router)
app.include_router(pantry_router)
app.include_router(profile_router)


@app.get("/health")
def health_check() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.on_event("startup")
def on_startup() -> None:
    seed_meals()
    db = SessionLocal()
    try:
        get_or_create_default_household(db)
    finally:
        db.close()
