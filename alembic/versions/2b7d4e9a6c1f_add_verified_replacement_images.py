"""add verified replacement images

Revision ID: 2b7d4e9a6c1f
Revises: 1a6e3c9b7d2f
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "2b7d4e9a6c1f"
down_revision: Union[str, Sequence[str], None] = "1a6e3c9b7d2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE meals SET image_url = :image_url WHERE name = :name"),
        {
            "image_url": "/static/images/tofu-mushroom-garden-scramble.jpg",
            "name": "Tofu & Mushroom Garden Scramble",
        },
    )
    connection.execute(
        sa.text("UPDATE meals SET image_url = :image_url WHERE name = :name"),
        {
            "image_url": "/static/images/asian-beef-broccoli-skillet.jpg",
            "name": "Chinese Beef & Broccoli with Garlic",
        },
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text(
            "UPDATE meals SET image_url = NULL WHERE name IN (:tofu_name, :beef_name)"
        ),
        {
            "tofu_name": "Tofu & Mushroom Garden Scramble",
            "beef_name": "Chinese Beef & Broccoli with Garlic",
        },
    )
