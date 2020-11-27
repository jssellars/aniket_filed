import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict, request_as_log_dict_nested, log_message_as_dict
from Core.Web.Security.Permissions import OptimizePermissions
from FacebookDexter.Api.QueryParamsValidators.DexterApiGetCampaignsQueryValidator import \
    DexterApiGetCampaignsQueryValidator
from FacebookDexter.Api.Startup import startup, logger
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


import logging

logger_native = logging.getLogger(__name__)


class DexterApiGetCampaignsQuery(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            logger.logger.info(request_as_log_dict_nested(request))
            request_args = request.args
            error_response_or_paramaters = DexterApiGetCampaignsQueryValidator().validate(request_args)

            if isinstance(error_response_or_paramaters, Response):
                return error_response_or_paramaters

            recommendation_repository = RecommendationsRepository(startup.mongo_config, logger=logger)
            campaigns = recommendation_repository.get_campaigns(error_response_or_paramaters['ad_account_id'],
                                                                error_response_or_paramaters['channel'])
            response = Response(response=json.dumps(campaigns), status=200, mimetype='application/json')
            return response
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="DexterApiGetCampaignsEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')
