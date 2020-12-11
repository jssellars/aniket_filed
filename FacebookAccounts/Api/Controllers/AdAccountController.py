import json

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import CampaignBuilderPermissions, AccountsPermissions
from FacebookAccounts.Api.Commands.AdAccountInsightsCommand import AdAccountInsightsCommand
from FacebookAccounts.Api.Dtos import AccountAgGridViewsDto
from FacebookAccounts.Api.Mappings.AdAccountInsightsCommandMapping import AdAccountInsightsCommandMapping
from FacebookAccounts.Api.Queries.AdAccountInstagramQuery import AdAccountInstagramQuery
from FacebookAccounts.Api.Queries.AdAccountPageInstagramQuery import AdAccountPageInstagramQuery
from FacebookAccounts.Api.Queries.AdAccountPagesQuery import AdAccountPagesQuery
from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers import GraphAPIAdAccountInsightsHandler
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInsightsHandler import \
    GraphAPIAdAccountInsightsHandlerClass


import logging

logger = logging.getLogger(__name__)


class AdAccountPagesEndpoint(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, account_id):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_id = extract_business_owner_facebook_id()
            pages = AdAccountPagesQuery.handle(business_owner_id, account_id)
            response = humps.camelize(pages)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": f"Failed to retrieve pages for {account_id}"}), status=400,
                            mimetype='application/json')


class AdAccountInstagramEndpoint(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, account_id):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_id = extract_business_owner_facebook_id()
            instagram_accounts = AdAccountInstagramQuery.handle(business_owner_id, account_id)
            response = humps.camelize(instagram_accounts)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps(
                {"message": f"Failed to retrieve instagram accounts for {account_id}. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class AdAccountPageInstagramEndpoint(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, page_id):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_id = extract_business_owner_facebook_id()
            instagram_accounts = AdAccountPageInstagramQuery.handle(business_owner_id, page_id)
            response = humps.camelize(instagram_accounts)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": f"Failed to retrieve instagram accounts for {page_id}. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class AdAccountInsightsEndpoint(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def post(self):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')

        try:
            response = GraphAPIAdAccountInsightsHandlerClass.handle(command, config, fixtures)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, 'POTTER_FACEBOOK_ACCOUNTS_BAD_REQUEST')
            response = json.dumps(response)
            return Response(response=response, status=400, mimetype='application/json')


class AdAccountsAgGridViewEndpoint(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AccountAgGridViewsDto.get_view()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps({"message": "Failed to retrieve ag grid views on Accounts."}), status=400,
                            mimetype='application/json')


class AdAccountAgGridInsights(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.CAN_ACCESS_ACCOUNTS)
    def post(self):
        # log request information
        logger.info(request_as_log_dict(request))

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id()
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_facebook_id = business_owner_facebook_id

            response = GraphAPIAdAccountInsightsHandler.handle_accounts_insights(command, config, fixtures)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')
