import traceback
import typing
from datetime import datetime

from FacebookDexter.Engine.Algorithms.AlgorithmsFactory import AlgorithmsFactory
from FacebookDexter.Engine.Algorithms.FuzzyfierFactory import FuzzyfierFactory
from FacebookDexter.Engine.Algorithms.RuleEvaluatorFactory import RuleEvaluatorFactory
from FacebookDexter.Engine.Algorithms.RulesFactory import RulesFactory
from FacebookDexter.Engine.MasterWorker.OrchestratorBuilder import OrchestratorBuilder
from FacebookDexter.Engine.MasterWorker.RunStatus import RunStatus
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEntryModel import DexterJournalEntryModel
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEnums import DexterEngineRunJournalEnum, \
    RunStatusDexterEngineJournal
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
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

    def orchestrate(self):
        query = DexterJournalMongoRepositoryHelper.get_search_for_other_instances_query(
            business_owner_id=self.business_owner_id,
            algorithm_type=self.algorithm_type,
            ad_account_id=self.ad_account_id,
            level=self.level)
        sort_query = DexterJournalMongoRepositoryHelper.get_sort_descending_by_start_date_query()

        ad_account_id_journal = list(self._journal_repository.get_last_two_entries(query, sort_query))

        if ad_account_id_journal:
            doc = ad_account_id_journal[0]

            if RunStatus.is_completed_or_failed(doc=doc):
                self.__run_from_completed_or_failed()

            elif RunStatus.is_in_progress(doc=doc):
                self.__save_pending_entry_to_journal()

            elif RunStatus.is_pending(doc=doc):

                antecedent_doc = ad_account_id_journal[1]
                if RunStatus.is_completed_or_failed(doc=antecedent_doc):
                    self.__run_from_pending()
                else:
                    search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.ad_account_id,
                                                                                               self.algorithm_type,
                                                                                               self.business_owner_id)
                    update_query = DexterJournalMongoRepositoryHelper.get_update_query_start_date_only()
                    self._journal_repository.update_one(search_query, update_query)
        else:
            self.__run_first_time()

    def __init_algorithm(self, alg_type, level) -> typing.Any:
        rule_algorithm = AlgorithmsFactory.get(algorithm_type=alg_type, level=level)
        rules = RulesFactory.get(algorithm_type=alg_type, level=level)
        fuzzyfier_factory = FuzzyfierFactory.get(algorithm_type=alg_type, level=level)
        rule_evaluator = RuleEvaluatorFactory.get(algorithm_type=alg_type, level=level)
        try:
            rule_algorithm = rule_algorithm. \
                set_business_owner_id(self.business_owner_id). \
                set_facebook_config(self.startup.facebook_config). \
                set_business_owner_repo_session(self.startup.session). \
                set_external_services(self.startup.external_services). \
                set_dexter_config(self.startup.dexter_config). \
                set_repository(self._data_repository). \
                set_fuzzyfier_factory(fuzzyfier_factory). \
                set_rules(rules). \
                set_rule_evaluator(rule_evaluator)
        except Exception as e:
            raise e

        return rule_algorithm

    def __run_first_time(self):
        rule_algorithm = self.__init_algorithm(self.algorithm_type, self.level)
        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS)

            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                           self.algorithm_type,
                                                                                           self.business_owner_id)
            self._journal_repository.add_one(journal_object_saving)

            self.__run_algorithm(search_query=search_query)

    def __run_from_pending(self):
        rule_algorithm = self.__init_algorithm(self.algorithm_type, self.level)
        if rule_algorithm is not None:
            search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.ad_account_id,
                                                                                       self.algorithm_type,
                                                                                       self.business_owner_id)
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_in_progress()
            self._journal_repository.update_one(search_query, update_query)

            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                           self.algorithm_type,
                                                                                           self.business_owner_id)

            self.__run_algorithm(search_query=search_query)

    def __save_pending_entry_to_journal(self):
        rule_algorithm = self.__init_algorithm(self.algorithm_type, self.level)
        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.PENDING)
            self._journal_repository.add_one(journal_object_saving)

    def __run_from_completed_or_failed(self):
        rule_algorithm = self.__init_algorithm(self.algorithm_type, self.level)
        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS)
            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                           self.algorithm_type,
                                                                                           self.business_owner_id)
            self._journal_repository.add_one(journal_object_saving)
            self.__run_algorithm(search_query=search_query)

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

    def __run_algorithm(self, search_query):
        try:
            campaigns_ids = self._data_repository.get_campaigns_by_account_id(key_value=self.ad_account_id)
            for campaign_id in campaigns_ids:
                algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.CAMPAIGN)
                should_run = algorithm. \
                    set_dexter_config(self.startup.dexter_config). \
                    set_repository(self._data_repository). \
                    check_run_status(campaign_id)

                if should_run:
                    recommendations = algorithm.run(campaign_id)
                    self._recommendations_repository.save_recommendations(recommendations,
                                                                          self.startup.dexter_config.recommendation_days_last_updated)
                    adset_ids = self._data_repository.get_adsets_by_campaign_id(key_value=campaign_id)
                    for adset_id in adset_ids:
                        algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.ADSET)
                        recommendations = algorithm.run(adset_id)
                        self._recommendations_repository.save_recommendations(recommendations,
                                                                              self.startup.dexter_config.recommendation_days_last_updated)

                        algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.AD)
                        recommendations = algorithm.run(adset_id)
                        self._recommendations_repository.save_recommendations(recommendations,
                                                                              self.startup.dexter_config.recommendation_days_last_updated)

                update_query = DexterJournalMongoRepositoryHelper.get_update_query_completed()

                self._journal_repository.update_one(search_query, update_query)

        except Exception as failed_to_run_exception:
            print(failed_to_run_exception.__traceback__)
            traceback.print_exc()
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_failed()
            self._journal_repository.update_one(search_query, update_query)

    def __create_journal_entry_object(self, run_status):
        journal_object = DexterJournalEntryModel()
        journal_object.business_owner_id = self.business_owner_id
        journal_object.ad_account_id = self.ad_account_id
        journal_object.algorithm_type = self.algorithm_type.value
        journal_object.level = self.level.value
        journal_object.run_status = run_status.value
        journal_object.start_timestamp = datetime.now()
        journal_object.end_timestamp = None
        journal_object_saving = journal_object.__dict__

        return journal_object_saving
