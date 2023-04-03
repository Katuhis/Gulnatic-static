from marshmallow import Schema, fields


class VersionSchema(Schema):
    _id = fields.Str(load_only=True)
    number = fields.String(required=True)
    dateUpload = fields.DateTime(required=True)
    status = fields.Bool(required=True)
