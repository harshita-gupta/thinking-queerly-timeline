"""empty message

Revision ID: b45dfca0b3c6
Revises: 822ac0b94648
Create Date: 2018-05-15 22:17:59.238992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b45dfca0b3c6'
down_revision = '822ac0b94648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_it', sa.Column('approved', sa.Boolean(), nullable=True))
    op.add_column('workshop_activity', sa.Column('enable_monitoring', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workshop_activity', 'enable_monitoring')
    op.drop_column('post_it', 'approved')
    # ### end Alembic commands ###
