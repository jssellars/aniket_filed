import json

from flask import Response

from FacebookDexter.Api.Commands.DexterApiDismissRecommendationCommand import DexterApiDismissRecommendationCommand
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Api.Infrastructure.PersistenceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationStatusEnum
from FacebookDexter.Api.Startup import startup


class DexterApiDismissRecommendationCommandHandler():
    def handle(self, command: DexterApiDismissRecommendationCommand):
        try:
            recommendation_id = command.id
            mongo_config = MongoConfig(startup.mongo_config)
            recommendation_repository = RecommendationsRepository(mongo_config)
            recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)
            if not recommendation:
                error_message = (f'Recommendation with id {recommendation_id} does not exist or was'
                                 ' already dismissed, applied or deprecated')
                return Response(response=json.dumps(error_message), status=404, mimetype='application/json')
            dismissed_recommendation = (recommendation_repository.
                                        set_recommendation_status(recommendation_id,
                                                                  RecommendationStatusEnum.DISMISSED.value))

            # This is probably unnecessary
            if dismissed_recommendation['status'] == RecommendationStatusEnum.DISMISSED.value:
                return Response(status=204, mimetype='application/json')
            else:
                message = 'Something went wrong while dismissing your recommendation'
                return Response(response=json.dumps(message), status=500, mimetype='application/json')

        except Exception as e:
            raise(e)

