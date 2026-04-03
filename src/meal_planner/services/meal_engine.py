import json
import random
from typing import Any, cast

from sqlalchemy.orm import Session

from meal_planner.models.meal import Meal


def parse_json_list(payload: str) -> list[str]:
    try:
        parsed = json.loads(payload)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except Exception:
        pass
    return []


def get_base_words(ingredients: list[str]) -> set[str]:
    """
    Extract standard base words ignoring common units and numbers
    to match shared ingredients.
    """
    stop_words = {
        "cup",
        "cups",
        "tsp",
        "tbsp",
        "g",
        "ml",
        "large",
        "small",
        "of",
        "and",
        "pinch",
        "clove",
        "can",
        "in",
        "diced",
        "chopped",
        "sliced",
        "minced",
        "grated",
        "peeled",
        "water",
        "salt",
        "pepper",
        "oil",
    }
    words = set()
    for item in ingredients:
        for word in item.lower().replace(",", "").replace(".", "").split():
            # ignore anything with digits (like '200g' or '1/2')
            if word.isnumeric() or any(char.isdigit() for char in word):
                continue
            if word not in stop_words and len(word) > 2:
                words.add(word)
    return words


def format_meal(meal: Meal | None) -> dict[str, Any]:
    if not meal:
        return {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
        }

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


def generate_meal_plan(db: Session) -> dict[str, dict[str, Any]]:
    # 1. Select Dinner (difficulty=full)
    dinners = (
        db.query(Meal)
        .filter(Meal.meal_type == "dinner", Meal.difficulty == "full")
        .all()
    )
    if not dinners:
        dinners = db.query(Meal).filter(Meal.meal_type == "dinner").all()

    dinner = random.choice(dinners) if dinners else None
    dinner_dict = format_meal(dinner)
    dinner_words = get_base_words(dinner_dict.get("ingredients", []))

    # 2. Select optimized breakfast/lunch
    def pick_optimized_simple_meal(meal_type: str) -> dict[str, Any]:
        candidates = (
            db.query(Meal)
            .filter(Meal.meal_type == meal_type, Meal.difficulty == "simple")
            .all()
        )
        if not candidates:
            candidates = db.query(Meal).filter(Meal.meal_type == meal_type).all()

        if not candidates:
            return format_meal(None)

        matching_candidates = []
        for c in candidates:
            c_dict = format_meal(c)
            c_words = get_base_words(c_dict["ingredients"])
            if dinner_words.intersection(c_words):
                matching_candidates.append(c)

        # Fallback to random candidate if no matches
        if not matching_candidates:
            matching_candidates = candidates

        return format_meal(random.choice(matching_candidates))

    return {
        "breakfast": pick_optimized_simple_meal("breakfast"),
        "lunch": pick_optimized_simple_meal("lunch"),
        "dinner": dinner_dict,
    }
