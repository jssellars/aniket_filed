from FacebookDexter.Api.Commands.DexterApiGetCountsByCategoryCommand import DexterApiGetCountsByCategoryCommand
from FacebookDexter.Api.Config.Config import MongoConfig
from FacebookDexter.Api.Infrastructure.PersistenceLayer.RecommendationsRepository import RecommendationsRepository
from FacebookDexter.Api.Startup import startup


class DexterApiGetCountsByCategoryCommandHandler:
    def handle(self, command: DexterApiGetCountsByCategoryCommand):
        mongo_config = MongoConfig(startup.mongo_config)
        recommendation_repository = RecommendationsRepository(mongo_config)

        count_filter = {}

        if isinstance(command.campaign_ids, list):
            count_filter['campaign_id'] = {'$in': command.campaign_ids}
        else:
            count_filter['campaign_id'] = command.campaign_ids

        if isinstance(command.channel, list):
            count_filter['channel'] = {'$in': command.channel}
        else:
            count_filter['channel'] = command.channel

        counts = recommendation_repository.get_counts(count_filter)
        return counts
