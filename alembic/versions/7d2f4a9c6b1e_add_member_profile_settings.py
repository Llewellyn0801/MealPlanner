"""add member profile settings

Revision ID: 7d2f4a9c6b1e
Revises: 5c1e8a7b4d2f
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "7d2f4a9c6b1e"
down_revision: Union[str, Sequence[str], None] = "5c1e8a7b4d2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "household_members",
        sa.Column("household_size", sa.Integer(), nullable=False, server_default="1"),
    )
    op.add_column(
        "household_members",
        sa.Column(
            "activity_level", sa.String(), nullable=False, server_default="sedentary"
        ),
    )
    op.add_column(
        "household_members",
        sa.Column("maintenance_calories", sa.Integer(), nullable=True),
    )
    op.add_column(
        "household_members",
        sa.Column("target_calories", sa.Integer(), nullable=True),
    )
    op.add_column(
        "household_members",
        sa.Column(
            "macro_focus", sa.String(), nullable=False, server_default="balanced"
        ),
    )


def downgrade() -> None:
    op.drop_column("household_members", "macro_focus")
    op.drop_column("household_members", "target_calories")
    op.drop_column("household_members", "maintenance_calories")
    op.drop_column("household_members", "activity_level")
    op.drop_column("household_members", "household_size")
