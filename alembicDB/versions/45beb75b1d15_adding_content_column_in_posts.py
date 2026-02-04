"""adding content column in posts

Revision ID: 45beb75b1d15
Revises: 59f9c8083056
Create Date: 2026-02-04 21:58:02.110210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45beb75b1d15'
down_revision: Union[str, Sequence[str], None] = '59f9c8083056'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False, server_default='')
    )
    op.execute("UPDATE posts SET content = '' WHERE content IS NULL")
    op.alter_column(
        'posts',
        'content',
        server_default=None
    )
    


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
    pass
