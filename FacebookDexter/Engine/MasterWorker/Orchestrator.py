import traceback
from datetime import datetime

from FacebookDexter.Engine.Algorithms.AlgorithmsFactory import AlgorithmsFactory
from FacebookDexter.Engine.MasterWorker.RunStatus import RunStatus
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEntryModel import DexterJournalEntryModel
from FacebookDexter.Infrastructure.Domain.DexterJournal.DexterJournalEnums import DexterEngineRunJournalEnum, RunStatusDexterEngineJournal
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterJournalMongoRepositoryHelper import DexterJournalMongoRepositoryHelper
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository
from FacebookDexter.Infrastructure.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository


class Orchestrator:

    def __init__(self, ad_account_id=None, algorithm_type=None, business_owner_id=None, level=None, startup=None):
        self.__ad_account_id = ad_account_id
        self.__algorithm_type = algorithm_type
        self.__business_owner_id = business_owner_id
        self.__level = level
        self.__startup = startup
        self.__dexter_default_repository = DexterMongoRepository(config=self.__startup.mongo_config)
        self.__dexter_recommendation_repository = DexterRecommendationsMongoRepository(config=self.__startup.mongo_config)
        self.__dexter_journal_repository = DexterJournalMongoRepository(config=self.__startup.mongo_config)

    def orchestrate(self):
        query = DexterJournalMongoRepositoryHelper.get_search_for_other_instances_query(business_owner_id=self.__business_owner_id,
                                                                                        algorithm_type=self.__algorithm_type,
                                                                                        ad_account_id=self.__ad_account_id,
                                                                                        level=self.__level
                                                                                        )
        sort_query = DexterJournalMongoRepositoryHelper.get_sort_descending_by_start_date_query()

        ad_account_id_journal = list(self.__dexter_journal_repository.get_last_two_entries(query, sort_query))

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
                    search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.__ad_account_id, self.__algorithm_type, self.__business_owner_id)
                    update_query = DexterJournalMongoRepositoryHelper.get_update_query_start_date_only()
                    self.__dexter_journal_repository.update_one(search_query, update_query)

        else:
            self.__run_first_time()

    def __run_first_time(self):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.__algorithm_type, level=self.__level)
        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS)

            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.__ad_account_id, self.__algorithm_type, self.__business_owner_id)
            self.__dexter_journal_repository.add_one(journal_object_saving)

            self.__run_algorithm(algorithm=rule_algorithm,
                                 search_query=search_query)

    def __run_from_pending(self):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.__algorithm_type, level=self.__level)

        if rule_algorithm is not None:
            search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.__ad_account_id, self.__algorithm_type, self.__business_owner_id)
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_in_progress()
            self.__dexter_journal_repository.update_one(search_query, update_query)

            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.__ad_account_id, self.__algorithm_type, self.__business_owner_id)

            self.__run_algorithm(algorithm=rule_algorithm,
                                 search_query=search_query)

    def __save_pending_entry_to_journal(self):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.__algorithm_type, level=self.__level)
        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.PENDING)
            self.__dexter_journal_repository.add_one(journal_object_saving)

    def __run_from_completed_or_failed(self):
        rule_algorithm = AlgorithmsFactory.factory(algorithm_type=self.__algorithm_type, level=self.__level)

        if rule_algorithm is not None:
            journal_object_saving = self.__create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS)
            search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.__ad_account_id, self.__algorithm_type, self.__business_owner_id)
            self.__dexter_journal_repository.add_one(journal_object_saving)
            self.__run_algorithm(algorithm=rule_algorithm,
                                 search_query=search_query)

    # TODO: this is probably a stupid way to do it. it might be better to simply just update every END_TIMESTAMP that is none to datetime.now()
    def update_remaining_null_dates(self):
        search_null_end_date_query = DexterJournalMongoRepositoryHelper.get_search_for_null_end_date(self.__business_owner_id, self.__ad_account_id)
        null_entries = list(self.__dexter_journal_repository.get_all_by_query(search_null_end_date_query))
        for entry in null_entries:
            if entry[DexterEngineRunJournalEnum.END_TIMESTAMP.value] is None:
                update_query = DexterJournalMongoRepositoryHelper.get_update_query_for_null_entries()
                search_query = {
                    DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value: entry[DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value],
                    DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value: entry[DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value],
                    DexterEngineRunJournalEnum.RUN_STATUS.value: entry[DexterEngineRunJournalEnum.RUN_STATUS.value],
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value: entry[DexterEngineRunJournalEnum.ALGORITHM_TYPE.value],
                    DexterEngineRunJournalEnum.START_TIMESTAMP.value: entry[DexterEngineRunJournalEnum.START_TIMESTAMP.value],
                    DexterEngineRunJournalEnum.LEVEL.value: entry[DexterEngineRunJournalEnum.LEVEL.value],
                }
                self.__dexter_journal_repository.update_one(search_query, update_query)

    def __run_algorithm(self, algorithm, search_query):
        try:
            campaigns_ids = self.__dexter_default_repository.get_campaigns_by_account_id(key_value=self.__ad_account_id)

            if self.__level == LevelEnum.CAMPAIGN:
                for campaign_id in campaigns_ids:
                    recommendations = algorithm.run(campaign_id=campaign_id)
                    self.__dexter_recommendation_repository.save_recommendations(recommendations)

                return

            if self.__level == LevelEnum.ADSET or self.__level == LevelEnum.AD:
                for campaign_id in campaigns_ids:
                    adset_ids = self.__dexter_default_repository.get_adsets_by_campaign_id(key_value=campaign_id)
                    for adset_id in adset_ids:
                        recommendations = algorithm.run(adset_id=adset_id)
                        self.__dexter_recommendation_repository.save_recommendations(recommendations)

                return

            update_query = DexterJournalMongoRepositoryHelper.get_update_query_completed()

            self.__dexter_journal_repository.update_one(search_query, update_query)

        except Exception as failed_to_run_exception:
            print(failed_to_run_exception.__traceback__)
            traceback.print_exc()
            update_query = DexterJournalMongoRepositoryHelper.get_update_query_failed()
            self.__dexter_journal_repository.update_one(search_query, update_query)

    def __create_journal_entry_object(self, run_status):
        journal_object = DexterJournalEntryModel()
        journal_object.business_owner_id = self.__business_owner_id
        journal_object.ad_account_id = self.__ad_account_id
        journal_object.algorithm_type = self.__algorithm_type
        journal_object.level = self.__level
        journal_object.run_status = run_status
        journal_object.start_timestamp = datetime.now()
        journal_object.end_timestamp = None
        journal_object_saving = journal_object.__dict__

        return journal_object_saving
