"""empty message

Revision ID: 120fa1592bc6
Revises: 6a65aa53d943
Create Date: 2018-05-24 14:12:23.554562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120fa1592bc6'
down_revision = '6a65aa53d943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('icon', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'icon')
    # ### end Alembic commands ###