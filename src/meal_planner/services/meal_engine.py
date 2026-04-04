import datetime
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


def _score_meal(meal: Meal, meal_type: str) -> int:
    """Scores a meal based on desired tags."""
    score = 0
    tags = meal.tags.split(",")
    if "low_carb" in tags:
        score += 1
    if "heart_healthy" in tags:
        score += 1
    if meal_type == "dinner" and "high_protein" in tags:
        score += 1
    if meal_type == "dinner" and "kid_friendly" in tags:
        score += 1
    return score


def _pick_meal(
    meals: list[Meal],
    meal_type: str,
    recent_meal_names: set[str],
) -> Meal | None:
    if not meals:
        return None

    # Primary pool: unseen meals if possible.
    unseen_meals = [m for m in meals if m.name not in recent_meal_names]

    if unseen_meals:
        selection_pool = unseen_meals
    else:
        # Fallback: if we've seen everything, we have to repeat.
        selection_pool = meals

    # Score and sort the meals
    scored_meals = [(_score_meal(m, meal_type), m) for m in selection_pool]
    scored_meals.sort(key=lambda x: x[0], reverse=True)

    # Take the top 5 (or fewer if not enough meals)
    top_meals = [m for score, m in scored_meals[:5]]

    return random.choice(top_meals) if top_meals else None


def generate_meal_plan(db: Session) -> dict[str, dict[str, Any]]:
    all_meals = db.query(Meal).all()
    cutoff_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(hours=48)
    recent_history = (
        db.query(MealHistory).filter(MealHistory.created_at >= cutoff_time).all()
    )

    recent_meals_by_type = {
        "breakfast": {
            cast(str, h.meal_name)
            for h in recent_history
            if h.meal_type == "breakfast"
        },
        "lunch": {
            cast(str, h.meal_name) for h in recent_history if h.meal_type == "lunch"
        },
        "dinner": {
            cast(str, h.meal_name) for h in recent_history if h.meal_type == "dinner"
        },
    }

    def pick_meal(
        meal_type: str, difficulty: str
    ) -> tuple[dict[str, Any], set[str]]:
        candidates = [
            m for m in all_meals
            if m.meal_type == meal_type and m.difficulty == difficulty
        ]
        if not candidates:
            candidates = [m for m in all_meals if m.meal_type == meal_type]

        if not candidates:
            return format_meal(None), set()

        recent_names = recent_meals_by_type.get(meal_type, set())
        chosen = _pick_meal(candidates, meal_type, recent_names)

        c_dict = format_meal(chosen)
        c_words = get_base_words(c_dict["ingredients"])
        return c_dict, c_words

    dinner_dict, dinner_words = pick_meal("dinner", "full_meal")
    breakfast_dict, _ = pick_meal("breakfast", "simple")
    lunch_dict, _ = pick_meal("lunch", "simple")

    plan = {
        "breakfast": breakfast_dict,
        "lunch": lunch_dict,
        "dinner": dinner_dict,
    }

    for meal_type, m_dict in plan.items():
        if m_dict and m_dict["name"] != "No meal available":
            db.add(MealHistory(meal_name=m_dict["name"], meal_type=meal_type))
    db.commit()

    return plan
