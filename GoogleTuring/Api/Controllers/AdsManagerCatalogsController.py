import humps
from flask import request
from flask_restful import Resource, abort

from Core.Web.Security.Permissions import ReportsPermissions
from GoogleTuring.Api.Dtos.AdsManagerCatalogReportsDto import AdsManagerCatalogReportsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsDimensionsDto import AdsManagerCatalogsDimensionsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsMetricsDto import AdsManagerCatalogsMetricsDto
from GoogleTuring.Api.Startup import startup

LEVEL_KEY = 'level'
REPORT_KEY = 'report'
DIMENSION_KEY = 'dimension'
METRICS_KEY = 'metrics'


class AdsManagerReportsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            args = request.args
            if LEVEL_KEY not in args or len(args) != 1:
                return {"error_message": "Wrong parameters"}, 400

            level = args[LEVEL_KEY]
            try:
                response = AdsManagerCatalogReportsDto.get(level=level)
            except Exception:
                return {"error_message": "Reports not found"}, 400

            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")


class AdsManagerDimensionsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            args = request.args
            if REPORT_KEY not in args or len(args) != 1:
                return {"error_message": "Wrong parameters"}, 400

            report = args[REPORT_KEY]
            response = AdsManagerCatalogsDimensionsDto.get(report=report)
            if not response:
                return {"error_message": "Dimensions not found"}, 400
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")


class AdsManagerMetricsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            args = request.args
            if REPORT_KEY not in args or DIMENSION_KEY not in args or len(args) != 2:
                return {"error_message": "Wrong parameters"}, 400

            report = args[REPORT_KEY]
            dimension = args[DIMENSION_KEY]
            response = AdsManagerCatalogsMetricsDto.get(report=report, dimension=dimension)
            if not response:
                return {"error_message": "Metrics not found"}, 400

            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")


class AdsManagerBreakdownsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            args = request.args
            if REPORT_KEY not in args or DIMENSION_KEY not in args or METRICS_KEY not in args or len(args) != 3:
                return {"error_message": "Wrong parameters"}, 400

            report = args[REPORT_KEY]
            dimension = args[DIMENSION_KEY]
            metrics = args[METRICS_KEY]
            response = AdsManagerCatalogsBreakdownsDto.get(report=report, dimension=dimension, metrics=metrics)
            if not response:
                return {"error_message": "Breakdowns not found"}, 400
            return humps.camelize(response)

        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")
