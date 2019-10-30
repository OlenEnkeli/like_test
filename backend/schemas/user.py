from marshmallow import Schema, fields


class ManagerLoginSchema(Schema):

    login = fields.String(required=True)
    password = fields.String(required=True)
