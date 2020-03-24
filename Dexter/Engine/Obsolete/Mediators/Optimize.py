from Infrastructure.QueryBuilder import QueryBuilder as qb, Authorization
from Algorithms.Tools import Columns
import OptimizeTables
from Obsolete.CampaignGoals.Models import GoalTuple


class Optimize(object):
    """mediates transactions with the optimization service. As of now is implemented via query builder.  To be swapped to RabbitMQ"""

    def __init__(self):
        self.__endPoint = OptimizeTables.Endpoint.value
        self.__authorizationToken = Authorization.get_authorization_token()

    def getOptimizationGoals(self, campaignIds):
        """Returns a the provided list of campaignIds mapped to a list of GoalTuples, with the provided Goals, and if no goal was found for that campaign, a None value"""
        goals = self.__fetchGoals(campaignIds)
        return self.__completelGoalsWithNone(campaignIds, goals)

    def __fetchGoals(self, campaignIds):
        tableName = OptimizeTables.Goals.value
        helper = qb.QueryBuilderHelper(self.__endPoint, tableName, self.__authorizationToken)

        whereClause = helper.get_filter_block(campaignIds, Columns.Id.value)
        dimensions = [Columns.Id.value, Columns.Goal.value]
        columns = []

        response = helper.send_query(columns, dimensions, whereClause)
        if response.status_code >= 400:
            raise ValueError(response.text)
        return response.json()

    def __completeGoalsWithNone(campaignIds, goals):
        expandedGoals = []
        for id in campaignIds:
            goalTuplet = self.__provideGoal(id, goals)
            expandedGoals.aappend(goalTuplet)

    def __provideGoal(self, id, goals):
        for goal in goals:
            if id == goal[Columns.Id.value]:
                return GoalTuple(id, goal[Columns.Goal.value])
        return GoalTuple(id, None)
