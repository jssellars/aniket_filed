import typing
from datetime import datetime

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.OrchestratorBase import OrchestratorBase
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalMongoRepositoryHelper import DexterJournalMongoRepositoryHelper
from Core.constants import DEFAULT_DATETIME
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleFuzzyfierFactory import GoogleFuzzyfierFactory
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsEnum import GoogleAlgorithmsEnum
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsFactory import GoogleAlgorithmsFactory
from GoogleDexter.Engine.Algorithms.GoogleRuleEvaluatorFactory import GoogleRuleEvaluatorFactory
from GoogleDexter.Engine.Algorithms.GoogleRulesFactory import GoogleRulesFactory

import logging

logger = logging.getLogger(__name__)


class DefaultGoogleOrchestrator(OrchestratorBase):

    def __init__(self):
        super().__init__()
        self.channel = ChannelEnum.GOOGLE

    def __init_algorithm(self, alg_type, level) -> typing.Any:
        algorithm = GoogleAlgorithmsFactory.get(algorithm_type=alg_type, level=level, channel=self.channel)
        rules = GoogleRulesFactory.get(algorithm_type=alg_type, level=level)
        fuzzyfier_factory = GoogleFuzzyfierFactory.get(algorithm_type=alg_type, level=level)

        try:
            if alg_type == GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE:
                algorithm = (algorithm.
                             set_business_owner_id(self.business_owner_id).
                             set_dexter_config(self.config.dexter).
                             set_fuzzyfier_factory(fuzzyfier_factory).
                             set_repository(self._data_repository).
                             set_rules(rules).
                             set_mongo_config(self.config.mongo))
        except Exception as e:
            raise e

        return algorithm

    def run_algorithm(self, search_query, time_interval, mongo_config):
        try:
            if not self.config.dexter.date_stop:
                date_stop = datetime.now()
            else:
                date_stop = datetime.strptime(self.config.dexter.date_stop, DEFAULT_DATETIME)

            time_interval_enum = DaysEnum(time_interval)
            campaigns_ids = self._data_repository.get_campaigns_by_account_id(key_value=self.ad_account_id)
            for campaign_id in campaigns_ids:
                print(len(campaigns_ids))
                algorithm = self.__init_algorithm(GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                                  level=LevelEnum.CAMPAIGN)
                rule_evaluator = GoogleRuleEvaluatorFactory.get(
                    algorithm_type=GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                    level=LevelEnum.CAMPAIGN)
                rule_evaluator.set_time_interval(time_interval_enum)
                (algorithm.
                 set_dexter_config(self.config.dexter).
                 set_repository(self._data_repository).
                 set_date_stop(date_stop).
                 set_time_interval(time_interval_enum).
                 set_rule_evaluator(rule_evaluator)
                 )

                recommendations = algorithm.run(campaign_id)
                self._recommendations_repository.save_recommendations(recommendations,
                                                                      self.config.dexter.recommendation_days_last_updated)
                adgroup_ids = self._data_repository.get_adgroups_by_campaign_id(key_value=campaign_id)
                for adgroup_id in adgroup_ids:
                    algorithm = self.__init_algorithm(GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                                      level=LevelEnum.ADGROUP)
                    rule_evaluator = GoogleRuleEvaluatorFactory.get(
                        algorithm_type=GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                        level=LevelEnum.ADGROUP)
                    rule_evaluator.set_time_interval(time_interval_enum)
                    algorithm.set_rule_evaluator(rule_evaluator). \
                        set_time_interval(time_interval_enum). \
                        set_date_stop(date_stop)

                    recommendations = algorithm.run(adgroup_id)
                    self._recommendations_repository.save_recommendations(recommendations,
                                                                          self.config.dexter.recommendation_days_last_updated)

                    algorithm = self.__init_algorithm(GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                                      level=LevelEnum.AD)
                    rule_evaluator = GoogleRuleEvaluatorFactory.get(
                        algorithm_type=GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                        level=LevelEnum.AD)
                    rule_evaluator.set_time_interval(time_interval_enum)
                    algorithm.set_rule_evaluator(rule_evaluator). \
                        set_time_interval(time_interval_enum). \
                        set_date_stop(date_stop)
                    recommendations = algorithm.run(adgroup_id)
                    self._recommendations_repository.save_recommendations(recommendations,
                                                                          self.config.dexter.recommendation_days_last_updated)

                update_query = DexterJournalMongoRepositoryHelper.get_update_query_completed()

                self._journal_repository.update_one(search_query, update_query)

        except Exception as e:
            logger.exception(repr(e))
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_failed()
            self._journal_repository.update_one(search_query, update_query)
