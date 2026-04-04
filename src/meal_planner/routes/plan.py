from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import Meal
from meal_planner.services.grocery import generate_grocery_list
from meal_planner.services.meal_engine import format_meal, generate_meal_plan

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    plan = generate_meal_plan(db)
    grocery_list = generate_grocery_list(plan)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "plan": plan,
            "grocery_list": grocery_list["grocery_list"],
        },
    )


@router.get("/plan")
def get_plan(db: Session = Depends(get_db)):
    return generate_meal_plan(db)


@router.post("/grocery-list")
def create_grocery_list(plan_data: dict[str, Any] = Body(...)):
    return generate_grocery_list(plan_data)


@router.post("/reroll-meal")
def reroll_meal(
    current_plan: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    meal_type_to_reroll = current_plan["meal_type"]
    existing_meal_names = [
        meal["name"] for meal in current_plan["meals"].values() if meal
    ]

    # A simple way to get a new meal: find one that isn't in the current plan
    new_meal = (
        db.query(Meal)
        .filter(
            Meal.meal_type == meal_type_to_reroll,
            Meal.name.notin_(existing_meal_names),
        )
        .first()
    )

    # Fallback: if no new meal is found, just get any meal of that type
    if not new_meal:
        new_meal = db.query(Meal).filter(Meal.meal_type == meal_type_to_reroll).first()

    return format_meal(new_meal)
