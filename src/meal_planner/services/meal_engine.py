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


def parse_json_dict_list(payload: str) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(payload)
        if isinstance(parsed, list):
            return [item for item in parsed if isinstance(item, dict)]
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
            if word.isnumeric() or any(char.isdigit() for char in word):
                continue
            if word not in stop_words and len(word) > 2:
                words.add(word)
    return words


def format_meal(meal: Meal | None) -> dict[str, Any]:
    if not meal:
        return {
            "meal_id": None,
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "calories": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fats_g": 0,
            "core_base": [],
            "family_additions": [],
            "user_alternatives": [],
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
            "tags": "",
            "prep_time_mins": 0,
            "cook_time_mins": 0,
            "total_time_mins": 0,
            "servings_default": 4,
            "difficulty": "simple",
            "rating": 0.0,
            "ratings_count": 0,
            "is_favorite": False,
            "prep_detail_steps": [],
        }

    meal_ingredients = cast(str, meal.ingredients)
    meal_instructions = cast(str, meal.instructions)
    meal_core_base = cast(str, getattr(meal, "core_base", "[]"))
    meal_family_additions = cast(str, getattr(meal, "family_additions", "[]"))
    meal_user_alternatives = cast(str, getattr(meal, "user_alternatives", "[]"))

    core_base = parse_json_dict_list(meal_core_base)
    family_additions = parse_json_dict_list(meal_family_additions)
    user_alternatives = parse_json_dict_list(meal_user_alternatives)
    ingredients = parse_json_list(meal_ingredients)

    if not ingredients and core_base:
        ingredients = [
            item["name"]
            for item in core_base + family_additions + user_alternatives
            if isinstance(item, dict) and "name" in item
        ]

    prep_time = getattr(meal, "prep_time_mins", 0) or 0
    cook_time = getattr(meal, "cook_time_mins", 0) or 0
    prep_detail_raw = cast(str, getattr(meal, "prep_detail_steps", "[]"))

    return {
        "meal_id": meal.id,
        "name": meal.name,
        "description": meal.description,
        "image_url": meal.image_url,
        "calories": getattr(meal, "calories", 0) or 0,
        "protein_g": getattr(meal, "protein_g", 0) or 0,
        "carbs_g": getattr(meal, "carbs_g", 0) or 0,
        "fats_g": getattr(meal, "fats_g", 0) or 0,
        "core_base": core_base,
        "family_additions": family_additions,
        "user_alternatives": user_alternatives,
        "ingredients": ingredients,
        "instructions": parse_json_list(meal_instructions),
        "cooking_tips": meal.cooking_tips or "",
        "tags": meal.tags or "",
        "prep_time_mins": prep_time,
        "cook_time_mins": cook_time,
        "total_time_mins": prep_time + cook_time,
        "servings_default": getattr(meal, "servings_default", 4) or 4,
        "difficulty": getattr(meal, "difficulty", "simple") or "simple",
        "rating": getattr(meal, "rating", 0.0) or 0.0,
        "ratings_count": getattr(meal, "ratings_count", 0) or 0,
        "is_favorite": bool(getattr(meal, "is_favorite", False)),
        "prep_detail_steps": parse_json_dict_list(prep_detail_raw),
    }


def calculate_total_macros(plan: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Calculates aggregated macro totals across all meals in the plan."""
    totals = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fats_g": 0}
    for m in plan.values():
        if isinstance(m, dict) and m.get("name") != "No meal available":
            totals["calories"] += int(m.get("calories", 0) or 0)
            totals["protein_g"] += int(m.get("protein_g", 0) or 0)
            totals["carbs_g"] += int(m.get("carbs_g", 0) or 0)
            totals["fats_g"] += int(m.get("fats_g", 0) or 0)
    return totals


def _meal_contains_dislikes(meal: Meal, dislikes: list[str]) -> bool:
    if not dislikes:
        return False
    text = f"{meal.name} {meal.tags} {meal.ingredients}".lower()
    for d in dislikes:
        term = d.strip().lower()
        if term and term in text:
            return True
    return False


def _score_meal(meal: Meal, meal_type: str, likes: list[str] | None = None) -> int:
    """Scores a meal based on desired tags and user liked preferences."""
    score = 0
    tags = [t.strip().lower() for t in meal.tags.split(",") if t.strip()]

    if "low_carb" in tags:
        score += 1
    if "heart_healthy" in tags:
        score += 1
    if meal_type == "dinner" and "high_protein" in tags:
        score += 1
    if meal_type == "dinner" and "kid_friendly" in tags:
        score += 1

    if likes:
        meal_name_lower = meal.name.lower()
        for like in likes:
            term = like.strip().lower()
            if term and (term in tags or term in meal_name_lower):
                score += 3  # Strong boost for user explicit likes

    return score


def _pick_meal(
    meals: list[Meal],
    meal_type: str,
    recent_meal_names: set[str],
    dislikes: list[str] | None = None,
    likes: list[str] | None = None,
) -> Meal | None:
    if not meals:
        return None

    # Filter out meals with disliked ingredients if alternatives exist
    if dislikes:
        non_disliked = [m for m in meals if not _meal_contains_dislikes(m, dislikes)]
        if non_disliked:
            meals = non_disliked

    # Primary pool: unseen meals if possible
    unseen_meals = [m for m in meals if m.name not in recent_meal_names]
    selection_pool = unseen_meals if unseen_meals else meals

    # Score and sort meals
    scored_meals = [(_score_meal(m, meal_type, likes), m) for m in selection_pool]
    scored_meals.sort(key=lambda x: x[0], reverse=True)

    top_meals = [m for score, m in scored_meals[:5]]
    return random.choice(top_meals) if top_meals else None


def generate_meal_plan(
    db: Session, dislikes: list[str] | None = None, likes: list[str] | None = None
) -> dict[str, dict[str, Any]]:
    all_meals = db.query(Meal).all()
    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        hours=48
    )
    recent_history = (
        db.query(MealHistory).filter(MealHistory.created_at >= cutoff_time).all()
    )

    recent_meals_by_type = {
        "breakfast": {
            cast(str, h.meal_name) for h in recent_history if h.meal_type == "breakfast"
        },
        "lunch": {
            cast(str, h.meal_name) for h in recent_history if h.meal_type == "lunch"
        },
        "dinner": {
            cast(str, h.meal_name) for h in recent_history if h.meal_type == "dinner"
        },
    }

    def pick_meal(meal_type: str, difficulty: str) -> tuple[dict[str, Any], set[str]]:
        candidates = [
            m
            for m in all_meals
            if m.meal_type == meal_type and m.difficulty == difficulty
        ]
        if not candidates:
            candidates = [m for m in all_meals if m.meal_type == meal_type]

        if not candidates:
            return format_meal(None), set()

        recent_names = recent_meals_by_type.get(meal_type, set())
        chosen = _pick_meal(candidates, meal_type, recent_names, dislikes, likes)

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


def _apply_dietary_preset(meals: list[Meal], preset: str | None) -> list[Meal]:
    """Filter meals by dietary preset."""
    if not preset:
        return meals
    p = preset.lower()
    if p == "keto":
        filtered = [m for m in meals if "low_carb" in (m.tags or "").lower()]
    elif p == "high_protein":
        filtered = [m for m in meals if m.is_high_protein or "high_protein" in (m.tags or "").lower()]
    elif p == "vegetarian":
        filtered = [m for m in meals if not m.is_carnivore]
    elif p == "kid_friendly":
        filtered = [m for m in meals if m.is_kid_friendly or "kid_friendly" in (m.tags or "").lower()]
    else:
        return meals
    return filtered if filtered else meals


def generate_multi_day_plan(
    db: Session,
    days: int = 1,
    dislikes: list[str] | None = None,
    likes: list[str] | None = None,
    dietary_preset: str | None = None,
) -> dict[str, Any]:
    """Generate a plan for 1, 3, or 7 days."""
    if days <= 1:
        return generate_meal_plan(db, dislikes=dislikes, likes=likes)

    all_meals = db.query(Meal).all()
    all_meals = _apply_dietary_preset(all_meals, dietary_preset)

    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=48)
    recent_history = db.query(MealHistory).filter(MealHistory.created_at >= cutoff).all()

    used_names: set[str] = set()
    multi_plan: dict[str, dict[str, dict[str, Any]]] = {}

    for day_num in range(1, days + 1):
        recent_by_type: dict[str, set[str]] = {
            mt: {cast(str, h.meal_name) for h in recent_history if h.meal_type == mt} | used_names
            for mt in ["breakfast", "lunch", "dinner"]
        }

        day_plan: dict[str, dict[str, Any]] = {}
        for meal_type, difficulty in [("breakfast", "simple"), ("lunch", "simple"), ("dinner", "full_meal")]:
            candidates = [m for m in all_meals if m.meal_type == meal_type and m.difficulty == difficulty]
            if not candidates:
                candidates = [m for m in all_meals if m.meal_type == meal_type]
            if not candidates:
                day_plan[meal_type] = format_meal(None)
                continue

            chosen = _pick_meal(candidates, meal_type, recent_by_type.get(meal_type, set()), dislikes, likes)
            day_plan[meal_type] = format_meal(chosen)
            if chosen:
                used_names.add(chosen.name)

        multi_plan[f"Day {day_num}"] = day_plan

    return multi_plan


def calculate_multi_day_macros(
    multi_plan: dict[str, Any],
) -> dict[str, Any]:
    """Calculate per-day and average macros for a multi-day plan."""
    if "breakfast" in multi_plan:
        # Single-day plan
        totals = calculate_total_macros(multi_plan)
        return {"days": {"Day 1": totals}, "average": totals}

    per_day: dict[str, dict[str, int]] = {}
    for day_key, day_data in multi_plan.items():
        if isinstance(day_data, dict):
            per_day[day_key] = calculate_total_macros(day_data)

    num_days = len(per_day) or 1
    avg = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fats_g": 0}
    for d in per_day.values():
        for k in avg:
            avg[k] += d.get(k, 0)
    for k in avg:
        avg[k] = round(avg[k] / num_days)

    return {"days": per_day, "average": avg}


def get_swap_candidates(
    db: Session,
    meal_type: str,
    current_meal_names: list[str],
    dislikes: list[str] | None = None,
    count: int = 5,
) -> list[dict[str, Any]]:
    """Return top alternative meals for swapping."""
    all_type = db.query(Meal).filter(Meal.meal_type == meal_type).all()
    candidates = [m for m in all_type if m.name not in current_meal_names]
    if not candidates:
        candidates = all_type

    if dislikes:
        non_disliked = [m for m in candidates if not _meal_contains_dislikes(m, dislikes)]
        if non_disliked:
            candidates = non_disliked

    scored = [(_score_meal(m, meal_type), m) for m in candidates]
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:count]
    return [format_meal(m) for _, m in top]

