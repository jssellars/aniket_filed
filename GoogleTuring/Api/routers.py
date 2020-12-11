import logging
import typing

import flask_restful
import humps
from flask import request
from flask_restful import abort

from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_google_id
from Core.Web.Security.Permissions import (
    AccountsPermissions,
    AdsManagerPermissions,
    OptimizePermissions,
    ReportsPermissions
)
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.utils import snake_to_camelcase
from GoogleTuring.Api.Commands.AdAccountInsightsCommand import AdAccountInsightsCommand
from GoogleTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from GoogleTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from GoogleTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import (
    AdsManagerDeleteStructureCommandHandler
)
from GoogleTuring.Api.CommandsHandlers.AdsManagerFilteredStructuresCommandHandler import (
    AdsManagerFilteredStructuresCommandHandler
)
from GoogleTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler
from GoogleTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import (
    AdsManagerUpdateStructureCommandHandler
)
from GoogleTuring.Api.CommandsHandlers.GoogleAdAccountInsightsHandler import GoogleAdAccountInsightsHandler
from GoogleTuring.Api.Dtos.AdsManagerCatalogReportsDto import AdsManagerCatalogReportsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsDimensionsDto import AdsManagerCatalogsDimensionsDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsMetricsDto import AdsManagerCatalogsMetricsDto
from GoogleTuring.Api.Mappings.AdAccountInsightsCommandMapping import AdAccountInsightsCommandMapping
from GoogleTuring.Api.Mappings.AdsManagerFilteredStructuresCommandMapping import (
    AdsManagerFilteredStructuresCommandMapping
)
from GoogleTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from GoogleTuring.Api.Queries.AdsManagerGetStructuresQuery import AdsManagerGetStructuresQuery
from GoogleTuring.Api.startup import config, fixtures
from GoogleTuring.Infrastructure.Domain.Structures.StructureType import StructureType

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):

        return None, 200


class Version(Resource):
    def get(self):

        return config.version_endpoint_payload, 200


class AdAccountInsights(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def post(self):
        try:
            business_owner_google_id = extract_business_owner_google_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_google_id = business_owner_google_id
        except Exception as e:
            return {"message": f"Failed to process request. Error {repr(e)}"}, 400

        try:
            return humps.camelize(GoogleAdAccountInsightsHandler.handle(config=config.google, command=command)), 200

        except Exception as e:
            return Tools.create_error(e, "GOOGLE_ACCOUNTS_BAD_REQUEST"), 400


LEVEL_KEY = "level"
REPORT_KEY = "report"
DIMENSION_KEY = "dimension"
METRICS_KEY = "metrics"


class AdsManagerReports(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            args = request.args
            if LEVEL_KEY not in args or len(args) != 1:
                return {"error_message": "Wrong parameters"}, 400

            level = args[LEVEL_KEY]
            try:
                return humps.camelize(AdsManagerCatalogReportsDto.get(level=level))
            except Exception:

                return {"error_message": "Reports not found"}, 400

        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {repr(e)}")


class AdsManagerDimensions(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
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
            abort(400, message=f"Invalid metacolumns definition request. Error {repr(e)}")


class AdsManagerMetrics(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
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
            abort(400, message=f"Invalid metacolumns definition request. Error {repr(e)}")


class AdsManagerBreakdowns(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
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
            abort(400, message=f"Invalid metacolumns definition request. Error {repr(e)}")


class AdsManager(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, account_id, level, structure_id):
        try:
            business_owner_google_id = extract_business_owner_google_id()
            raw_request = request.get_json(force=True)
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            AdsManagerUpdateStructureCommandHandler.handle(
                config=config.google,
                command=command,
                account_id=account_id,
                level=level,
                structure_id=structure_id,
                business_owner_google_id=business_owner_google_id,
            )
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {repr(e)}")

        return None, 204

    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_DELETE)
    def delete(self, account_id, level, structure_id):
        try:
            level = StructureType.get_enum_by_value(level)
            business_owner_google_id = extract_business_owner_google_id()
            AdsManagerDeleteStructureCommandHandler.handle(
                config=config.google,
                account_id=account_id,
                level=level,
                structure_id=structure_id,
                business_owner_google_id=business_owner_google_id,
            )
        except Exception as e:
            abort(400, message=f"Could not process your request. Error: {repr(e)}")

        return None, 204


class GetStructuresHandler:
    @staticmethod
    def handle(level, account_id):
        if level == "adset":
            level = "adgroup"
        try:
            return snake_to_camelcase(AdsManagerGetStructuresQuery.get_structures(level, account_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not retrieve {level} for {account_id}"}, 400


# TODO: keywords level should be renamed to keyword
class AdsManagerGetStructures(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def get(self, level, account_id):

        return GetStructuresHandler.handle(level, account_id)


class OptimizeGetStructures(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self, level, account_id):

        return GetStructuresHandler.handle(level, account_id)


class AdsManagerFilteredStructures(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.FILTERED_STRUCTURES_PERMISSION)
    def post(self, level: typing.AnyStr = None):
        if level == "adset":
            level = "adgroup"
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerFilteredStructuresCommandMapping(target=AdsManagerFilteredStructuresCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": str(e)}, 400

        try:
            response = AdsManagerFilteredStructuresCommandHandler.handle(level=level, command=command)
            if not response:

                return {"error_message": "Structures not found!"}, 404

            response = humps.camelize(response)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return str(e), 400


class GetInsightsHandler:
    @staticmethod
    def handle():
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id()
            response = AdsManagerInsightsCommandHandler.get_insights(
                config=config.google,
                query_json=request_json["query"],
                business_owner_google_id=business_owner_google_id,
            )

            return response

        except Exception as e:
            abort(400, message=f"Failed to process your insights request. {repr(e)}")


class AdsManagerInsightsWithTotals(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self):
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id()
            response = AdsManagerInsightsCommandHandler.get_insights_with_totals(
                config=config.google,
                query_json=request_json["query"],
                business_owner_google_id=business_owner_google_id,
            )

            return response

        except Exception as e:
            abort(400, message=f"Failed to process your insights request. {repr(e)}")


class AccountsReportInsights(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self):

        return GetInsightsHandler().handle(), 200


class OptimizeReportInsights(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):

        return GetInsightsHandler().handle(), 200


class AdsManagerReportInsights(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def post(self):

        return GetInsightsHandler().handle(), 200


class ReportsReportInsights(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CAN_ACCESS_REPORTS_DATA)
    def post(self):

        return GetInsightsHandler().handle(), 200
