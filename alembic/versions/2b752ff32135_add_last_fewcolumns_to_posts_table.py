"""add last fewcolumns to posts_table

Revision ID: 2b752ff32135
Revises: e00615b0d532
Create Date: 2025-10-21 20:26:03.404424

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b752ff32135"
down_revision: Union[str, Sequence[str], None] = "e00615b0d532"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "updated_at")
    pass
