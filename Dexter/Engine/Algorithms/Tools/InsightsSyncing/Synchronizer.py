import logging

from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import ColumnsEnum, Columns
from Algorithms.Tools.InsightsSyncing.ActorsSynchroniser import ActorsSynchroniser
from Algorithms.Tools.TimeInterval import TimeInterval
from Infrastructure.Mongo.Mongo import MongoMediator
from Infrastructure.QueryBuilder.QueryBuilderMediator import QueryBuilderMediator


class Synchronizer(object):
    """Fetches Insights and Actor Metadata"""

    def __init__(self, token, insights_mediator=None, mongo_mediator=None):
        """Grants the class an instance of the insightsMediator and of the mongoMediator that it can access"""
        if insights_mediator is None:
            self.__insights_mediator = QueryBuilderMediator(token)
        else:
            self.__insights_mediator = insights_mediator

        if mongo_mediator is None:
            self.__mongo_mediator = MongoMediator()
        else:
            self.__mongo_mediator = mongo_mediator

    def sync_data_for_type(self, optimization_type: Tw.OptimizationTuple, date_range: TimeInterval, ad_account_id):
        """Stores insights data for one insight type and relevant actors metadata"""

        try:
            logging_message = ' for date range {' + date_range.to_string() + '} , ad account ' + ad_account_id + ' and optimization type ' + optimization_type.level
            logging.info('Started synchronizing' + logging_message)

            data_for_type = self.__insights_mediator.get_data_for_optimization_tuple(optimization_type, date_range, ad_account_id)

            actors_synchroniser = ActorsSynchroniser(self.__mongo_mediator)
            actor_type = optimization_type.breakdown
            if actor_type == Tw.LevelNames.Breakdown.value:
                actor_type = Tw.LevelNames.AdSet.value
            if actor_type == Tw.LevelNames.Interest.value:
                actor_type = Tw.LevelNames.AdSet.value

            data_for_type = self.__add_actor_type_to_ids(data_for_type, actor_type)
            actors_synchroniser.store_new_actors_from_insights(data_for_type, optimization_type)

            data_for_type = self.__strip_actor_meta_data(data_for_type, optimization_type)
            self.__mongo_mediator.store_insights_data(data_for_type, optimization_type)

            logging.info('Finished synchronizing ' + logging_message)
        except Exception as e:
            logging.exception(e)

    def update_actor_states(self, ad_account_id):
        actor_states = self.__insights_mediator.get_actor_states(ad_account_id)
        self.__mongo_mediator.update_actor_states(actor_states)

    def __strip_actor_meta_data(self, data, optimization_type: Tw.OptimizationTuple):
        parent_column_name = Columns.Parents[optimization_type.breakdown].value
        campaign_id_column_name = Columns.CampaignId[optimization_type.breakdown].value
        face_book_id_column_name = ColumnsEnum.GroupBy.FACEBOOK_ID.value
        for insight in data:
            if parent_column_name in insight and parent_column_name != ColumnsEnum.GroupBy.AD_ACCOUNT_ID.value:
                del insight[parent_column_name]
            if campaign_id_column_name != Columns.INSIGHT_ACTOR_COLUMN and campaign_id_column_name in insight:
                del insight[campaign_id_column_name]
            if face_book_id_column_name in insight:
                del insight[face_book_id_column_name]

        return data

    def __add_actor_type_to_ids(self, data, actor_type):
        for insight in data:
            insight[Columns.INSIGHT_ACTOR_COLUMN] = actor_type + '_' + str(insight[Columns.INSIGHT_ACTOR_COLUMN])

            ad_account_id_string = str(insight[ColumnsEnum.GroupBy.AD_ACCOUNT_ID.value])
            ad_account_id_prefix_index = ad_account_id_string.rfind("_")
            ad_account_id_string = ad_account_id_string[ad_account_id_prefix_index + 1:]
            insight[ColumnsEnum.GroupBy.AD_ACCOUNT_ID.value] = "AdAccount_" + ad_account_id_string
        return data
