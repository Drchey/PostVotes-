"""add is_published

Revision ID: a2736c076ae0
Revises: 32ca0d3f8002
Create Date: 2025-10-21 19:59:45.529435

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2736c076ae0"
down_revision: Union[str, Sequence[str], None] = "32ca0d3f8002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("is_published", sa.Boolean, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "is_published")
    pass
