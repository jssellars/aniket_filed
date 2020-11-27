import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict, request_as_log_dict_nested, log_message_as_dict
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import AccountsPermissions, AdsManagerPermissions, OptimizePermissions, \
    ReportsPermissions
from FacebookTuring.Api.Commands.AdsManagerInsightsCommand import AdsManagerInsightsCommandEnum
from FacebookTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler
from FacebookTuring.Api.Startup import logger, startup


import logging

logger_native = logging.getLogger(__name__)


class AdsManagerInsightsWithTotalsEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self):
        logger.logger.info(request_as_log_dict_nested(request))
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            response = (AdsManagerInsightsCommandHandler.
                        handle(handler_type=AdsManagerInsightsCommandEnum.INSIGHTS_WITH_TOTALS,
                               query_json=request_json,
                               business_owner_id=business_owner_id))
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="AdsManagerInsightsWithTotalsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AdsManagerAgGridInsightsEndpoint(Resource):

    @startup.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self, level):
        logger.logger.info(request_as_log_dict_nested(request))

        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            response = (AdsManagerInsightsCommandHandler.handle(
                handler_type=AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS,
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=level)
            )
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="AdsManagerInsightsWithTotalsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AdsManagerAgGridTrendEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self, level):
        return AgGridTrendHandler.post(level)


class AccountsAgGridTrendEndpoint(Resource):
    @startup.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self, level):
        return AgGridTrendHandler.post(level)


class AgGridTrendHandler:
    @staticmethod
    def post(level):
        logger.logger.info(request_as_log_dict_nested(request))

        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            response = (AdsManagerInsightsCommandHandler.handle(
                handler_type=AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS_TREND,
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=level)
            )
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="AdsManagerInsightsWithTotalsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class GetInsightsHandler:
    @staticmethod
    def handle():
        logger.logger.info(request_as_log_dict_nested(request))
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id()
            response = (AdsManagerInsightsCommandHandler.
                        handle(handler_type=AdsManagerInsightsCommandEnum.REPORTS,
                               query_json=request_json,
                               business_owner_id=business_owner_id))
            return response
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="AdsManagerReportInsightsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AccountsReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()


class OptimizeReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        return GetInsightsHandler.handle()


class AdsManagerReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()


class ReportsReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler.handle()
