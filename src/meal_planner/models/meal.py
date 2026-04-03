from sqlalchemy import Boolean, Column, Integer, String

from meal_planner.database.session import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    meal_type = Column(String, nullable=False, index=True)
    is_carnivore = Column(Boolean, default=False)
    is_high_protein = Column(Boolean, default=False)
    is_kid_friendly = Column(Boolean, default=False)
