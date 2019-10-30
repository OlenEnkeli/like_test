from resources.index import IndexController
from resources.auth import (
    ManagerLoginController, WorkerLoginController, CurrentUserController
)


def make_route(app):

    app.add_route('/', IndexController())
    app.add_route('/login/worker', WorkerLoginController())
    app.add_route('/login/manager', ManagerLoginController())
    app.add_route('/users/current', CurrentUserController())
