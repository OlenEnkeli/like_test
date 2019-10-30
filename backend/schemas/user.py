from marshmallow import Schema, fields



class ManagerLoginSchema(Schema):

    login = fields.String(required=True)
    password = fields.String(required=True)


class UserPublicSchema(Schema):

    id = fields.Integer()

    name = fields.String()
    middle_name = fields.String()
    surname = fields.String()

    type = fields.Function(lambda obj: obj.type.name.swapcase())