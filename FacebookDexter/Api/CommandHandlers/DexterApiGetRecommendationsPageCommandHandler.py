from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Api.Infrastructure.PersistenceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.Startup import startup


class DexterApiGetRecommendationsPageCommandHandler:
    def handle(self, command: DexterApiGetRecommendationsPageCommand):

        mongo_config = MongoConfig(startup.mongo_config)
        recommendation_repository = RecommendationsRepository(mongo_config)
        recommendations_list = recommendation_repository.get_recommendations_page(command.page_number,
                                                                                  command.page_size,
                                                                                  command.recommendation_filter,
                                                                                  command.recommendation_sort,
                                                                                  command.excluded_ids)
        return recommendations_list
