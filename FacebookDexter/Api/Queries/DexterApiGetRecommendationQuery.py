import json

from flask import request, make_response, Response
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Api.Infrastructure.PersistenceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.Startup import startup, logger


class DexterApiGetRecommendationQuery(Resource):
    def get(self):
        try:
            recommendation_id = request.args.get('id')
            if recommendation_id is None:
                return Response(response=json.dumps('Please provide a recommendation id'),
                                status=400, mimetype='application/json')
            mongo_config = MongoConfig(startup.mongo_config)
            recommendation_repository = RecommendationsRepository(mongo_config)
            recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
            response = Response(response=json.dumps(recommendation), status=200, mimetype='application/json')
            return response
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApiGetRecommendationEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')
