import json

from flask import request, Response
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Api.Infrastructure.PersistenceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.Startup import startup, logger


class DexterApiGetActionHistoryQuery(Resource):

    def get(self):
        try:
            structure_id = request.args.get('structureId')
            mongo_config = MongoConfig(startup.mongo_config)
            if structure_id is None:
                return Response(response='Please provide structure id', status=400, mimetype='application/json')
            recommendation_repository = RecommendationsRepository(mongo_config)
            history = recommendation_repository.get_action_history(structure_id)
            response = Response(response=json.dumps(history), status=200, mimetype='application/json')
            return response
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApiActionHistoryEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')

