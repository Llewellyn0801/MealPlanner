"""remove wrong shrimp salad image

Revision ID: 9f5d2c8b4e1a
Revises: 8e4c1b7a2d6f
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "9f5d2c8b4e1a"
down_revision: Union[str, Sequence[str], None] = "8e4c1b7a2d6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE meals SET image_url = NULL "
            "WHERE name = :name"
        ).bindparams(name="Mediterranean Grilled Shrimp & Zucchini Salad")
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE meals SET image_url = :image_url "
            "WHERE name = :name"
        ).bindparams(
            image_url="/static/images/mediterranean-grilled-shrimp-zucchini-salad.jpg",
            name="Mediterranean Grilled Shrimp & Zucchini Salad",
        )
    )
