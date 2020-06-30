import time
import traceback
import typing
from datetime import datetime, timedelta
from threading import Thread

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsFactory import AlgorithmsFactory
from FacebookDexter.Engine.Algorithms.FuzzyfierFactory import FuzzyfierFactory
from FacebookDexter.Engine.Algorithms.RuleEvaluatorFactory import RuleEvaluatorFactory
from FacebookDexter.Engine.Algorithms.RulesFactory import RulesFactory
from FacebookDexter.Engine.MasterWorker.OrchestratorBuilder import OrchestratorBuilder
from FacebookDexter.Engine.MasterWorker.RunStatus import RunStatus
from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEntryModel import DexterJournalEntryModel
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEnums import DexterEngineRunJournalEnum, \
    RunStatusDexterEngineJournal
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Rules.RuleEnums import RuleTypeSelectionEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepositoryHelper import \
    DexterJournalMongoRepositoryHelper


class Orchestrator(OrchestratorBuilder):

    def __init__(self,
                 business_owner_id: typing.AnyStr = None,
                 ad_account_id: typing.AnyStr = None,
                 algorithm_type=None,
                 level: LevelEnum = None,
                 startup: typing.Any = None):
        self.business_owner_id = business_owner_id
        self.ad_account_id = ad_account_id
        self.algorithm_type = algorithm_type
        self.level = level
        self.startup = startup

        super().__init__()

    def keep_latest_recommendations(self):

        grouped_recommendations = {}
        recommendations = self._recommendations_repository.get_active_recommendations()
        for recommendation in recommendations:
            id = recommendation['recommendation_id']
            time_interval = recommendation['time_interval']
            ad_account_id = recommendation['ad_account_id']
            structure_id = recommendation['structure_id']
            metric = recommendation['metrics'][0]['display_name']
            breakdown = recommendation['breakdown']['name']
            level = recommendation['level']

            group_tuple = (ad_account_id, metric, breakdown, level, structure_id)
            if group_tuple not in grouped_recommendations.keys():
                grouped_recommendations[group_tuple] = [(id, time_interval)]
            else:
                grouped_recommendations[group_tuple].append((id, time_interval))

        ids_to_deprecate = []
        for rec_list in grouped_recommendations.values():
            sorted_rec_list = sorted(rec_list, key=lambda x: x[1]['value'])
            ids_to_deprecate += list(map(lambda x: x[0], sorted_rec_list))[1:]

        self._recommendations_repository.deprecate_recommendations(recommendation_ids=ids_to_deprecate)

    def orchestrate(self):
        for time_interval in self.startup.dexter_config.time_intervals:
            query = DexterJournalMongoRepositoryHelper.get_search_for_other_instances_query(
                business_owner_id=self.business_owner_id,
                ad_account_id=self.ad_account_id,
                time_interval=time_interval)

            sort_query = DexterJournalMongoRepositoryHelper.get_sort_descending_by_start_date_query()
            ad_account_id_journal = list(self._journal_repository.get_last_two_entries(query, sort_query))

            if ad_account_id_journal:
                doc = ad_account_id_journal[0]

                if RunStatus.is_completed_or_failed(doc=doc):
                    self.__run_from_completed_or_failed(time_interval=time_interval)

                elif RunStatus.is_in_progress(doc=doc):
                    self.__save_pending_entry_to_journal(time_interval=time_interval)

                elif RunStatus.is_pending(doc=doc):

                    antecedent_doc = ad_account_id_journal[1]
                    if RunStatus.is_completed_or_failed(doc=antecedent_doc):
                        self.__run_from_pending(time_interval=time_interval)
                    else:
                        search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(
                            ad_account_id=self.ad_account_id,
                            business_owner_id=self.business_owner_id)
                        update_query = DexterJournalMongoRepositoryHelper.get_update_query_start_date_only()
                        self._journal_repository.update_one(search_query, update_query)
            else:
                self.__run_first_time(time_interval=time_interval)

    def __init_algorithm(self, alg_type, level) -> typing.Any:
        algorithm = AlgorithmsFactory.get(algorithm_type=alg_type, level=level)
        rules = RulesFactory.get(algorithm_type=alg_type, level=level)
        fuzzyfier_factory = FuzzyfierFactory.get(algorithm_type=alg_type, level=level)

        try:
            if alg_type == AlgorithmsEnum.DEXTER_FUZZY_INFERENCE:
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
            elif alg_type == AlgorithmsEnum.FACEBOOK_ENHANCER:
                algorithm = (algorithm.
                             set_debug_mode(self.startup.debug).
                             set_mongo_config(self.startup.mongo_config).
                             create_mongo_repository())
        except Exception as e:
            raise e

        return algorithm

    def __run_first_time(self, time_interval):
        journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS,
                                                                   time_interval)

        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)
        self._journal_repository.add_one(journal_object_saving)

        self.__run_algorithm(search_query=search_query, time_interval=time_interval)

    def __run_from_pending(self, time_interval):
        search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.ad_account_id,
                                                                                   self.business_owner_id,
                                                                                   time_interval)
        update_query = DexterJournalMongoRepositoryHelper.get_update_query_in_progress()
        self._journal_repository.update_one(search_query, update_query)

        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)

        self.__run_algorithm(search_query=search_query, time_interval=time_interval)

    def __save_pending_entry_to_journal(self, time_interval):
        journal_object_saving = self.__create_journal_entry_object(run_status=RunStatusDexterEngineJournal.PENDING,
                                                                   time_interval=time_interval)
        self._journal_repository.add_one(journal_object_saving)

    def __run_from_completed_or_failed(self, time_interval):
        journal_object_saving = self.__create_journal_entry_object(run_status=RunStatusDexterEngineJournal.IN_PROGRESS,
                                                                   time_interval=time_interval)
        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)
        self._journal_repository.add_one(journal_object_saving)
        self.__run_algorithm(search_query=search_query, time_interval=time_interval)

    def update_remaining_null_dates(self):
        search_null_end_date_query = DexterJournalMongoRepositoryHelper.get_search_for_null_end_date(
            self.business_owner_id, self.ad_account_id)
        null_entries = list(self._journal_repository.get_all_by_query(search_null_end_date_query))
        for entry in null_entries:
            if entry[DexterEngineRunJournalEnum.END_TIMESTAMP.value] is None:
                update_query = DexterJournalMongoRepositoryHelper.get_update_query_for_null_entries()
                search_query = {
                    DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value: entry[
                        DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value],
                    DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: entry[
                        DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value],
                    DexterEngineRunJournalEnum.RUN_STATUS.value: entry[DexterEngineRunJournalEnum.RUN_STATUS.value],
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value: entry[
                        DexterEngineRunJournalEnum.ALGORITHM_TYPE.value],
                    DexterEngineRunJournalEnum.START_TIMESTAMP.value: entry[
                        DexterEngineRunJournalEnum.START_TIMESTAMP.value],
                    DexterEngineRunJournalEnum.LEVEL.value: entry[DexterEngineRunJournalEnum.LEVEL.value],
                }
                self._journal_repository.update_one(search_query, update_query)

    def __run_algorithm(self, search_query, time_interval):
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
                print('Started campaign {}[id: {}] out of {}'.format(c, campaign_id, len(campaign_ids)))
                c+=1
                start_time = time.time()
                rule_evaluator = RuleEvaluatorFactory.get(algorithm_type=AlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                                          level=LevelEnum.CAMPAIGN)
                rule_evaluator.set_time_interval(time_interval_enum)
                rule_algorithm_campaign = self.get_rule_algorithm(date_stop,
                                                                  rule_evaluator,
                                                                  time_interval_enum,
                                                                  LevelEnum.CAMPAIGN)
                should_stop = False
                adset_ids = self._data_repository.get_adset_ids_by_campaign_id(campaign_id)
                for adset_id in adset_ids:
                    t = Thread(target=self.run_facebook_enhancer,
                               args=(adset_id, date_stop, time_interval_enum, LevelEnum.ADSET))
                    t.start()

                    ad_ids = self._data_repository.get_ads_by_adset_id(adset_id)
                    for ad_id in ad_ids:
                        t = Thread(target=self.run_facebook_enhancer,
                                   args=(ad_id, date_stop, time_interval_enum, LevelEnum.AD))
                        t.start()
                if rule_algorithm_campaign.check_run_status(campaign_id):
                    for adset_id in adset_ids:
                        rule_evaluator = RuleEvaluatorFactory.get(
                            algorithm_type=AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.ADSET)
                        rule_evaluator.set_time_interval(time_interval_enum)
                        rule_algorithm_adset_breakdown = self.get_rule_algorithm(date_stop,
                                                                                 rule_evaluator,
                                                                                 time_interval_enum,
                                                                                 LevelEnum.ADSET)
                        rule_based_recommendations = rule_algorithm_adset_breakdown.run(adset_id,
                                                                            [RuleTypeSelectionEnum.REMOVE_BREAKDOWN])
                        if rule_based_recommendations:
                            should_stop = True
                            self._recommendations_repository.save_recommendations(rule_based_recommendations,
                                                                                  last_updated)
                        if not should_stop:
                            rule_evaluator = RuleEvaluatorFactory.get(
                                algorithm_type=AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.AD)
                            rule_evaluator.set_time_interval(time_interval_enum)
                            rule_algorithm_ad = self.get_rule_algorithm(date_stop,
                                                                        rule_evaluator,
                                                                        time_interval_enum,
                                                                        LevelEnum.AD)
                            rule_based_recommendations = rule_algorithm_ad.run(adset_id,
                                                                               [RuleTypeSelectionEnum.GENERAL,
                                                                                RuleTypeSelectionEnum.BUDGET])
                            if rule_based_recommendations:
                                should_stop = True
                                self._recommendations_repository.save_recommendations(rule_based_recommendations,
                                                                                      last_updated)
                            else:

                                rule_evaluator = RuleEvaluatorFactory.get(
                                    algorithm_type=AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, level=LevelEnum.ADSET)
                                rule_evaluator.set_time_interval(time_interval_enum)
                                rule_algorithm_adset_other = self.get_rule_algorithm(date_stop,
                                                                                     rule_evaluator,
                                                                                     time_interval_enum,
                                                                                     LevelEnum.ADSET)
                                rule_based_recommendations = rule_algorithm_adset_other.run(adset_id,
                                                                                            [
                                                                                                RuleTypeSelectionEnum.GENERAL,
                                                                                                RuleTypeSelectionEnum.CREATE,
                                                                                                RuleTypeSelectionEnum.BUDGET])
                                if rule_based_recommendations:
                                    should_stop = True
                                    self._recommendations_repository.save_recommendations(
                                        rule_based_recommendations,
                                        last_updated)

                    rule_based_recommendations = rule_algorithm_campaign.run(campaign_id,
                                                                             [RuleTypeSelectionEnum.GENERAL,
                                                                              RuleTypeSelectionEnum.BUDGET])
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
        facebook_enhancer_algorithm = self.__init_algorithm(alg_type=AlgorithmsEnum.FACEBOOK_ENHANCER,
                                                            level=level)
        (facebook_enhancer_algorithm.
         set_date_stop(date_stop).
         set_time_interval(time_interval_enum))
        return facebook_enhancer_algorithm

    def get_rule_algorithm(self, date_stop, rule_evaluator, time_interval_enum, level):
        rule_algorithm = self.__init_algorithm(alg_type=AlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
                                               level=level)
        (rule_algorithm.
         set_date_stop(date_stop).
         set_time_interval(time_interval_enum).
         set_rule_evaluator(rule_evaluator))
        return rule_algorithm

    def __create_journal_entry_object(self, run_status, time_interval):
        journal_object = DexterJournalEntryModel()
        journal_object.business_owner_id = self.business_owner_id
        journal_object.ad_account_id = self.ad_account_id
        journal_object.run_status = run_status.value
        journal_object.start_timestamp = datetime.now()
        journal_object.time_interval = time_interval
        journal_object_saving = journal_object.__dict__

        return journal_object_saving
