from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Api.Startup import startup, logger
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


class DexterApiGetRecommendationsPageCommandHandler:
    def handle(self, command: DexterApiGetRecommendationsPageCommand):
        recommendation_repository = RecommendationsRepository(startup.mongo_config, logger=logger)
        recommendations_list = recommendation_repository.get_recommendations_page(command.page_number,
                                                                                  command.page_size,
                                                                                  command.recommendation_filter,
                                                                                  command.recommendation_sort,
                                                                                  command.excluded_ids)
        return recommendations_list
