"""add local household profiles

Revision ID: 5c1e8a7b4d2f
Revises: 3b7f0f9a2c1e
Create Date: 2026-09-20 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

revision: str = "5c1e8a7b4d2f"
down_revision: Union[str, Sequence[str], None] = "3b7f0f9a2c1e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "households",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_households_id"), "households", ["id"], unique=False)
    op.create_index(op.f("ix_households_name"), "households", ["name"], unique=True)
    op.create_table(
        "household_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("household_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("profile", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_household_members_id"), "household_members", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_household_members_household_id"),
        "household_members",
        ["household_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_household_members_household_id"), table_name="household_members"
    )
    op.drop_index(op.f("ix_household_members_id"), table_name="household_members")
    op.drop_table("household_members")
    op.drop_index(op.f("ix_households_name"), table_name="households")
    op.drop_index(op.f("ix_households_id"), table_name="households")
    op.drop_table("households")
