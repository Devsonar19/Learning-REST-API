"""adding user table

Revision ID: 998fe0b736c7
Revises: 45beb75b1d15
Create Date: 2026-02-04 22:47:04.345777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '998fe0b736c7'
down_revision: Union[str, Sequence[str], None] = '45beb75b1d15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()',),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.execute("UPDATE posts SET content = '' WHERE content IS NULL")
    pass
    

def downgrade() -> None:
    op.drop_table('users')
    pass
