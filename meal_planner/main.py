from fastapi import FastAPI

from database.base import Base
from database.seed import seed_meals
from database.session import engine
from routes.plan import router as plan_router


app = FastAPI(title="Meal Planner")

app.include_router(plan_router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    seed_meals()
