import datetime as dt

import falcon

from sqlalchemy import extract
from sqlalchemy.orm import aliased
from sqlalchemy.sql import functions

from libs.auth import manager_required
from models.user import User, UserType
from models.manager import Manager
from models.worker import Worker, WorkerType
from models.activity_log import ActivityLog, ActivityType
from schemas.productivity import (
    ProductivityPublicSchema, ProductivitySchema, WorkdayPublicSchema
)


class ProductivityController(object):

    @falcon.before(manager_required)
    def on_get(self, req, resp):

        if 'date' not in req.params:
            raise falcon.HTTPUnprocessableEntity()

        try:
            date = dt.datetime.strptime(req.params['date'], '%Y-%m-%d')
        except Exception:
            raise falcon.HTTPUnprocessableEntity()

        activity_alias = aliased(ActivityLog)

        activities = (
            self.db_session
            .query(
                functions.sum(ActivityLog.payload), activity_alias.worker_id,
                extract('hour', activity_alias.local_time)
            )
            .join(activity_alias, ActivityLog.box_code == activity_alias.box_code)
            .filter(ActivityLog.type == ActivityType.REVIEW)
            .filter(activity_alias.type == ActivityType.COLLECT)
            .filter(extract('year', activity_alias.local_time) == date.year)
            .filter(extract('month', activity_alias.local_time) == date.month)
            .filter(extract('day', activity_alias.local_time) == date.day)
            .group_by(
                extract('hour', activity_alias.local_time),
                activity_alias.worker_id
            )
            .order_by(activity_alias.worker_id)
            .all()
        )

        collectors = (
            User
            .query
            .join(Worker)
            .having(Worker.type == WorkerType.COLLECTOR)
            .filter(User.type == UserType.WORKER)
            .group_by(User.id, Worker.type)
            .all()
        )

        if not activities or not collectors:
            raise falcon.HTTPNotFound()

        activity_dict = {}
        result = []

        for activity in activities:
            if activity.worker_id in activity_dict.keys():
                activity_dict[activity.worker_id][str(int(activity[2]))] = activity[0]
            else:
                activity_dict[activity.worker_id] = {}

        for user in collectors:

            values = {}
            values['worker'] = {}
            values['worker']['id'] = user.worker.id
            values['worker']['ean13'] = user.worker.ean13
            values['worker']['name'] = user.name
            values['worker']['surname'] = user.surname
            values['worker']['middle_name'] = user.middle_name
            values['productivity'] = activity_dict[user.worker.id]

            result.append(values)

        resp.body = ProductivityPublicSchema(many=True).dumps(result)


class WorkDateController(object):

    @falcon.before(manager_required)
    def on_get(self, req, resp):

        dates = (
            self.db_session
            .query(
                functions.min(ActivityLog.local_time),
                functions.max(ActivityLog.local_time),
            ).all()
        )

        resp.body = WorkdayPublicSchema().dumps({
            'min_date': dates[0][0],
            'max_date': dates[0][1],
        })