"""removed  column Employees.age

Revision ID: 941fdf6d0207
Revises: 1411e5e5172c
Create Date: 2022-04-20 21:23:26.247416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '941fdf6d0207'
down_revision = '1411e5e5172c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('age')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###