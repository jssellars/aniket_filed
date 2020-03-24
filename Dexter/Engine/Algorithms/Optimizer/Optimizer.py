import datetime
import json
import math
import sys

import matplotlib.pyplot as plt
import xlsxwriter

from Algorithms.Dexter_Fuzzy_Inference.Trends import TrendTypes
from Algorithms.Models.Types import TypesWrapper as Tw
from Algorithms.Tools import Columns
from Algorithms.Tools.TimeInterval import TimeInterval
from Infrastructure.Rabbit.Messages.RabbitMessagesMetadata import (BudgetMessageFieldNames,
                                                                   RemoveBDMessageFieldNames, Recommendation)
from Obsolete import GoalsEnum


def generate_recommendations(evaluated_parents, optimization_type: Tw.OptimizationTuple, ad_account_id, metric):
    recommendations = []
    for parent in evaluated_parents:
        evaluated_actors = parent.get(Columns.EvaluatedParentsColumnNames.ACTORS.value)
        # take this out in new function
        for actor in evaluated_actors:
            weighted_volumes = add_weights_to_sorted_volumes(actor.get(
                Columns.EvaluatedActorColumnNames.INSIGHTS_COLUMN.value))
            actor[Columns.EvaluatedActorColumnNames.SCORE_COLUMN.value] = calculate_actor_weighted_average(weighted_volumes)

        sorted_evaluated_actors = sorted(evaluated_actors, key=lambda a: a[
            Columns.EvaluatedActorColumnNames.SCORE_COLUMN.value], reverse=True)

        for recommendation in generate_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type, ad_account_id, metric):
            recommendations.append(recommendation)

    return recommendations


def generate_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type: Tw.OptimizationTuple, ad_account_id, metric):
    recommendations = []

    if optimization_type.level == 'Budget':
        # split simirally performing actors before generating actor ranking recommendations

        recommendations = generate_budget_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type, ad_account_id, metric)

    if optimization_type.breakdown in [Tw.LevelNames.Breakdown.value, Tw.LevelNames.Interest.value]:
        recommendations = generate_break_down_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type, ad_account_id, metric)

    return recommendations


def generate_budget_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type: Tw.OptimizationTuple, ad_account_id, metric):
    recommendations = []
    num_actors = len(sorted_evaluated_actors)

    if optimization_type.breakdown == Tw.LevelNames.Ad.value:
        # TODO : make this more nuanced now we just runAlgorithm2 stopping the worst Ad of each Adset
        # Also starting the best one if it's stopped :D

        ad_middle = num_actors // 2
        for actor in sorted_evaluated_actors[0:ad_middle]:
            if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.Off.value:
                recommendations.append(generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))
        for actor in sorted_evaluated_actors[ad_middle + 1:]:
            if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                recommendations.append(generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.Stop, ad_account_id, metric))

        return recommendations

    if num_actors == 1:
        if sorted_evaluated_actors[0].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.IncreaseBudget, ad_account_id,
                                               metric))
        else:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))

    if num_actors == 2:
        if sorted_evaluated_actors[0].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.IncreaseBudget, ad_account_id,
                                               metric))
        else:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))

        if sorted_evaluated_actors[1].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[1], optimization_type, Tw.RecommendationVerdicts.DecreaseBudget, ad_account_id,
                                               metric))

    if num_actors == 3:
        if sorted_evaluated_actors[0].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.IncreaseBudget, ad_account_id,
                                               metric))
        else:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[0], optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))

        if optimization_type.breakdown != Tw.LevelNames.Campaign.value:
            if sorted_evaluated_actors[1].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                recommendations.append(
                    generate_split_structure_recommendation([sorted_evaluated_actors[1]], optimization_type, Tw.RecommendationVerdicts.Split,
                                                            ad_account_id, metric))

        if sorted_evaluated_actors[0].get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
            recommendations.append(
                generate_budget_recommendation(sorted_evaluated_actors[2], optimization_type, Tw.RecommendationVerdicts.Stop, ad_account_id, metric))

    if num_actors >= 4:
        actor_group_size = num_actors // 4
        for actor in sorted_evaluated_actors[1:actor_group_size + 1]:
            if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                recommendations.append(
                    generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.IncreaseBudget, ad_account_id, metric))
            else:
                recommendations.append(generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))

        if optimization_type.breakdown != Tw.LevelNames.Campaign.value:
            to_split = []
            for actor in sorted_evaluated_actors[actor_group_size + 1: 2 * actor_group_size + 1]:
                if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                    to_split.append(actor)
                else:
                    recommendations.append(
                        generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.Start, ad_account_id, metric))

            if len(to_split) > 0:
                recommendations.append(generate_split_structure_recommendation(parent, to_split, optimization_type, metric))

        for actor in sorted_evaluated_actors[2 * actor_group_size + 1: 3 * actor_group_size + 1]:
            if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                recommendations.append(
                    generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.DecreaseBudget, ad_account_id, metric))

        for actor in sorted_evaluated_actors[3 * actor_group_size + 1: num_actors]:
            if actor.get(Columns.PreProcessColumnNames.STATE.value) == Tw.ActorStates.On.value:
                recommendations.append(generate_budget_recommendation(actor, optimization_type, Tw.RecommendationVerdicts.Stop, ad_account_id, metric))

    good_recommendations = [recommendation for recommendation in recommendations if recommendation is not None]

    return good_recommendations


def generate_split_structure_recommendation(parent, actors, optimization_type: Tw.OptimizationTuple, ad_account_id, metric):
    if Columns.EvaluatedParentsColumnNames.ID.value not in parent:
        return
    recommendation = Recommendation()
    recommendation.structureId = parent[Columns.EvaluatedParentsColumnNames.ID.value]
    recommendation.level = Columns.ParentPrefixesByLevel[optimization_type.breakdown].value
    # Application Details
    recommendation.applicationDetails = {"values": [actor[Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value] for actor in actors]}
    #
    recommendation.recommendationType = Columns.RecommendationTypes.SplitStructure.value
    recommendation.optimizationType = optimization_type.level
    recommendation.source = Columns.RecommendationSource.DEXTER.value
    recommendation.confidence = Columns.ConfidenceImportanceValues.LOW.value
    recommendation.importance = Columns.ConfidenceImportanceValues.LOW.value
    recommendation.adAccountId = 'act_' + ad_account_id
    recommendation.metric = metric
    # TODO: WRITE TEMPLATE FOR SPLIT STRUCTURE
    children_level = ''
    if recommendation.level == Tw.LevelNames.Campaign.value:
        children_level = Tw.LevelNames.AdSet.value
    if recommendation.level == Tw.LevelNames.AdSet.value:
        children_level = Tw.LevelNames.Ad.value
    recommendation.template = f"Split ${children_level}s "
    for actor in actors:
        print(actor)
    return recommendation


def generate_budget_recommendation(actor, optimization_type: Tw.OptimizationTuple, recommendation_type: Tw.RecommendationVerdicts, ad_account_id, metric,
                                   budget_fluctuation_value=15):
    # BudgetFluctuationValue =  percent change of budget for Increase Budget / Decrease Budget recommendations
    recommendation = Recommendation()
    recommendation.structureId = actor[Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value]
    recommendation.level = optimization_type.breakdown

    recommendation.optimizationType = optimization_type.level

    recommendation.source = Columns.RecommendationSource.DEXTER.value
    recommendation.confidence = Columns.ConfidenceImportanceValues.MEDIUM.value
    recommendation.importance = Columns.ConfidenceImportanceValues.MEDIUM.value

    old_budget = actor[Columns.EvaluatedActorColumnNames.INSIGHTS_COLUMN.value][-1].get(
        Columns.ProcessColumnNames.BUDGET_COLUMN.value, 0)
    if old_budget is None:  # ugly hack but necessary because the Mongo Collections for some Optimizations type don't have a BudgetField
        old_budget = 0  # not sure if necessary now because we won't generate Budget recommendation for non-Budget recommendation types
        # however, the current Data in Mongo might still have this gap so we should keep this until the next sync

    if old_budget == 0 and recommendation_type in [Tw.RecommendationVerdicts.IncreaseBudget, Tw.RecommendationVerdicts.DecreaseBudget]:
        return

    recommendation.applicationDetails = {"budgetFluctuationValue": budget_fluctuation_value}
    recommendation.adAccountId = 'act_' + ad_account_id
    recommendation.metric = metric

    if recommendation_type == Tw.RecommendationVerdicts.Stop:
        recommendation.template = f"{recommendation.level}" + " {" + recommendation.structureId.split('_')[
            1] + "} is performing very poorly. Turn it off!"
        recommendation.recommendationType = Columns.RecommendationTypes.PERFORMANCE.value
        return recommendation

    if recommendation_type == Tw.RecommendationVerdicts.Start:
        recommendation.template = f"{recommendation.level}" + " {" + recommendation.structureId.split('_')[
            1] + "}  performed very well in the past. Turn it on!!"
        recommendation.recommendationType = Columns.RecommendationTypes.PERFORMANCE.value
        return recommendation

    new_budget = 0
    if recommendation_type == Tw.RecommendationVerdicts.IncreaseBudget:
        new_budget = old_budget + old_budget * budget_fluctuation_value / 100
        recommendation.applicationDetails[BudgetMessageFieldNames.EFFECT.value] = "Increase"
        recommendation.template = f"Increase {recommendation.level}'s" + " {" + recommendation.structureId.split('_')[
            1] + "}" + f" budget by {budget_fluctuation_value}%"
        recommendation.recommendationType = Columns.RecommendationTypes.BUDGET_AND_BID.value
    if recommendation_type == Tw.RecommendationVerdicts.DecreaseBudget:
        new_budget = old_budget - old_budget * budget_fluctuation_value / 100
        recommendation.applicationDetails[BudgetMessageFieldNames.EFFECT.value] = "Decrease"
        recommendation.template = f"Decrease {recommendation.level}'s" + " {" + recommendation.structureId.split('_')[
            1] + "}" + f" budget by {budget_fluctuation_value}%"
        recommendation.recommendationType = Columns.RecommendationTypes.BUDGET_AND_BID.value
    recommendation.applicationDetails[BudgetMessageFieldNames.VALUE.value] = new_budget

    return recommendation


def generate_break_down_recommendations_by_actor_ranking(parent, sorted_evaluated_actors, optimization_type: Tw.OptimizationTuple, ad_account_id, metric,
                                                         remove_threshhold_difference=3):
    # remove_threshhold_difference = how much worse an actor needs to perform than the best one in order to be removed instead of split
    # 3 means it has to perform three times as bad to be removed, otherwise it will be split
    recommendations = []
    num_actors = len(sorted_evaluated_actors)
    to_split = []
    to_remove = []
    # how much worse an actor needs to perform than the best one in order to be removed instead of split
    # 3 means it has to perform three times as bad
    # otherwise it will be split

    if num_actors >= 2:
        best_score = sorted_evaluated_actors[0].get(Columns.EvaluatedActorColumnNames.SCORE_COLUMN.value)

        if best_score == 0:
            best_score = best_score - sys.float_info.epsilon

        for actor in sorted_evaluated_actors[1:]:
            # get the score of the actor
            # if it is 0 we need to add or substract epsilon from it so that division works
            # if the best score is negative we compare negative numbers so we subtract
            # if the best score is positive we need to compare positive numbers so we add

            actor_score = actor.get(Columns.EvaluatedActorColumnNames.SCORE_COLUMN.value)
            if actor_score == 0:
                if best_score < 0:
                    actor_score = actor_score - sys.float_info.epsilon
                else:
                    actor_score = actor_score + sys.float_info.epsilon

            if best_score < 0:
                actor_difference = actor_score / best_score
            else:
                actor_difference = best_score / actor_score

            if actor_difference < remove_threshhold_difference:
                to_split.append(actor)
            else:
                to_remove.append(actor)

    if len(to_split) > 0:
        recommendations.append(
            generate_break_down_recommendation(parent, to_split, optimization_type, Tw.RecommendationVerdicts.Split, ad_account_id, metric))
    if len(to_remove) > 0:
        recommendations.append(
            generate_break_down_recommendation(parent, to_remove, optimization_type, Tw.RecommendationVerdicts.Remove, ad_account_id, metric))

    return recommendations


def get_optimization_type(optimization_type: Tw.OptimizationTuple):
    mapping = {
        'Budget': 'Budget',
        'Age': 'Age',
        'Gender': 'Gender',
        'Age and Gender': 'AgeGender',
        'Placement': 'Placement',
        'Impression Device': 'Device',
        'Country': 'Country',
        'Region': 'Region',
        'Interest': 'Interest'}
    return mapping[optimization_type.level]


def generate_break_down_recommendation(parent, actors, optimization_type: Tw.OptimizationTuple, recommendation_type: Tw.RecommendationVerdicts,
                                       ad_account_id, metric):
    recommendation = Recommendation()
    recommendation.structureId = parent[Columns.EvaluatedParentsColumnNames.ID.value]
    recommendation.level = Tw.LevelNames.AdSet.value  # Adset is the only level at which BreakDown Recommendations operate
    recommendation.applicationDetails = dict()

    recommendation.applicationDetails[RemoveBDMessageFieldNames.BREAKDOWN_TYPE.value] = get_optimization_type(optimization_type)
    if optimization_type.breakdown == Tw.LevelNames.Interest.value:
        recommendation.applicationDetails[RemoveBDMessageFieldNames.BREAKDOWN_IDS.value] = [{'id': actor[
            Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value],
                                                                                            'name': actor[Columns.interest_name]} for actor in actors]
    else:
        recommendation.applicationDetails[RemoveBDMessageFieldNames.BREAKDOWN_IDS.value] = [{'id': actor[
            Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value]} for actor in actors]
    recommendation.optimizationType = get_optimization_type(optimization_type)

    if optimization_type.action_breakdown in ['Placement', 'Impression Device']:
        recommendation.recommendationType = Columns.RecommendationTypes.PLACEMENT_AND_DEVICE.value
    else:
        recommendation.recommendationType = Columns.RecommendationTypes.AUDIENCE.value

    template = None
    if recommendation_type == Tw.RecommendationVerdicts.Remove:
        template = 'Remove '

    if recommendation_type == Tw.RecommendationVerdicts.Split:
        template = 'Split '

    template += optimization_type.level
    if len(actors) > 1:
        template += 's '
        for actor in actors:
            template += actor['FiledId'] + ", "
        template = template[0:-2]
    else:
        template += ' '
        template += actors[0]['FiledId']

    template += " from AdSet {" + recommendation.structureId.split('_')[1] + "}"

    if recommendation_type == Tw.RecommendationVerdicts.Remove:
        template += " to improve performance."

    if recommendation_type == Tw.RecommendationVerdicts.Split:
        template += " to better asses their performance."

    recommendation.source = Columns.RecommendationSource.DEXTER.value
    recommendation.confidence = Columns.ConfidenceImportanceValues.MEDIUM.value
    recommendation.importance = Columns.ConfidenceImportanceValues.LOW.value
    recommendation.adAccountId = 'act_' + ad_account_id
    recommendation.metric = metric
    recommendation.template = template
    return recommendation


def add_weights_to_sorted_volumes(sorted_volumes):
    actor_volumes = [x[Columns.ProcessColumnNames.VOLUME_COLUMN.value] for x in sorted_volumes]

    actor_volume_time_stamps = [x[Columns.ProcessColumnNames.TIME_STAMP.value] for x in sorted_volumes]
    # get weights
    weighted_volumes = []
    for element in zip(actor_volumes, actor_volume_time_stamps):  # tuple[0] = insightVolume tuple[1] = timeStamp
        weight = get_insight_weight(element[1], sorted_volumes[-1].get(Columns.ProcessColumnNames.TIME_STAMP.value))
        weighted_volume = dict()
        weighted_volume[Columns.WeightedVolumeColumnNames.VOLUME_COLUMN.value] = element[0]
        weighted_volume[Columns.WeightedVolumeColumnNames.WEIGHT_COLUMN.value] = weight
        weighted_volumes.append(weighted_volume)

    return weighted_volumes


def get_insight_weight(date, last_actor_date):
    days_delta_as_float = TimeInterval.get_time_delta(date, last_actor_date)
    computed_weight = __weight_computation_function(days_delta_as_float)
    ampliffication_coefficient = __weight_amplification_function()
    return computed_weight * ampliffication_coefficient


def __weight_computation_function(days_delta_x):
    if days_delta_x < 0:
        raise ValueError("Invalid Day delta!")

    x = -1 * days_delta_x  # I computed the function on the [-infinity, 0] interval. This is merely convenience
    first_big_interval = 30  # the quadratic function has one big inflexion point. This roughly defines where the "really" important days come in
    relevancy_interval = 90  # after this point the quadratic function will tend towards 0

    quadratic_member = (x - first_big_interval) / (relevancy_interval + first_big_interval)
    quadratic_result = quadratic_member * quadratic_member
    reversed_quadratic = 1 / quadratic_result

    quadratic_divider = 16  # This helps "normalize" the quadratic result, flattening the weights ( making the values towards 0 less "eplosive" )
    quadratic_component = reversed_quadratic / quadratic_divider

    linear_coefficient = 0.4  # This coefficient determines how much additional growth is injected into the quadratic result,
    # making all dates weigh more based on how close they are to the 0 day
    linear_component = linear_coefficient * (1 / (-x + 1))  # The plus 1 here helps dodge the dreaded division by 0

    constant_component = 0.05  # This makes sure that all insights have a minimum weight

    intermediary_weight = quadratic_component + linear_component + constant_component
    normalized_weight = max(intermediary_weight,
                            1)  # makes the last 3-4 days have equal (maximum) weight. If this approach to functional weighing remains in place, this normalization does not scale well

    return normalized_weight


def __weight_amplification_function():
    """Placeholder for a function that fetches relevant real world event (like Christmas!) related data that may amplify a particular date"""
    return 1


def calculate_actor_weighted_average(weighted_actor_volumes):
    total_volume = 0
    total_weight = 0
    for weightedVolume in weighted_actor_volumes:
        total_volume += weightedVolume[Columns.WeightedVolumeColumnNames.VOLUME_COLUMN.value]
        total_weight += weightedVolume[Columns.WeightedVolumeColumnNames.WEIGHT_COLUMN.value]

    return total_volume / total_weight


#
# Currently unused functions, might need Later
# Probably won't
#


def get_display_name(s, optimization_type: Tw.OptimizationTuple, actor):
    return s.format(actortype=optimization_type.breakdown, id=actor[
        Columns.EvaluatedActorColumnNames.IDENTITY_COLUMN.value])


def get_trend(actor_insight_volumes, metric_mean_value):
    if len(actor_insight_volumes) < 2:
        if actor_insight_volumes[0] >= metric_mean_value:
            return TrendTypes.TrendTypes.StableIncrease.value, TrendTypes.TrendTypes.StableIncrease.value
        else:
            return TrendTypes.TrendTypes.StableDecrease.value, TrendTypes.TrendTypes.StableDecrease.value
    else:

        ups = 0  # times there's been an increase between consecutive values
        downs = 1  # times there's been a decrease between consecutive values starts at 1 to avoid division by 0 change this
        for i in range(len(actor_insight_volumes) - 1):
            if actor_insight_volumes[i] >= actor_insight_volumes[i + 1]:
                ups += 1
            else:
                downs += 1

        difference = actor_insight_volumes[-1] - actor_insight_volumes[0]
        percent_change = difference / (actor_insight_volumes[0] + 0.000001) * 100  # avoid division by 0
        trend_raport = ups / downs

        up_down_trend = TrendTypes.GetUpDownTrendType(trend_raport)
        perc_change_trend = TrendTypes.GetPercentileChangeTrendType(percent_change)

    return up_down_trend, perc_change_trend


def get_mean_metric_from_parent(parent, campaign_goal: GoalsEnum.Goals = None):
    sum_of_metric = 0
    data_points_of_metric = 0

    relevant_metrics = Columns.relevant_metrics.get(campaign_goal)
    optimization_metric = relevant_metrics[0]

    for actor in parent.get(Columns.PreProcessColumnNames.PARENT_ACTORS_KEY.value):
        for insight in actor[Columns.PreProcessColumnNames.ACTOR_INSIGHTS_KEY.value]:
            volume = insight.get(optimization_metric)
            if volume is not None:
                if not math.isnan(volume):
                    sum_of_metric += volume
                    data_points_of_metric += 1

    if data_points_of_metric == 0:
        raise Exception(f"No data for the metric {optimization_metric} in {parent}")

    return sum_of_metric / data_points_of_metric


def plot_cpc_c_licks_and_spend(actor):
    print('plotting...')
    timestamps = [x for x in actor]
    cpc = [actor[x]['Cpc'] for x in actor]
    spend = [actor[x]['Spend'] for x in actor]
    clicks = [actor[x]['Clicks'] for x in actor]
    fig = plt.figure(figsize=(17, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(timestamps, spend, 'b', label='Spend')
    ax1.plot(timestamps, clicks, 'g', label='Clicks')
    ax1.plot(timestamps, cpc, 'ro', label='CPC')
    fig.legend()
    plt.show()


def plot_metric_angles(angles, metric, actor):
    # temp = angles
    fig = plt.figure(figsize=(17, 9))
    ax1 = fig.add_subplot(111)
    fig.suptitle(f'{actor} - {metric}', fontsize=16)
    ax1.plot([0], [0], color='black', marker='o')
    ax1.plot([-1, 1], [0, 0], color='black')
    ax1.plot([0, 0], [-1, 1], color='black')
    # colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'chartreuse', 'burlywood']
    i = 0
    for angle in angles:
        value = angles[angle]
        if angle != 'Current' and value != 'N/A':
            if angle == 'Resultant':
                ax1.plot([0, math.cos(value)], [0, math.sin(value)], label=angle, color=(1.0, 0.1, 0.1), linewidth=5.0)
            else:
                ax1.plot([0, math.cos(value)], [0, math.sin(value)], label=angle, color=(1.0, float((i + 1) / 10), float((i + 1) / 10)))
            i = i + 1
    fig.legend()
    plt.show()


# TODO: break this into smaller functions
# TODO: take the timeIntervals definition to an outside resource
# calculate angle(with atan2) on the average of the observations in the Interval instead of the interval's beggining value
# calculate angle(with atan2) instead of slopes beause slopes vary wildly based on metric (impressions are in the millions while CTR is a percentage)

def CalculateAngles(data):
    analized_actors = {}

    time_intervals = [datetime.timedelta(days=1), datetime.timedelta(days=3), datetime.timedelta(days=7), datetime.timedelta(days=14),
                      datetime.timedelta(days=31),  # ~one month
                      datetime.timedelta(days=93),  # ~three months
                      datetime.timedelta(days=186),  # ~ six months
                      ]

    for actor in data:
        analized_actors[actor] = {}
        for breakdown in data[actor]:
            max_time_stamp = datetime.datetime.min
            min_time_stamp = datetime.datetime.max
            analized_actors[actor][breakdown] = {}
            for timestamp in data[actor][breakdown]:
                timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
                if timestamp > max_time_stamp:
                    max_time_stamp = timestamp
                if timestamp < min_time_stamp:
                    min_time_stamp = timestamp

            max_time_stamp_aux = datetime.datetime.strftime(max_time_stamp, '%Y-%m-%d')

            for metric in data[actor][breakdown][max_time_stamp_aux]:
                if metric not in ['ad_name', 'adset_name', 'campaign_name', 'ad_id', 'adset_id', 'campaign_id']:
                    analized_actors[actor][breakdown][metric] = {}
                    # calculate slope for intervals
                    current_value = data[actor][breakdown][max_time_stamp_aux][metric]

                    # set all angles to 'N/A' if the current value is unknown
                    if current_value is None:
                        for interval in time_intervals:
                            day_difference = interval.days
                            if day_difference > 15:
                                analized_actors[actor][breakdown][metric][f"{day_difference / 31} months"] = 'N/A'
                            else:
                                analized_actors[actor][breakdown][metric][f"{day_difference} days"] = 'N/A'
                        analized_actors[actor][breakdown][metric]['LifeTime'] = 'N/A'
                        analized_actors[actor][breakdown][metric]['Current'] = 'N/A'
                        continue

                    for interval in time_intervals:
                        compare_date = max_time_stamp - interval
                        day_difference = interval.days

                        compare_date_aux = datetime.datetime.strftime(compare_date, '%Y-%m-%d')

                        if compare_date_aux in data[actor][breakdown]:
                            #   Average all values inside the interval instead of just taking the one at the start as compare value
                            compare_value_sum = 0
                            compare_value_number_of_days = 0
                            while compare_date < max_time_stamp:
                                if compare_date_aux in data[actor][breakdown]:
                                    if data[actor][breakdown][compare_date_aux][metric] is not None:
                                        compare_value_sum = compare_value_sum + data[actor][breakdown][compare_date_aux][metric]
                                        compare_value_number_of_days = compare_value_number_of_days + 1
                                compare_date = compare_date + datetime.timedelta(days=1)

                            if compare_value_number_of_days > 0:
                                compare_value = compare_value_sum / compare_value_number_of_days
                            else:
                                compare_value = None

                            if compare_value is None:
                                angle = 'N/A'
                            else:
                                difference = current_value - compare_value
                                angle = math.atan2(float(difference), float(day_difference))

                            if day_difference > 15:
                                analized_actors[actor][breakdown][metric][f"{day_difference / 31} months"] = angle
                                analized_actors[actor][breakdown][metric][f"{day_difference / 31} months value"] = compare_value
                            else:
                                analized_actors[actor][breakdown][metric][f"{day_difference} days"] = angle
                                analized_actors[actor][breakdown][metric][f"{day_difference} days value"] = compare_value
                        else:
                            # no data for the interval
                            if day_difference > 15:
                                analized_actors[actor][breakdown][metric][f"{day_difference / 31} months"] = 'N/A'
                                analized_actors[actor][breakdown][metric][f"{day_difference / 31} months value"] = 'N/A'
                            else:
                                analized_actors[actor][breakdown][metric][f"{day_difference} days"] = 'N/A'
                                analized_actors[actor][breakdown][metric][f"{day_difference} days value"] = 'N/A'
                    # calculate lifetime slope
                    lifetime_day_difference = (max_time_stamp - min_time_stamp).days
                    if lifetime_day_difference > time_intervals[-1].days:
                        lifetime_compare_value_sum = 0
                        lifetime_compare_number_of_days = 0
                        lifetime_compare_date = min_time_stamp
                        while lifetime_compare_date < max_time_stamp:
                            if lifetime_compare_date in data[actor][breakdown]:
                                if data[actor][breakdown][lifetime_compare_date][metric] is not None:
                                    lifetime_compare_value_sum = lifetime_compare_value_sum + data[actor][breakdown][lifetime_compare_date][metric]
                                    lifetime_compare_number_of_days = lifetime_compare_number_of_days + 1
                            lifetime_compare_date = lifetime_compare_date + datetime.timedelta(days=1)

                        if lifetime_compare_number_of_days > 0:
                            compare_value = lifetime_compare_value_sum / lifetime_compare_number_of_days
                        else:
                            compare_value = None
                        if compare_value is None:
                            analized_actors[actor][breakdown][metric]['LifeTime'] = 'N/A'
                        else:
                            lifetime_difference = current_value - compare_value
                            if lifetime_day_difference > 0:
                                lifetime_angle = math.atan2(float(lifetime_difference), float(lifetime_day_difference))
                            else:
                                lifetime_angle = 'N/A'
                            analized_actors[actor][breakdown][metric]['LifeTime'] = lifetime_angle
                    else:
                        analized_actors[actor][breakdown][metric]['LifeTime'] = 'N/A'

                    analized_actors[actor][breakdown][metric]['Current'] = current_value
                else:
                    analized_actors[actor][metric] = data[actor][breakdown][max_time_stamp_aux][metric]

    return analized_actors


def get_recommendations_from_fb_details(fb_details, level):
    blame_field_to_optimization_type_mapping = {
        'targeting': 'Targeting',
        'optimization_goal': 'Optimization Goal',
        'end_time': 'End Time',
        'creative': 'Creative',
        'tracking_specs': 'Tracking Specs',
        'other': 'Ad Warning'
    }

    fb_recos = []
    for detail in fb_details:
        detail_id = detail['id']
        details = detail['FacebookDetails']
        details_dict = json.loads(details)
        if 'recommendations' in details_dict:
            recommendations = details_dict['recommendations']
            for facebook_recommendation in recommendations:
                recommendation = Recommendation()
                recommendation.structureId = level + '_' + str(detail_id)
                recommendation.optimizationType = 'overall'
                recommendation.template = facebook_recommendation[Columns.FacebookRecommendationFieldNames.MESSAGE.value]
                recommendation.confidence = facebook_recommendation[Columns.FacebookRecommendationFieldNames.CONFIDENCE.value]
                recommendation.importance = facebook_recommendation[Columns.FacebookRecommendationFieldNames.IMPORTANCE.value]
                recommendation.source = Columns.RecommendationSources.FACEBOOK.value
                recommendation.level = level
                recommendation.adAccountId = detail['AdAccountId']
                recommendation.metric = None
                recommendation.applicationDetails = None

                if level == Tw.LevelNames.Campaign.value:
                    recommendation.campaignId = str(detail_id)
                    recommendation.parentId = detail['AdAccountId']

                if level == Tw.LevelNames.AdSet.value:
                    recommendation.campaignId = str(detail['CampaignId'])
                    recommendation.parentId = str(detail['CampaignId'])

                if level == Tw.LevelNames.Ad.value:
                    recommendation.campaignId = str(detail['CampaignId'])
                    recommendation.parentId = str(detail['AdSetId'])

                if Columns.FacebookRecommendationFieldNames.BLAME_FIELD.value in facebook_recommendation:
                    recommendation.recommendationType = blame_field_to_optimization_type_mapping[
                        facebook_recommendation[Columns.FacebookRecommendationFieldNames.BLAME_FIELD.value]]
                else:
                    recommendation.recommendationType = blame_field_to_optimization_type_mapping['other']
                fb_recos.append(recommendation)
    return fb_recos


def exportRecommendationsToExcel(recommendations):
    workbook = xlsxwriter.Workbook('DexterRecommendations.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 80)
    for i, recommendation in enumerate(recommendations):
        worksheet.write(f'A{i}', recommendation)
    print('Xcel Writing done!')
    workbook.close()


def export_csv():
    pass


def exportSlopesToExcel(slopes):
    workbook = xlsxwriter.Workbook('DexterAnalysisAngles.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 18)
    worksheet.set_column('E:L', 15)
    worksheet.write('A1', 'Structure', bold)
    worksheet.write('B1', 'Breakdown', bold)
    worksheet.write('C1', 'Metric', bold)
    worksheet.write('D1', 'Last observed value', bold)
    worksheet.write('E1', '1 day angle', bold)
    worksheet.write('F1', '3 days angle', bold)
    worksheet.write('G1', '7 days angle', bold)
    worksheet.write('H1', '14 days angle', bold)
    worksheet.write('I1', '1 month angle', bold)
    worksheet.write('J1', '3 months angle', bold)
    worksheet.write('K1', '6 months angle', bold)
    worksheet.write('L1', 'Lifetime angle', bold)

    index = 1
    for actor in slopes:
        act = slopes[actor]
        for breakdown in act:
            bd = act[breakdown]
            for bd_value in bd:
                metrics = bd[bd_value]
                for metric in metrics:
                    intervals = metrics[metric]
                    index = index + 1
                    worksheet.write(f'A{index}', actor)
                    worksheet.write(f'B{index}', f'{breakdown}-{bd_value}')
                    worksheet.write(f'C{index}', f'{metric}')
                    worksheet.write(f'D{index}', intervals['Current'])
                    worksheet.write(f'E{index}', intervals['1 days'])
                    worksheet.write(f'F{index}', intervals['3 days'])
                    worksheet.write(f'G{index}', intervals['7 days'])
                    worksheet.write(f'H{index}', intervals['14 days'])
                    worksheet.write(f'I{index}', intervals['1.0 months'])
                    worksheet.write(f'J{index}', intervals['3.0 months'])
                    worksheet.write(f'K{index}', intervals['6.0 months'])
                    worksheet.write(f'L{index}', intervals['LifeTime'])

    print('Xcel Writing done!')
    workbook.close()
