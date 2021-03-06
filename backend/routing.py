from resources.index import IndexController
from resources.auth import (
    ManagerLoginController, WorkerLoginController,
    CurrentUserController, LogoutController
)
from resources.productivity import ProductivityController, WorkDateController


def make_route(app):

    app.add_route('/', IndexController())
    app.add_route('/logout', LogoutController())
    app.add_route('/login/worker', WorkerLoginController())
    app.add_route('/login/manager', ManagerLoginController())
    app.add_route('/users/current', CurrentUserController())
    app.add_route('/productivity', ProductivityController())
    app.add_route('/workdate', WorkDateController())
