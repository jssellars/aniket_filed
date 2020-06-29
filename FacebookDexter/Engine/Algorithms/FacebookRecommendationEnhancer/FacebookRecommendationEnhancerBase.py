import typing

from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendation import \
    FacebookRecommendation
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerBuilder import \
    FacebookRecommendationEnhancerBuilder
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnum import \
    FacebookRecommendationImportanceEnum, FacebookRecommendationConfidenceEnum, FacebookRecommendationFieldsEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationBuilder import RecommendationBuilder


class FacebookRecommendationEnhancerBase(FacebookRecommendationEnhancerBuilder):
    def __init__(self):
        super().__init__()

    def check_run_status(self, *args, **kwargs):
        return True

    def _map_importance(self, importance):
        if not importance:
            return None

        mapper = {
            'HIGH': FacebookRecommendationImportanceEnum.HIGH,
            'MEDIUM': FacebookRecommendationImportanceEnum.MEDIUM,
            'LOW': FacebookRecommendationImportanceEnum.LOW,
        }
        return mapper[importance]

    def _map_confidence(self, confidence):
        if not confidence:
            return None

        mapper = {
            'HIGH': FacebookRecommendationConfidenceEnum.HIGH.value,
            'MEDIUM': FacebookRecommendationConfidenceEnum.MEDIUM.value,
            'LOW': FacebookRecommendationConfidenceEnum.LOW.value,
        }
        return mapper[confidence]

    def run(self, structure_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        if not structure_id:
            return []

        details = self._mongo_repository.get_structure_details(structure_id, level=self._level)
        try:
            facebook_recommendations_raw = details['recommendations']
            facebook_recommendations = []
            for facebook_recommendation_raw in facebook_recommendations_raw:
                facebook_recommendation = FacebookRecommendation()
                facebook_recommendation.title = facebook_recommendation_raw.get(
                    FacebookRecommendationFieldsEnum.TITLE.value, None)
                facebook_recommendation.message = facebook_recommendation_raw.get(
                    FacebookRecommendationFieldsEnum.MESSAGE.value, None)
                facebook_recommendation.importance = self._map_importance(
                    facebook_recommendation_raw.get(FacebookRecommendationFieldsEnum.IMPORTANCE.value, None))
                facebook_recommendation.confidence = self._map_confidence(
                    facebook_recommendation_raw.get(FacebookRecommendationFieldsEnum.CONFIDENCE.value, None))
                facebook_recommendation.blame_field = facebook_recommendation_raw.get(
                    FacebookRecommendationFieldsEnum.BLAME_FIELD.value, None)

                recommendation = RecommendationBuilder(mongo_repository=self._mongo_repository,
                                                       time_interval=self._time_interval)
                recommendation = recommendation.create_facebook_recommendation(facebook_id=structure_id,
                                                                               level=self._level,
                                                                               template=facebook_recommendation.message,
                                                                               confidence=facebook_recommendation.confidence,
                                                                               importance=facebook_recommendation.importance,
                                                                               )
                facebook_recommendations.append(recommendation.to_dict())
        except Exception as e:
            return []

        return facebook_recommendations