import typing

from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerBuilder import \
    FacebookRecommendationEnhancerBuilder


class FacebookRecommendationEnhancerBase(FacebookRecommendationEnhancerBuilder):
    def __init__(self):
        super().__init__()

    def run(self, **kwargs) -> typing.List[typing.Dict]:
        raise NotImplementedError("Method run() not implemented.")

    def check_run_status(self, **kwargs):
        return True