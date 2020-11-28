"""empty message

Revision ID: 415947efc650
Revises: d04a972bd549
Create Date: 2020-11-22 15:08:40.666167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '415947efc650'
down_revision = 'd04a972bd549'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('correct_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('correctanswer', sa.Float(), nullable=True),
    sa.Column('n_reg', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('correct_answer')
    # ### end Alembic commands ###
