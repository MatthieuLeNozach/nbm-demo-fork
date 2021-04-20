"""Add column invalid_label_text to MediaLabel model

Revision ID: ccc3ff2274d0
Revises: 4a996e29c713
Create Date: 2021-03-28 10:12:19.443600

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ccc3ff2274d0'
down_revision = '4a996e29c713'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('device', 'model_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('media', 'begin_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('media', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('media', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('medialabel', sa.Column('invalid_label_text', sa.String(), nullable=True))
    op.alter_column('medialabel', 'begin_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('medialabel', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('medialabel', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('medialabel', 'end_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('medialabel', 'media_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('site', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('site', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('site', 'latitude',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('site', 'longitude',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('site', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_site_created_by', table_name='site')
    op.drop_index('ix_site_locality_precision', table_name='site')
    op.drop_index('ix_site_updated_by', table_name='site')
    op.alter_column('species', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('standardlabel', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('standardlabel', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('standardlabel', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('standardlabel', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('standardlabel', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('standardlabel', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('species', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_index('ix_site_updated_by', 'site', ['updated_by'], unique=False)
    op.create_index('ix_site_locality_precision', 'site', ['locality_precision'], unique=False)
    op.create_index('ix_site_created_by', 'site', ['created_by'], unique=False)
    op.alter_column('site', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('site', 'longitude',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('site', 'latitude',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('site', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('site', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('medialabel', 'media_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('medialabel', 'end_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('medialabel', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('medialabel', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('medialabel', 'begin_time',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_column('medialabel', 'invalid_label_text')
    op.alter_column('media', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('media', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('media', 'begin_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('device', 'model_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###