import json

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from PotterFacebookAccounts.Api.Commands.AdAccountInsightsCommand import AdAccountInsightsCommand
from PotterFacebookAccounts.Api.Mappings.AdAccountInsightsCommandMapping import AdAccountInsightsCommandMapping
from PotterFacebookAccounts.Api.Queries.AdAccountInstagramQuery import AdAccountInstagramQuery
from PotterFacebookAccounts.Api.Queries.AdAccountPageInstagramQuery import AdAccountPageInstagramQuery
from PotterFacebookAccounts.Api.Queries.AdAccountPagesQuery import AdAccountPagesQuery
from PotterFacebookAccounts.Api.Startup import startup, logger
from PotterFacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInsightsHandler import \
    GraphAPIAdAccountInsightsHandler


class AdAccountPagesEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            pages = AdAccountPagesQuery.handle(business_owner_id, account_id)
            response = humps.camelize(pages)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdAccountPagesEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": f"Failed to retrieve pages for {account_id}"}), status=400,
                            mimetype='application/json')


class AdAccountInstagramEndpoint(Resource):

    @jwt_required
    def get(self, account_id):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            instagram_accounts = AdAccountInstagramQuery.handle(business_owner_id, account_id)
            response = humps.camelize(instagram_accounts)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdAccountInstagramEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(
                {"message": f"Failed to retrieve instagram accounts for {account_id}. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class AdAccountPageInstagramEndpoint(Resource):

    @jwt_required
    def get(self, page_id):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            instagram_accounts = AdAccountPageInstagramQuery.handle(business_owner_id, page_id)
            response = humps.camelize(instagram_accounts)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdAccountPageInstagramEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": f"Failed to retrieve instagram accounts for {page_id}. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')


class AdAccountInsightsEndpoint(Resource):

    @jwt_required
    def post(self):
        #  log request information
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
            raw_request = humps.decamelize(request.get_json(force=True))
            mapping = AdAccountInsightsCommandMapping(AdAccountInsightsCommand)
            command = mapping.load(raw_request)
            command.business_owner_facebook_id = business_owner_facebook_id
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdAccountInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps({"message": f"Failed to process request. Error {str(e)}"})
            return Response(response=response, status=400, mimetype='application/json')

        try:
            response = GraphAPIAdAccountInsightsHandler.handle(command, startup)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdAccountInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, 'POTTER_FACEBOOK_ACCOUNTS_BAD_REQUEST')
            response = json.dumps(response)
            return Response(response=response, status=400, mimetype='application/json')
