"""add foriegn-key to posts table

Revision ID: 7dd298e51702
Revises: a7a06d1f7cd2
Create Date: 2022-10-15 21:58:13.099919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd298e51702'
down_revision = 'a7a06d1f7cd2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
