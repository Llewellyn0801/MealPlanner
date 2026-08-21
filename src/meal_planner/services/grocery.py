import urllib.parse
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
        "pork",
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
        "apple",
        "apples",
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
        "goat cheese",
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


def _extract_meals_from_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    meals = []
    # Single day plan format: {"breakfast": {...}, "lunch": {...}, "dinner": {...}}
    if "breakfast" in plan or "lunch" in plan or "dinner" in plan:
        for meal_type in ["breakfast", "lunch", "dinner"]:
            m = plan.get(meal_type)
            if (
                isinstance(m, dict)
                and m.get("name")
                and m.get("name") != "No meal available"
            ):
                meals.append(m)
    else:
        # Multi-day plan format: {"Day 1": {"breakfast": ...}, "Day 2": ...}
        for day_key, day_data in plan.items():
            if isinstance(day_data, dict):
                for meal_type in ["breakfast", "lunch", "dinner"]:
                    m = day_data.get(meal_type)
                    if (
                        isinstance(m, dict)
                        and m.get("name")
                        and m.get("name") != "No meal available"
                    ):
                        meals.append(m)
    return meals


def is_in_pantry_stock(ingredient_name: str, in_stock_names: set[str]) -> bool:
    ing_lower = ingredient_name.lower()
    for stock_item in in_stock_names:
        if stock_item.lower() in ing_lower or ing_lower in stock_item.lower():
            return True
    return False


def generate_grocery_list(
    plan: dict[str, Any], in_stock_pantry: set[str] | list[str] | None = None
) -> dict[str, Any]:
    categories = ["Produce", "Protein", "Pantry/Grains", "Dairy/Fats"]
    in_stock_set = set(in_stock_pantry or [])

    structured_grocery: dict[str, dict[str, list[dict[str, Any]]]] = {
        cat: {"core": [], "family_only": [], "user_only": []} for cat in categories
    }

    seen_core = set()
    seen_family = set()
    seen_user = set()

    meals = _extract_meals_from_plan(plan)

    for meal in meals:
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
                        in_stock = is_in_pantry_stock(name, in_stock_set)
                        structured_grocery[category]["core"].append(
                            {"name": name, "in_pantry": in_stock}
                        )

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
                        in_stock = is_in_pantry_stock(name, in_stock_set)
                        structured_grocery[category]["family_only"].append(
                            {"name": name, "in_pantry": in_stock}
                        )

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
                        in_stock = is_in_pantry_stock(name, in_stock_set)
                        structured_grocery[category]["user_only"].append(
                            {"name": name, "in_pantry": in_stock}
                        )

        # 4. Fallback for legacy flat ingredients list
        if not core_base and not family_additions and not user_alternatives:
            ingredients = meal.get("ingredients", [])
            if isinstance(ingredients, list):
                for ing in ingredients:
                    if isinstance(ing, str) and ing not in seen_core:
                        seen_core.add(ing)
                        category = categorize_ingredient(ing)
                        in_stock = is_in_pantry_stock(ing, in_stock_set)
                        structured_grocery[category]["core"].append(
                            {"name": ing, "in_pantry": in_stock}
                        )

    # Build plain text export string
    text_lines = ["🛒 **Meal Planner Grocery List**\n"]
    category_emojis = {
        "Produce": "🥗",
        "Protein": "🥩",
        "Pantry/Grains": "🌾",
        "Dairy/Fats": "🥑",
    }

    for cat in categories:
        cat_data = structured_grocery[cat]
        all_items = cat_data["core"] + cat_data["family_only"] + cat_data["user_only"]
        # Filter out items already in pantry stock for export
        needed_items = [i["name"] for i in all_items if not i["in_pantry"]]
        if needed_items:
            emoji = category_emojis.get(cat, "🛒")
            text_lines.append(f"{emoji} **{cat}**:")
            for item_name in needed_items:
                text_lines.append(f"  • {item_name}")
            text_lines.append("")

    formatted_text = "\n".join(text_lines).strip()
    encoded_text = urllib.parse.quote(formatted_text)
    whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_text}"

    all_flat = sorted(list(seen_core.union(seen_family).union(seen_user)))

    return {
        "grocery_list": structured_grocery,
        "flat_list": all_flat,
        "formatted_text": formatted_text,
        "whatsapp_url": whatsapp_url,
    }
