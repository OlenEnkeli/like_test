from marshmallow import fields, Schema

from schemas.user import WorkerExtendedSchema


class ProductivitySchema(Schema):
    pass


for hour in range(0, 24):
    ProductivitySchema._declared_fields[str(hour)] = fields.Integer()


class ProductivityPublicSchema(Schema):

    worker = fields.Nested(WorkerExtendedSchema)
    productivity = fields.Nested(ProductivitySchema)


class WorkdayPublicSchema(Schema):

    min_date = fields.Date()
    max_date = fields.Date()
