from marshmallow import Schema, fields
from ..bbox_coord_schema import BboxCoordAttrsSchema
from ..bbox_pixels_coord_schema import BboxPixelsCoordAttrsSchema
from ..category_schema import CategoryAttrsSchema
from ..inferred_schema import InferredAttrsSchema


class DetectionSchema(Schema):
    bbox_coord = fields.Nested(BboxCoordAttrsSchema())
    bbox_pixels_coord = fields.Nested(BboxPixelsCoordAttrsSchema())
    bbox_pixels_coord_area = fields.Int()
    category = fields.Nested(CategoryAttrsSchema())
    score = fields.Float()
    inferred = fields.Nested(InferredAttrsSchema())
