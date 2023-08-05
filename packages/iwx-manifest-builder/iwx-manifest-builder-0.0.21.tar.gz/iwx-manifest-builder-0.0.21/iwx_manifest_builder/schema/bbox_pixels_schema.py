from marshmallow import Schema, fields


class BboxPixelsAttrsSchema(Schema):
    min_x = fields.Int()
    max_x = fields.Int()
    min_y = fields.Int()
    max_y = fields.Int()


class BboxPixelsSchema(Schema):
    bbox_pixels = fields.Nested(BboxPixelsAttrsSchema())
    bbox_pixel_area = fields.Int()
