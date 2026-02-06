"""added phone_number field

Revision ID: dcd763279a36
Revises: 959f2c73ec23
Create Date: 2026-02-05 20:14:54.684064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcd763279a36'
down_revision: Union[str, Sequence[str], None] = '959f2c73ec23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('phone_number', sa.String(), nullable=True)
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'users', 'phone_number'
    )
    pass
