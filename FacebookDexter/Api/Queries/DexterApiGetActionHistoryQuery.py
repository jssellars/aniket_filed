import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import OptimizePermissions
from FacebookDexter.Api.startup import config, fixtures
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


import logging

logger = logging.getLogger(__name__)


class GetActionHistoryQuery(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            logger.info(request_as_log_dict(request))
            structure_id = request.args.get('structureId')
            if structure_id is None:
                return Response(response='Please provide structure id', status=400, mimetype='application/json')
            recommendation_repository = RecommendationsRepository(config.mongo)
            history = recommendation_repository.get_action_history(structure_id)
            response = Response(response=json.dumps(history), status=200, mimetype='application/json')
            return response
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')

