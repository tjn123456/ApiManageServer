"""empty message

Revision ID: caa1068afb74
Revises: 
Create Date: 2018-07-16 15:20:15.417044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caa1068afb74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apicase_info', sa.Column('apicasedetail', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apicase_info', 'apicasedetail')
    # ### end Alembic commands ###
