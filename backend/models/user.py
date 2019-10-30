from enum import Enum

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.sqltypes import BigInteger, String, Boolean, Enum as EnumField
from sqlalchemy.orm import relation

from models import Base
from models.worker import Worker
from models.manager import Manager


class UserType(Enum):

    MANAGER = 1
    WORKER = 2


class User(Base):

    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    worker_id = Column(BigInteger, ForeignKey('worker.id'))
    worker = relation('Worker')

    manager_id = Column(BigInteger, ForeignKey('manager.id'))
    manager = relation('Manager')

    name = Column(String)
    surname = Column(String)
    middle_name = Column(String)

    type = Column(EnumField(UserType), nullable=False)

    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False, nullable=False)

    @hybrid_property
    def entity(self):
        if self.type == UserType.MANAGER:
            return self.manager
        elif self.type == UserType.WORKER:
            return self.worker
        else:
            return None
