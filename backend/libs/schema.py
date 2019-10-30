import json

import falcon

from marshmallow import Schema, fields


def with_body_params(*dec_args, **dec_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):

            if len(dec_args) == 1:
                schema = dec_args[0]
            else:
                schema = type('schema', (Schema,), {**dec_kwargs})

            try:
                load = schema().load(args[1].media)
            except Exception:
                raise falcon.HTTPUnprocessableEntity()

            args[1].parsed = load

            return func(*args, **kwargs)
        return wrapper
    return decorator
