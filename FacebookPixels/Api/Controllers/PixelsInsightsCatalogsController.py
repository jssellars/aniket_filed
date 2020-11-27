import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict, request_as_log_dict_nested, log_message_as_dict
from Core.Web.Security.Permissions import PixelPermissions
from FacebookPixels.Api.Dtos.PixelsInsightsCatalogsDto import PixelsInsightsCatalogsDto
from FacebookPixels.Api.Startup import logger, startup


import logging

logger_native = logging.getLogger(__name__)


class PixelsInsightsCatalogsEndpoint(Resource):
    @startup.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        logger.logger.info(request_as_log_dict_nested(request))
        try:
            response = PixelsInsightsCatalogsDto.pixels
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="PixelsInsightsCatalogsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            response = json.dumps({"message": "Failed to retrieve pixel insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')


class CustomConversionsInsightsCatalogsEndpoint(Resource):
    @startup.authorize_permission(permission=PixelPermissions.CAN_ACCESS_PIXELS)
    def get(self):
        logger.logger.info(request_as_log_dict_nested(request))
        try:
            response = PixelsInsightsCatalogsDto.custom_conversions
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="CustomConversionsInsightsCatalogsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            response = json.dumps({"message": "Failed to retrieve custom conversion insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')
