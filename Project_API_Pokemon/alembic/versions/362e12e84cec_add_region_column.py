"""add region column

Revision ID: 362e12e84cec
Revises: 03e920c3ac82
Create Date: 2026-03-16 00:07:07.748122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '362e12e84cec'
down_revision: Union[str, Sequence[str], None] = '03e920c3ac82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('pokemon', sa.Column('region', sa.String(100)))

def downgrade() -> None:
    op.drop_column('pokemon', 'region')
