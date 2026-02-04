"""add foreign-key to posts table

Revision ID: 93bda34972fa
Revises: 998fe0b736c7
Create Date: 2026-02-05 00:02:47.855149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93bda34972fa'
down_revision: Union[str, Sequence[str], None] = '998fe0b736c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
            'posts_users_fk',
            source_table='posts',
            referent_table='users',
            local_cols=['owner_id'],
            remote_cols=['id'],
            ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint(
        'posts_users_fk',
        table_name='posts'
    )
    op.drop_column(
        'posts',
        'owner_id'
    )
    pass
