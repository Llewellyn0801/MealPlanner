import json
import random
from typing import Any, cast

from sqlalchemy.orm import Session

from meal_planner.models.meal import Meal, MealHistory


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
        "cup", "cups", "tsp", "tbsp", "g", "ml", "large", "small",
        "of", "and", "pinch", "clove", "can", "in", "diced", "chopped",
        "sliced", "minced", "grated", "peeled", "water", "salt", "pepper", "oil",
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
    # Get all recent meals to avoid repetition (e.g. last 15 inserted)
    recent_history = (
        db.query(MealHistory)
        .order_by(MealHistory.created_at.desc())
        .limit(15)
        .all()
    )
    recent_meal_names = {h.meal_name for h in recent_history}

    def pick_meal(
        meal_type: str, difficulty: str, dinner_words: set[str] | None = None
    ) -> tuple[dict[str, Any], set[str]]:
        candidates = (
            db.query(Meal)
            .filter(Meal.meal_type == meal_type, Meal.difficulty == difficulty)
            .all()
        )
        if not candidates:
            candidates = db.query(Meal).filter(Meal.meal_type == meal_type).all()

        if not candidates:
            return format_meal(None), set()

        # 1. Prefer health tags and no memory
        unseen_matching = [
            c for c in candidates
            if c.name not in recent_meal_names
            and ("low_carb" in c.tags or "heart_healthy" in c.tags)
        ]

        # 2. Fallbacks
        unseen = [c for c in candidates if c.name not in recent_meal_names]

        # Determine base selection list
        if unseen_matching:
            selection_pool = unseen_matching
        elif unseen:
            selection_pool = unseen
        else:
            selection_pool = candidates

        # Try to match ingredients if we have dinner words
        if dinner_words:
            ingredient_matches = []
            for c in selection_pool:
                c_dict = format_meal(c)
                c_words = get_base_words(c_dict["ingredients"])
                if dinner_words.intersection(c_words):
                    ingredient_matches.append(c)

            if ingredient_matches:
                selection_pool = ingredient_matches

        chosen = random.choice(selection_pool)
        recent_meal_names.add(chosen.name)

        c_dict = format_meal(chosen)
        c_words = get_base_words(c_dict["ingredients"])
        return c_dict, c_words

    # Pick dinner first (to get ingredient words)
    dinner_dict, dinner_words = pick_meal("dinner", "full_meal")

    # Pick breakfast and lunch attempting to match dinner words
    breakfast_dict, _ = pick_meal("breakfast", "simple", dinner_words=dinner_words)
    lunch_dict, _ = pick_meal("lunch", "simple", dinner_words=dinner_words)

    plan = {
        "breakfast": breakfast_dict,
        "lunch": lunch_dict,
        "dinner": dinner_dict,
    }

    # Save the new plan into history
    for meal_type, m_dict in plan.items():
        if m_dict and m_dict["name"] != "No meal available":
            db.add(MealHistory(meal_name=m_dict["name"]))
    db.commit()

    return plan
