"""blogadd5

Revision ID: a0dae3da21c6
Revises: 267126266556
Create Date: 2023-01-25 16:59:21.722474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0dae3da21c6'
down_revision = '267126266556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BlogMains', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'users', ['author'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BlogMains', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
