"""Create content column

Revision ID: 5e8b6bff2e03
Revises: 9f82a4d94d5f
Create Date: 2023-01-11 16:34:41.995696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e8b6bff2e03'
down_revision = '9f82a4d94d5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
