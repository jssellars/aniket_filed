from flask import request
from flask_restful import Resource, abort

from Core.Web.Security.JWTTools import extract_business_owner_google_id
from Core.Web.Security.Permissions import AccountsPermissions, AdsManagerPermissions, OptimizePermissions, \
    ReportsPermissions
from GoogleTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler
from GoogleTuring.Api.Startup import startup


class GetInsightsHandler:
    @staticmethod
    def handle():
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id()
            response = AdsManagerInsightsCommandHandler.get_insights(config=startup.google_config,
                                                                     query_json=request_json["query"],
                                                                     business_owner_google_id=business_owner_google_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))


class AdsManagerInsightsWithTotalsEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def post(self):
        request_json = request.get_json(force=True)

        try:
            business_owner_google_id = extract_business_owner_google_id()
            response = AdsManagerInsightsCommandHandler.get_insights_with_totals(config=startup.google_config,
                                                                                 query_json=request_json["query"],
                                                                                 business_owner_google_id=business_owner_google_id)
            return response
        except Exception as e:
            abort(400, message="Failed to process your insights request. %s" % str(e))


class AccountsReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler().handle()


class OptimizeReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        return GetInsightsHandler().handle()


class AdsManagerReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler().handle()


class ReportsReportInsightsEndpoint(Resource):
    @startup.authorize_permission(permission=ReportsPermissions.REPORT_CAN_ACCESS_REPORTS_DATA)
    def post(self):
        return GetInsightsHandler().handle()
