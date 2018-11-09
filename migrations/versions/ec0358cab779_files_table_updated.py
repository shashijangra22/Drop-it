"""files table updated

Revision ID: ec0358cab779
Revises: 5ccb612c7f12
Create Date: 2018-11-09 14:47:04.436952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec0358cab779'
down_revision = '5ccb612c7f12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('isFile', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'isFile')
    # ### end Alembic commands ###
