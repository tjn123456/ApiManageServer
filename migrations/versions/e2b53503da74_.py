"""empty message

Revision ID: e2b53503da74
Revises: 35295758267d
Create Date: 2018-09-04 10:41:35.990237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2b53503da74'
down_revision = '35295758267d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_info', sa.Column('status', sa.String(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('api_info', 'status')
    # ### end Alembic commands ###