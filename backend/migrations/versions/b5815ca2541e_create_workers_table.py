from enum import Enum

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

revision = 'b5815ca2541e'
down_revision = None
branch_labels = None
depends_on = None


class WorkerType(Enum):

    COLLECTOR = 1
    INSPECTOR = 2


def upgrade():

    op.create_table(
        'worker',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('ean13', sa.BigInteger, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('type', ENUM(WorkerType, name="worker_type"), nullable=False)
    )


def downgrade():

    op.drop_table('worker')
