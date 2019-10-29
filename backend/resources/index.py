import json

from config import config


class IndexController(object):

    def on_get(self, req, resp):

        resp.body = json.dumps(config['project'])
