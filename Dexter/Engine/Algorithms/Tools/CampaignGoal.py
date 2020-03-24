from Infrastructure.Mongo.Mongo import MongoMediator
from Algorithms.Tools import Columns
from Obsolete import GoalsEnum
from Algorithms.Tools.RemoveActorPrefix import remove_actor_prefix
from Infrastructure.QueryBuilder.QueryBuilderMediator import QueryBuilderMediator


class GoalGetter:

    def __init__(self, token):        
        self.qb = QueryBuilderMediator(token)
        self.campaign_goals = self.__get_campaign_goals_from_campaign_insights()

    def get_campaign_goal(self, actor_id):
        mongo_mediator = MongoMediator()
        parent_and_campaign_id = mongo_mediator.get_parent_and_campaign_id(actor_id)
        campaign_id = parent_and_campaign_id[Columns.ParentAndCampaignIdsColumnNames.CAMPAIGN.value]
        goal = self.campaign_goals.get(int(remove_actor_prefix(campaign_id)))
        return goal

    def __get_campaign_goals_from_campaign_insights(self):
        response = self.qb.get_goals()
        result = {}
        for campaign in response:
            if campaign['Goal'] is None:
                result[campaign['id']] = GoalsEnum.Goals.CPC.value
            else:
                result[campaign['id']] = campaign['Goal']
        return result
