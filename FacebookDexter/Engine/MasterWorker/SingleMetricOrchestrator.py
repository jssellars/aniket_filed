from datetime import datetime, timedelta

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.OrchestratorBase import OrchestratorBase
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalMongoRepositoryHelper import DexterJournalMongoRepositoryHelper
from Core.constants import DEFAULT_DATETIME
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FacebookAlgorithmsFactory import FacebookAlgorithmsFactory
from FacebookDexter.Engine.Algorithms.FacebookRuleEvaluatorFactory import FacebookRuleEvaluatorFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricFuzzyfierFactory import \
    FacebookRuleBasedSingleMetricFuzzyfierFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationRulesFactory import \
    FacebookRuleBasedSingleMetricOptimizationRulesFactory
from FacebookDexter.Engine.MasterWorker.FacebookStrategyEnum import FacebookStrategyEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeSelectionEnum
from FacebookDexter.Infrastructure.PersistanceLayer.FacebookDexterMongoRepository import FacebookDexterMongoRepository


class SingleMetricOrchestrator(OrchestratorBase):

    def __init__(self):
        super().__init__()
        self._channel = ChannelEnum.FACEBOOK
        self._algorithm_type = FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE

    def __get_rule_algorithm(self, date_stop, time_interval, level, rule_evaluator):
        algorithm = FacebookAlgorithmsFactory.get(algorithm_type=self._algorithm_type,
                                                  level=level,
                                                  channel=self._channel,
                                                  strategy=FacebookStrategyEnum.SINGLE_METRIC)
        rules = FacebookRuleBasedSingleMetricOptimizationRulesFactory.get(algorithm_type=self._algorithm_type,
                                                                          level=level)
        fuzzyfier_factory = FacebookRuleBasedSingleMetricFuzzyfierFactory.get(algorithm_type=self._algorithm_type,
                                                                              level=level)

        try:
            algorithm = (algorithm.
                         set_business_owner_id(self.business_owner_id).
                         set_facebook_config(self.config.facebook).
                         set_business_owner_repo_session(self.config.sql_db_session).
                         set_external_services(self.config.external_services).
                         set_dexter_config(self.config.dexter).
                         set_fuzzyfier_factory(fuzzyfier_factory).
                         set_rules(rules).
                         set_mongo_config(self.config.mongo).
                         set_auth_token(self._auth_token).
                         set_date_stop(date_stop=date_stop).
                         set_time_interval(time_interval=time_interval).
                         set_rule_evaluator(rule_evaluator=rule_evaluator).
                         set_minimum_number_of_data_points_dict(self.config.dexter.
                                                                minimum_number_of_data_points).
                         create_mongo_repository())
        except Exception as e:
            raise e

        return algorithm

    def run_algorithm(self, search_query, time_interval, mongo_config):
        self.set_data_repository(FacebookDexterMongoRepository(config=mongo_config))

        try:
            if not self.config.dexter.date_stop:
                date_stop = datetime.now() - timedelta(days=1)
            else:
                date_stop = datetime.strptime(self.config.dexter.date_stop, DEFAULT_DATETIME) - \
                            timedelta(days=1)

            time_interval_enum = DaysEnum(time_interval)
            last_updated = self.config.dexter.recommendation_days_last_updated
            campaign_ids = self._data_repository.get_campaigns_by_account_id(self.ad_account_id)

            for campaign_id in campaign_ids:
                self.generate_recommendations(structure_id=campaign_id,
                                              date_stop=date_stop,
                                              last_updated=last_updated,
                                              time_interval=time_interval_enum,
                                              level=LevelEnum.CAMPAIGN)

                adset_ids = self._data_repository.get_adset_ids_by_campaign_id(campaign_id)
                for adset_id in adset_ids:
                    self.generate_recommendations(structure_id=adset_id,
                                                  date_stop=date_stop,
                                                  last_updated=last_updated,
                                                  time_interval=time_interval_enum,
                                                  level=LevelEnum.ADSET)

                    self.generate_recommendations(structure_id=adset_id,
                                                  date_stop=date_stop,
                                                  last_updated=last_updated,
                                                  time_interval=time_interval_enum,
                                                  level=LevelEnum.AD)

            update_query = DexterJournalMongoRepositoryHelper.get_update_query_completed()
            self._journal_repository.update_one(search_query, update_query)
        except:
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_failed()
            self._journal_repository.update_one(search_query, update_query)

    def generate_recommendations(self, structure_id, date_stop, last_updated, time_interval, level):
        rule_evaluator = FacebookRuleEvaluatorFactory.get(
            algorithm_type=self._algorithm_type, level=level)
        rule_evaluator.set_time_interval(time_interval)
        algorithm = self.__get_rule_algorithm(level=level,
                                              time_interval=time_interval,
                                              date_stop=date_stop,
                                              rule_evaluator=rule_evaluator)
        recommendations = algorithm.run(structure_id, [FacebookRuleTypeSelectionEnum.GENERAL])
        self._recommendations_repository.save_recommendations(recommendations, last_updated)
