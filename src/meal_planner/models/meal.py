import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

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


class MealHistory(Base):
    __tablename__ = "meal_history"

    id = Column(Integer, primary_key=True, index=True)
    meal_name = Column(String, nullable=False, index=True)
    meal_type = Column(String, nullable=False, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
