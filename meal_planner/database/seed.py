from sqlalchemy.orm import Session

from database.session import SessionLocal
from models.meal import Meal


SEED_MEALS = [
    # Breakfast
    {
        "name": "Scrambled eggs with butter",
        "meal_type": "breakfast",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Omelette",
        "meal_type": "breakfast",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Greek yogurt bowl",
        "meal_type": "breakfast",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Protein pancakes",
        "meal_type": "breakfast",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    # Lunch
    {
        "name": "Ground beef bowl",
        "meal_type": "lunch",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chicken thighs",
        "meal_type": "lunch",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Minced beef patties",
        "meal_type": "lunch",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Tuna salad plate",
        "meal_type": "lunch",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    # Dinner
    {
        "name": "Ribeye steak",
        "meal_type": "dinner",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Baked salmon with greens",
        "meal_type": "dinner",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Turkey meatballs",
        "meal_type": "dinner",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Grilled chicken breast",
        "meal_type": "dinner",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
]


def _seed_if_empty(db: Session) -> None:
    meals_count = db.query(Meal).count()
    if meals_count > 0:
        return

    for meal_data in SEED_MEALS:
        db.add(Meal(**meal_data))
    db.commit()


def seed_meals() -> None:
    db = SessionLocal()
    try:
        _seed_if_empty(db)
    finally:
        db.close()
