"""History table for downloads

Revision ID: c5ded65bfc5f
Revises: a9db58bd03dc
Create Date: 2021-06-26 21:25:34.886360

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5ded65bfc5f'
down_revision = 'd4da2311e4ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('historytable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('most_recent_downloaded_file', sa.DateTime(), nullable=True),
    sa.Column('download_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('historytable')
    # ### end Alembic commands ###
