from marshmallow import Schema, fields


class ManagerLoginSchema(Schema):

    login = fields.String(required=True)
    password = fields.String(required=True)


class WorkerSchema(Schema):

    id = fields.Integer()

    ean13 = fields.String()
    type = fields.Function(lambda obj: obj.type.name.swapcase())


class ManagerSchema(Schema):

    id = fields.String()
    login = fields.String()


class UserPublicSchema(Schema):

    id = fields.Integer()

    name = fields.String()
    middle_name = fields.String()
    surname = fields.String()

    type = fields.Function(lambda obj: obj.type.name.swapcase())

    is_active = fields.Boolean()
    deleted = fields.Boolean()

    manager = fields.Nested(ManagerSchema)
    worker = fields.Nested(WorkerSchema)


class WorkerExtendedSchema(Schema):

    id = fields.Integer()

    ean13 = fields.String()

    name = fields.String()
    middle_name = fields.String()
    surname = fields.String()
