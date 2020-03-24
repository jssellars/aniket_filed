from enum import Enum

from Config import Endpoints

# TODO: check to see if this is still used
class ExternalTables(Enum):
    """Holds a reference to the relevant tables for insight fetching.
     Might need to be updated. Whole logic restructuring incoming"""

    # TODO : get rid of 2 from ActorStates
    ENDPOINT = Endpoints.get_campaing_insights_endpoint()
    CAMPAIGN = 'vCampaignInsightsDexter'
    ADSET = 'vAdSetInsightsDexter'
    AD = 'vAdInsightsDexter'
    BREAKDOWN = 'vAdSetInsightsDexter'
    INTEREST = 'vInterestInsightsDexter'
    ACTOR_STATES = 'vActorStatesDexter2'

# TODO: check to see if this is still used
class DetailsTables(Enum):
    AD = 'vAdDetailsDexter2'
    ADSET = 'vAdSetDetailsDexter2'
    CAMPAIGN = 'vCampaignDetailsDexter2'

# TODO: check to see if this is still used
class InternalTables(Enum):
    """Holds a reference to the relevant tables for insight updating and optimization fetching."""
    CONNECTION_STRING = 'mongodb+srv://admin:aB$1004--@stresstest-rg4rp.mongodb.net/test?retryWrites=true&w=majority'

    class Optimizations(Enum):
        DB_NAME = 'DexterOptimizations'
        OPTIMIZATION_TYPES = 'OptimizationTypes'
        EXPANDED_SUFFIX = 'Expanded'

    class ActorsData(Enum):
        DB_NAME = 'DexterActorsInfo'
        COLLECTION_NAME = 'New_ParentAndCampaignFiledIds'

    class InsightsData(Enum):
        DB_NAME = 'Filed_Turing_Facebook_Insights_Test'

    class GoalsData(Enum):
        DB_NAME = 'DexterCampaignGoals'
        COLLECTION_NAME = 'GoalDefinitions'

    class LogsData(Enum):
        DB_NAME = 'Dexter_Fuzzy_Inference_Recommendations'
        RECOMMENDATIONS_COLLECTION_NAME = 'recommendations-test-bugs'
        ERRORS_COLLECTION_NAME = 'errors'



