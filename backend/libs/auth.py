import redis

import falcon
import hashlib

from config import config
from models.user import User, UserType


Redis = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_user(user_session):

    user_id = Redis.get(user_session)

    if not user_id:
        raise falcon.HTTPUnauthorized()

    return (
        User.query.filter(User.id == user_id).one_or_none()
    )


def auth_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user or not user.is_active:
        raise falcon.HTTPUnauthorized()

    resource.user = user


def manager_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user or not user.is_active:
        raise falcon.HTTPUnauthorized()

    if not user.type == UserType.MANAGER:
        raise falcon.HTTPForbidden()

    resource.user = user


def make_session(credential, user_data, user_id):

    user_credential = credential+config['secure']['salt_session']+user_data

    session = hashlib.sha256(user_credential.encode()).hexdigest()

    Redis.set(session, user_id)

    return session


def remove_session(session):

    Redis.delete(session)
