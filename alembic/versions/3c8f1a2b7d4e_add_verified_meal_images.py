"""add verified meal images

Revision ID: 3c8f1a2b7d4e
Revises: 2b7d4e9a6c1f
Create Date: 2026-09-21 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "3c8f1a2b7d4e"
down_revision: Union[str, Sequence[str], None] = "2b7d4e9a6c1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


VERIFIED_IMAGES = {
    "Pan-Seared Salmon & Quinoa Grain Bowl": "/static/images/salmon-quinoa-grain-bowl.jpg",
    "Rosemary Chicken Thighs & Roasted Brussels Sprouts": "/static/images/rosemary-chicken-thighs-roasted-brussels-sprouts.jpg",
    "Grass-Fed Sirloin Steak & Sauteed Green Beans": "/static/images/grass-fed-sirloin-steak-sauteed-green-beans.jpg",
}


def upgrade() -> None:
    connection = op.get_bind()
    for name, image_url in VERIFIED_IMAGES.items():
        connection.execute(
            sa.text("UPDATE meals SET image_url = :image_url WHERE name = :name"),
            {"image_url": image_url, "name": name},
        )


def downgrade() -> None:
    connection = op.get_bind()
    for name in VERIFIED_IMAGES:
        connection.execute(
            sa.text("UPDATE meals SET image_url = NULL WHERE name = :name"),
            {"name": name},
        )
