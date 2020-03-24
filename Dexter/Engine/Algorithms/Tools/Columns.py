import collections
from enum import Enum

from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import ColumnsEnum
from Infrastructure.QueryBuilder import QueryBuilder as Qb
from Obsolete import GoalsEnum

# TODO: This should be in QueryBuilder. Kinda

breakdown_name_to_id_mapping = {
    "None": 0,
    "Age": 2,
    "Age and Gender": 3,
    "Gender": 6,
    "Impression Device": 8,
    "Device Platform": 21,
    "Country": 22,
    "Region": 23,
    "Placement": 26
}

interest_name = "InterestName"

breakdown_columns = {
    "Breakdown": 'Parameters_DeliveryBreakdownValue',
    "Interest": "Parameters_DeliveryBreakdownValue"
}

class DexterEngineRunJournalObject:

    def __init__(self,
                 business_owner_id=None,
                 ad_account_id=None,
                 algorithm_type=None,
                 run_status=None,
                 start_timestamp=None,
                 end_timestamp=None):

        self.business_owner_id = business_owner_id
        self.ad_account_id = ad_account_id
        self.algorithm_type = algorithm_type.value if algorithm_type is not None else None
        self.run_status = run_status.value if run_status is not None else None
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

class DexterEngineRunJournalEnum(Enum):

    BUSINESS_OWNER_ID = 'business_owner_id'
    AD_ACCOUNT_ID = 'ad_account_id'
    ALGORITHM_TYPE = 'algorithm_type'
    RUN_STATUS = 'run_status'
    START_TIMESTAMP = 'start_timestamp'
    END_TIMESTAMP = 'end_timestamp'


class RunStatusDexterEngineJournal(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    PENDING = 'pending'
    FAILED = 'failed'

class ExtraColumnInfo:
    column_name = ''
    aggregator = ''

    def __init__(self, column_name, aggregator):
        self.column_name = column_name
        self.aggregator = aggregator


extra_columns = {
    'Budget': [ExtraColumnInfo('Budget', Qb.ColumnAggregator.sum)],
    'Ad': [ExtraColumnInfo('RelevancyScore', Qb.ColumnAggregator.avg)]
}

goal_metric = collections.namedtuple('GoalMetric',
                                     'Metric Multiplier')  # named tuple of Type GoalMetric with the Metric and MultyplierFields


# Multiplyer should be -1 for costs and 1 for other metrics (so higher cost lead to lower scores because of greater negative numbers)


class EvaluatedActorColumnNames(Enum):
    IDENTITY_COLUMN = "FiledId"
    INSIGHTS_COLUMN = "Insights"
    SCORE_COLUMN = "Score"
    STATE_COLUMN = "State"


extra_dimensions = {
    'Interest': ['CampaignFiledId']
}


class RecommendationSource(Enum):
    DEXTER = 'Dexter'
    FACEBOOK = 'Facebook'
    GOOGLE = 'Google'


class RecommendationFieldNames(Enum):
    MESSAGE_TYPE = "MessageType"
    ACTOR_ID = "ActorId"
    FACEBOOK_ID = "facebook_id"
    LEVEL = "Level"
    PARAMS = "Params"
    TIME_STAMP = "TimeStamp"
    SOURCE = "Source"


parent = "Parent"
INSIGHT_ACTOR_COLUMN = "FiledId"


class WeightedVolumeColumnNames(Enum):
    VOLUME_COLUMN = "Volume"
    WEIGHT_COLUMN = "Weight"


class PreProcessColumnNames(Enum):
    INSIGHT_ACTOR_COLUMN = "FiledId"  # the column of an insight from which we get the actor
    ACTOR_INSIGHTS_KEY = 'Insights'  # The key of the Actor at which the insight list is found
    PARENT_ACTORS_KEY = 'Actors'  # The key of the Parent at which the Actor list is found
    PARENT_COLUMN = 'Parent'
    CAMPAIGN_GOAL = 'Goal'
    STATE = 'State'


class ProcessColumnNames(Enum):
    ACTOR_IDENTITY_COLUMN = "FiledId"  # the unique identifier of the actors after being grouped by parent
    TIME_STAMP = 'Parameters_Until'
    VOLUME_COLUMN = 'Volume'
    BUDGET_COLUMN = 'Budget'
    PARENT_COLUMN = 'Parent'


class EvaluatedParentsColumnNames(Enum):
    ACTORS = 'Actors'
    ID = 'id'


class CampaignId(Enum):
    CAMPAIGN = "FiledId"
    ADSET = "CampaignFiledId"
    AD = "CampaignFiledId"
    BREAKDOWN = "CampaignFiledId"
    INTEREST = "CampaignFiledId"


class ConfidenceImportanceValues(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class RecommendationSources(Enum):
    FACEBOOK = "Facebook"
    DEXTER = "Dexter"


relevant_metrics = {GoalsEnum.Goals.CPC.value: [goal_metric(Metric=ColumnsEnum.Costs.CPC.value, Multiplier=-1),
                                                goal_metric(Metric=ColumnsEnum.Metrics.CLICKS.value, Multiplier=1)
                                                ],
                    GoalsEnum.Goals.CPM.value: [goal_metric(Metric=ColumnsEnum.Metrics.IMPRESSIONS.value, Multiplier=1),
                                                goal_metric(Metric=ColumnsEnum.Costs.CPM.value, Multiplier=-1)
                                                ],
                    GoalsEnum.Goals.CTR.value: [goal_metric(Metric=ColumnsEnum.Metrics.CLICKS.value, Multiplier=1),
                                                goal_metric(Metric=ColumnsEnum.Metrics.CTR.value, Multiplier=1)
                                                ],
                    GoalsEnum.Goals.Impressions.value: [
                        goal_metric(Metric=ColumnsEnum.Metrics.IMPRESSIONS.value, Multiplier=1)],
                    GoalsEnum.Goals.Clicks.value: [goal_metric(Metric=ColumnsEnum.Metrics.CLICKS.value, Multiplier=1)],
                    GoalsEnum.Goals.Reach.value: [goal_metric(Metric=ColumnsEnum.Metrics.REACH.value, Multiplier=1)],
                    GoalsEnum.Goals.CPP.value: [goal_metric(Metric=ColumnsEnum.Costs.CPP.value, Multiplier=-1)]

                    # GoalsEnum.Goals.CPA.value : [],  # Results / Costs per action. We don't have this columns yet
                    # GoalsEnum.Goals.ROAS.value: []  # Conversions / Results. We don't have this columns yet (they might be if we get new data, but they are not in DexterInsightsTest)
                    }


class RecommendationTypes(Enum):
    AUDIENCE = 'Audience'
    BUDGET_AND_BID = 'Budget & Bid'
    CREATIVE = 'Creative'
    PERFORMANCE = 'Performance'
    PLACEMENT_AND_DEVICE = 'Placement & Device'


class Parents(Enum):
    CAMPAIGN = 'AdAccountId'
    ADSET = 'CampaignFiledId'
    AD = 'AdSetFiledId'
    INTEREST = 'CampaignFiledId'
    BREAKDOWN = 'CampaignFiledId'


class ParentPrefixesByLevel(Enum):
    CAMPAIGN = 'AdAccount'
    ADSET = 'Campaign'
    AD = 'AdSet'
    BREAKDOWN = 'AdSet'
    INTEREST = 'AdSet'  # not sure need to see Interest Data Fetching


class ParentAndCampaignIdsColumnNames(Enum):
    ID = "FiledId"
    PARENT = "ParentId"
    CAMPAIGN = "CampaignId"
    STATE = "State"


class FacebookRecommendationFieldNames(Enum):
    BLAME_FIELD = 'blame_field'
    CONFIDENCE = 'confidence'
    IMPORTANCE = 'importance'
    MESSAGE = 'message'
    TITLE = 'title'


class ChannelEnum(Enum):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'

class AlgorithmName(Enum):
    DEXTER_FUZZY_INFERENCE = "Dexter_Fuzzy_Inference"
    DEXTER_FUZZY_INFERENCE_TEST = "Dexter_Fuzzy_Inference_Test"


# this violates DRY needs refactor
def get_all_column_and_dimension_names(optimization: Tw.OptimizationTuple):
    all_names = []
    for cost in ColumnsEnum.Costs:
        all_names.append(cost.value)
    for metric in ColumnsEnum.Metrics:
        all_names.append(metric.value)
    for group_col in ColumnsEnum.GroupBy:
        all_names.append(group_col.value)
    if optimization is not None:
        # Extra columns by optimization type
        extra_cols = extra_columns.get(optimization.level, [])
        extra_col_names = [x.column_name for x in extra_cols]
        all_names.extend(extra_col_names)
        # Extra dimensions by optimization type
        all_names.extend(extra_dimensions.get(optimization.level, []))
        # Parent specific dimensions
        parent_ = Parents[optimization.breakdown].value
        all_names.append(parent_)
        if optimization.breakdown == Tw.LevelNames.Interest.value:
            all_names.append(interest_name)

    return all_names


def get_columns(optimization: Tw.OptimizationTuple = None):
    columns = []
    dimensions = []
    # COSTS. Add Cpr once it's in the db
    costs = []
    costs_aggregator = Qb.ColumnAggregator.avg
    for cost in ColumnsEnum.Costs:
        costs.append(_to_column(cost.value, costs_aggregator))
    columns += costs

    # Metrics
    metrics = []
    metrics_aggregator = Qb.ColumnAggregator.sum
    for metric in ColumnsEnum.Metrics:
        metrics.append(_to_column(metric.value, metrics_aggregator))
    columns += metrics

    # Meta - dimensions
    group_by = []
    for group_col in ColumnsEnum.GroupBy:
        group_by.append(group_col.value)
    dimensions += group_by
    if optimization.breakdown == Tw.LevelNames.Interest.value:
        dimensions.append(interest_name)

    if optimization is not None:
        # Extra columns by optimization type
        columns.extend([_to_column(x.column_name, x.aggregator) for x in extra_columns.get(optimization.level, [])])
        columns.extend([_to_column(x.column_name, x.aggregator) for x in extra_columns.get(optimization.breakdown, [])])
        # Extra dimensions by optimization type
        dimensions.extend(extra_dimensions.get(optimization.level, []))
        # Parent specific dimensions
        parent_ = Parents[optimization.breakdown].value
        if parent_ not in dimensions:
            dimensions.append(parent_)
        if optimization.breakdown == Tw.LevelNames.Ad.value:
            # We need the CampaignFiledId regardless for fetching goals
            dimensions.append("CampaignFiledId")

    query_data = dict()
    query_data["Columns"] = columns
    query_data["Dimensions"] = dimensions

    return query_data


def _to_column(name, aggregator):
    return {
        'name': name,
        'Aggregator': aggregator
    }
