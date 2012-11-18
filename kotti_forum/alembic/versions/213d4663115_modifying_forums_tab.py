"""modifying forums table to add sort_order_is_ascending

Revision ID: 213d4663115
Revises: d36fb141ced
Create Date: 2012-11-18 14:38:23.730268

"""

# revision identifiers, used by Alembic.
revision = '213d4663115'
down_revision = 'd36fb141ced'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('forums', sa.Column('sort_order_is_ascending', sa.Boolean))


def downgrade():
    op.drop_column('topics', 'sort_order_is_ascending')
