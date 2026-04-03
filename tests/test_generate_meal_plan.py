from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meal_planner.database.session import Base
from meal_planner.models.meal import Meal
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
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
        },
        "lunch": {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
        },
        "dinner": {
            "name": "No meal available",
            "description": "",
            "image_url": None,
            "ingredients": [],
            "instructions": [],
            "cooking_tips": "",
        },
    }


def test_generate_meal_plan_returns_meal_per_type(monkeypatch):
    db = _make_session()
    try:
        db.add_all(
            [
                Meal(
                    name="Eggs",
                    meal_type="breakfast",
                    is_high_protein=True,
                    description="Simple scrambled eggs.",
                    image_url="https://example.com/eggs.jpg",
                    ingredients='["eggs"]',
                    instructions='["Crack eggs into a bowl.", "Scramble in a pan."]',
                    cooking_tips="Use low heat for soft curds.",
                ),
                Meal(
                    name="Chicken Bowl",
                    meal_type="lunch",
                    is_high_protein=True,
                    description="Chicken and rice bowl.",
                    image_url=None,
                    ingredients='["chicken", "rice"]',
                    instructions='["Cook chicken.", "Serve over rice."]',
                ),
                Meal(
                    name="Steak",
                    meal_type="dinner",
                    is_high_protein=True,
                    description="Pan-seared steak.",
                    image_url=None,
                    ingredients='["steak", "salt"]',
                    instructions='["Season steak.", "Sear each side."]',
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

    assert plan == {
        "breakfast": {
            "name": "Eggs",
            "description": "Simple scrambled eggs.",
            "image_url": "https://example.com/eggs.jpg",
            "ingredients": ["eggs"],
            "instructions": ["Crack eggs into a bowl.", "Scramble in a pan."],
            "cooking_tips": "Use low heat for soft curds.",
        },
        "lunch": {
            "name": "Chicken Bowl",
            "description": "Chicken and rice bowl.",
            "image_url": None,
            "ingredients": ["chicken", "rice"],
            "instructions": ["Cook chicken.", "Serve over rice."],
            "cooking_tips": "",
        },
        "dinner": {
            "name": "Steak",
            "description": "Pan-seared steak.",
            "image_url": None,
            "ingredients": ["steak", "salt"],
            "instructions": ["Season steak.", "Sear each side."],
            "cooking_tips": "",
        },
    }
