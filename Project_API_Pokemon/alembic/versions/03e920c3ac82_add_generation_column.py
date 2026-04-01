"""add generation column

Revision ID: 03e920c3ac82
Revises: b288f813060e
Create Date: 2026-03-15 23:47:22.986886
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '03e920c3ac82'
down_revision: Union[str, Sequence[str], None] = 'b288f813060e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('pokemon', sa.Column('image_path', sa.String(), nullable=True))

def downgrade():
    op.drop_column('pokemon', 'image_path')
