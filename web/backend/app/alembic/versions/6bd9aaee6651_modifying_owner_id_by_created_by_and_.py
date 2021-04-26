"""modifying owner_id by created_by and some adjustments to the models

Revision ID: 6bd9aaee6651
Revises: 24853bd71dd8
Create Date: 2021-02-28 19:46:49.808525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6bd9aaee6651'
down_revision = '24853bd71dd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.drop_index('ix_media_owner_id', table_name='media')
    op.create_index(op.f('ix_media_updated_by'), 'media', ['updated_by'], unique=False)
    op.drop_constraint('media_owner_id_fkey', 'media', type_='foreignkey')
    op.create_foreign_key("fk_media_updated_by", 'media', 'user', ['updated_by'], ['id'])
    op.drop_column('media', 'owner_id')
    op.add_column('site', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('site', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('site', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.drop_index('ix_site_user_id', table_name='site')
    op.create_index(op.f('ix_site_created_by'), 'site', ['created_by'], unique=False)
    op.create_index(op.f('ix_site_updated_by'), 'site', ['updated_by'], unique=False)
    op.drop_constraint('site_user_id_fkey', 'site', type_='foreignkey')
    op.create_foreign_key("fk_site_updated_by", 'site', 'user', ['updated_by'], ['id'])
    op.create_foreign_key("fk_site_created_by", 'site', 'user', ['created_by'], ['id'])
    op.drop_column('site', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint("fk_site_created_by", 'site', type_='foreignkey')
    op.drop_constraint("fk_site_updated_by", 'site', type_='foreignkey')
    op.create_foreign_key('site_user_id_fkey', 'site', 'user', ['user_id'], ['id'])
    op.drop_index(op.f('ix_site_updated_by'), table_name='site')
    op.drop_index(op.f('ix_site_created_by'), table_name='site')
    op.create_index('ix_site_user_id', 'site', ['user_id'], unique=False)
    op.drop_column('site', 'updated_by')
    op.drop_column('site', 'updated_at')
    op.drop_column('site', 'created_by')
    op.add_column('media', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint("fk_media_updated_by", 'media', type_='foreignkey')
    op.create_foreign_key('media_owner_id_fkey', 'media', 'user', ['owner_id'], ['id'])
    op.drop_index(op.f('ix_media_updated_by'), table_name='media')
    op.create_index('ix_media_owner_id', 'media', ['owner_id'], unique=False)
    op.drop_column('media', 'updated_by')
    # ### end Alembic commands ###
