from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, String, Enum as EnumField

from models import Base


class Manager(Base):

    __tablename__ = 'manager'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
