"""remove more wrong recipe images

Revision ID: 1a6e3c9b7d2f
Revises: 9f5d2c8b4e1a
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "1a6e3c9b7d2f"
down_revision: Union[str, Sequence[str], None] = "9f5d2c8b4e1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMES = (
    "Grilled Chicken Shawarma & Herb Tahini Bowl",
    "Pan-Seared Salmon & Quinoa Grain Bowl",
    "Rosemary Chicken Thighs & Roasted Brussels Sprouts",
    "Grass-Fed Sirloin Steak & Sauteed Green Beans",
    "Mediterranean Tofu Steak & Roasted Ratatouille",
    "Chinese Beef & Broccoli with Garlic",
)


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE meals SET image_url = NULL WHERE name IN :names").bindparams(
            sa.bindparam("names", expanding=True)
        ),
        {"names": list(NAMES)},
    )


def downgrade() -> None:
    return None
