from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meal_planner.database.session import Base
from meal_planner.models.meal import Meal
from meal_planner.routes.plan import generate_meal_plan


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
        "breakfast": "No meal available",
        "lunch": "No meal available",
        "dinner": "No meal available",
    }


def test_generate_meal_plan_returns_meal_per_type(monkeypatch):
    db = _make_session()
    try:
        db.add_all(
            [
                Meal(name="Eggs", meal_type="breakfast", is_high_protein=True),
                Meal(name="Chicken Bowl", meal_type="lunch", is_high_protein=True),
                Meal(name="Steak", meal_type="dinner", is_high_protein=True),
            ]
        )
        db.commit()

        monkeypatch.setattr(
            "meal_planner.routes.plan.random.choice", lambda meals: meals[0]
        )
        plan = generate_meal_plan(db)
    finally:
        db.close()

    assert plan == {"breakfast": "Eggs", "lunch": "Chicken Bowl", "dinner": "Steak"}
