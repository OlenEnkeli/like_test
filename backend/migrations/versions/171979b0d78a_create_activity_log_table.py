"""create activity log table

Revision ID: 171979b0d78a
Revises: b5815ca2541e
Create Date: 2019-10-29 20:33:13.934593

"""
import datetime as dt

from enum import Enum

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects.postgresql import ENUM


class ActivityType(Enum):

    SELECT_CONTENT_TYPE = 1
    COLLECT = 2
    REVIEW = 3


class ActivityStatus(Enum):

    SUCCESS = 1
    ERROR_CONTENT_TYPE_NOT_FOUND = 2
    ERROR_COLLECTOR_NOT_FOUND = 3
    ERROR_DUPLICATED = 4


# revision identifiers, used by Alembic.
revision = '171979b0d78a'
down_revision = 'b5815ca2541e'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'activity_log',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('box_code', sa.BigInteger),
        sa.Column('worker_id', sa.BigInteger, sa.ForeignKey('worker.id')),
        sa.Column('payload', sa.Integer),
        sa.Column('type', ENUM(ActivityType, name="activity_type")),
        sa.Column('status', ENUM(ActivityStatus, name="activity_status")),
        sa.Column('local_time', sa.DateTime()),
        sa.Column('server_time', sa.DateTime(), default=dt.datetime.now())
    )


def downgrade():

    op.drop_table('worker')
