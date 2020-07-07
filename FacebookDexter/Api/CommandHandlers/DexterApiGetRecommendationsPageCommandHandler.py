from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.Startup import startup


class DexterApiGetRecommendationsPageCommandHandler:
    def handle(self, command: DexterApiGetRecommendationsPageCommand):

        recommendation_repository = RecommendationsRepository(startup.mongo_config)
        recommendations_list = recommendation_repository.get_recommendations_page(command.page_number,
                                                                                  command.page_size,
                                                                                  command.recommendation_filter,
                                                                                  command.recommendation_sort,
                                                                                  command.excluded_ids)
        return recommendations_list
