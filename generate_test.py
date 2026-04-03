from meal_planner.database.session import SessionLocal, Base, engine
from meal_planner.database.seed import seed_meals
from meal_planner.services.meal_engine import generate_meal_plan

Base.metadata.create_all(bind=engine)
seed_meals()

db = SessionLocal()
print("First generated plan:")
plan1 = generate_meal_plan(db)
for meal_type, data in plan1.items():
    print(f"{meal_type}: {data['name']}")

print("\nSecond generated plan (should avoid the first plan's meals):")
plan2 = generate_meal_plan(db)
for meal_type, data in plan2.items():
    print(f"{meal_type}: {data['name']}")
db.close()
