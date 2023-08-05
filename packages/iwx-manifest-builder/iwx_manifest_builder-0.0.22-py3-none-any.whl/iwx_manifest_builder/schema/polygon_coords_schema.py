from marshmallow import Schema, fields


class PolygonCoordsSchema(Schema):
    polygon_coords = fields.List(fields.List(fields.Float(default=0)))
