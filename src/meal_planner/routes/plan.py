from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
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

    new_meal = (
        db.query(Meal)
        .filter(
            Meal.meal_type == meal_type_to_reroll,
            Meal.name.notin_(existing_meal_names),
        )
        .first()
    )

    if not new_meal:
        new_meal = db.query(Meal).filter(Meal.meal_type == meal_type_to_reroll).first()

    return format_meal(new_meal)


@router.get("/search", response_class=HTMLResponse)
def search_meals(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    if not q or not q.strip():
        return RedirectResponse(url="/")

    search_results = (
        db.query(Meal)
        .filter(or_(Meal.name.ilike(f"%{q}%"), Meal.tags.ilike(f"%{q}%")))
        .all()
    )

    formatted_results = [format_meal(meal) for meal in search_results]

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={"request": request, "results": formatted_results, "query": q},
    )
