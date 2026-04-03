from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.services.grocery import generate_grocery_list
from meal_planner.services.meal_engine import generate_meal_plan

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


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


@router.post("/grocery-list")
def create_grocery_list(plan_data: dict[str, Any] = Body(...)):
    return generate_grocery_list(plan_data)
