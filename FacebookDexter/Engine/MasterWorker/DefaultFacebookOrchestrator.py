import time
import traceback
import typing
from datetime import datetime, timedelta

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.OrchestratorBase import OrchestratorBase
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalMongoRepositoryHelper import DexterJournalMongoRepositoryHelper
from Core.Tools.Misc.Constants import DEFAULT_DATETIME
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FacebookAlgorithmsFactory import FacebookAlgorithmsFactory
from FacebookDexter.Engine.Algorithms.FacebookRuleEvaluatorFactory import FacebookRuleEvaluatorFactory
from FacebookDexter.Engine.Algorithms.FacebookRulesFactory import FacebookRulesFactory
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookFuzzyfierFactory import \
    FacebookFuzzyfierFactory

from FacebookDexter.Engine.MasterWorker.FacebookStrategyEnum import FacebookStrategyEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeSelectionEnum
from FacebookDexter.Infrastructure.PersistanceLayer.FacebookDexterMongoRepository import FacebookDexterMongoRepository


class DefaultFacebookOrchestrator(OrchestratorBase):

    def __init__(self):
        super().__init__()
        self.channel = ChannelEnum.FACEBOOK

    def __init_algorithm(self, alg_type, level) -> typing.Any:
        algorithm = FacebookAlgorithmsFactory.get(algorithm_type=alg_type, level=level, channel=self.channel,
                                                  strategy=FacebookStrategyEnum.DEFAULT)
        rules = FacebookRulesFactory.get(algorithm_type=alg_type, level=level)
        fuzzyfier_factory = FacebookFuzzyfierFactory.get(algorithm_type=alg_type, level=level)

        try:
            if alg_type == FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE:
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
                             create_mongo_repository())
            elif alg_type == FacebookAlgorithmsEnum.FACEBOOK_ENHANCER:
                algorithm = (algorithm.
                             set_debug_mode(self.startup.debug).
                             set_mongo_config(self.startup.mongo_config).
                             create_mongo_repository())
        except Exception as e:
            raise e

        return algorithm

    def adset_is_olp(self, adset_id):
        structure_details = self._data_repository.get_structure_details(level=LevelEnum.ADSET, key_value=adset_id)
        try:
            status = structure_details['learning_stage_info']['status']
            if status == 'SUCCESS':
                return 1
        except:
            return 0

        return 0

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
                all_adsets_olp = True

                c += 1
                start_time = time.time()
                rule_evaluator = FacebookRuleEvaluatorFactory.get(
                    algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                    level=LevelEnum.CAMPAIGN)
                rule_evaluator.set_time_interval(time_interval_enum)
                rule_algorithm_campaign = self.get_rule_algorithm(date_stop,
                                                                  rule_evaluator,
                                                                  time_interval_enum,
                                                                  LevelEnum.CAMPAIGN)

                adset_ids = self._data_repository.get_adset_ids_by_campaign_id(campaign_id)
                # for adset_id in adset_ids:
                #     thread = Thread(target=self.run_facebook_enhancer,
                #                     args=(adset_id, date_stop, time_interval_enum, LevelEnum.ADSET))
                #     thread.start()
                #
                #     ad_ids = self._data_repository.get_ads_by_adset_id(adset_id)
                #     for ad_id in ad_ids:
                #         thread = Thread(target=self.run_facebook_enhancer,
                #                         args=(ad_id, date_stop, time_interval_enum, LevelEnum.AD))
                #         thread.start()

                print(
                    'Started campaign {} [id: {}] out of {} ---> acc_id: {} T{}'.format(c, campaign_id,
                                                                                        len(campaign_ids),
                                                                                        self.ad_account_id,
                                                                                        time_interval))
                if rule_algorithm_campaign.check_run_status(campaign_id):
                    for adset_id in adset_ids:
                        # self.adset_is_olp(adset_id) replace 1 with this
                        if 1:
                            rule_evaluator = FacebookRuleEvaluatorFactory.get(
                                algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.AD)
                            rule_evaluator.set_time_interval(time_interval_enum)
                            rule_algorithm_ad = self.get_rule_algorithm(date_stop,
                                                                        rule_evaluator,
                                                                        time_interval_enum,
                                                                        LevelEnum.AD)
                            rule_based_recommendations = rule_algorithm_ad.run(adset_id,
                                                                               [FacebookRuleTypeSelectionEnum.GENERAL,
                                                                                FacebookRuleTypeSelectionEnum.BUDGET])
                            self._recommendations_repository.save_recommendations(rule_based_recommendations,
                                                                                  last_updated)
                            # if not rule_based_recommendations:
                            rule_evaluator = FacebookRuleEvaluatorFactory.get(
                                algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                level=LevelEnum.ADSET)
                            rule_evaluator.set_time_interval(time_interval_enum)
                            rule_algorithm_adset_other = self.get_rule_algorithm(date_stop,
                                                                                 rule_evaluator,
                                                                                 time_interval_enum,
                                                                                 LevelEnum.ADSET)
                            rule_based_recommendations = rule_algorithm_adset_other.run(adset_id,
                                                                                        [
                                                                                            FacebookRuleTypeSelectionEnum.GENERAL,
                                                                                            FacebookRuleTypeSelectionEnum.CREATE,
                                                                                            FacebookRuleTypeSelectionEnum.BUDGET])
                            self._recommendations_repository.save_recommendations(
                                rule_based_recommendations,
                                last_updated)
                        # there is an else here
                        # else:
                        # all_adsets_olp = False
                        rule_evaluator = FacebookRuleEvaluatorFactory.get(
                            algorithm_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.ADSET)
                        rule_evaluator.set_time_interval(time_interval_enum)
                        rule_algorithm_adset_breakdown = self.get_rule_algorithm(date_stop,
                                                                                 rule_evaluator,
                                                                                 time_interval_enum,
                                                                                 LevelEnum.ADSET)
                        rule_based_recommendations = rule_algorithm_adset_breakdown.run(adset_id,
                                                                                        [
                                                                                            FacebookRuleTypeSelectionEnum.REMOVE_BREAKDOWN])
                        self._recommendations_repository.save_recommendations(rule_based_recommendations,
                                                                              last_updated)
                    if all_adsets_olp:
                        rule_based_recommendations = rule_algorithm_campaign.run(campaign_id,
                                                                                 [
                                                                                     FacebookRuleTypeSelectionEnum.GENERAL,
                                                                                     FacebookRuleTypeSelectionEnum.BUDGET])
                        self._recommendations_repository.save_recommendations(
                            rule_based_recommendations,
                            last_updated)

                    print("Elapsed time: {}".format(time.time() - start_time))

            update_query = DexterJournalMongoRepositoryHelper.get_update_query_completed()
            self._journal_repository.update_one(search_query, update_query)

        except Exception as failed_to_run_exception:
            print(failed_to_run_exception.__traceback__)
            traceback.print_exc()
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_failed()
            self._journal_repository.update_one(search_query, update_query)

        self.keep_latest_recommendations()

    def run_facebook_enhancer(self, structure_id, date_stop, time_interval_enum, level):
        facebook_enhancer_algorithm = self.get_facebook_enhancer_algorithm(date_stop,
                                                                           time_interval_enum,
                                                                           level)
        facebook_recommendations = facebook_enhancer_algorithm.run(structure_id)
        self._recommendations_repository.save_recommendations(facebook_recommendations,
                                                              self.startup.dexter_config.recommendation_days_last_updated)

    def get_facebook_enhancer_algorithm(self, date_stop, time_interval_enum, level):
        facebook_enhancer_algorithm = self.__init_algorithm(alg_type=FacebookAlgorithmsEnum.FACEBOOK_ENHANCER,
                                                            level=level)
        (facebook_enhancer_algorithm.
         set_date_stop(date_stop).
         set_time_interval(time_interval_enum))
        return facebook_enhancer_algorithm

    def get_rule_algorithm(self, date_stop, rule_evaluator, time_interval_enum, level):
        rule_algorithm = self.__init_algorithm(alg_type=FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                               level=level)
        (rule_algorithm.
         set_date_stop(date_stop).
         set_time_interval(time_interval_enum).
         set_rule_evaluator(rule_evaluator))
        return rule_algorithm
