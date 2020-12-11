import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import PixelPermissions
from FacebookPixels.Api.Dtos.PixelsInsightsCatalogsDto import PixelsInsightsCatalogsDto
from FacebookPixels.Api.startup import config, fixtures


import logging

logger = logging.getLogger(__name__)


class PixelsInsightsCatalogsEndpoint(Resource):
    @fixtures.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = PixelsInsightsCatalogsDto.pixels
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": "Failed to retrieve pixel insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')


class CustomConversionsInsightsCatalogsEndpoint(Resource):
    @fixtures.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = PixelsInsightsCatalogsDto.custom_conversions
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": "Failed to retrieve custom conversion insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')
