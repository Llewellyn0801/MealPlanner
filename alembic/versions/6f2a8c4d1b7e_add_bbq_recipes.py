"""add BBQ recipes

Revision ID: 6f2a8c4d1b7e
Revises: 5e1b3c7d9a2f
Create Date: 2026-09-21 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "6f2a8c4d1b7e"
down_revision: Union[str, Sequence[str], None] = "5e1b3c7d9a2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


RECIPES = [
    {
        "name": "Smoky BBQ Beef Back Ribs",
        "description": "Slow-roasted beef ribs with a smoky house BBQ glaze, crisp slaw, and tender roasted vegetables.",
        "tags": "bbq,high_protein,comfort_food,family_favorite,full_meal",
        "calories": 680,
        "protein_g": 48,
        "carbs_g": 34,
        "fats_g": 38,
        "ingredients": '["320g Beef Back Ribs", "2 tbsp Smoky BBQ Sauce", "1 cup Cabbage & Carrot Slaw", "1 tsp Smoked Paprika & Garlic", "1 cup Roasted Sweet Potato Wedges", "Extra Green Beans"]',
        "instructions": '["Rub ribs with smoked paprika, garlic, and black pepper.", "Roast covered at 150°C for 2.5 hours until tender.", "Brush with BBQ sauce and finish uncovered until caramelized.", "Serve with slaw and sweet potato wedges or extra green beans."]',
        "cooking_tips": "Finish the ribs under high heat for a glossy glaze while keeping the meat tender.",
        "prep_time_mins": 15,
        "cook_time_mins": 150,
        "servings_default": 4,
    },
    {
        "name": "Backyard BBQ Beef Burger",
        "description": "Juicy grilled beef burger with smoky BBQ sauce, crunchy lettuce, tomato, and a toasted whole-grain bun.",
        "tags": "bbq,high_protein,family_favorite,comfort_food,simple",
        "calories": 590,
        "protein_g": 42,
        "carbs_g": 42,
        "fats_g": 27,
        "ingredients": '["180g Lean Ground Beef Patty", "1 Whole-Grain Burger Bun", "1 tbsp Smoky BBQ Sauce", "Lettuce, Tomato & Pickled Onion", "1 slice Cheddar Cheese", "Lettuce Wrap"]',
        "instructions": '["Season the beef patty with smoked paprika, garlic, and black pepper.", "Grill over medium-high heat until cooked to preference.", "Toast the bun, then layer lettuce, tomato, patty, BBQ sauce, and pickled onion.", "Use a lettuce wrap for the lighter profile portion."]',
        "cooking_tips": "Do not press the patty while grilling; keeping the juices inside makes the burger tender.",
        "prep_time_mins": 15,
        "cook_time_mins": 12,
        "servings_default": 4,
    },
]


def upgrade() -> None:
    connection = op.get_bind()
    for recipe in RECIPES:
        exists = connection.execute(
            sa.text("SELECT 1 FROM meals WHERE name = :name"), {"name": recipe["name"]}
        ).first()
        if exists:
            continue
        connection.execute(
            sa.text(
                """INSERT INTO meals (
                    name, meal_type, difficulty, description, image_url, ingredients,
                    instructions, cooking_tips, tags, core_base, family_additions,
                    user_alternatives, calories, protein_g, carbs_g, fats_g,
                    nutrition_basis, prep_time_mins, cook_time_mins, servings_default,
                    rating, ratings_count, is_favorite, prep_detail_steps
                ) VALUES (
                    :name, 'dinner', 'full_meal', :description, NULL, :ingredients,
                    :instructions, :cooking_tips, :tags, '[]', '[]', '[]',
                    :calories, :protein_g, :carbs_g, :fats_g, 'per_serving',
                    :prep_time_mins, :cook_time_mins, :servings_default,
                    4.5, 12, 0, '[]'
                )"""
            ),
            recipe,
        )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM meals WHERE name IN :names").bindparams(
            sa.bindparam("names", expanding=True)
        ),
        {"names": [recipe["name"] for recipe in RECIPES]},
    )
