import json

from flask import request, Response
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.QueryParamsValidators.DexterApiGetCampaignsQueryValidator import \
    DexterApiGetCampaignsQueryValidator
from FacebookDexter.Api.Startup import startup, logger


class DexterApiGetCampaignsQuery(Resource):
    @jwt_required
    def get(self):
        try:
            request_args = request.args
            error_response_or_paramaters = DexterApiGetCampaignsQueryValidator().validate(request_args)

            if isinstance(error_response_or_paramaters, Response):
                return error_response_or_paramaters

            recommendation_repository = RecommendationsRepository(startup.mongo_config)
            campaigns = recommendation_repository.get_campaigns(error_response_or_paramaters['ad_account_id'],
                                                                error_response_or_paramaters['channel'])
            response = Response(response=json.dumps(campaigns), status=200, mimetype='application/json')
            return response
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApiGetCampaignsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')