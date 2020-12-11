import json
from enum import Enum

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import ReportsPermissions
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsBreakdownsDto import AdsManagerCatalogsReportsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDimensionsDto import AdsManagerCatalogsReportsDimensionsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDto import AdsManagerCatalogsReportsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsMetricsDto import AdsManagerCatalogsReportsMetricsDto
from FacebookTuring.Api.startup import config, fixtures


import logging

logger = logging.getLogger(__name__)


class QueryParamsEnum(Enum):
    LEVEL_KEY = 'level'
    REPORT_KEY = 'report'
    DIMENSION_KEY = 'dimension'
    METRICS_KEY = 'metrics'


class AdsManagerReportsEndpoint(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsReportsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsDimensionsEndpoint(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsReportsDimensionsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsMetricsEndpoint(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsReportsMetricsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')


class AdsManagerReportsBreakdownsEndpoint(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsReportsBreakdownsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Invalid request. Error {str(e)}"}),
                            status=400,
                            mimetype='application/json')
