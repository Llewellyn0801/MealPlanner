"""add nutrition basis to meals

Revision ID: 3b7f0f9a2c1e
Revises: 1272a7f54636
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "3b7f0f9a2c1e"
down_revision: Union[str, Sequence[str], None] = "1272a7f54636"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("meals")}
    if "nutrition_basis" not in columns:
        op.add_column(
            "meals",
            sa.Column(
                "nutrition_basis",
                sa.String(),
                nullable=False,
                server_default="per_serving",
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("meals")}
    if "nutrition_basis" in columns:
        op.drop_column("meals", "nutrition_basis")
