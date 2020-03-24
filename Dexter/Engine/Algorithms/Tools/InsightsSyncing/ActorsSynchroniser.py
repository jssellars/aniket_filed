from Algorithms.Models import Actor
from Algorithms.Models.Types import TypesWrapper as tw
from Algorithms.Tools import ColumnsEnum, Columns
from Infrastructure.Mongo.Mongo import MongoMediator


class ActorsSynchroniser(object):
    """Stores new actors and their metadata"""

    def __init__(self, mongo_mediator=None):
        if mongo_mediator is None:
            self.__mongo_mediator = MongoMediator()
        else:
            self.__mongo_mediator = mongo_mediator

    def store_new_actors_from_insights(self, data_for_type, optimization_type):
        new_actors_ids = self.__get_new_actor_ids(data_for_type, optimization_type)
        if len(new_actors_ids) != 0:
            actors_meta_data = self.__get_actors_metadata(new_actors_ids, data_for_type, optimization_type)
            self.__mongo_mediator.store_actors_metadata(actors_meta_data)

    def __get_new_actor_ids(self, data_for_type, optimization_type):
        existing_actors = self.__mongo_mediator.get_existing_actor_ids()

        data_actors = self.__get_actor_ids_out_of_data(data_for_type)
        new_actors = data_actors.difference(existing_actors)  # Set Difference. Returns the elements that are present in dataActors but no in existing_actors
        return new_actors

    def __get_actor_ids_out_of_data(self, data):
        actors = set()
        for insight in data:
            actors.add(str(insight[Columns.INSIGHT_ACTOR_COLUMN]))
        return actors

    def __get_actors_metadata(self, new_actor_ids, data_for_type, optimization_type: tw.OptimizationTuple):
        actors = []
        parent_column_name = Columns.Parents[optimization_type.breakdown].value
        id_column = Columns.INSIGHT_ACTOR_COLUMN
        campaign_id_column_name = Columns.CampaignId[optimization_type.breakdown].value
        for actor_id in new_actor_ids:
            matching_insight = self.__get_matching_insight(data_for_type, id_column, actor_id)
            # TODO Make this Sane somehow parentcolumn name is CampaignFiledId but we need Campaign
            # enums for id prefixes by level for the guy and parent ?
            parent_prefix = Columns.ParentPrefixesByLevel[optimization_type.breakdown].value
            parent_last_u_score_index = str(matching_insight[parent_column_name]).rfind("_")
            parent_id_for_prefix = str(matching_insight[parent_column_name])[parent_last_u_score_index + 1:]
            parent_id = parent_prefix + '_' + parent_id_for_prefix

            # this checks if the actor is an campaign
            # if it is, there is no need to prefix it anymore because the actor's own id is already prefixed
            if optimization_type.breakdown != tw.LevelNames.Campaign.value:
                campaign_id = tw.LevelNames.Campaign.value + '_' + str(matching_insight[campaign_id_column_name])
            else:
                campaign_id = str(matching_insight[campaign_id_column_name])
            face_book_id = matching_insight[ColumnsEnum.GroupBy.FACEBOOK_ID.value]
            actors.append(Actor(actor_id, parent_id, campaign_id, face_book_id))
        return actors

    def __get_matching_insight(self, insights_set, id_column_name, id):
        for insight in insights_set:
            if insight[id_column_name] == id:
                return insight
        return None
