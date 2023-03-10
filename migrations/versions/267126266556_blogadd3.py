"""blogadd3

Revision ID: 267126266556
Revises: e733429f9ce2
Create Date: 2023-01-25 16:30:06.442491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '267126266556'
down_revision = 'e733429f9ce2'
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
