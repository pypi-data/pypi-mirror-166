from marshmallow import Schema, fields


class WorkflowSchema(Schema):
    name = fields.Str()
    part_id = fields.Int()
