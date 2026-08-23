"""add_prep_detail_steps

Revision ID: 1272a7f54636
Revises: 699ec9e1324f
Create Date: 2026-08-17 23:02:58.792483

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision: str = "1272a7f54636"
down_revision: Union[str, Sequence[str], None] = "699ec9e1324f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "meals",
        sa.Column("prep_detail_steps", sa.Text(), nullable=False, server_default="[]"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("meals", "prep_detail_steps")
