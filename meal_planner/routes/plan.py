import random

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.session import get_db
from models.meal import Meal


router = APIRouter()
templates = Jinja2Templates(directory="templates")


def generate_meal_plan(db: Session) -> dict[str, str]:
    def pick_random(meal_type: str) -> str:
        meals = db.query(Meal).filter(Meal.meal_type == meal_type).all()
        if not meals:
            return "No meal available"
        return random.choice(meals).name

    return {
        "breakfast": pick_random("breakfast"),
        "lunch": pick_random("lunch"),
        "dinner": pick_random("dinner"),
    }


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    plan = generate_meal_plan(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "plan": plan},
    )


@router.get("/plan")
def get_plan(db: Session = Depends(get_db)):
    return generate_meal_plan(db)
