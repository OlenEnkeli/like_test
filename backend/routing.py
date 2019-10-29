from resources.index import IndexController


def make_route(app):
    
    app.add_route('/', IndexController())