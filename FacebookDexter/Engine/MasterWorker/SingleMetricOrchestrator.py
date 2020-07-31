from datetime import datetime, timedelta

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.OrchestratorBase import OrchestratorBase
from Core.Tools.Misc.Constants import DEFAULT_DATETIME
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
        self.channel = ChannelEnum.FACEBOOK

    def __get_rule_algorithm(self, date_stop, time_interval, level, rule_evaluator):
        algorithm = FacebookAlgorithmsFactory.get(algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                                  level=level, channel=self.channel,
                                                  strategy=FacebookStrategyEnum.SINGLE_METRIC)
        rules = FacebookRuleBasedSingleMetricOptimizationRulesFactory.get(
            algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=level)
        fuzzyfier_factory = FacebookRuleBasedSingleMetricFuzzyfierFactory.get(
            algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
            level=level)

        try:
            algorithm = (algorithm.
                         set_business_owner_id(self.business_owner_id).
                         set_facebook_config(self.startup.facebook_config).
                         set_business_owner_repo_session(self.startup.session).
                         set_external_services(self.startup.external_services).
                         set_dexter_config(self.startup.dexter_config).
                         set_fuzzyfier_factory(fuzzyfier_factory).
                         set_rules(rules).
                         set_debug_mode(self.startup.debug).
                         set_mongo_config(self.startup.mongo_config).
                         set_auth_token(self._auth_token).
                         set_date_stop(date_stop=date_stop).
                         set_time_interval(time_interval=time_interval).
                         set_rule_evaluator(rule_evaluator=rule_evaluator).
                         create_mongo_repository())
        except Exception as e:
            raise e

        return algorithm

    def run_algorithm(self, search_query, time_interval, mongo_config):
        self.set_data_repository(FacebookDexterMongoRepository(config=mongo_config))

        try:
            if not self.startup.dexter_config.date_stop:
                date_stop = datetime.now() - timedelta(days=1)
            else:
                date_stop = datetime.strptime(self.startup.dexter_config.date_stop, DEFAULT_DATETIME) - \
                            timedelta(days=1)

            time_interval_enum = DaysEnum(time_interval)
            last_updated = self.startup.dexter_config.recommendation_days_last_updated

            campaign_ids = self._data_repository.get_campaigns_by_account_id(self.ad_account_id)
            c = 1
            for campaign_id in campaign_ids:
                print("Running {} out of {}".format(c, len(campaign_ids)))
                c += 1
                rule_evaluator = FacebookRuleEvaluatorFactory.get(
                    algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.CAMPAIGN)
                rule_evaluator.set_time_interval(time_interval_enum)
                campaign_alg = self.__get_rule_algorithm(level=LevelEnum.CAMPAIGN,
                                                         time_interval=time_interval_enum,
                                                         date_stop=date_stop,
                                                         rule_evaluator=rule_evaluator)
                recommendations = campaign_alg.run(campaign_id, [FacebookRuleTypeSelectionEnum.GENERAL])
                self._recommendations_repository.save_recommendations(recommendations, last_updated)
        except Exception as e:
            print(e)
