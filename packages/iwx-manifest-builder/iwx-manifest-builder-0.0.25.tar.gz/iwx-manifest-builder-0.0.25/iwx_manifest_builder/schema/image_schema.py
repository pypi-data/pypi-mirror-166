from marshmallow import Schema, fields
from .bbox_coord_schema import BboxCoordAttrsSchema
from .maxar_feature_schema import MaxarFeatureAttrsSchema


class ImageAttrsSchema(Schema):
    name = fields.Str()
    width = fields.Int()
    height = fields.Int()
    resolution = fields.Float()
    bbox_coord = fields.Nested(BboxCoordAttrsSchema())
    feature = fields.Nested(MaxarFeatureAttrsSchema())


class ImageSchema(Schema):
    image = fields.Nested(ImageAttrsSchema())
