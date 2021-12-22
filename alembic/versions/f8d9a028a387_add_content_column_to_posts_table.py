"""add content column to posts table

Revision ID: f8d9a028a387
Revises: d512e6edbfa1
Create Date: 2021-12-22 16:51:02.796790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8d9a028a387'
down_revision = 'd512e6edbfa1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
