"""Add new column content in posts table

Revision ID: 83f1116152d0
Revises: daaf462879bb
Create Date: 2024-12-01 11:49:55.715277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83f1116152d0'
down_revision: Union[str, None] = 'daaf462879bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', column_name='content')
    pass
