import logging
import typing

import flask_restful
import humps
from flask import request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import PixelPermissions
from FacebookPixels.Api.commands import PixelsInsightsCommand
from FacebookPixels.Api.command_handlers import PixelsInsightsCommandHandler
from FacebookPixels.Api.dtos import PixelsInsightsCatalogsDto
from FacebookPixels.Api.mappings import PixelsInsightsCommandMapping
from FacebookPixels.Api.startup import config, fixtures

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class PixelsInsightsCatalogs(Resource):
    @fixtures.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        try:
            return PixelsInsightsCatalogsDto.pixels, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve pixel insights breakdowns."}, 400


class CustomConversionsInsightsCatalogs(Resource):
    @fixtures.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        try:
            return PixelsInsightsCatalogsDto.custom_conversions, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve custom conversion insights breakdowns."}, 400


class PixelsInsights(Resource):
    @fixtures.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def post(self, level: typing.AnyStr = None):
        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = PixelsInsightsCommandMapping(target=PixelsInsightsCommand)
            command = mapping.load(raw_request)
            command.level = level
            command.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400

        try:
            return object_to_json(PixelsInsightsCommandHandler.handle(command)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return (Tools.create_error(e, code="POTTER_BAD_REQUEST")), 400
