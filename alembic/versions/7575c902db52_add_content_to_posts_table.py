"""add content to posts table

Revision ID: 7575c902db52
Revises: 36048a8db0be
Create Date: 2022-10-15 21:40:22.495867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7575c902db52'
down_revision = '36048a8db0be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
