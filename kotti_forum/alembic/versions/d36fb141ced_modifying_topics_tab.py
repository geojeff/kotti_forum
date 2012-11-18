"""modifying topics table to add sort_order_is_ascending

Revision ID: d36fb141ced
Revises: 1fe536595183
Create Date: 2012-11-18 07:13:16.495703

"""

# revision identifiers, used by Alembic.
revision = 'd36fb141ced'
down_revision = '1fe536595183'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('topics', sa.Column('sort_order_is_ascending', sa.Boolean))


def downgrade():
    op.drop_column('topics', 'votable')
