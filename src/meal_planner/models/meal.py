import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from meal_planner.database.session import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    meal_type = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False, default="simple")
    description = Column(String, nullable=False, default="")
    image_url = Column(String, nullable=True)
    ingredients = Column(Text, nullable=False, default="[]")
    instructions = Column(Text, nullable=False, default="")
    cooking_tips = Column(Text, nullable=True)
    tags = Column(String, nullable=False, default="")
    core_base = Column(Text, nullable=False, default="[]")
    family_additions = Column(Text, nullable=False, default="[]")
    user_alternatives = Column(Text, nullable=False, default="[]")
    is_carnivore = Column(Boolean, default=False)
    is_high_protein = Column(Boolean, default=False)
    is_kid_friendly = Column(Boolean, default=False)
    calories = Column(Integer, nullable=False, default=0)
    protein_g = Column(Integer, nullable=False, default=0)
    carbs_g = Column(Integer, nullable=False, default=0)
    fats_g = Column(Integer, nullable=False, default=0)
    nutrition_basis = Column(String, nullable=False, default="per_serving")
    prep_time_mins = Column(Integer, nullable=False, default=10)
    cook_time_mins = Column(Integer, nullable=False, default=15)
    servings_default = Column(Integer, nullable=False, default=4)
    rating = Column(Float, nullable=False, default=0.0)
    ratings_count = Column(Integer, nullable=False, default=0)
    is_favorite = Column(Boolean, nullable=False, default=False)
    prep_detail_steps = Column(Text, nullable=False, default="[]")


class MealHistory(Base):
    __tablename__ = "meal_history"

    id = Column(Integer, primary_key=True, index=True)
    meal_name = Column(String, nullable=False, index=True)
    meal_type = Column(String, nullable=False, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class PantryItem(Base):
    __tablename__ = "pantry_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    category = Column(String, nullable=False, default="Pantry/Grains")
    is_in_stock = Column(Boolean, nullable=False, default=True)


class SavedPlan(Base):
    __tablename__ = "saved_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    plan_json = Column(Text, nullable=False, default="{}")
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class HouseholdMember(Base):
    __tablename__ = "household_members"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="member")
    profile = Column(String, nullable=False, default="general")
    household_size = Column(Integer, nullable=False, default=1)
    activity_level = Column(String, nullable=False, default="sedentary")
    maintenance_calories = Column(Integer, nullable=True)
    target_calories = Column(Integer, nullable=True)
    macro_focus = Column(String, nullable=False, default="balanced")
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
