#!./env/bin/python3

from random import randrange
import datetime as dt
import hashlib

from models.user import User, UserType
from models.manager import Manager
from models.worker import Worker, WorkerType
from models.activity_log import ActivityLog, ActivityStatus, ActivityType
from config import config


ACITIVITY_START_DATE = dt.date(year=2018, month=1, day=1)
ACITIVITY_END_DATE = dt.date(year=2018, month=2, day=1)
WORKDAY_START_TIME = dt.time(hour=8)
WORKDAY_END_TIME = dt.time(hour=19, minute=30)
BOX_COLLECT_TIME_MIN = dt.timedelta(minutes=40)
BOX_COLLECT_TIME_MAX = dt.timedelta(hours=1, minutes=10)
BOX_REVIEW_TIME_MIN = dt.timedelta(minutes=5)
BOX_REVIEW_TIME_MAX = dt.timedelta(minutes=7)
BOX_PAYLOAD_MIN = 10000
BOX_PAYLOAD_MAX = 14000


def make_user(type, name, surname, middle_name, password=None, worker_type=None, login=None, ean13=None):

    if type == UserType.MANAGER:

        if not login or not password:
            return None

        user = User()
        user.type = UserType.MANAGER
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

        print('Created manager {0} {1} with login {2}.'.format(name, surname, login))

        return user

    else:

        if not ean13 or not worker_type:
            return None

        user = User()
        user.type = UserType.WORKER
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

        print('Created {0} {1} {2} with ean13 {3}.'.format(
            worker_type.name.swapcase(), name, surname, ean13)
        )

        return user


class ActivityGenerator:

    def __init__(
        self, manager, inspector, collectors, workday_start, workday_end,
        box_collect_time_min, box_collect_time_max,
        box_review_time_min, box_review_time_max,
        box_payload_min, box_payload_max
    ):

        self.manager = manager
        self.inspector = inspector
        self.collectors = collectors
        self.workday_start = workday_start
        self.workday_end = workday_end
        self.box_collect_time_min = box_collect_time_min
        self.box_collect_time_max = box_collect_time_max
        self.box_review_time_min = box_review_time_min
        self.box_review_time_max = box_review_time_max
        self.box_payload_min = box_payload_min
        self.box_payload_max = box_payload_max

    def make_collect(self, collector, box_code, datetime):

        time = self.collect_time

        activity = ActivityLog()
        activity.local_time = datetime + time
        activity.server_time = datetime + time
        activity.box_code = box_code + 1
        activity.type = ActivityType.COLLECT
        activity.payload = collector.worker.ean13
        activity.status = ActivityStatus.SUCCESS
        activity.worker_id = collector.worker.id
        activity.save()
        activity.db_session.commit()

        time += self.make_review(collector, box_code, datetime + time)

        return time

    def make_review(self, collector, box_code, datetime):

        time = self.review_time

        activity = ActivityLog()
        activity.local_time = datetime + time
        activity.server_time = datetime + time
        activity.box_code = box_code + 1
        activity.type = ActivityType.REVIEW
        activity.payload = self.box_payload
        activity.status = ActivityStatus.SUCCESS
        activity.worker_id = inspector.worker.id
        activity.save()
        activity.db_session.commit()

        return time

    @property
    def collect_time(self):

        return dt.timedelta(seconds=(
            randrange(
                self.box_collect_time_min.total_seconds(),
                self.box_collect_time_max.total_seconds(),
                1
            )
        ))

    @property
    def review_time(self):

        return dt.timedelta(seconds=(
            randrange(
                self.box_review_time_min.total_seconds(),
                self.box_review_time_max.total_seconds(),
                1
            )
        ))

    @property
    def box_payload(self):

        return randrange(
            self.box_payload_min,
            self.box_payload_max,
            1
        )

    def make_activity(self, start_at, ended_at):

        current_dt = dt.datetime.combine(start_at, self.workday_start)
        box_last_id = 1

        while current_dt < dt.datetime.combine(ended_at, self.workday_end):

            if (current_dt + self.box_collect_time_max).time() > self.workday_end:
                current_dt = dt.datetime.combine(
                    current_dt.date() + dt.timedelta(days=1), self.workday_start
                )

            if current_dt.weekday() == 5:
                current_dt = dt.datetime.combine(
                    current_dt.date() + dt.timedelta(days=2), self.workday_start
                )

            times = []

            for collector in self.collectors:
                times.append(self.make_collect(collector, box_last_id, current_dt))
                box_last_id += 1

            current_dt += max(times)


print('Creating users ...')

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

print('Creating activities ...')

generator = ActivityGenerator(
    manager, inspector, [collector1, collector2, collector3],
    WORKDAY_START_TIME, WORKDAY_END_TIME,
    BOX_COLLECT_TIME_MIN, BOX_COLLECT_TIME_MAX,
    BOX_REVIEW_TIME_MIN, BOX_REVIEW_TIME_MAX,
    BOX_PAYLOAD_MIN, BOX_PAYLOAD_MAX
)

generator.make_activity(ACITIVITY_START_DATE, ACITIVITY_END_DATE)

print('Acitities was created!')
