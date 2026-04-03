import json
import random
from pathlib import Path
from typing import Any, cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import Meal

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


def generate_meal_plan(db: Session) -> dict[str, dict[str, Any]]:
    def parse_json_list(payload: str) -> list[str]:
        parsed = json.loads(payload)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
        return []

    def pick_random(meal_type: str) -> dict[str, Any]:
        meals = db.query(Meal).filter(Meal.meal_type == meal_type).all()
        if not meals:
            return {
                "name": "No meal available",
                "description": "",
                "image_url": None,
                "ingredients": [],
                "instructions": [],
                "cooking_tips": "",
            }
        meal = random.choice(meals)
        meal_ingredients = cast(str, meal.ingredients)
        meal_instructions = cast(str, meal.instructions)
        return {
            "name": meal.name,
            "description": meal.description,
            "image_url": meal.image_url,
            "ingredients": parse_json_list(meal_ingredients),
            "instructions": parse_json_list(meal_instructions),
            "cooking_tips": meal.cooking_tips or "",
        }

    return {
        "breakfast": pick_random("breakfast"),
        "lunch": pick_random("lunch"),
        "dinner": pick_random("dinner"),
    }


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    plan = generate_meal_plan(db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "plan": plan},
    )


@router.get("/plan")
def get_plan(db: Session = Depends(get_db)):
    return generate_meal_plan(db)
