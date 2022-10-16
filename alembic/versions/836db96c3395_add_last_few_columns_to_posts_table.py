"""add last few columns to posts table

Revision ID: 836db96c3395
Revises: 7dd298e51702
Create Date: 2022-10-15 22:05:38.743282

"""
from contextlib import nullcontext
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '836db96c3395'
down_revision = '7dd298e51702'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column('create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
