"""add user table

Revision ID: a7a06d1f7cd2
Revises: 7575c902db52
Create Date: 2022-10-15 21:49:16.496500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7a06d1f7cd2'
down_revision = '7575c902db52'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('create_at', sa.TIMESTAMP(timezone=True),
                server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
            )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
