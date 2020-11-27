import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict, request_as_log_dict_nested, log_message_as_dict
from Core.Web.Security.Permissions import OptimizePermissions
from FacebookDexter.Api.Startup import startup, logger
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


import logging

logger_native = logging.getLogger(__name__)


class DexterApiGetRecommendationQuery(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            logger.logger.info(request_as_log_dict_nested(request))
            recommendation_id = request.args.get('id')
            if recommendation_id is None:
                return Response(response=json.dumps('Please provide a recommendation id'),
                                status=400, mimetype='application/json')
            recommendation_repository = RecommendationsRepository(startup.mongo_config, logger=logger)
            recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
            response = Response(response=json.dumps(recommendation), status=200, mimetype='application/json')
            return response
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="DexterApiGetRecommendationEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')
