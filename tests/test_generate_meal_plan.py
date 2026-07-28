import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meal_planner.database.session import Base
from meal_planner.models.meal import Meal
from meal_planner.services.grocery import generate_grocery_list
from meal_planner.services.meal_engine import generate_meal_plan


def _make_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_generate_meal_plan_returns_fallback_when_no_meals():
    db = _make_session()
    try:
        plan = generate_meal_plan(db)
    finally:
        db.close()

    assert plan == {
        "breakfast": {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "core_base": [],
            "family_additions": [],
            "user_alternatives": [],
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
            "tags": "",
        },
        "lunch": {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "core_base": [],
            "family_additions": [],
            "user_alternatives": [],
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
            "tags": "",
        },
        "dinner": {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "core_base": [],
            "family_additions": [],
            "user_alternatives": [],
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
            "tags": "",
        },
    }


def test_generate_meal_plan_returns_structured_components(monkeypatch):
    db = _make_session()
    try:
        db.add_all(
            [
                Meal(
                    name="Eggs & Avocado",
                    meal_type="breakfast",
<<<<<<< HEAD
                    difficulty="simple",
                    is_high_protein=True,
                    description="Simple scrambled eggs.",
=======
                    tags="user_safe,heart_healthy,low_carb",
                    description="Scrambled eggs with avocado.",
>>>>>>> 4c0665a (update meal planner and use uv instead of poetry)
                    image_url="https://example.com/eggs.jpg",
                    core_base=json.dumps(
                        [
                            {
                                "name": "3 Eggs",
                                "category": "Protein",
                                "tags": ["user_safe"],
                            },
                            {
                                "name": "1/2 Avocado",
                                "category": "Produce",
                                "tags": ["user_safe", "heart_healthy"],
                            },
                        ]
                    ),
                    family_additions=json.dumps(
                        [
                            {
                                "name": "2 Toast Slices",
                                "category": "Pantry/Grains",
                                "tags": ["family_side"],
                            }
                        ]
                    ),
                    user_alternatives=json.dumps(
                        [
                            {
                                "name": "1/2 cup Zucchini",
                                "category": "Produce",
                                "tags": ["user_safe"],
                            }
                        ]
                    ),
                    ingredients='["3 Eggs", "1/2 Avocado", "2 Toast Slices", "1/2 cup Zucchini"]',
                    instructions='["Crack eggs.", "Scramble."]',
                ),
                Meal(
                    name="Chicken & Salad",
                    meal_type="lunch",
<<<<<<< HEAD
                    difficulty="simple",
                    is_high_protein=True,
                    description="Chicken and rice bowl.",
=======
                    tags="user_safe,heart_healthy",
                    description="Grilled chicken with salad.",
>>>>>>> 4c0665a (update meal planner and use uv instead of poetry)
                    image_url=None,
                    core_base=json.dumps(
                        [
                            {
                                "name": "180g Chicken Breast",
                                "category": "Protein",
                                "tags": ["user_safe"],
                            }
                        ]
                    ),
                    family_additions=json.dumps(
                        [
                            {
                                "name": "1 cup Brown Rice",
                                "category": "Pantry/Grains",
                                "tags": ["family_side"],
                            }
                        ]
                    ),
                    user_alternatives=json.dumps([]),
                    ingredients='["180g Chicken Breast", "1 cup Brown Rice"]',
                    instructions='["Grill chicken."]',
                ),
                Meal(
                    name="Salmon & Asparagus",
                    meal_type="dinner",
<<<<<<< HEAD
                    difficulty="full_meal",
                    is_high_protein=True,
                    description="Pan-seared steak.",
=======
                    tags="user_safe,heart_healthy",
                    description="Roasted salmon.",
>>>>>>> 4c0665a (update meal planner and use uv instead of poetry)
                    image_url=None,
                    core_base=json.dumps(
                        [
                            {
                                "name": "200g Salmon",
                                "category": "Protein",
                                "tags": ["user_safe", "heart_healthy"],
                            },
                            {
                                "name": "1 cup Asparagus",
                                "category": "Produce",
                                "tags": ["user_safe"],
                            },
                        ]
                    ),
                    family_additions=json.dumps([]),
                    user_alternatives=json.dumps(
                        [
                            {
                                "name": "1 cup Cauliflower Rice",
                                "category": "Produce",
                                "tags": ["user_safe"],
                            }
                        ]
                    ),
                    ingredients='["200g Salmon", "1 cup Asparagus", "1 cup Cauliflower Rice"]',
                    instructions='["Bake salmon."]',
                ),
            ]
        )
        db.commit()

        monkeypatch.setattr(
            "meal_planner.services.meal_engine.random.choice", lambda meals: meals[0]
        )
        plan = generate_meal_plan(db)
    finally:
        db.close()

    assert plan["breakfast"]["name"] == "Eggs & Avocado"
    assert len(plan["breakfast"]["core_base"]) == 2
    assert plan["breakfast"]["family_additions"][0]["name"] == "2 Toast Slices"

    # Test grocery aggregation
    grocery_res = generate_grocery_list(plan)
    g_list = grocery_res["grocery_list"]

    assert "3 Eggs" in g_list["Protein"]["core"]
    assert "200g Salmon" in g_list["Protein"]["core"]
    assert "2 Toast Slices" in g_list["Pantry/Grains"]["family_only"]
    assert "1 cup Brown Rice" in g_list["Pantry/Grains"]["family_only"]
    assert "1/2 cup Zucchini" in g_list["Produce"]["user_only"]
