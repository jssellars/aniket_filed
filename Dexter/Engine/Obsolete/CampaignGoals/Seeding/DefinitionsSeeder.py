from Algorithms.Tools import Columns
from Obsolete import GoalsEnum
from Infrastructure.Mongo.Mongo import MongoMediator
from Obsolete.CampaignGoals import GoalTuple
import logging

class DefinitionsSeeder(object):
    """This class aims to provide a goal definition Seeding mechanism"""
    @staticmethod
    def SeedGoals() :
        try:
            logging.info("Started seeding goal definitions")
            goalDefinitions = []
            for i , kvpair in enumerate(Columns.relevant_metrics.items()):
                # kvpair[0] - internal name kvpair[1] - MetricsDefinition

                id = i
                internalName = kvpair[0]
                metricsList = [{"Metric" : x.Metric , "Multiplier" : x.Multiplier } for x in kvpair[1]]
                displayName = GoalsEnum.goalDisplayNames[internalName]

                goalDefinition = GoalTuple(id, internalName,  displayName, metricsList).__dict__
            
                goalDefinitions.append(goalDefinition)

            mediator = MongoMediator()
            mediator.store_goal_definitions(goalDefinitions)
            logging.info('Finished seeding goal definitions')
        
        except Exception as e:
            logging.exception(e)
