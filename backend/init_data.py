#!./env/bin/python3

import hashlib

from models.user import User, UserType
from models.manager import Manager
from models.worker import Worker, WorkerType
from config import config


def make_user(type, name, surname, middle_name, password=None, worker_type=None, login=None, ean13=None):

    if type == UserType.MANAGER:

        if not login or not password:
            return None

        user = User()
        user.name = name
        user.surname = surname
        user.middle_name = middle_name
        user.manager = Manager()
        user.manager.login = login
        user.manager.password = (
            hashlib.sha256(
                (password + config['secure']['salt_password']).encode()
            ).hexdigest()
        )
        user.manager.save()
        user.save()
        user.db_session.commit()

        return user

    else:

        if not ean13 or not worker_type:
            return None

        user = User()
        user.name = name
        user.surname = surname
        user.middle_name = middle_name
        user.worker = Worker()
        user.worker.type = worker_type
        user.worker.ean13 = ean13
        user.worker.password = Worker.generate_worker_password()
        user.worker.save()
        user.save()
        user.db_session().commit()

        return user



print('Creating users...')

manager = make_user(
    type=UserType.MANAGER, name='Иван', surname='Иванов', middle_name='Иванович',
    password='qwerty', login='ivan666'
)

collector1 = make_user(
    type=UserType.WORKER, name='Федор', surname='Некариенко', middle_name='Алексеевич',
    worker_type=WorkerType.COLLECTOR, ean13='111111'
)

collector2 = make_user(
    type=UserType.WORKER, name='Николай', surname='Некариенко', middle_name='Алексеевич',
    worker_type=WorkerType.COLLECTOR, ean13='111123'
)

collector3 = make_user(
    type=UserType.WORKER, name='Вячеслав', surname='Романов', middle_name='Дмитриевич',
    worker_type=WorkerType.COLLECTOR, ean13='111125'
)

inspector = make_user(
    type=UserType.WORKER, name='Ева', surname='Хладнова', middle_name='Сергеевна',
    worker_type=WorkerType.INSPECTOR, ean13='111309'
)
