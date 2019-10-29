"""create user table

Revision ID: f811cb0887af
Revises: 03e1b462ddcf
Create Date: 2019-10-29 21:46:38.332469

"""
import sqlalchemy as sa

from enum import Enum

from alembic import op
from sqlalchemy.dialects.postgresql import ENUM


class UserType(Enum):

    MANAGER = 1
    WORKER = 2


# revision identifiers, used by Alembic.
revision = 'f811cb0887af'
down_revision = '03e1b462ddcf'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('worker_id', sa.BigInteger, sa.ForeignKey('worker.id')),
        sa.Column('manager_id', sa.BigInteger, sa.ForeignKey('manager.id')),
        sa.Column('name', sa.String),
        sa.Column('surname', sa.String),
        sa.Column('middle_name', sa.String),
        sa.Column('type', ENUM(UserType, name='user_type')),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('deleted', sa.Boolean, default=False, nullable=False)
    )


def downgrade():

    op.drop_table('user')
