"""add endtime in medialabel unique constraint

Revision ID: d4da2311e4ae
Revises: a9db58bd03dc
Create Date: 2021-06-26 20:49:01.765178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd4da2311e4ae'
down_revision = 'a9db58bd03dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_medialabel', 'medialabel', type_='unique')
    op.create_unique_constraint(None, 'medialabel', ['begin_time', 'end_time', 'media_id', 'label_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'medialabel', type_='unique')
    op.create_unique_constraint('unique_medialabel', 'medialabel', ['begin_time', 'media_id', 'label_id'])
    # ### end Alembic commands ###
