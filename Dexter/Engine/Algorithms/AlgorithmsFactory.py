import math

from Algorithms.Dexter_Fuzzy_Inference.Rules.Rules import Rules
from Algorithms.Models.Types import TypesWrapper
from Algorithms.Optimizer import Optimizer
from Algorithms.Tools import Constants
from Algorithms.Tools import PreProcessor
from Algorithms.Tools.Mappers.FactoryMapper import FactoryMapper
from Algorithms.Tools.TimeInterval import TimeInterval
from Infrastructure.Mongo.Mongo import MongoMediator
from Infrastructure.QueryBuilder.QueryBuilderMediator import QueryBuilderMediator
from Infrastructure.Rabbit.RabbitMQMediator import RabbitMqMediator
from Obsolete.GoalsEnum import Goals
from Algorithms.Tools.Columns import AlgorithmName


class AlgorithmsFactory:
    @staticmethod
    def factory(algorithm_type,
                ad_account_id,
                mongo_recommender,
                data=None,
                combination=None,
                date_range=None,
                logging=None,
                inter_types=None,
                token=None,
                channel=None):

        if algorithm_type == AlgorithmName.DEXTER_FUZZY_INFERENCE:
            return RuleBasedAlgorithm(ad_account_id=ad_account_id,
                                      channel=channel,
                                      data=data,
                                      combination=combination,
                                      mongo_recommender=mongo_recommender)
        if algorithm_type == "breakdowns":
            return BreakdownAlgorithm(ad_account_id=ad_account_id,
                                      date_range=date_range,
                                      logging=logging,
                                      inter_types=inter_types,
                                      channel=channel,
                                      mongo_recommender=mongo_recommender)
        if algorithm_type == "Facebook":
            return FacebookAlgorithm(ad_account_id=ad_account_id,
                                     token=token,
                                     channel=channel,
                                     mongo_recommender=mongo_recommender)


class BaseAlgorithm:
    def __init__(self, ad_account_id, channel, mongo_recommender):
        self._ad_account_id = ad_account_id
        self._channel = channel
        self._mongo_recommender = mongo_recommender

    def run(self):
        raise NotImplementedError()


class RuleBasedAlgorithm(BaseAlgorithm):
    def __init__(self, ad_account_id, channel, data, combination, mongo_recommender):
        super().__init__(ad_account_id=ad_account_id, channel=channel, mongo_recommender=mongo_recommender)
        self.__mapper = FactoryMapper.get_mapper(channel)
        self.data = data
        self.combination = combination

    def run(self):

        consolidated_analized_actors = {}

        result = PreProcessor.group_data_for_analise(self.data, self.combination)
        analized_actors = Optimizer.CalculateAngles(result)
        for actor in analized_actors:
            if actor not in consolidated_analized_actors:
                consolidated_analized_actors[actor] = {}
            consolidated_analized_actors[actor][self.combination.breakdown] = analized_actors[actor]
            consolidated_analized_actors[actor]['level'] = self.combination.level

        # TODO: Needed
        # TODO: Structure_name, breakdown - breakdown_value, metric, last_observed_value, 1 day angle, 1 day value....

        resulting_angle_actor_data = {}
        recommendations = []
        for actor in consolidated_analized_actors:
            actor_data = consolidated_analized_actors[actor]
            resulting_angles = {}
            for breakdown_type in actor_data:
                if breakdown_type != 'level':
                    resulting_angles[breakdown_type] = {}
                    all_data = actor_data[breakdown_type]
                    for breakdown_value in all_data:
                        # TODO: this list should be an enum or something like that
                        if breakdown_value not in Constants.SPECIFIC_IDS_AND_NAMES:
                            angles = all_data[breakdown_value]
                            resulting_angles[breakdown_type][breakdown_value] = {}

                            for metric in angles:
                                angle_info = angles[metric]

                                metric_x = 0
                                metric_y = 0
                                num_values = 0

                                for interval in angle_info:
                                    # TODO: Remove this after .csv file extraction
                                    if 'value' not in interval:
                                        if interval != 'Current':
                                            value = angle_info[interval]
                                            if value != 'N/A':
                                                value_x = math.cos(value)
                                                value_y = math.sin(value)
                                                metric_x += value_x
                                                metric_y += value_y
                                                num_values += 1
                                if num_values > 0:
                                    metric_y = metric_y / num_values
                                    metric_x = metric_x / num_values
                                    resulting_angle = math.atan2(metric_y, metric_x)
                                    resulting_angles[breakdown_type][breakdown_value][metric] = {}
                                    resulting_angles[breakdown_type][breakdown_value][metric]['Angle'] = resulting_angle
                                    resulting_angles[breakdown_type][breakdown_value][metric]['CurrentValue'] = angle_info['Current']
                        else:
                            resulting_angles[breakdown_value] = all_data[breakdown_value]
                    resulting_angles['level'] = consolidated_analized_actors[actor]['level']

            resulting_angle_actor_data[actor] = resulting_angles

        for actor in resulting_angle_actor_data:
            actor_data_keys = resulting_angle_actor_data[actor][self.combination.breakdown].keys()

            for breakdown_value in actor_data_keys:
                actor_data = resulting_angle_actor_data[actor][self.combination.breakdown][breakdown_value]
                level = resulting_angle_actor_data[actor]['level']
                for rule in Rules[level]:
                    if rule.check_application(actor=actor_data, mapper=self.__mapper):
                        recommendation = rule.generate_recommendation(level=level, structure_id=actor,
                                                                      ad_account_id=self._ad_account_id,
                                                                      actor_data=resulting_angle_actor_data[actor],
                                                                      )
                        if breakdown_value is not None:
                            recommendation.template += f'[{self.combination.breakdown} : {breakdown_value}]'

                        recommendation.channel = self._channel.value
                        recommendations.append(recommendation)

        self._mongo_recommender.send_recommendations(recommendations)


class BreakdownAlgorithm(BaseAlgorithm):
    def __init__(self, ad_account_id, date_range: TimeInterval, logging, inter_types, channel, mongo_recommender):
        super().__init__(ad_account_id=ad_account_id, channel=channel, mongo_recommender=mongo_recommender)
        self.ad_account_id = ad_account_id
        self.date_range = date_range
        self.logging = logging
        self.inter_types = inter_types

    def run(self):
        mongo_mediator = MongoMediator()
        rabbit_mediator = RabbitMqMediator()

        logging_message = ' for date range {' + self.date_range.to_string() + '} and ad account ' + self.ad_account_id
        self.logging.info('Starting runAlgorithm2' + logging_message)

        # moved the try - except block inside the for loop because outside of it it would break the for statement at the first exception
        # and no recommendations would be made for the remaining interTypes (the ones after the one that threw the exception)
        # campaignIds = mongo_mediator.get_campaign_ids_by_ad_account_id(self.ad_account_id)

        # Recommendations for comparing between actors (adsets of the same campaign or ads of the same adset or breakdowns)
        for inter_type in self.inter_types:
            try:
                # get data from mongo
                data = mongo_mediator.get_data_for_optimization(inter_type, self.date_range, self.ad_account_id)
                if len(data) > 0:
                    for goal in Goals:
                        processed_data = PreProcessor.pre_process_data(data, inter_type, goal)
                        recommendations = Optimizer.generate_recommendations(processed_data, inter_type,
                                                                             self.ad_account_id, goal.value)
                        rabbit_mediator.send_recommendations(recommendations)
                    self.logging.info(f"Sent recommendations for optimization {inter_type}")

                else:
                    self.logging.warning(
                        f"No data for optimization {inter_type} for range ( date_range.to_string()) for AdAccount {self.ad_account_id}")
            except Exception as e:
                self.logging.exception(e)

            # TODO: new Dexter ROI alerts recommendations

            self.logging.info('Finished runAlgorithm2' + logging_message)


class FacebookAlgorithm(BaseAlgorithm):
    def __init__(self, ad_account_id, token, channel, mongo_recommender):
        super().__init__(ad_account_id=ad_account_id, channel=channel, mongo_recommender=mongo_recommender)
        self.__ad_account_id = ad_account_id
        self.__token = token

    def run(self):
        rabbit_mediator = RabbitMqMediator()

        insights_mediator = QueryBuilderMediator(self.__token)

        """
            ============================== FACEBOOK_RECOMMENDATIONS START ==================================
        """
        fb_ad_details = insights_mediator.get_details(self.__ad_account_id, TypesWrapper.LevelNames.Ad.value)
        fb_ad_recommendations = Optimizer.get_recommendations_from_fb_details(fb_ad_details,
                                                                              TypesWrapper.LevelNames.Ad.value)
        rabbit_mediator.send_recommendations(fb_ad_recommendations)

        fb_ad_set_details = insights_mediator.get_details(self.__ad_account_id, TypesWrapper.LevelNames.AdSet.value)
        fb_ad_set_recommendations = Optimizer.get_recommendations_from_fb_details(fb_ad_set_details,
                                                                                  TypesWrapper.LevelNames.AdSet.value)
        rabbit_mediator.send_recommendations(fb_ad_set_recommendations)

        fb_campaign_details = insights_mediator.get_details(self.__ad_account_id, TypesWrapper.LevelNames.Campaign.value)
        fb_campaign_recommendations = Optimizer.get_recommendations_from_fb_details(fb_campaign_details,
                                                                                    TypesWrapper.LevelNames.Campaign.value)
        rabbit_mediator.send_recommendations(fb_campaign_recommendations)
        """
            ============================== FACEBOOK_RECOMMENDATIONS END ==================================
        """
