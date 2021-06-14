import logging
import typing
from enum import Enum

import flask_restful
import humps
from flask import request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.utils import snake_to_camelcase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import (
    AccountsPermissions,
    AdsManagerPermissions,
    OptimizePermissions,
    ReportsPermissions,
)
from FacebookTuring.Api.Commands.AdsManagerDuplicateStructureCommand import AdsManagerDuplicateStructureCommand
from FacebookTuring.Api.Commands.AdsManagerFilteredStructuresCommand import AdsManagerFilteredStructuresCommand
from FacebookTuring.Api.Commands.AdsManagerUpdateStructureCommand import AdsManagerUpdateStructureCommand
from FacebookTuring.Api.CommandsHandlers.AdsManagerDeleteStructureCommandHandler import (
    AdsManagerDeleteStructureCommandHandler,
)
from FacebookTuring.Api.CommandsHandlers.AdsManagerDuplicateStructureCommandHandler import (
    AdsManagerDuplicateStructureCommandHandler,
    AdsManagerDuplicateStructureCommandHandlerException,
)
from FacebookTuring.Api.CommandsHandlers.AdsManagerFilteredStructuresCommandHandler import (
    AdsManagerFilteredStructuresCommandHandler,
)
from FacebookTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import (
    AdsManagerInsightsAgGridInsights,
    AdsManagerInsightsAgGridPopup,
    AdsManagerInsightsAgGridTrend,
    AdsManagerInsightsReports,
)
from FacebookTuring.Api.CommandsHandlers.AdsManagerUpdateStructureCommandHandler import (
    AdsManagerUpdateStructureCommandHandler,
)

# Dexter Lab Imports.
from FacebookTuring.Api.CommandsHandlers.LabsHiddenInterests.LabsHiddenInterestsCommandHandlers import (
    GetInterestsHandler,
)
from FacebookTuring.Api.Dtos import AdsManagerAgGridPopupViewsDto, ElementsCardViews
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsCombinationsDto import (
    AdsManagerCatalogsBreakdownsCombinationsDto,
)
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsMetacolumnsDto import AdsManagerCatalogsMetacolumnsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsBreakdownsDto import AdsManagerCatalogsReportsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDimensionsDto import AdsManagerCatalogsReportsDimensionsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsDto import AdsManagerCatalogsReportsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsReportsMetricsDto import AdsManagerCatalogsReportsMetricsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsAgGridDto import AdsManagerCatalogsViewsAgGridDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsByLevelDto import AdsManagerCatalogsViewsByLevelDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsDto import AdsManagerCatalogsViewsDto
from FacebookTuring.Api.Mappings.AdsManagerDuplicateStructureCommandMapping import (
    AdsManagerDuplicateStructureCommandMapping,
)
from FacebookTuring.Api.Mappings.AdsManagerFilteredStructuresCommandMapping import (
    AdsManagerFilteredStructuresCommandMapping,
)
from FacebookTuring.Api.Mappings.AdsManagerUpdateStructureCommandMapping import AdsManagerUpdateStructureCommandMapping
from FacebookTuring.Api.Queries.AdsManagerCampaignTreeStructureQuery import AdsManagerCampaignTreeStructureQuery
from FacebookTuring.Api.Queries.AdsManagerGetStructuresQuery import AdsManagerGetStructuresQuery
from FacebookTuring.Api.startup import config, fixtures

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class AdsManagerCatalogsViews(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsViewsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve views."}, 400


class AdsManagerCatalogsViewsByLevel(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self, level):
        try:
            return humps.camelize(AdsManagerCatalogsViewsByLevelDto.get(level)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve views by level."}, 400


class AdsManagerCatalogsViewsAgGrid(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self, level):
        try:
            return humps.camelize(AdsManagerCatalogsViewsAgGridDto.get(level)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve ag grid views by level."}, 400


class AdsManagerAgGridStructuresPerformanceViews(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self, level):
        try:
            if level not in [Level.CAMPAIGN.value, Level.ADSET.value]:
                raise ValueError

            response = AdsManagerAgGridPopupViewsDto.get_view(level)
            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve ag grid views by level."}, 400


class ElementsViewsHandler:
    @staticmethod
    def get():
        try:
            return humps.camelize(ElementsCardViews.get_card_views()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve ag grid views by level."}, 400


class AdsManagerElementsViews(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def get(self):
        return ElementsViewsHandler.get()


class AccountsElementsViews(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def get(self):
        return ElementsViewsHandler.get()


class AdsManagerAgGridStructuresPerformance(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self, level):
        logger.info(request_as_log_dict(request))

        try:
            if level not in [Level.CAMPAIGN.value, Level.ADSET.value]:
                raise ValueError

            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            response = AdsManagerInsightsAgGridPopup().handle(
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=level,
            )
            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400


class AdsManagerCatalogsMetacolumns(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsMetacolumnsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve meta columns."}, 400


class AdsManagerCatalogsBreakdowns(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsBreakdownsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve breakdowns."}, 400


class AdsManagerCatalogsBreakdownsCombinations(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsBreakdownsCombinationsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve breakdowns combinations columns."}, 400


class QueryParamsEnum(Enum):
    LEVEL_KEY = "level"
    REPORT_KEY = "report"
    DIMENSION_KEY = "dimension"
    METRICS_KEY = "metrics"


class AdsManagerReports(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsReportsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Invalid request. Error {repr(e)}"}, 400


class AdsManagerReportsDimensions(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsReportsDimensionsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Invalid request. Error {repr(e)}"}, 400


class AdsManagerReportsMetrics(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsReportsMetricsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Invalid request. Error {repr(e)}"}, 400


class AdsManagerReportsBreakdowns(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CHART_TEMPLATES_CREATE)
    def get(self):
        try:
            return humps.camelize(AdsManagerCatalogsReportsBreakdownsDto.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Invalid request. Error {repr(e)}"}, 400


class AdsManagerCampaignTreeStructure(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, level, facebook_id):
        try:
            return humps.camelize(AdsManagerCampaignTreeStructureQuery.get(level, facebook_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not retrieve tree for {facebook_id}"}, 400


class GetStructuresHandler:
    @staticmethod
    def handle(level, account_id):
        try:
            return snake_to_camelcase(AdsManagerGetStructuresQuery.get_structures(level, account_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not retrieve {level} for {account_id}"}, 400


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

            return humps.camelize(response), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            error = Tools.create_error(e)

            return error, 400


class AdsManager(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, level, facebook_id):
        try:
            return snake_to_camelcase(AdsManagerGetStructuresQuery.get_structure_details(level, facebook_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not retrieve {level} for {facebook_id}"}, 400

    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, level, facebook_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerUpdateStructureCommandMapping(target=AdsManagerUpdateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id()
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400

        try:
            response = AdsManagerUpdateStructureCommandHandler.handle(
                command=command,
                level=level,
                facebook_id=facebook_id,
                business_owner_facebook_id=business_owner_facebook_id,
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            error = Tools.create_error(e)

            return error, 400

    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_DELETE)
    def delete(self, level, facebook_id):
        business_owner_facebook_id = extract_business_owner_facebook_id()
        try:
            response = AdsManagerDeleteStructureCommandHandler.handle(level, facebook_id, business_owner_facebook_id)

            if not response:
                return {"message": f"Missing structure {facebook_id}."}, 400

            return None, 204

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to delete structure {facebook_id}."}, 400


class AdsManagerDuplicateStructure(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def post(self, level, facebook_id):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdsManagerDuplicateStructureCommandMapping(target=AdsManagerDuplicateStructureCommand)
            command = mapping.load(raw_request)
            business_owner_facebook_id = extract_business_owner_facebook_id()
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400

        try:
            command_handler = AdsManagerDuplicateStructureCommandHandler()
            command_handler.handle(command, level, facebook_id, business_owner_facebook_id)

            return None, 204

        except AdsManagerDuplicateStructureCommandHandlerException as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not find structure {facebook_id} tree."}, 404

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to duplicate structure {facebook_id}."}, 400


class AdsManagerAgGridInsights(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self, level):

        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            response = AdsManagerInsightsAgGridInsights().handle(
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=level,
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400


class AdsManagerAgGridTrend(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self):
        return AgGridTrendHandler.post()


class AccountsAgGridTrend(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return AgGridTrendHandler.post()


class AgGridTrendHandler:
    @staticmethod
    def post():

        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            response = AdsManagerInsightsAgGridTrend().handle(
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=Level.ACCOUNT.value,
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400


class GetInsightsHandler:
    @staticmethod
    def handle():
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            response = AdsManagerInsightsReports().handle(
                query_json=request_json,
                business_owner_id=business_owner_id,
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400


class AccountsReportInsights(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()


class OptimizeReportInsights(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        return GetInsightsHandler.handle()


class AdsManagerReportInsights(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()


class ReportsReportInsights(Resource):
    @fixtures.authorize_permission(permission=ReportsPermissions.REPORT_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()


class GetInterests:
    @staticmethod
    def handle():
        """
        Handle Requests from /labs/hidden-interests

        """
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            response = GetInterestsHandler().handle(query_json=request_json, business_owner_id=business_owner_id)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400


class LabsHiddenInterests(Resource):
    """
    Base for Labs Hidden Interests CRUD Operations.
    """

    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        """
        Returns Response for POST.

        """
        return GetInterests.handle()
