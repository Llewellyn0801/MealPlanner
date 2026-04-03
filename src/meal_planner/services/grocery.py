from typing import Any


def generate_grocery_list(plan: dict[str, Any]) -> dict[str, list[str]]:
    """
    Takes a meal plan dictionary and extracts a deduplicated list of ingredients.
    """
    ingredients = set()
    for meal_type in ["breakfast", "lunch", "dinner"]:
        meal = plan.get(meal_type)
        if meal and "ingredients" in meal:
            for ingredient in meal.get("ingredients", []):
                ingredients.add(ingredient)
    return {"grocery_list": sorted(list(ingredients))}
