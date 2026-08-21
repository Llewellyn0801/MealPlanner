import json
import os
import shutil
from pathlib import Path
from typing import Any

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import Meal
from meal_planner.services.meal_engine import format_meal

router = APIRouter(prefix="/recipes")
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)
STATIC_IMAGES_DIR = Path(__file__).resolve().parents[1] / "static" / "images"


@router.get("/manage", response_class=HTMLResponse)
def manage_recipes(
    request: Request,
    q: str | None = None,
    meal_type: str | None = None,
    favorite_only: bool = False,
    db: Session = Depends(get_db),
):
    query = db.query(Meal)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(Meal.name.ilike(term), Meal.tags.ilike(term)))
    if meal_type and meal_type.strip() and meal_type != "all":
        query = query.filter(Meal.meal_type == meal_type.strip())
    if favorite_only:
        query = query.filter(Meal.is_favorite == True)  # noqa: E712

    meals = query.all()
    formatted_meals = [format_meal(m) for m in meals]

    return templates.TemplateResponse(
        request=request,
        name="manage_recipes.html",
        context={
            "request": request,
            "recipes": formatted_meals,
            "query": q or "",
            "selected_meal_type": meal_type or "all",
            "favorite_only": favorite_only,
        },
    )


@router.post("/create")
def create_recipe(
    name: str = Form(...),
    meal_type: str = Form(...),
    difficulty: str = Form("simple"),
    description: str = Form(""),
    calories: int = Form(0),
    protein_g: int = Form(0),
    carbs_g: int = Form(0),
    fats_g: int = Form(0),
    prep_time_mins: int = Form(10),
    cook_time_mins: int = Form(15),
    servings_default: int = Form(4),
    tags: str = Form(""),
    ingredients_raw: str = Form(""),
    instructions_raw: str = Form(""),
    cooking_tips: str = Form(""),
    image_url_input: str | None = Form(None),
    image_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = "/static/images/greek-yogurt-berry-&-chia-bowl.png"

    if image_file and image_file.filename:
        filename = image_file.filename.replace(" ", "-").lower()
        save_path = STATIC_IMAGES_DIR / filename
        os.makedirs(STATIC_IMAGES_DIR, exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        image_url = f"/static/images/{filename}"
    elif image_url_input and image_url_input.strip():
        image_url = image_url_input.strip()

    ingredients = [i.strip() for i in ingredients_raw.split("\n") if i.strip()]
    instructions = [i.strip() for i in instructions_raw.split("\n") if i.strip()]

    core_base = [{"name": ing, "category": "Pantry/Grains"} for ing in ingredients]

    new_meal = Meal(
        name=name.strip(),
        meal_type=meal_type.strip(),
        difficulty=difficulty.strip(),
        description=description.strip(),
        image_url=image_url,
        calories=calories,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fats_g=fats_g,
        prep_time_mins=prep_time_mins,
        cook_time_mins=cook_time_mins,
        servings_default=servings_default,
        tags=tags.strip(),
        ingredients=json.dumps(ingredients),
        instructions=json.dumps(instructions),
        core_base=json.dumps(core_base),
        family_additions=json.dumps([]),
        user_alternatives=json.dumps([]),
        cooking_tips=cooking_tips.strip(),
    )

    db.add(new_meal)
    db.commit()
    return RedirectResponse(url="/recipes/manage", status_code=303)


@router.post("/{recipe_id}/update")
def update_recipe(
    recipe_id: int,
    name: str = Form(...),
    meal_type: str = Form(...),
    difficulty: str = Form("simple"),
    description: str = Form(""),
    calories: int = Form(0),
    protein_g: int = Form(0),
    carbs_g: int = Form(0),
    fats_g: int = Form(0),
    prep_time_mins: int = Form(10),
    cook_time_mins: int = Form(15),
    servings_default: int = Form(4),
    tags: str = Form(""),
    ingredients_raw: str = Form(""),
    instructions_raw: str = Form(""),
    cooking_tips: str = Form(""),
    image_url_input: str | None = Form(None),
    db: Session = Depends(get_db),
):
    meal = db.query(Meal).filter(Meal.id == recipe_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Recipe not found")

    meal.name = name.strip()
    meal.meal_type = meal_type.strip()
    meal.difficulty = difficulty.strip()
    meal.description = description.strip()
    meal.calories = calories
    meal.protein_g = protein_g
    meal.carbs_g = carbs_g
    meal.fats_g = fats_g
    meal.prep_time_mins = prep_time_mins
    meal.cook_time_mins = cook_time_mins
    meal.servings_default = servings_default
    meal.tags = tags.strip()
    meal.cooking_tips = cooking_tips.strip()

    if image_url_input and image_url_input.strip():
        meal.image_url = image_url_input.strip()

    ingredients = [i.strip() for i in ingredients_raw.split("\n") if i.strip()]
    instructions = [i.strip() for i in instructions_raw.split("\n") if i.strip()]
    meal.ingredients = json.dumps(ingredients)
    meal.instructions = json.dumps(instructions)
    meal.core_base = json.dumps([{"name": ing, "category": "Pantry/Grains"} for ing in ingredients])

    db.commit()
    return RedirectResponse(url="/recipes/manage", status_code=303)


@router.post("/{recipe_id}/delete")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == recipe_id).first()
    if meal:
        db.delete(meal)
        db.commit()
    return RedirectResponse(url="/recipes/manage", status_code=303)


@router.post("/{recipe_id}/favorite")
def toggle_favorite(recipe_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == recipe_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Recipe not found")
    meal.is_favorite = not meal.is_favorite
    db.commit()
    return {"id": meal.id, "is_favorite": meal.is_favorite}


@router.post("/{recipe_id}/rate")
def rate_recipe(
    recipe_id: int, payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    stars = float(payload.get("rating", 5.0))
    meal = db.query(Meal).filter(Meal.id == recipe_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Recipe not found")

    current_rating = meal.rating or 0.0
    count = meal.ratings_count or 0

    new_count = count + 1
    new_rating = round(((current_rating * count) + stars) / new_count, 1)

    meal.rating = new_rating
    meal.ratings_count = new_count
    db.commit()

    return {"id": meal.id, "rating": meal.rating, "ratings_count": meal.ratings_count}
