import json

import requests
from flask import Response

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from FacebookDexter.Api.Commands.DexterApiApplyRecommendationCommand import DexterApiApplyRecommendationCommand
from FacebookDexter.Api.Startup import startup, logger
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleRedirectEnum
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


class DexterApiApplyRecommendationCommandHandler:
    def handle(self, command: DexterApiApplyRecommendationCommand):
        try:
            recommendation_id = command.id
            recommendation_repository = RecommendationsRepository(startup.mongo_config, logger=logger)
            recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
            external_services = startup.external_services
            if not recommendation:
                error_message = (f'Recommendation with id {recommendation_id} does not exist or was'
                                 ' already dismissed, applied or deprecated')
                return Response(response=json.dumps(error_message), status=404, mimetype='application/json')
            details = recommendation.get("application_details")
            if not details:
                error_message = f'Recommendation with id {recommendation_id} cannot be applied automatically'
                return Response(response=json.dumps(error_message), status=400, mimetype='application/json')

            request_header = {'HTTP_AUTHORIZATION': command.token}

            if recommendation['channel'] == ChannelEnum.GOOGLE.value:
                # TODO: change this when there's auto apply for Google
                error_message = f' Google recommendations cannot be applied automatically yet'
                return Response(response=json.dumps(error_message), status=400, mimetype='application/json')

            if recommendation['channel'] == ChannelEnum.FACEBOOK.value:
                url = external_services.facebook_auto_apply.format(level=recommendation['level'],
                                                                      structureId=recommendation['structureId'])
                if recommendation['redirect_for_edit'] == FacebookRuleRedirectEnum.DUPLICATE.value:
                    url += '/duplicate'
                    apply_request = requests.post(url, details, headers=request_header)
                else:
                    apply_request = requests.put(url, details, headers=request_header)

            if apply_request.ok:
                recommendation_repository.set_recommendation_statuses_by_structure_id(recommendation['structureId'],
                                                                                      RecommendationStatusEnum.DISMISSED.value)
                _ = recommendation_repository.set_recommendation_status(recommendation_id,
                                                                        RecommendationStatusEnum.APPLIED.value)
                return Response(status=204, mimetype='application/json')
            else:
                error_message = 'There was a problem applying your recommendation'
                return Response(response=json.dumps(error_message), status=500, mimetype='application/json')

        except Exception as e:
            raise e
