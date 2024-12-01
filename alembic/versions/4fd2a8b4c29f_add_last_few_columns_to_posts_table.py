"""add last few columns to posts table

Revision ID: 4fd2a8b4c29f
Revises: 2bc9b326224f
Create Date: 2024-12-01 12:21:46.703104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fd2a8b4c29f'
down_revision: Union[str, None] = '2bc9b326224f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', column_name='published')
    op.drop_column('posts', column_name='created_at')
    pass
