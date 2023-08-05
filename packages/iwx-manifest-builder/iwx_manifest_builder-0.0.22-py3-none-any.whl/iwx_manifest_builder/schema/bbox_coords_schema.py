from marshmallow import Schema, fields


class BboxCoordsAttrsSchema(Schema):
    min_lat = fields.Float()
    max_lat = fields.Float()
    min_lon = fields.Float()
    max_lon = fields.Float()


class BboxCoordsSchema(Schema):
    bbox_coords = fields.Nested(BboxCoordsAttrsSchema())
