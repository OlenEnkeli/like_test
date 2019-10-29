"""create manager table

Revision ID: 03e1b462ddcf
Revises: a9764a6fa33f
Create Date: 2019-10-29 21:41:38.540682

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '03e1b462ddcf'
down_revision = '171979b0d78a'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'manager',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade():

    op.drop_table('manager')