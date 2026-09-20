"""fix tofu scramble image

Revision ID: 8e4c1b7a2d6f
Revises: 7d2f4a9c6b1e
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "8e4c1b7a2d6f"
down_revision: Union[str, Sequence[str], None] = "7d2f4a9c6b1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE meals SET image_url = :image_url "
            "WHERE name = :name"
        ).bindparams(
            image_url="/static/images/mediterranean-tofu-steak-roasted-ratatouille.jpg",
            name="Tofu & Mushroom Garden Scramble",
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE meals SET image_url = :image_url "
            "WHERE name = :name"
        ).bindparams(
            image_url="/static/images/tofu-mushroom-garden-scramble.jpg",
            name="Tofu & Mushroom Garden Scramble",
        )
    )
