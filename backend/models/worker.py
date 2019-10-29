from random import randint
from enum import Enum
from falcon import HTTPNotFound

from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import BigInteger, String, Enum as EnumField, Boolean

from models import Base
from libs.barcodes import calculate_checksum


class WorkerType(Enum):

    COLLECTOR = 1
    INSPECTOR = 2


class Worker(Base):

    __tablename__ = "worker"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    ean13 = Column(BigInteger, unique=True, nullable=False)
    password = Column(String, nullable=False)

    name = Column(String)
    surname = Column(String)
    middle_name = Column(String)

    type = Column(EnumField(WorkerType), nullable=False)

    deleted = Column(Boolean(), default=False, nullable=False)

    @staticmethod
    def get_by_code(code):
        return Worker.query.filter(
            Worker.ean13 == code,
            Worker.deleted.is_(False)
        ).one_or_none()

    def is_password_valid(self, password):
        return str(password) == str(self.password)

    @staticmethod
    def get_by_code_or_not_found(code):
        worker = Worker.get_by_code(code)
        if worker is None:
            raise HTTPNotFound(
                description={
                    "error_code": 201,
                    "error_message": "Рабочий с таким кодом не найден"
                }
            )
        return worker

    @staticmethod
    def generate_worker_password():
        prefix = '299'
        body = randint(000000000, 999999999)
        code = prefix + str(body)
        checksum = calculate_checksum(code)

        return code + str(checksum)
