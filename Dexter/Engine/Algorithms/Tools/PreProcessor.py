import math

import pandas as pd

from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import Columns
from Algorithms.Tools import Constants
from Infrastructure.Mongo.Mongo import MongoMediator
from Obsolete import GoalsEnum

mongo_mediator = MongoMediator()


def group_insights_on_actors_recommend(insights_data, optimization: Tw.OptimizationTuple, goal_enum: GoalsEnum.Goals):
    # Creates a new pandas Data Frame with all the insights grouped by Actor
    insights_data_frame = pd.DataFrame(insights_data)

    actor_parent = Columns.Parents[optimization.breakdown].value

    dicts_for_new_df = {
        Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value: [],
        actor_parent: [],
        Columns.ParentAndCampaignIdsColumnNames.CAMPAIGN.value: [],
        Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value: [],
        Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value: [],
        Columns.PreProcessColumnNames.STATE.value: []
    }

    all_columns = Columns.get_all_column_and_dimension_names(optimization)

    for name, group in insights_data_frame.groupby(Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value):
        insights = []
        actor_parent_and_campaign_data = mongo_mediator.get_parent_and_campaign_id(name)
        parent_id = actor_parent_and_campaign_data[Columns.ParentAndCampaignIdsColumnNames.PARENT.value]
        campaign_id = actor_parent_and_campaign_data[Columns.ParentAndCampaignIdsColumnNames.CAMPAIGN.value]
        state = actor_parent_and_campaign_data[Columns.ParentAndCampaignIdsColumnNames.STATE.value]
        goal = goal_enum.value

        for insight in group.itertuples(name="insight"):
            mini_insight = {}
            for key, value in insight._asdict().items():
                if key not in [Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value] and key in all_columns:
                    mini_insight[key] = value

            insights.append(mini_insight)
        if state != Tw.ActorStates.Deleted.value:
            dicts_for_new_df[Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value].append(name)
            if actor_parent != Columns.ParentAndCampaignIdsColumnNames.CAMPAIGN.value:
                dicts_for_new_df[actor_parent].append(parent_id)
            dicts_for_new_df[Columns.ParentAndCampaignIdsColumnNames.CAMPAIGN.value].append(campaign_id)
            dicts_for_new_df[Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value].append(insights)
            dicts_for_new_df[Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value].append(goal)
            dicts_for_new_df[Columns.PreProcessColumnNames.STATE.value].append(state)

    new_df = pd.DataFrame(dicts_for_new_df)
    return new_df


def group_breakdowns_inside_actors(bd_actors: pd.DataFrame, optimization: Tw.OptimizationTuple):
    # actor_parent = Columns.Parents[optimization.breakdown].value
    breakdown_grouped_actors = []
    all_columns = Columns.get_all_column_and_dimension_names(optimization)
    breakdown_column_name = Columns.breakdown_columns[optimization.breakdown]

    for actor in bd_actors.itertuples():
        # the tuple returned by itertuples holds the following information by index
        # 0 - index
        # 1 - FiledId (the Actor identifier)
        # 2 - AdAccountId
        # 3 - CampaignId
        # 4 - Insights        
        # 5 - Goal
        # 6 - State

        tuple_insights_index = 4
        # actorIdIndex = 1
        grouped_actor = dict()
        grouped_actor[Columns.PreProcessColumnNames.PARENT_COLUMN.value] = actor[1]
        grouped_actor[Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value] = actor[5]
        grouped_actor[Columns.PreProcessColumnNames.STATE.value] = actor[6]
        breakdowns = {}

        # TODO : Clean this up don't iterate twice
        for insight in actor[tuple_insights_index]:
            if insight[breakdown_column_name] not in breakdowns:
                breakdowns[insight[breakdown_column_name]] = []
            mini_insight = {}
            for key, value in insight.items():
                if key not in [Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value,
                               breakdown_column_name] and key in all_columns:
                    mini_insight[key] = value
            breakdowns[insight[breakdown_column_name]].append(mini_insight)

        final_breakdowns = []

        for breakdown in breakdowns.items():
            final_breakdown = dict()
            final_breakdown[Columns.PreProcessColumnNames.INSIGHT_ACTOR_COLUMN.value] = breakdown[0]
            final_breakdown[Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value] = breakdown[1]
            if optimization.breakdown == Tw.LevelNames.Interest.value:
                # breakdown[1] is the list of insights. breakdown[1][0] is the first insights.
                # InterestName is in each insight at this point
                # it will be dropped from each insight after volume is computed
                final_breakdown[Columns.interest_name] = breakdown[1][0][Columns.interest_name]
            final_breakdowns.append(final_breakdown)

        grouped_actor[Columns.PreProcessColumnNames.PARENT_ACTORS_KEY.value] = final_breakdowns
        breakdown_grouped_actors.append(grouped_actor)

    return breakdown_grouped_actors


def group_actors_on_parents(actors: pd.DataFrame, optimization: Tw.OptimizationTuple, goal: GoalsEnum.Goals):
    # Creates a list of dictionaries out of a DataFrame.
    # Each dictionary represents a parent with a list of Actors and each Actor has a list of insights
    # Use this after group_insights_on_actors
    # Note : Campaigns are grouped on goals, not Ad Accounts

    actor_parent = Columns.Parents[optimization.breakdown].value
    if optimization.breakdown == Tw.LevelNames.Campaign.value:
        actor_parent = Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value

    parent_dicts = []
    for name, group in actors.groupby(actor_parent):

        parent_dict = dict()
        parent_dict[Columns.parent] = actor_parent
        parent_dict[Columns.PreProcessColumnNames.PARENT_COLUMN.value] = name
        actors = []
        all_columns = Columns.get_all_column_and_dimension_names(optimization)

        for actor in group.itertuples(name="actor"):
            mini_actor = {}
            for key, value in actor._asdict().items():
                # need to check if the key is in AllColumnAndDimensionNames because pandas adds index column
                # or key == Columns.actorInsightsKey because the list of Insights
                # is not in the Columns in Mongo and we need that as well (the most)
                if key not in [actor_parent] and (
                        key in all_columns or key in [Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value,
                                                      Columns.PreProcessColumnNames.STATE.value]):
                    mini_actor[key] = value
            actors.append(mini_actor)

        parent_dict[Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value] = goal.value
        parent_dict[Columns.PreProcessColumnNames.PARENT_ACTORS_KEY.value] = actors
        parent_dicts.append(parent_dict)

    return parent_dicts

    # Maps the actor's insight to volume for each insight of each parent


def evaluate_actors_by_campaign_goal(insights_data):
    evaluated_parents = []
    for parent in insights_data:
        evaluated_actors = []
        goal = parent.get(Columns.PreProcessColumnNames.CAMPAIGN_GOAL.value)

        for actor in parent.get(Columns.PreProcessColumnNames.PARENT_ACTORS_KEY.value):
            actor_volumes = get_insight_volumes_from_actor_by_campaign_goal(actor, goal)
            new_actor = dict()
            new_actor[Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value] = actor.get(
                Columns.ProcessColumnNames.ACTOR_IDENTITY_COLUMN.value)
            new_actor[Columns.EvaluatedActorColumnNames.INSIGHTS_COLUMN.value] = actor_volumes
            new_actor[Columns.EvaluatedActorColumnNames.STATE_COLUMN.value] = actor.get(
                Columns.EvaluatedActorColumnNames.STATE_COLUMN.value)
            if Columns.interest_name in actor:
                new_actor[Columns.interest_name] = actor[Columns.interest_name]
            if new_actor[Columns.EvaluatedActorColumnNames.STATE_COLUMN.value] != Tw.ActorStates.Deleted.value:
                evaluated_actors.append(new_actor)
        evaluated_parent = dict()
        evaluated_parent[Columns.EvaluatedParentsColumnNames.ACTORS.value] = evaluated_actors
        evaluated_parent[Columns.EvaluatedParentsColumnNames.ID.value] = parent[
            Columns.PreProcessColumnNames.PARENT_COLUMN.value]

        evaluated_parents.append(evaluated_parent)
    return evaluated_parents

    # Strips the insights of an Actor for non-relevant metrics,
    # keeping only those relevant to the campaign goal (as volume) ,
    # the timestamp and the insight's budget (necessary for a Increase Budget or Decrease Budget Verdict)


def get_insight_volumes_from_actor_by_campaign_goal(actor, campaign_goal):
    if campaign_goal is None:
        campaign_goal = GoalsEnum.Goals.CPC.value

    relevant_metrics = Columns.relevant_metrics.get(campaign_goal)
    optimization_metric = relevant_metrics[0].Metric
    optimization_multiplier = relevant_metrics[0].Multiplier
    actor_insights_volumes = []
    time_stamps = []
    budgets = []

    sorted_insights = sorted(actor[Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value], key=lambda i: i[
        Columns.ProcessColumnNames.TIME_STAMP.value])

    for insight in sorted_insights:
        volume = insight.get(optimization_metric)
        timestamp = insight.get(Columns.ProcessColumnNames.TIME_STAMP.value)
        budget = insight.get(Columns.ProcessColumnNames.BUDGET_COLUMN.value)

        #  check for a volume of null
        #  on cost metrics because it means the actor generates no clicks so we need a big value there 
        # (there is a huge cost when the returns are 0)
        # 1000 instead of math.inf because weighted average of a list including infinities is kinda iffy
        # for other goals, volume is a return not a cost so 0 is fine

        if math.isnan(volume):
            # TODO: Extend with other cost metrics
            if campaign_goal in [GoalsEnum.Goals.CPC.value, GoalsEnum.Goals.CPM.value]:
                volume = 1000
            else:
                volume = 0

        actor_insights_volumes.append(volume)
        time_stamps.append(timestamp)
        budgets.append(budget)

    # fill Nans which are now -1
    actor_insights_volumes = fill_minus_ones(actor_insights_volumes)

    # optimization multiplier is -1 for goals which seek minimization
    # of a metric (mostly costs which should be minimized not maximized)
    # the values are made negative so that greater costs are worse

    actor_insights_volumes = [x * optimization_multiplier for x in actor_insights_volumes]

    final_actor_insights_volumes = [{
        Columns.ProcessColumnNames.VOLUME_COLUMN.value: x[0],
        Columns.ProcessColumnNames.TIME_STAMP.value: x[1],
        Columns.ProcessColumnNames.BUDGET_COLUMN.value: x[2]

    } for x in zip(actor_insights_volumes, time_stamps, budgets)]

    return final_actor_insights_volumes


# Full Preprocessing Pipeline
def pre_process_data(insights_data, optimization: Tw.OptimizationTuple, goal_getter: GoalsEnum.Goals):
    if len(insights_data) == 0:
        raise Exception("Cannot preprocess empty insights Data")
    intermediary_df = group_insights_on_actors_recommend(insights_data, optimization, goal_getter)

    if optimization.breakdown in [Tw.LevelNames.Breakdown.value, Tw.LevelNames.Interest.value]:
        parent_dicts = group_breakdowns_inside_actors(intermediary_df, optimization)
    else:
        parent_dicts = group_actors_on_parents(intermediary_df, optimization, goal_getter)

    evaluated_actors = evaluate_actors_by_campaign_goal(parent_dicts)
    return evaluated_actors


def fill_minus_ones(values):
    last_good_index = -1

    i = 0
    while i < len(values):
        next_good_index = len(values)
        if values[i] != -1:
            last_good_index = i
        if values[i] == -1:
            # find the next non -1 value in the list            
            for j in range(i + 1, len(values)):
                if values[j] != -1:
                    next_good_index = j
                    break

            fill_value = 0
            num_values = 0
            if last_good_index != -1:
                fill_value += values[last_good_index]
                num_values += 1

            if next_good_index != len(values):
                fill_value += values[next_good_index]
                num_values += 1
                fill_value = fill_value / num_values

            if num_values == 0:
                fill_value = 0

            for k in range(i, next_good_index):
                values[k] = fill_value

            i = next_good_index
        i += 1

    return values


def group_data_for_analise(insights_data, combination):
    data = group_insights_on_actors(insights_data)
    data = group_breakdowns(data, combination)
    return data


# TODO: get rid of useless fields from insight
def group_breakdowns(actor_insights_data, combination):
    actors_with_grouped_breakdowns = {}
    keys = list(actor_insights_data.keys())
    if len(actor_insights_data) > 0:
        actor_insight = actor_insights_data[keys[0]]
        insight = actor_insight[0]
    else:
        return actors_with_grouped_breakdowns

    # TODO: remove 'results' from this list, Andrei fucked up :D
    # TODO: remove also conversions from this list
    unusable_metric_fields = ['account_id', 'conversions', 'objective', 'date_start', 'date_stop', 'account_id',
                              'link_click', 'account_name', combination.breakdown, 'results',
                              'bid_info', 'bid_strategy', 'bid_info', 'bid_amount', 'conversion_rate_ranking', 'engagement_rate_ranking']
    actual_breakdown = 'none'
    for breakdown in Constants.BREAKDOWNS:
        if breakdown in insight.keys():
            actual_breakdown = breakdown
            break

    for actor in actor_insights_data:
        grouped_breakdowns = {}
        for insight in actor_insights_data[actor]:
            mini_insight = {}
            for key in insight:
                if key not in unusable_metric_fields:
                    insight_value = insight[key]
                    if insight_value is not None:
                        mini_insight[key] = insight_value
                    else:
                        mini_insight[key] = 0.0

            if actual_breakdown == 'none':
                if 'none' not in grouped_breakdowns:
                    grouped_breakdowns['none'] = {}
                    grouped_breakdowns['none'][insight['date_stop']] = mini_insight
                else:
                    grouped_breakdowns['none'][insight['date_stop']] = mini_insight
            else:
                if insight[actual_breakdown] not in grouped_breakdowns:
                    grouped_breakdowns[insight[actual_breakdown]] = {}
                    grouped_breakdowns[insight[actual_breakdown]][
                        insight['date_stop']] = mini_insight
                else:
                    grouped_breakdowns[insight[actual_breakdown]][
                        insight['date_stop']] = mini_insight
        actors_with_grouped_breakdowns[actor] = grouped_breakdowns
    return actors_with_grouped_breakdowns


# TODO: get facebook_id instead of iterating through levels
def group_insights_on_actors(insights_data):
    grouped_insights = {}

    # Not sure if the right way to go

    if len(insights_data) > 0:
        insight = insights_data[0]
    else:
        return grouped_insights

    if 'ad_id' in insight.keys():
        facebook_id = 'ad_id'
    elif 'adset_id' in insight.keys():
        facebook_id = 'adset_id'
    else:
        facebook_id = 'campaign_id'

    for insight in insights_data:
        if insight[facebook_id] in grouped_insights:
            grouped_insights[insight[facebook_id]].append(insight)
        else:
            grouped_insights[insight[facebook_id]] = []
            grouped_insights[insight[facebook_id]].append(insight)

    return grouped_insights
