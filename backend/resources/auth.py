import hashlib

import falcon

from models.user import User
from models.manager import Manager
from libs.auth import make_session, auth_required, remove_session
from libs.schema import with_body_params
from schemas.user import ManagerLoginSchema, UserPublicSchema
from config import config


class ManagerLoginController(object):

    @with_body_params(ManagerLoginSchema)
    def on_post(self, req, resp):

        login = req.parsed['login']
        password = req.parsed['password']+config['secure']['salt_password']

        user = (
            User
            .query
            .join(Manager)
            .filter(Manager.login == login)
            .filter(Manager.password == hashlib.sha256(password.encode()).hexdigest())
            .one_or_none()
        )

        if not user:
            raise falcon.HTTPUnauthorized()

        try:
            resp.set_cookie(
                'user_session',
                make_session(
                    credential=login,
                    user_data=req.host+req.user_agent,
                    user_id=user.id
                ),
                path='/'
            )
        except Exception:
            raise falcon.HTTPUnauthorized()


class WorkerLoginController(object):

    def on_post(self, req, resp):

        raise falcon.HTTPNotFound(description='Not implemented')


class LogoutController(object):
    
    @falcon.before(auth_required)
    def on_get(self, req, resp):

        remove_session(req.cookies['user_session'])


class CurrentUserController(object):

    @falcon.before(auth_required)
    def on_get(self, req, resp):

        resp.body = UserPublicSchema().dumps(self.user)
