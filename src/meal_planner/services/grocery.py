from typing import Any


def categorize_ingredient(name: str) -> str:
    lower_name = name.lower()
    protein_keywords = [
        "chicken",
        "turkey",
        "beef",
        "steak",
        "salmon",
        "tuna",
        "cod",
        "fish",
        "shrimp",
        "egg",
        "eggs",
        "tofu",
        "meatball",
        "meatballs",
        "lentil",
        "lentils",
    ]
    produce_keywords = [
        "spinach",
        "berry",
        "berries",
        "avocado",
        "cucumber",
        "tomato",
        "tomatoes",
        "lettuce",
        "mushroom",
        "mushrooms",
        "broccoli",
        "pepper",
        "peppers",
        "zucchini",
        "asparagus",
        "kale",
        "garlic",
        "lemon",
        "celery",
        "carrot",
        "carrots",
        "green beans",
        "brussels sprouts",
        "eggplant",
        "herbs",
        "dill",
        "rosemary",
        "cauliflower",
        "banana",
        "blueberries",
    ]
    dairy_fats_keywords = [
        "yogurt",
        "milk",
        "cheese",
        "butter",
        "olive oil",
        "sesame oil",
        "mayo",
        "mayonnaise",
        "cream",
    ]

    for kw in protein_keywords:
        if kw in lower_name:
            return "Protein"
    for kw in produce_keywords:
        if kw in lower_name:
            return "Produce"
    for kw in dairy_fats_keywords:
        if kw in lower_name:
            return "Dairy/Fats"

    return "Pantry/Grains"


def generate_grocery_list(plan: dict[str, Any]) -> dict[str, Any]:
    """
    Takes a meal plan dictionary and extracts categorized ingredients,
    distinguishing shared Core Base items from Family-Only additions
    and User-Only alternatives.
    """
    categories = ["Produce", "Protein", "Pantry/Grains", "Dairy/Fats"]

    structured_grocery: dict[str, dict[str, list[str]]] = {
        cat: {"core": [], "family_only": [], "user_only": []} for cat in categories
    }

    seen_core = set()
    seen_family = set()
    seen_user = set()

    for meal_type in ["breakfast", "lunch", "dinner"]:
        meal = plan.get(meal_type)
        if not isinstance(meal, dict):
            continue

        # 1. Process Core Base items (Shared)
        core_base = meal.get("core_base", [])
        if isinstance(core_base, list) and core_base:
            for item in core_base:
                if isinstance(item, dict) and "name" in item:
                    name = item["name"]
                    category = item.get("category") or categorize_ingredient(name)
                    if category not in structured_grocery:
                        category = "Pantry/Grains"
                    if name not in seen_core:
                        seen_core.add(name)
                        structured_grocery[category]["core"].append(name)

        # 2. Process Family-Only Additions
        family_additions = meal.get("family_additions", [])
        if isinstance(family_additions, list) and family_additions:
            for item in family_additions:
                if isinstance(item, dict) and "name" in item:
                    name = item["name"]
                    category = item.get("category") or categorize_ingredient(name)
                    if category not in structured_grocery:
                        category = "Pantry/Grains"
                    if name not in seen_family:
                        seen_family.add(name)
                        structured_grocery[category]["family_only"].append(name)

        # 3. Process User-Only Alternatives
        user_alternatives = meal.get("user_alternatives", [])
        if isinstance(user_alternatives, list) and user_alternatives:
            for item in user_alternatives:
                if isinstance(item, dict) and "name" in item:
                    name = item["name"]
                    category = item.get("category") or categorize_ingredient(name)
                    if category not in structured_grocery:
                        category = "Pantry/Grains"
                    if name not in seen_user:
                        seen_user.add(name)
                        structured_grocery[category]["user_only"].append(name)

        # 4. Fallback for legacy flat ingredients list
        if not core_base and not family_additions and not user_alternatives:
            ingredients = meal.get("ingredients", [])
            if isinstance(ingredients, list):
                for ing in ingredients:
                    if isinstance(ing, str) and ing not in seen_core:
                        seen_core.add(ing)
                        category = categorize_ingredient(ing)
                        structured_grocery[category]["core"].append(ing)

    # Flat list for backwards compatibility or simple rendering
    all_flat = sorted(list(seen_core.union(seen_family).union(seen_user)))

    return {
        "grocery_list": structured_grocery,
        "flat_list": all_flat,
    }
