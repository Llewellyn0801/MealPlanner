"""correct mismatched recipe images

Revision ID: 5e1b3c7d9a2f
Revises: 4d9a2b7c1e5f
Create Date: 2026-09-21 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "5e1b3c7d9a2f"
down_revision: Union[str, Sequence[str], None] = "4d9a2b7c1e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE meals SET image_url = :image_url WHERE name = :name"),
        {
            "image_url": "/static/images/chicken-shawarma-tahini-platter.jpg",
            "name": "Grilled Chicken Shawarma & Herb Tahini Bowl",
        },
    )
    connection.execute(
        sa.text("UPDATE meals SET image_url = NULL WHERE name = :name"),
        {"name": "Rosemary Chicken Thighs & Roasted Brussels Sprouts"},
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE meals SET image_url = NULL WHERE name = :name"),
        {"name": "Grilled Chicken Shawarma & Herb Tahini Bowl"},
    )
