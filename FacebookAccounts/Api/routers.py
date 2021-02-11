import logging
import typing

import flask_restful
import humps
from flask import request

import FacebookAccounts.Api.mappings
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import (
    AccountsPermissions,
    CampaignBuilderPermissions,
    MiscellaneousPermissions,
    SettingsPermissions
)
from FacebookAccounts.Api.commands import BusinessOwnerCreateCommand, AdAccountInsightsCommand
from FacebookAccounts.Api.command_handlers import BusinessOwnerCreateCommandHandler, \
    BusinessOwnerDeletePermissionsCommandHandler
from FacebookAccounts.Api import dtos
from FacebookAccounts.Api.mappings import AdAccountInsightsCommandMapping
from FacebookAccounts.Api.queries import AdAccountPageInstagramQuery, AdAccountPagesQuery
from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers import GraphAPIAdAccountInsightsHandler

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class AdAccountPages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, account_id):

        try:
            business_owner_id = extract_business_owner_facebook_id()
            pages = AdAccountPagesQuery.handle(business_owner_id, account_id)
            response = humps.camelize(pages)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to retrieve pages for {account_id}"}, 400


class AdAccountPageInstagram(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, page_id):

        try:
            business_owner_id = extract_business_owner_facebook_id()
            instagram_accounts = AdAccountPageInstagramQuery.handle(business_owner_id, page_id)
            response = humps.camelize(instagram_accounts)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to retrieve instagram accounts for {page_id}. Error {repr(e)}"}, 400


class AdAccountsAgGridView(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def get(self):
        try:
            response = dtos.get_view()
            response = humps.camelize(response)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve ag grid views on Accounts."}, 400


class AdAccountAgGridInsights(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def post(self):

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_facebook_id = business_owner_facebook_id

            response = GraphAPIAdAccountInsightsHandler.handle_accounts_insights(command, config, fixtures)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = {"message": f"Failed to process request. Error {repr(e)}"}

            return response, 400


class BusinessOwner(Resource):
    @fixtures.authorize_permission(permission=MiscellaneousPermissions.MISCELLANEOUS_CONNECT_TO_FACEBOOK)
    def post(self):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = FacebookAccounts.Api.mappings.BusinessOwnerCreateCommandMapping(BusinessOwnerCreateCommand)
            command = mapping.load(raw_request)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to process request. Error {repr(e)}"}, 400

        try:
            BusinessOwnerCreateCommandHandler.handle(command)

            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to add new business owner. Error {repr(e)}"}, 400


class BusinessOwnerDeletePermissions(Resource):
    @fixtures.authorize_permission(permission=SettingsPermissions.SETTINGS_MANAGE_PERMISSIONS_EDIT)
    def delete(self, permissions: typing.List[typing.AnyStr] = None):

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()

            response = BusinessOwnerDeletePermissionsCommandHandler.handle(business_owner_facebook_id, permissions)
            response = humps.camelize(response)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Failed to delete permissions. Error {repr(e)}"}, 400
