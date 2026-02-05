"""new votes table

Revision ID: 959f2c73ec23
Revises: 73fb6c9990cc
Create Date: 2026-02-05 20:04:36.837400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '959f2c73ec23'
down_revision: Union[str, Sequence[str], None] = '73fb6c9990cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
