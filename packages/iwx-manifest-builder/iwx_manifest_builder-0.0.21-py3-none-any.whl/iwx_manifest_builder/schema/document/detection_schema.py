from marshmallow import Schema, fields
from ..bbox_coords_schema import BboxCoordsAttrsSchema
from ..bbox_pixels_schema import BboxPixelsAttrsSchema
from ..category_schema import CategoryAttrsSchema
from ..maxar_features_schema import MaxarFeaturesAttrsSchema
from ..inferred_schema import InferredAttrsSchema


class DetectionSchema(Schema):
    bbox_coords = fields.Nested(BboxCoordsAttrsSchema())
    bbox_pixels = fields.Nested(BboxPixelsAttrsSchema())
    bbox_pixels_area = fields.Int()
    category = fields.Nested(CategoryAttrsSchema())
    feature = fields.Nested(MaxarFeaturesAttrsSchema())
    score = fields.Float()
    inferred = fields.Nested(InferredAttrsSchema())
