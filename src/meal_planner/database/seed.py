import json
from typing import Any

from sqlalchemy.orm import Session

from meal_planner.database.session import SessionLocal
from meal_planner.models.meal import Meal

IMAGE_MAPPING = {
    "Ground Beef & Eggs Bowl": "https://source.unsplash.com/600x400/?beef-eggs",
    "Greek Yogurt Berry Bowl": "https://source.unsplash.com/600x400/?yogurt-berries",
    "Spinach Cheese Omelette": "https://source.unsplash.com/600x400/?omelette-spinach",
    "Overnight Oats": "https://source.unsplash.com/600x400/?overnight-oats",
    "Avocado Toast with Poached Egg": (
        "https://source.unsplash.com/600x400/?avocado-toast-egg"
    ),
    "Scrambled Eggs with Spinach": (
        "https://source.unsplash.com/600x400/?scrambled-eggs-spinach"
    ),
    "Omelette with Mushrooms": "https://source.unsplash.com/600x400/?omelette-mushrooms",
    "Greek Yogurt with Nuts": "https://source.unsplash.com/600x400/?yogurt-nuts",
    "Chicken Salad Wrap": "https://source.unsplash.com/600x400/?chicken-wrap",
    "Turkey Lettuce Cups": "https://source.unsplash.com/600x400/?lettuce-wraps",
    "Beef Stir-Fry Bowl": "https://source.unsplash.com/600x400/?beef-stir-fry",
    "Quinoa Salad Bowl": "https://source.unsplash.com/600x400/?quinoa-salad",
    "Chicken Salad Bowl": "https://source.unsplash.com/600x400/?chicken-salad",
    "Tuna Avocado Bowl": "https://source.unsplash.com/600x400/?tuna-avocado",
    "Ground Beef Bowl": "https://source.unsplash.com/600x400/?ground-beef-bowl",
    "Egg Salad Lettuce Wraps": "https://source.unsplash.com/600x400/?egg-salad-wrap",
    "Baked Salmon & Asparagus": "https://source.unsplash.com/600x400/?salmon-asparagus",
    "Beef Meatballs with Zucchini": (
        "https://source.unsplash.com/600x400/?meatballs-zucchini"
    ),
    "Lemon Garlic Chicken Thighs": "https://source.unsplash.com/600x400/?lemon-chicken",
    "Shrimp Cauliflower Fried Rice": (
        "https://source.unsplash.com/600x400/?shrimp-fried-rice"
    ),
    "Grilled Chicken Thighs & Broccoli": (
        "https://source.unsplash.com/600x400/?grilled-chicken-broccoli"
    ),
    "Beef Patties & Eggs": "https://source.unsplash.com/600x400/?beef-patties-eggs",
}

ALL_MEALS = [
    # Breakfasts
    {
        "name": "Ground Beef & Eggs Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "carnivore,low_carb,high_protein",
        "ingredients": ["200g ground beef", "2 eggs"],
        "instructions": ["Cook beef, add eggs."],
    },
    {
        "name": "Greek Yogurt Berry Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "high_protein,heart_healthy",
        "ingredients": ["Greek yogurt", "berries"],
        "instructions": ["Mix and serve."],
    },
    {
        "name": "Spinach Cheese Omelette",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "low_carb,high_protein",
        "ingredients": ["3 eggs", "spinach", "cheese"],
        "instructions": ["Make omelette."],
    },
    {
        "name": "Overnight Oats",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "high_protein,heart_healthy",
        "ingredients": ["oats", "milk", "peanut butter"],
        "instructions": ["Mix and refrigerate."],
    },
    {
        "name": "Avocado Toast with Poached Egg",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "heart_healthy",
        "ingredients": ["bread", "avocado", "egg"],
        "instructions": ["Toast, mash, poach."],
    },
    {
        "name": "Scrambled Eggs with Spinach",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "low_carb,heart_healthy",
        "ingredients": ["2 eggs", "spinach"],
        "instructions": ["Scramble eggs with spinach."],
    },
    {
        "name": "Omelette with Mushrooms",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "low_carb",
        "ingredients": ["2 eggs", "mushrooms"],
        "instructions": ["Make mushroom omelette."],
    },
    {
        "name": "Greek Yogurt with Nuts",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "tags": "high_protein,heart_healthy",
        "ingredients": ["yogurt", "nuts"],
        "instructions": ["Mix and serve."],
    },
    # Lunches
    {
        "name": "Chicken Salad Wrap",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "high_protein",
        "ingredients": ["chicken", "wrap", "lettuce"],
        "instructions": ["Assemble wrap."],
    },
    {
        "name": "Turkey Lettuce Cups",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "low_carb,high_protein",
        "ingredients": ["ground turkey", "lettuce"],
        "instructions": ["Cook turkey, serve in lettuce."],
    },
    {
        "name": "Beef Stir-Fry Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "high_protein,low_carb",
        "ingredients": ["beef", "broccoli", "soy sauce"],
        "instructions": ["Stir-fry."],
    },
    {
        "name": "Quinoa Salad Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "heart_healthy,low_sodium",
        "ingredients": ["quinoa", "tomatoes", "cucumber"],
        "instructions": ["Mix salad."],
    },
    {
        "name": "Chicken Salad Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "low_carb,high_protein",
        "ingredients": ["chicken", "lettuce"],
        "instructions": ["Grill chicken, serve on lettuce."],
    },
    {
        "name": "Tuna Avocado Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "low_carb,heart_healthy",
        "ingredients": ["tuna", "avocado"],
        "instructions": ["Mix and serve."],
    },
    {
        "name": "Ground Beef Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "low_carb,high_protein",
        "ingredients": ["ground beef"],
        "instructions": ["Cook and serve."],
    },
    {
        "name": "Egg Salad Lettuce Wraps",
        "meal_type": "lunch",
        "difficulty": "simple",
        "tags": "low_carb",
        "ingredients": ["eggs", "lettuce", "mayo"],
        "instructions": ["Make egg salad, wrap in lettuce."],
    },
    # Dinners
    {
        "name": "Baked Salmon & Asparagus",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,high_protein,heart_healthy",
        "ingredients": ["salmon", "asparagus"],
        "instructions": ["Bake at 200C."],
    },
    {
        "name": "Beef Meatballs with Zucchini",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,high_protein",
        "ingredients": ["ground beef", "zucchini"],
        "instructions": ["Make meatballs, serve with zucchini."],
    },
    {
        "name": "Lemon Garlic Chicken Thighs",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,high_protein",
        "ingredients": ["chicken thighs", "lemon", "garlic"],
        "instructions": ["Cook chicken."],
    },
    {
        "name": "Shrimp Cauliflower Fried Rice",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,high_protein",
        "ingredients": ["shrimp", "cauliflower rice"],
        "instructions": ["Make fried rice."],
    },
    {
        "name": "Grilled Chicken Thighs & Broccoli",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,heart_healthy",
        "ingredients": ["chicken thighs", "broccoli"],
        "instructions": ["Grill chicken, steam broccoli."],
    },
    {
        "name": "Beef Patties & Eggs",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "tags": "low_carb,high_protein",
        "ingredients": ["ground beef", "eggs"],
        "instructions": ["Cook patties and eggs."],
    },
]


def get_or_create_meal(db: Session, meal_data: dict[str, Any]) -> None:
    """Checks if a meal exists by name and creates it if it doesn't."""
    existing_meal = db.query(Meal).filter(Meal.name == meal_data["name"]).first()
    if existing_meal:
        return

    instructions = meal_data.get("instructions")
    if isinstance(instructions, str):
        instructions = [instructions]

    meal_payload = {
        "name": meal_data["name"],
        "meal_type": meal_data["meal_type"],
        "difficulty": meal_data.get("difficulty", "simple"),
        "ingredients": json.dumps(meal_data.get("ingredients", [])),
        "instructions": json.dumps(instructions),
        "tags": meal_data.get("tags", ""),
        "description": meal_data.get(
            "description", f"A delicious {meal_data['name'].lower()}."
        ),
        "image_url": IMAGE_MAPPING.get(meal_data["name"]),
        "cooking_tips": meal_data.get("cooking_tips"),
        "is_carnivore": "carnivore" in meal_data.get("tags", ""),
        "is_high_protein": "high_protein" in meal_data.get("tags", ""),
        "is_kid_friendly": "kid_friendly" in meal_data.get("tags", ""),
    }
    db.add(Meal(**meal_payload))


def seed_meals() -> None:
    """Seeds the database with an initial set of meals."""
    db = SessionLocal()
    try:
        for meal_data in ALL_MEALS:
            get_or_create_meal(db, meal_data)
        db.commit()
    finally:
        db.close()
