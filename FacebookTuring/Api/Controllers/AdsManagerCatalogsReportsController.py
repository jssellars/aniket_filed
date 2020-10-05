import json
from enum import Enum

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsBreakdownsDto import AdsManagerCatalogsReportsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDimensionsDto import AdsManagerCatalogsReportsDimensionsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDto import AdsManagerCatalogsReportsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsMetricsDto import AdsManagerCatalogsReportsMetricsDto
from FacebookTuring.Api.Startup import logger


class QueryParamsEnum(Enum):
    LEVEL_KEY = 'level'
    REPORT_KEY = 'report'
    DIMENSION_KEY = 'dimension'
    METRICS_KEY = 'metrics'


class AdsManagerReportsEndpoint(Resource):
    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsReportsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')

        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerReportsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsDimensionsEndpoint(Resource):
    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsReportsDimensionsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerReportsDimensionsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsMetricsEndpoint(Resource):
    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsReportsMetricsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerReportsMetricsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsBreakdownsEndpoint(Resource):
    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsReportsBreakdownsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerReportsMetricsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')
