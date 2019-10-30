from marshmallow import fields, Schema

from schemas.user import WorkerExtendedSchema


class ProductivitySchema(Schema):
    pass


for hour in range(0, 24):
    ProductivitySchema._declared_fields[str(hour)] = fields.Integer()


class ProductivityPublicSchema(Schema):

    worker = fields.Nested(WorkerExtendedSchema)
    productivity = fields.Nested(ProductivitySchema)
