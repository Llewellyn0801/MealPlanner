import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meal_planner.database.seed import SEED_MEALS, _seed_if_empty
from meal_planner.database.session import Base
from meal_planner.models.meal import Meal
from meal_planner.services.grocery import generate_grocery_list
from meal_planner.services.meal_engine import (
    calculate_total_macros,
    generate_meal_plan,
)


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

    fallback = {
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

    assert plan == {
        "breakfast": fallback,
        "lunch": fallback,
        "dinner": fallback,
    }


def test_seed_if_empty_serializes_list_fields_for_sqlite():
    db = _make_session()
    try:
        _seed_if_empty(db)
        saved = db.query(Meal).first()

        assert saved is not None
        assert isinstance(saved.core_base, str)
        assert isinstance(saved.family_additions, str)
        assert isinstance(saved.user_alternatives, str)
        assert isinstance(saved.ingredients, str)
        assert isinstance(saved.instructions, str)
        assert isinstance(saved.prep_detail_steps, str)
        assert json.loads(saved.prep_detail_steps)[0]["detail"]
    finally:
        db.close()


def test_generate_meal_plan_returns_structured_components(monkeypatch):
    db = _make_session()
    try:
        db.add_all(
            [
                Meal(
                    name="Eggs & Avocado",
                    meal_type="breakfast",
                    difficulty="simple",
                    tags="user_safe,heart_healthy,low_carb",
                    description="Scrambled eggs with avocado.",
                    image_url="https://example.com/eggs.jpg",
                    calories=350,
                    protein_g=20,
                    carbs_g=10,
                    fats_g=25,
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
                    difficulty="simple",
                    tags="user_safe,heart_healthy",
                    description="Grilled chicken with salad.",
                    image_url=None,
                    calories=450,
                    protein_g=40,
                    carbs_g=15,
                    fats_g=20,
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
                    difficulty="full_meal",
                    tags="user_safe,heart_healthy",
                    description="Roasted salmon.",
                    image_url=None,
                    calories=500,
                    protein_g=45,
                    carbs_g=12,
                    fats_g=30,
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
    assert plan["breakfast"]["calories"] == 350
    assert plan["breakfast"]["protein_g"] == 20
    assert len(plan["breakfast"]["core_base"]) == 2
    assert plan["breakfast"]["family_additions"][0]["name"] == "2 Toast Slices"

    totals = calculate_total_macros(plan)
    assert totals["calories"] == 1300
    assert totals["protein_g"] == 105
    assert totals["carbs_g"] == 37
    assert totals["fats_g"] == 75

    # Test grocery aggregation
    grocery_res = generate_grocery_list(plan)
    g_list = grocery_res["grocery_list"]

    assert any(i["name"] == "3 Eggs" for i in g_list["Protein"]["core"])
    assert any(i["name"] == "200g Salmon" for i in g_list["Protein"]["core"])
    assert any(
        i["name"] == "2 Toast Slices" for i in g_list["Pantry/Grains"]["family_only"]
    )
    assert any(
        i["name"] == "1 cup Brown Rice" for i in g_list["Pantry/Grains"]["family_only"]
    )
    assert any(i["name"] == "1/2 cup Zucchini" for i in g_list["Produce"]["user_only"])


def test_seed_meals_include_indian_curry_recipes():
    meal_names = {meal["name"].lower() for meal in SEED_MEALS}

    assert any("chana masala" in name for name in meal_names)
    assert any("paneer butter masala" in name for name in meal_names)
    assert any("chicken tikka masala" in name for name in meal_names)

    curry_meals = [meal for meal in SEED_MEALS if "masala" in meal["name"].lower()]
    assert curry_meals
    for meal in curry_meals:
        assert meal["prep_time_mins"] > 0
        assert meal["cook_time_mins"] > 0
        assert meal["prep_detail_steps"]


def test_all_seed_meals_include_restaurant_style_metadata():
    assert len(SEED_MEALS) >= 20

    for meal in SEED_MEALS:
        assert meal["prep_time_mins"] > 0
        assert meal["cook_time_mins"] > 0
        assert meal["servings_default"] > 0
        assert 0 < meal["rating"] <= 5
        assert meal["ratings_count"] > 0
        assert meal["prep_detail_steps"]
        assert all(
            step["title"] and not step["title"].startswith("Step ")
            for step in meal["prep_detail_steps"]
        )
        assert all(step["detail"] for step in meal["prep_detail_steps"])


def test_generate_meal_plan_dislikes_filtering():
    db = _make_session()
    try:
        db.add_all(
            [
                Meal(
                    name="Tuna Romaine Salad",
                    meal_type="lunch",
                    difficulty="simple",
                    tags="heart_healthy",
                    ingredients='["Tuna", "Celery", "Avocado"]',
                    calories=380,
                    protein_g=35,
                ),
                Meal(
                    name="Lemon Chicken Salad",
                    meal_type="lunch",
                    difficulty="simple",
                    tags="heart_healthy",
                    ingredients='["Chicken", "Greens", "Olive Oil"]',
                    calories=420,
                    protein_g=40,
                ),
            ]
        )
        db.commit()

        # Generate plan excluding tuna
        plan = generate_meal_plan(db, dislikes=["tuna"])
        assert plan["lunch"]["name"] == "Lemon Chicken Salad"
    finally:
        db.close()
