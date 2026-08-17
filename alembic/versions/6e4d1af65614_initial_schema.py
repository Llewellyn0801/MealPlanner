"""initial schema

Revision ID: 6e4d1af65614
Revises:
Create Date: 2026-07-29 13:05:53.749268

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision: str = "6e4d1af65614"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "meals",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("meal_type", sa.String(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False, server_default="simple"),
        sa.Column("description", sa.String(), nullable=False, server_default=""),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("ingredients", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("instructions", sa.Text(), nullable=False, server_default=""),
        sa.Column("cooking_tips", sa.Text(), nullable=True),
        sa.Column("tags", sa.String(), nullable=False, server_default=""),
        sa.Column("core_base", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("family_additions", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("user_alternatives", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("is_carnivore", sa.Boolean(), server_default="0"),
        sa.Column("is_high_protein", sa.Boolean(), server_default="0"),
        sa.Column("is_kid_friendly", sa.Boolean(), server_default="0"),
    )
    op.create_index(op.f("ix_meals_id"), "meals", ["id"], unique=False)
    op.create_index(op.f("ix_meals_meal_type"), "meals", ["meal_type"], unique=False)

    op.create_table(
        "meal_history",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("meal_name", sa.String(), nullable=False),
        sa.Column("meal_type", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index(op.f("ix_meal_history_id"), "meal_history", ["id"], unique=False)
    op.create_index(
        op.f("ix_meal_history_meal_name"), "meal_history", ["meal_name"], unique=False
    )
    op.create_index(
        op.f("ix_meal_history_meal_type"), "meal_history", ["meal_type"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_meal_history_meal_type"), table_name="meal_history")
    op.drop_index(op.f("ix_meal_history_meal_name"), table_name="meal_history")
    op.drop_index(op.f("ix_meal_history_id"), table_name="meal_history")
    op.drop_table("meal_history")
    op.drop_index(op.f("ix_meals_meal_type"), table_name="meals")
    op.drop_index(op.f("ix_meals_id"), table_name="meals")
    op.drop_table("meals")
