import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchInterestsSearchQuery import \
    TargetingSearchInterestsSearchQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchInterestsSuggestionsQuery import \
    TargetingSearchInterestsSuggestionsQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchInterestsTreeQuery import \
    TargetingSearchInterestsTreeQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchLanguagesQuery import TargetingSearchLanguagesQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchLocationsCountryGroupsQuery import \
    TargetingSearchLocationsCountryGroupsQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchLocationsSearchQuery import \
    TargetingSearchLocationsSearchQuery
from Potter.FacebookCampaignsBuilder.Api.Startup import startup, logger


class TargetingSearchInterestsTreeEndpoint(Resource):
    @jwt_required
    def get(self) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchInterestsTreeQuery(session=startup.session,
                                                      business_owner_id=business_owner_id,
                                                      facebook_config=startup.facebook_config)
            response = query.get()
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchInterestsTreeEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class TargetingSearchInterestsSearchEndpoint(Resource):
    @jwt_required
    def get(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchInterestsSearchQuery(session=startup.session,
                                                        business_owner_id=business_owner_id,
                                                        facebook_config=startup.facebook_config)
            response = query.search(query_string=query_string)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchInterestsSearchEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class TargetingSearchInterestsSuggestionsEndpoint(Resource):
    @jwt_required
    def get(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchInterestsSuggestionsQuery(session=startup.session,
                                                             business_owner_id=business_owner_id,
                                                             facebook_config=startup.facebook_config)
            response = query.search(query_string=query_string)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchInterestsSuggestionsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class TargetingSearchLocationsEndpoint(Resource):
    @jwt_required
    def get(self) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchLocationsCountryGroupsQuery(session=startup.session,
                                                               business_owner_id=business_owner_id,
                                                               facebook_config=startup.facebook_config)
            response = query.get()
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchLocationsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class TargetingSearchLocationSearchEndpoint(Resource):
    @jwt_required
    def get(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchLocationsSearchQuery(session=startup.session,
                                                        business_owner_id=business_owner_id,
                                                        facebook_config=startup.facebook_config)
            response = query.search(query_string=query_string)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchLocationSearchEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class TargetingSearchLanguagesEndpoint(Resource):
    @jwt_required
    def get(self) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            query = TargetingSearchLanguagesQuery(session=startup.session,
                                                  business_owner_id=business_owner_id,
                                                  facebook_config=startup.facebook_config)
            response = query.get()
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="TargetingSearchLanguagesEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")
