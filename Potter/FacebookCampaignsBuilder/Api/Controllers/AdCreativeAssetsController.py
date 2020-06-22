import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsImagesQuery import AdCreativeAssetsImagesQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsPagePostsQuery import AdCreativeAssetsPagePostsQuery
from Potter.FacebookCampaignsBuilder.Api.Queries.AdCreativeAssetsVideosQuery import AdCreativeAssetsVideosQuery
from Potter.FacebookCampaignsBuilder.Api.Startup import logger, startup


class AdCreativeAssetsImagesEndpoint(Resource):
    @jwt_required
    def get(self,
            business_owner_facebook_id: typing.AnyStr = None,
            ad_account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            query = AdCreativeAssetsImagesQuery(session=startup.session,
                                                business_owner_id=business_owner_facebook_id,
                                                facebook_config=startup.facebook_config)
            response = query.get(ad_account_id=ad_account_id)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdCreativeAssetsImagesEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class AdCreativeAssetsVideosEndpoint(Resource):
    @jwt_required
    def get(self,
            business_owner_facebook_id: typing.AnyStr = None,
            ad_account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            query = AdCreativeAssetsVideosQuery(session=startup.session,
                                                business_owner_id=business_owner_facebook_id,
                                                facebook_config=startup.facebook_config)
            response = query.get(ad_account_id=ad_account_id)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdCreativeAssetsImagesEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")


class AdCreativeAssetsPagePostsEndpoint(Resource):
    @jwt_required
    def get(self,
            business_owner_facebook_id: typing.AnyStr = None,
            page_facebook_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            query = AdCreativeAssetsPagePostsQuery(session=startup.session,
                                                   business_owner_id=business_owner_facebook_id,
                                                   facebook_config=startup.facebook_config)
            response = query.get(page_facebook_id=page_facebook_id)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdCreativeAssetsImagesEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")
