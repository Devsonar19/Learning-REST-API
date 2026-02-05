"""additional columns in posts table

Revision ID: 73fb6c9990cc
Revises: 93bda34972fa
Create Date: 2026-02-05 16:35:53.247782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73fb6c9990cc'
down_revision: Union[str, Sequence[str], None] = '93bda34972fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE',
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()'),
        )
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts', 'published'
    )
    op.drop_column(
        'posts', 'created_at'
    )
    pass
