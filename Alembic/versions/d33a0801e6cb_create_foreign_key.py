"""create Foreign key

Revision ID: d33a0801e6cb
Revises: 79f75a852d78
Create Date: 2023-01-16 12:04:15.187906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd33a0801e6cb'
down_revision = '79f75a852d78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", 
    local_cols=[
                    'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts','owner_id') 
    pass
