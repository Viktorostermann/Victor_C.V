"""add types and abilities columns

Revision ID: f91c33100cd6
Revises: 
Create Date: 2026-03-15 23:33:22.880279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f91c33100cd6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('pokemon', sa.Column('types', sa.String(length=100)))
    op.add_column('pokemon', sa.Column('abilities', sa.String(length=100)))

def downgrade() -> None:
    op.drop_column('pokemon', 'types')
    op.drop_column('pokemon', 'abilities')
