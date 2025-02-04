"""Delete masked_coord column

Revision ID: f96766b34008
Revises: c66154026535
Create Date: 2021-02-26 18:39:42.698178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f96766b34008'
down_revision = 'c66154026535'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_site_masked_coord', table_name='site')
    op.drop_column('site', 'masked_coord')

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('masked_coord', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_index('ix_site_masked_coord', 'site', ['masked_coord'], unique=False)
    # ### end Alembic commands ###
