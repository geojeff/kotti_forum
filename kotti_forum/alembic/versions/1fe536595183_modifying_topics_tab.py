"""modifying topics table

Revision ID: 1fe536595183
Revises: None
Create Date: 2012-11-17 09:09:38.193663

"""

# revision identifiers, used by Alembic.
revision = '1fe536595183'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('topics', sa.Column('votable', sa.Boolean))


def downgrade():
    pass
