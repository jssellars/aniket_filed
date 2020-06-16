import traceback
import typing
from datetime import datetime

from GoogleDexter.Engine.Algorithms.AlgorithmsFactory import AlgorithmsFactory
from GoogleDexter.Engine.Algorithms.FuzzyfierFactory import FuzzyfierFactory
from GoogleDexter.Engine.Algorithms.RuleEvaluatorFactory import RuleEvaluatorFactory
from GoogleDexter.Engine.Algorithms.RulesFactory import RulesFactory
from GoogleDexter.Engine.MasterWorker.OrchestratorBuilder import OrchestratorBuilder
from GoogleDexter.Engine.MasterWorker.RunStatus import RunStatus
from GoogleDexter.Infrastructure.Constants import DEFAULT_DATETIME
from GoogleDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from GoogleDexter.Infrastructure.Domain.DexterJournal.DexterJournalEntryModel import DexterJournalEntryModel
from GoogleDexter.Infrastructure.Domain.DexterJournal.DexterJournalEnums import DexterEngineRunJournalEnum, \
    RunStatusDexterEngineJournal
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepositoryHelper import \
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
        try:
            rule_algorithm = (rule_algorithm.
                              set_business_owner_id(self.business_owner_id).
                              set_external_services(self.startup.external_services).
                              set_dexter_config(self.startup.dexter_config).
                              set_repository(self._data_repository).
                              set_fuzzyfier_factory(fuzzyfier_factory).
                              set_rules(rules))
        except Exception as e:
            raise e

        return rule_algorithm

    def __run_first_time(self):
        journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS)

        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.algorithm_type,
                                                                                       self.business_owner_id)
        self._journal_repository.add_one(journal_object_saving)
        self.__run_algorithm(search_query=search_query)

    def __run_from_pending(self):
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
        journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.PENDING)
        self._journal_repository.add_one(journal_object_saving)

    def __run_from_completed_or_failed(self):
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
                    DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value:
                        entry[DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value],
                    DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value:
                        entry[DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value],
                    DexterEngineRunJournalEnum.RUN_STATUS.value:
                        entry[DexterEngineRunJournalEnum.RUN_STATUS.value],
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value:
                        entry[DexterEngineRunJournalEnum.ALGORITHM_TYPE.value],
                    DexterEngineRunJournalEnum.START_TIMESTAMP.value:
                        entry[DexterEngineRunJournalEnum.START_TIMESTAMP.value],
                    DexterEngineRunJournalEnum.LEVEL.value:
                        entry[DexterEngineRunJournalEnum.LEVEL.value],
                }
                self._journal_repository.update_one(search_query, update_query)

    def __run_algorithm(self, search_query):
        try:
            if not self.startup.dexter_config.date_stop:
                date_stop = datetime.now()
            else:
                date_stop = datetime.strptime(self.startup.dexter_config.date_stop, DEFAULT_DATETIME)

            for time_interval in self.startup.dexter_config.time_intervals:
                time_interval_enum = DaysEnum(time_interval)
                campaigns_ids = self._data_repository.get_campaigns_by_account_id(key_value=self.ad_account_id)
                for campaign_id in campaigns_ids:
                    algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.CAMPAIGN)
                    rule_evaluator = RuleEvaluatorFactory.get(algorithm_type=self.algorithm_type,
                                                              level=LevelEnum.CAMPAIGN)
                    rule_evaluator.set_time_interval(time_interval_enum)
                    (algorithm.
                     set_dexter_config(self.startup.dexter_config).
                     set_repository(self._data_repository).
                     set_date_stop(date_stop).
                     set_time_interval(time_interval_enum).
                     set_rule_evaluator(rule_evaluator)
                     )

                    recommendations = algorithm.run(campaign_id)
                    self._recommendations_repository.save_recommendations(recommendations,
                                                                          self.startup.dexter_config.recommendation_days_last_updated)
                    adgroup_ids = self._data_repository.get_adgroups_by_campaign_id(key_value=campaign_id)
                    for adgroup_id in adgroup_ids:
                        algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.ADGROUP)
                        rule_evaluator = RuleEvaluatorFactory.get(algorithm_type=self.algorithm_type,
                                                                  level=LevelEnum.ADGROUP)
                        rule_evaluator.set_time_interval(time_interval_enum)
                        algorithm.set_rule_evaluator(rule_evaluator). \
                            set_time_interval(time_interval_enum). \
                            set_date_stop(date_stop)

                        recommendations = algorithm.run(adgroup_id)
                        self._recommendations_repository.save_recommendations(recommendations,
                                                                              self.startup.dexter_config.recommendation_days_last_updated)

                        algorithm = self.__init_algorithm(self.algorithm_type, level=LevelEnum.AD)
                        rule_evaluator = RuleEvaluatorFactory.get(algorithm_type=self.algorithm_type,
                                                                  level=LevelEnum.AD)
                        rule_evaluator.set_time_interval(time_interval_enum)
                        algorithm.set_rule_evaluator(rule_evaluator). \
                            set_time_interval(time_interval_enum). \
                            set_date_stop(date_stop)
                        recommendations = algorithm.run(adgroup_id)
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
