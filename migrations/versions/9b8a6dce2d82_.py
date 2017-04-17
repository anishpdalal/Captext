"""empty message

Revision ID: 9b8a6dce2d82
Revises: 
Create Date: 2017-03-13 21:04:18.062065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8a6dce2d82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('keywords', sa.String(length=500), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entries')
    # ### end Alembic commands ###