import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meal_planner.database.session import Base
from meal_planner.models.meal import Meal, MealHistory
from meal_planner.services.meal_engine import generate_meal_plan


def _make_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_generate_meal_plan_saves_history():
    db = _make_session()
    try:
        db.add(
            Meal(
                name="Test Breakfast",
                meal_type="breakfast",
                difficulty="simple",
                ingredients="[]",
                instructions="[]",
            )
        )
        db.commit()

        generate_meal_plan(db)

        history = db.query(MealHistory).all()
        assert len(history) == 1
        assert history[0].meal_name == "Test Breakfast"
        assert history[0].meal_type == "breakfast"
    finally:
        db.close()


def test_generate_meal_plan_excludes_recent_meals():
    db = _make_session()
    try:
        # Add two breakfast options
        db.add_all(
            [
                Meal(
                    name="Recent Breakfast",
                    meal_type="breakfast",
                    difficulty="simple",
                    ingredients="[]",
                    instructions="[]",
                ),
                Meal(
                    name="New Breakfast",
                    meal_type="breakfast",
                    difficulty="simple",
                    ingredients="[]",
                    instructions="[]",
                ),
            ]
        )
        # Add a recent history entry for one of them
        db.add(
            MealHistory(
                meal_name="Recent Breakfast",
                meal_type="breakfast",
                created_at=datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(hours=1),
            )
        )
        db.commit()

        # Run the planner
        plan = generate_meal_plan(db)

        # The plan should pick the *other* breakfast
        assert plan["breakfast"]["name"] == "New Breakfast"
    finally:
        db.close()


def test_generate_meal_plan_falls_back_if_all_meals_are_recent():
    db = _make_session()
    try:
        # Add only one breakfast option
        db.add(
            Meal(
                name="Recent Breakfast",
                meal_type="breakfast",
                difficulty="simple",
                ingredients="[]",
                instructions="[]",
            )
        )
        # Add a recent history entry for it
        db.add(
            MealHistory(
                meal_name="Recent Breakfast",
                meal_type="breakfast",
                created_at=datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(hours=1),
            )
        )
        db.commit()

        # Run the planner
        plan = generate_meal_plan(db)

        # The planner should still return the only available meal
        assert plan["breakfast"]["name"] == "Recent Breakfast"
    finally:
        db.close()
