from fastapi import FastAPI

from meal_planner.database.base import Base
from meal_planner.database.seed import seed_meals
from meal_planner.database.session import engine
from meal_planner.routes.plan import router as plan_router

app = FastAPI(title="Meal Planner")

app.include_router(plan_router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    seed_meals()
