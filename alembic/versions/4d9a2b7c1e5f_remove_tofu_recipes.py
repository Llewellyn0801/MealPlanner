"""remove tofu recipes

Revision ID: 4d9a2b7c1e5f
Revises: 3c8f1a2b7d4e
Create Date: 2026-09-21 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "4d9a2b7c1e5f"
down_revision: Union[str, Sequence[str], None] = "3c8f1a2b7d4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TOFU_RECIPE_NAMES = [
    "Tofu & Mushroom Garden Scramble",
    "Mediterranean Tofu Steak & Roasted Ratatouille",
    "Thai Green Curry Tofu & Vegetables",
]


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM meals WHERE name IN :names").bindparams(
            sa.bindparam("names", expanding=True)
        ),
        {"names": TOFU_RECIPE_NAMES},
    )


def downgrade() -> None:
    # The removed seed records are intentionally not restored automatically.
    pass
