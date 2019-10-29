import falcon

from routing import make_route
from libs.db import SQLAlchemySessionManager


app = falcon.API(middleware=[
    SQLAlchemySessionManager(),
])

app.req_options.auto_parse_form_urlencoded = True
app.resp_options.secure_cookies_by_default = False

make_route(app)
