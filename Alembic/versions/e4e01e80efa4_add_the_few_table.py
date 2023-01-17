"""add the few table 

Revision ID: e4e01e80efa4
Revises: d33a0801e6cb
Create Date: 2023-01-16 12:10:24.964631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4e01e80efa4'
down_revision = 'd33a0801e6cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'
    ),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.text('NOW()')
    ),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
