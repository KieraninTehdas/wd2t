from datetime import date

from marshmallow import Schema, fields


class TagSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)


class DecisionSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    tags = fields.List(fields.Nested(TagSchema()))
    decided_on = fields.Date(missing=date.today())
