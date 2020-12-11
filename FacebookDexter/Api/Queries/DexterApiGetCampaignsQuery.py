import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import OptimizePermissions
from FacebookDexter.Api.QueryParamsValidators.DexterApiGetCampaignsQueryValidator import \
    DexterApiGetCampaignsQueryValidator
from FacebookDexter.Api.startup import config, fixtures
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


import logging

logger = logging.getLogger(__name__)


class GetCampaignsQuery(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            logger.info(request_as_log_dict(request))
            request_args = request.args
            error_response_or_paramaters = DexterApiGetCampaignsQueryValidator().validate(request_args)

            if isinstance(error_response_or_paramaters, Response):
                return error_response_or_paramaters

            recommendation_repository = RecommendationsRepository(config.mongo)
            campaigns = recommendation_repository.get_campaigns(error_response_or_paramaters['ad_account_id'],
                                                                error_response_or_paramaters['channel'])
            response = Response(response=json.dumps(campaigns), status=200, mimetype='application/json')
            return response
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')
