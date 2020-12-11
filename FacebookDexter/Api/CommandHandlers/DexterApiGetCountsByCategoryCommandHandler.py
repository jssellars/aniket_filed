from FacebookDexter.Api.Commands.DexterApiGetCountsByCategoryCommand import DexterApiGetCountsByCategoryCommand
from FacebookDexter.Api.startup import config, fixtures
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository


class DexterApiGetCountsByCategoryCommandHandler:
    def handle(self, command: DexterApiGetCountsByCategoryCommand):
        recommendation_repository = RecommendationsRepository(config.mongo)

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
