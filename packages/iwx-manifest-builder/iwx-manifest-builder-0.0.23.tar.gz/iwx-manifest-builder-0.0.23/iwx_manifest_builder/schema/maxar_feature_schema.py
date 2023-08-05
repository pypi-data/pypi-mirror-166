from marshmallow import Schema, fields


class MaxarFeatureAttrsSchema(Schema):
    acquisitionDate = fields.Str(allow_none=True, data_key="acquisition_date")
    acquisitionTime = fields.Int(data_key="acquisition_time")
    acquisitionType = fields.Str(allow_none=True, data_key="acquisition_type")
    antennaLookDirection = fields.Str(
        allow_none=True, data_key="antenna_look_direction"
    )
    ageDays = fields.Int(data_key="age_days")
    assetName = fields.Str(allow_none=True, data_key="asset_name")
    assetType = fields.Str(allow_none=True, data_key="asset_type")
    beamMode = fields.Str(allow_none=True, data_key="beam_mode")
    CE90Accuracy = fields.Str(allow_none=True, data_key="ce_90_accuracy")
    cloudCover = fields.Float(data_key="cloud_cover")
    colorBandOrder = fields.Str(allow_none=True, data_key="color_band_order")
    companyName = fields.Str(allow_none=True, data_key="company_name")
    copyright = fields.Str(allow_none=True, data_key="copyright")
    crsFromPixels = fields.Str(allow_none=True, data_key="crs_from_pixels")
    dataLayer = fields.Str(allow_none=True, data_key="data_layer")
    earliestAcquisitionDate = fields.Str(
        allow_none=True, data_key="earliest_acquisition_date"
    )
    factoryOrderNumber = fields.Str(allow_none=True, data_key="factory_order_number")
    featureId = fields.Str(allow_none=True, data_key="feature_id")
    formattedDate = fields.Str(allow_none=True, data_key="formatted_date")
    groundSampleDistance = fields.Float(data_key="ground_sample_distance")
    groundSampleDistanceUnit = fields.Str(
        allow_none=True, data_key="ground_sample_distance_unit"
    )
    ingestDate = fields.Str(allow_none=True, data_key="ingest_date")
    isBrowse = fields.Bool(data_key="is_browse")
    isMirrored = fields.Bool(data_key="is_mirrored")
    isMultipleWKB = fields.Bool(data_key="is_multiple_wkb")
    latestAcquisitionDate = fields.Str(
        allow_none=True, data_key="latest_acquisition_date"
    )
    legacyDescription = fields.Str(allow_none=True, data_key="legacy_description")
    legacyId = fields.Str(allow_none=True, data_key="legacy_id")
    licenseType = fields.Str(allow_none=True, data_key="license_type")
    niirs = fields.Float(data_key="niirs")
    offNadirAngle = fields.Float(data_key="off_nadir_angle")
    orbitDirection = fields.Str(allow_none=True, data_key="orbit_direction")
    outputMosaic = fields.Bool(data_key="output_mosaic")
    perPixelX = fields.Float(data_key="per_pixel_x")
    perPixelY = fields.Float(data_key="per_pixel_y")
    pixelsIngested = fields.Bool(data_key="pixels_ingested")
    polarisationChannel = fields.Str(allow_none=True, data_key="polarisation_channel")
    polarisationMode = fields.Str(allow_none=True, data_key="polarisation_mode")
    preciseGeometry = fields.Bool(data_key="precise_geometry")
    productType = fields.Str(allow_none=True, data_key="product_type")
    RMSEAccuracy = fields.Str(allow_none=True, data_key="rmse_accuracy")
    sensorType = fields.Str(allow_none=True, data_key="sensor_type")
    source = fields.Str(allow_none=True, data_key="source")
    sourceUnit = fields.Str(allow_none=True, data_key="source_unit")
    spatialAccuracy = fields.Str(allow_none=True, data_key="spatial_accuracy")
    sunAzimuth = fields.Float(data_key="sun_azimuth")
    sunElevation = fields.Float(data_key="sun_elevation")
    tagsAsString = fields.Str(allow_none=True, data_key="tags_as_string")
    url = fields.Str(allow_none=True, data_key="url")
    vendorName = fields.Str(allow_none=True, data_key="vendor_name")
    vendorReference = fields.Str(allow_none=True, data_key="vendor_reference")
    verticalAccuracy = fields.Str(allow_none=True, data_key="vertical_accuracy")


class MaxarFeatureSchema(Schema):
    feature = fields.Nested(MaxarFeatureAttrsSchema())
