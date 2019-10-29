import falcon

from routing import make_route


app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True
app.resp_options.secure_cookies_by_default = False

make_route(app)
