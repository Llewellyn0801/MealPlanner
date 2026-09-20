import json
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
from meal_planner.services.images import (
    STATIC_IMAGES_DIR,
    is_available_local_image,
    safe_image_filename,
)
from meal_planner.services.meal_engine import format_meal, parse_ingredient_measurement

router = APIRouter(prefix="/recipes")


@router.get("/image-audit")
def image_audit(db: Session = Depends(get_db)):
    missing = []
    for meal in db.query(Meal).all():
        image_url = meal.image_url or ""
        if image_url.startswith("/static/images/") and not is_available_local_image(
            image_url
        ):
            missing.append({"id": meal.id, "name": meal.name, "image_url": image_url})
    return {"missing": missing, "missing_count": len(missing)}


templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)


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


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == recipe_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe = format_meal(meal)
    recipe["meal_type"] = meal.meal_type
    return recipe


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
    nutrition_basis: str = Form("per_serving"),
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
    image_url = None

    if image_file and image_file.filename:
        try:
            filename = safe_image_filename(image_file.filename)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        save_path = STATIC_IMAGES_DIR / filename
        STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        image_url = f"/static/images/{filename}"
    elif image_url_input and image_url_input.strip():
        image_url = image_url_input.strip()
        if not is_available_local_image(image_url):
            raise HTTPException(status_code=400, detail="Local image does not exist")

    ingredients = [i.strip() for i in ingredients_raw.split("\n") if i.strip()]
    instructions = [i.strip() for i in instructions_raw.split("\n") if i.strip()]
    prep_detail_steps = [
        {"step": idx, "title": f"Step {idx}", "detail": instruction}
        for idx, instruction in enumerate(instructions, start=1)
    ]

    core_base = [
        {
            **parse_ingredient_measurement(ingredient),
            "category": "Pantry/Grains",
        }
        for ingredient in ingredients
    ]

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
        nutrition_basis=nutrition_basis.strip(),
        prep_time_mins=prep_time_mins,
        cook_time_mins=cook_time_mins,
        servings_default=servings_default,
        tags=tags.strip(),
        ingredients=json.dumps(ingredients),
        instructions=json.dumps(instructions),
        prep_detail_steps=json.dumps(prep_detail_steps),
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
    nutrition_basis: str = Form("per_serving"),
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
    meal.nutrition_basis = nutrition_basis.strip()
    meal.prep_time_mins = prep_time_mins
    meal.cook_time_mins = cook_time_mins
    meal.servings_default = servings_default
    meal.tags = tags.strip()
    meal.cooking_tips = cooking_tips.strip()

    if image_file and image_file.filename:
        try:
            filename = safe_image_filename(image_file.filename)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        save_path = STATIC_IMAGES_DIR / filename
        STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        meal.image_url = f"/static/images/{filename}"
    elif image_url_input and image_url_input.strip():
        meal.image_url = image_url_input.strip()
        if not is_available_local_image(meal.image_url):
            raise HTTPException(status_code=400, detail="Local image does not exist")

    ingredients = [i.strip() for i in ingredients_raw.split("\n") if i.strip()]
    instructions = [i.strip() for i in instructions_raw.split("\n") if i.strip()]
    prep_detail_steps = [
        {"step": idx, "title": f"Step {idx}", "detail": instruction}
        for idx, instruction in enumerate(instructions, start=1)
    ]
    meal.ingredients = json.dumps(ingredients)
    meal.instructions = json.dumps(instructions)
    meal.prep_detail_steps = json.dumps(prep_detail_steps)
    meal.core_base = json.dumps(
        [
            {
                **parse_ingredient_measurement(ingredient),
                "category": "Pantry/Grains",
            }
            for ingredient in ingredients
        ]
    )

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
