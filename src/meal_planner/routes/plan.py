import json
import random
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import Meal, SavedPlan
from meal_planner.services.grocery import generate_grocery_list
from meal_planner.services.meal_engine import (
    _meal_contains_dislikes,
    calculate_multi_day_macros,
    calculate_total_macros,
    format_meal,
    generate_meal_plan,
    generate_multi_day_plan,
    get_swap_candidates,
)

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    dislikes: str | None = None,
    likes: str | None = None,
    q: str | None = None,
    saved_plan_id: int | None = None,
    day: str = "Day 1",
    db: Session = Depends(get_db),
):
    dislikes_list = (
        [d.strip() for d in dislikes.split(",") if d.strip()] if dislikes else []
    )
    likes_list = (
        [item.strip() for item in likes.split(",") if item.strip()] if likes else []
    )

    saved_plan = None
    if saved_plan_id is not None:
        saved_plan = db.query(SavedPlan).filter(SavedPlan.id == saved_plan_id).first()

    if saved_plan:
        saved_plan_data = json.loads(saved_plan.plan_json)
        if isinstance(saved_plan_data.get("plan"), dict):
            saved_plan_data = saved_plan_data["plan"]
        plan = saved_plan_data.get(day, saved_plan_data.get("Day 1", {}))
    else:
        plan = generate_meal_plan(db, dislikes=dislikes_list, likes=likes_list)
    total_macros = calculate_total_macros(plan)
    grocery_data = generate_grocery_list(plan)
    search_query = q.strip() if q else ""
    search_results: list[dict[str, Any]] = []
    if search_query:
        term = f"%{search_query}%"
        for meal in (
            db.query(Meal)
            .filter(
                or_(
                    Meal.name.ilike(term),
                    Meal.tags.ilike(term),
                    Meal.description.ilike(term),
                    Meal.ingredients.ilike(term),
                )
            )
            .all()
        ):
            result = format_meal(meal)
            result["meal_type"] = meal.meal_type
            search_results.append(result)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "plan": plan,
            "total_macros": total_macros,
            "grocery_data": grocery_data,
            "dislikes": dislikes or "",
            "likes": likes or "",
            "search_query": search_query,
            "search_results": search_results,
            "saved_plan_id": saved_plan_id if saved_plan else None,
            "selected_day": day if saved_plan else None,
        },
    )


@router.get("/weekly", response_class=HTMLResponse)
def weekly_workspace(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="weekly.html",
        context={"request": request},
    )


@router.post("/plan")
def get_plan(payload: dict[str, Any] = Body(default={}), db: Session = Depends(get_db)):
    dislikes_raw = payload.get("dislikes", [])
    likes_raw = payload.get("likes", [])
    days = int(payload.get("days", 1))
    dietary_preset = payload.get("dietary_preset") or None

    if isinstance(dislikes_raw, str):
        dislikes_list = [d.strip() for d in dislikes_raw.split(",") if d.strip()]
    else:
        dislikes_list = [str(d).strip() for d in dislikes_raw if str(d).strip()]

    if isinstance(likes_raw, str):
        likes_list = [item.strip() for item in likes_raw.split(",") if item.strip()]
    else:
        likes_list = [str(item).strip() for item in likes_raw if str(item).strip()]

    if days > 1:
        plan = generate_multi_day_plan(
            db,
            days=days,
            dislikes=dislikes_list,
            likes=likes_list,
            dietary_preset=dietary_preset,
        )
        macros = calculate_multi_day_macros(plan)
        return {
            "plan": plan,
            "total_macros": macros["average"],
            "multi_day_macros": macros,
            "days": days,
        }
    else:
        plan = generate_meal_plan(
            db,
            dislikes=dislikes_list,
            likes=likes_list,
            dietary_preset=dietary_preset,
        )
        total_macros = calculate_total_macros(plan)
        return {"plan": plan, "total_macros": total_macros, "days": 1}


@router.post("/grocery-list")
def create_grocery_list(plan_data: dict[str, Any] = Body(...)):
    raw_plan = plan_data.get("plan", plan_data)
    in_stock = plan_data.get("in_stock_pantry", [])
    res = generate_grocery_list(raw_plan, in_stock_pantry=in_stock)
    return res


@router.post("/reroll-meal")
def reroll_meal(
    current_plan: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    meal_type_to_reroll = current_plan.get("meal_type")
    dislikes_raw = current_plan.get("dislikes", [])
    if isinstance(dislikes_raw, str):
        dislikes = [d.strip() for d in dislikes_raw.split(",") if d.strip()]
    else:
        dislikes = [str(d).strip() for d in dislikes_raw if str(d).strip()]

    meals_dict = current_plan.get("meals", {})
    existing_meal_names = [
        meal["name"]
        for meal in meals_dict.values()
        if isinstance(meal, dict) and "name" in meal
    ]

    all_type_meals = db.query(Meal).filter(Meal.meal_type == meal_type_to_reroll).all()

    candidates = [m for m in all_type_meals if m.name not in existing_meal_names]
    if not candidates:
        candidates = all_type_meals

    if dislikes:
        non_disliked = [
            m for m in candidates if not _meal_contains_dislikes(m, dislikes)
        ]
        if non_disliked:
            candidates = non_disliked

    new_meal = (
        random.choice(candidates)
        if candidates
        else (all_type_meals[0] if all_type_meals else None)
    )
    return format_meal(new_meal)


@router.post("/swap-candidates")
def swap_candidates(payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    meal_type = payload.get("meal_type", "")
    current_names = payload.get("current_meal_names", [])
    dislikes_raw = payload.get("dislikes", [])
    if isinstance(dislikes_raw, str):
        dislikes = [d.strip() for d in dislikes_raw.split(",") if d.strip()]
    else:
        dislikes = [str(d).strip() for d in dislikes_raw if str(d).strip()]

    candidates = get_swap_candidates(db, meal_type, current_names, dislikes)
    return {"candidates": candidates}


@router.post("/plan/save")
def save_plan(payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    name = str(payload.get("name", "My Plan")).strip()
    plan = payload.get("plan", {})
    metadata = payload.get("metadata")
    saved_payload: Any = plan
    if isinstance(metadata, dict):
        saved_payload = {"plan": plan, "metadata": metadata}
    saved = SavedPlan(name=name, plan_json=json.dumps(saved_payload))
    db.add(saved)
    db.commit()
    return {"id": saved.id, "name": saved.name}


@router.get("/plan/saved")
def list_saved_plans(db: Session = Depends(get_db)):
    plans = db.query(SavedPlan).order_by(SavedPlan.created_at.desc()).all()
    return [
        {"id": p.id, "name": p.name, "created_at": str(p.created_at)} for p in plans
    ]


@router.get("/plan/saved/{plan_id}")
def load_saved_plan(plan_id: int, db: Session = Depends(get_db)):
    p = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"id": p.id, "name": p.name, "plan": json.loads(p.plan_json)}


@router.delete("/plan/saved/{plan_id}")
def delete_saved_plan(plan_id: int, db: Session = Depends(get_db)):
    p = db.query(SavedPlan).filter(SavedPlan.id == plan_id).first()
    if p:
        db.delete(p)
        db.commit()
    return {"success": True}


@router.get("/search", response_class=HTMLResponse)
def search_meals(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    if not q or not q.strip():
        return RedirectResponse(url="/")

    return RedirectResponse(url=f"/?q={quote(q.strip())}", status_code=303)
