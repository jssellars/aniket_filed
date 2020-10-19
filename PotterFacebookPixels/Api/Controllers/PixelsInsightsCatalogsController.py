import json

from flask import request, Response
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from PotterFacebookPixels.Api.Dtos.PixelsInsightsCatalogsDto import PixelsInsightsCatalogsDto
from PotterFacebookPixels.Api.Startup import logger


class PixelsInsightsCatalogsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = PixelsInsightsCatalogsDto.pixels
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="PixelsInsightsCatalogsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": "Failed to retrieve pixel insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')


class CustomConversionsInsightsCatalogsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = PixelsInsightsCatalogsDto.custom_conversions
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="CustomConversionsInsightsCatalogsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": "Failed to retrieve custom conversion insights breakdowns."})
            return Response(response=response, status=400, mimetype='application/json')
