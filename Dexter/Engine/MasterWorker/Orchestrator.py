from datetime import datetime

from Algorithms.AlgorithmsFactory import AlgorithmsFactory
from Algorithms.Dexter_Fuzzy_Inference.Tools import BusinessOwnerUtilitaries
from Algorithms.Tools.Columns import ChannelEnum
from Algorithms.Tools.Columns import RunStatusDexterEngineJournal, DexterEngineRunJournalObject, DexterEngineRunJournalEnum
from Algorithms.Tools.JournalHelper import JournalHelper
from MasterWorker.Tools.RunStatusChecker import RunStatusChecker


class Orchestrator:

    def __init__(self, ad_account_id=None, algorithm_type=None, all_insights_collections=None, business_owner_id=None, channel=None):
        self.ad_account_id = ad_account_id
        self.algorithm_type = algorithm_type
        self.all_insights_collections = all_insights_collections
        self.business_owner_id = business_owner_id
        self.channel = channel

    def __get_data_and_run_algorithm(self, mongo_journalizer, mongo_repository_insights, rule_algorithm, search_query):
        try:
            actual_data = BusinessOwnerUtilitaries.get_data_for_account_id(ad_account_id=self.ad_account_id,
                                                                           mongo_repository=mongo_repository_insights,
                                                                           all_insights_collections=self.all_insights_collections
                                                                           )

            if actual_data:
                for insights_and_combination in actual_data:
                    if insights_and_combination[0]:
                        rule_algorithm.data = insights_and_combination[0]
                        rule_algorithm.combination = insights_and_combination[1]
                        rule_algorithm.run()

            update_query = JournalHelper.get_update_query_completed()

            mongo_journalizer.update(search_query, update_query)

        except Exception as failed_to_run_exception:
            # TODO: maybe log this error, but I assume not needed that much
            print(failed_to_run_exception)
            update_query = JournalHelper.get_update_query_failed()
            mongo_journalizer.update(search_query, update_query)

    def __run_first_time(self, mongo_journalizer, mongo_recommender, mongo_repository_insights):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.algorithm_type,
                                                   ad_account_id=self.ad_account_id,
                                                   channel=self.channel,
                                                   mongo_recommender=mongo_recommender
                                                   )
        if rule_algorithm is not None:
            # TODO: state-machine pattern

            # Create the object
            journal_object = DexterEngineRunJournalObject(business_owner_id=self.business_owner_id,
                                                          ad_account_id=self.ad_account_id,
                                                          algorithm_type=self.algorithm_type,
                                                          run_status=RunStatusDexterEngineJournal.IN_PROGRESS,
                                                          start_timestamp=datetime.now(),
                                                          end_timestamp=None
                                                          )
            journal_object_saving = journal_object.__dict__
            search_query = JournalHelper.get_search_in_progress_query(self.ad_account_id, self.algorithm_type, self.business_owner_id)
            mongo_journalizer.add_one(journal_object_saving)

            self.__get_data_and_run_algorithm(mongo_journalizer, mongo_repository_insights, rule_algorithm, search_query)

    def __run_from_pending(self, mongo_journalizer, mongo_recommender, mongo_repository_insights):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.algorithm_type,
                                                   ad_account_id=self.ad_account_id,
                                                   channel=self.channel,
                                                   mongo_recommender=mongo_recommender
                                                   )
        if rule_algorithm is not None:
            # Update the pending with in_progress
            search_query = JournalHelper.get_search_pending_query(self.ad_account_id, self.algorithm_type, self.business_owner_id)
            update_query = JournalHelper.get_update_query_in_progress()
            mongo_journalizer.update(search_query, update_query)

            search_query = JournalHelper.get_search_in_progress_query(self.ad_account_id, self.algorithm_type, self.business_owner_id)

            self.__get_data_and_run_algorithm(mongo_journalizer, mongo_repository_insights, rule_algorithm, search_query)

    def __save_pending_entry_to_journal(self, mongo_journalizer, mongo_recommender):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.algorithm_type,
                                                   ad_account_id=self.ad_account_id,
                                                   channel=self.channel,
                                                   mongo_recommender=mongo_recommender
                                                   )
        if rule_algorithm is not None:
            journal_object = DexterEngineRunJournalObject(business_owner_id=self.business_owner_id,
                                                          ad_account_id=self.ad_account_id,
                                                          algorithm_type=self.algorithm_type,
                                                          run_status=RunStatusDexterEngineJournal.PENDING,
                                                          start_timestamp=datetime.now(),
                                                          end_timestamp=None
                                                          )
            journal_object_saving = journal_object.__dict__
            mongo_journalizer.add_one(journal_object_saving)

    def __run_from_completed_or_failed(self, mongo_journalizer, mongo_recommender, mongo_repository_insights):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.algorithm_type,
                                                   ad_account_id=self.ad_account_id,
                                                   channel=self.channel,
                                                   mongo_recommender=mongo_recommender
                                                   )
        if rule_algorithm is not None:
            journal_object = DexterEngineRunJournalObject(business_owner_id=self.business_owner_id,
                                                          ad_account_id=self.ad_account_id,
                                                          algorithm_type=self.algorithm_type,
                                                          run_status=RunStatusDexterEngineJournal.IN_PROGRESS,
                                                          start_timestamp=datetime.now(),
                                                          end_timestamp=None
                                                          )
            journal_object_saving = journal_object.__dict__
            search_query = JournalHelper.get_search_in_progress_query(self.ad_account_id, self.algorithm_type, self.business_owner_id)
            mongo_journalizer.add_one(journal_object_saving)

            self.__get_data_and_run_algorithm(mongo_journalizer, mongo_repository_insights, rule_algorithm, search_query)

    def update_remaining_null_dates(self, mongo_journalizer):
        search_null_end_date_query = JournalHelper.get_search_for_null_end_date(self.business_owner_id, self.ad_account_id)
        null_entries = list(mongo_journalizer.find(search_null_end_date_query))
        for entry in null_entries:
            if entry[DexterEngineRunJournalEnum.END_TIMESTAMP.value] is None:
                update_query = JournalHelper.get_update_query_for_null_entries()
                search_query = {
                    DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value: entry[DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value],
                    DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: entry[DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value],
                    DexterEngineRunJournalEnum.RUN_STATUS.value: entry[DexterEngineRunJournalEnum.RUN_STATUS.value],
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value: entry[DexterEngineRunJournalEnum.ALGORITHM_TYPE.value],
                    DexterEngineRunJournalEnum.START_TIMESTAMP.value: entry[DexterEngineRunJournalEnum.START_TIMESTAMP.value],
                }
                mongo_journalizer.update(search_query, update_query)

    def orchestrate(self, mongo_recommender=None, mongo_journalizer=None, mongo_repository_insights=None):

        query = JournalHelper.get_search_for_other_instances_query(business_owner_id=self.business_owner_id,
                                                                   algorithm_type=self.algorithm_type,
                                                                   ad_account_id=self.ad_account_id
                                                                   )
        sort_query = JournalHelper.get_sort_descending_by_start_date_query()

        ad_account_id_journal = list(mongo_journalizer.get_last_two_entries(query, sort_query))
        if ad_account_id_journal:
            doc = ad_account_id_journal[0]

            if RunStatusChecker.is_run_status_failed_or_completed(doc=doc):
                self.__run_from_completed_or_failed(mongo_journalizer=mongo_journalizer, mongo_recommender=mongo_recommender, mongo_repository_insights=mongo_repository_insights)

            elif RunStatusChecker.is_run_status_in_progress(doc=doc):
                self.__save_pending_entry_to_journal(mongo_journalizer=mongo_journalizer, mongo_recommender=mongo_recommender)

            elif RunStatusChecker.is_run_status_pending(doc=doc):

                antecedent_doc = ad_account_id_journal[1]
                if RunStatusChecker.is_run_status_failed_or_completed(doc=antecedent_doc):
                    self.__run_from_pending(mongo_journalizer=mongo_journalizer, mongo_recommender=mongo_recommender, mongo_repository_insights=mongo_repository_insights)
                else:
                    search_query = JournalHelper.get_search_pending_query(self.ad_account_id, self.algorithm_type, self.business_owner_id)
                    update_query = JournalHelper.get_update_query_start_date_only()
                    mongo_journalizer.update(search_query, update_query)
        # There was no entry for this algorithm, ad_account_id, business_owner_id combination
        else:
            self.__run_first_time(mongo_journalizer=mongo_journalizer, mongo_recommender=mongo_recommender, mongo_repository_insights=mongo_repository_insights)
