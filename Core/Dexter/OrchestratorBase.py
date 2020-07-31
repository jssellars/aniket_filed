from datetime import datetime

from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import RunStatusDexterEngineJournal, \
    DexterEngineRunJournalEnum
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationFieldInsidersEnum, \
    RecommendationField
from Core.Dexter.OrchestratorBuilder import OrchestratorBuilder
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalEntryModel import DexterJournalEntryModel
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalMongoRepositoryHelper import DexterJournalMongoRepositoryHelper
from Core.Dexter.PersistanceLayer.Helpers.DexterJournalRunStatus import DexterJournalRunStatus


class OrchestratorBase(OrchestratorBuilder):

    def __init__(self):
        super().__init__()

    def _create_journal_entry_object(self, run_status, time_interval):
        journal_object = DexterJournalEntryModel()
        journal_object.business_owner_id = self.business_owner_id
        journal_object.ad_account_id = self.ad_account_id
        journal_object.run_status = run_status.value
        journal_object.start_timestamp = datetime.now()
        journal_object.time_interval = time_interval
        journal_object_saving = journal_object.__dict__

        return journal_object_saving

    def keep_latest_recommendations(self):
        grouped_recommendations = {}
        recommendations = self._recommendations_repository.get_active_recommendations()
        for recommendation in recommendations:
            id = recommendation[RecommendationField.RECOMMENDATION_ID.value]
            time_interval = recommendation[RecommendationField.TIME_INTERVAL.value]
            ad_account_id = recommendation[RecommendationField.AD_ACCOUNT_ID.value]
            structure_id = recommendation[RecommendationField.STRUCTURE_ID.value]
            metric = recommendation[RecommendationField.METRICS.value][0][
                RecommendationFieldInsidersEnum.DISPLAY_NAME.value]
            breakdown = recommendation[RecommendationField.BREAKDOWN.value][RecommendationFieldInsidersEnum.NAME.value]
            level = recommendation[RecommendationField.LEVEL.value]

            group_tuple = (ad_account_id, metric, breakdown, level, structure_id)
            if group_tuple not in grouped_recommendations.keys():
                grouped_recommendations[group_tuple] = [(id, time_interval)]
            else:
                grouped_recommendations[group_tuple].append((id, time_interval))

        ids_to_deprecate = []
        for rec_list in grouped_recommendations.values():
            sorted_rec_list = sorted(rec_list, key=lambda x: x[1][RecommendationFieldInsidersEnum.VALUE.value])
            ids_to_deprecate += list(map(lambda x: x[0], sorted_rec_list))[1:]

        self._recommendations_repository.deprecate_recommendations(recommendation_ids=ids_to_deprecate)

    def __run_from_completed_or_failed(self, time_interval):
        journal_object_saving = self._create_journal_entry_object(run_status=RunStatusDexterEngineJournal.IN_PROGRESS,
                                                                  time_interval=time_interval)
        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)
        self._journal_repository.add_one(journal_object_saving)
        return search_query

    def __save_pending_entry_to_journal(self, time_interval):
        journal_object_saving = self._create_journal_entry_object(run_status=RunStatusDexterEngineJournal.PENDING,
                                                                  time_interval=time_interval)
        self._journal_repository.add_one(journal_object_saving)

    def __run_from_pending(self, time_interval):
        search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(self.ad_account_id,
                                                                                   self.business_owner_id,
                                                                                   time_interval)
        update_query = DexterJournalMongoRepositoryHelper.get_update_query_in_progress()
        self._journal_repository.update_one(search_query, update_query)

        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)

        return search_query

    def __run_first_time(self, time_interval):
        journal_object_saving = self._create_journal_entry_object(RunStatusDexterEngineJournal.IN_PROGRESS,
                                                                  time_interval)

        search_query = DexterJournalMongoRepositoryHelper.get_search_in_progress_query(self.ad_account_id,
                                                                                       self.business_owner_id,
                                                                                       time_interval)
        self._journal_repository.add_one(journal_object_saving)

        return search_query

    def orchestrate(self, time_interval):
        query = DexterJournalMongoRepositoryHelper.get_search_for_other_instances_query(
            business_owner_id=self.business_owner_id,
            ad_account_id=self.ad_account_id,
            time_interval=time_interval)

        sort_query = DexterJournalMongoRepositoryHelper.get_sort_descending_by_start_date_query()
        ad_account_id_journal = list(self._journal_repository.get_last_two_entries(query, sort_query))
        search_query = None
        if ad_account_id_journal:
            doc = ad_account_id_journal[0]

            if DexterJournalRunStatus.is_completed_or_failed(doc=doc):
                search_query = self.__run_from_completed_or_failed(time_interval=time_interval)

            elif DexterJournalRunStatus.is_in_progress(doc=doc):
                search_query = self.__save_pending_entry_to_journal(time_interval=time_interval)

            elif DexterJournalRunStatus.is_pending(doc=doc):
                antecedent_doc = ad_account_id_journal[1]

                if DexterJournalRunStatus.is_completed_or_failed(doc=antecedent_doc):
                    search_query = self.__run_from_pending(time_interval=time_interval)
                else:
                    search_query = DexterJournalMongoRepositoryHelper.get_search_pending_query(
                        ad_account_id=self.ad_account_id,
                        business_owner_id=self.business_owner_id,
                        time_interval=time_interval)
                    update_query = DexterJournalMongoRepositoryHelper.get_update_query_start_date_only()
                    self._journal_repository.update_one(search_query, update_query)
        else:
            search_query = self.__run_first_time(time_interval=time_interval)

        return search_query

    def update_remaining_null_dates(self):
        search_null_end_date_query = (DexterJournalMongoRepositoryHelper.
                                      get_search_for_null_end_date(self.business_owner_id, self.ad_account_id))
        null_entries = list(self._journal_repository.get_all_by_query(search_null_end_date_query))
        for entry in null_entries:
            if entry[DexterEngineRunJournalEnum.END_TIMESTAMP.value] is None and \
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value in entry:
                update_query = DexterJournalMongoRepositoryHelper.get_update_query_for_null_entries()
                search_query = {
                    DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value:
                        entry[DexterEngineRunJournalEnum.AD_ACCOUNT_ID.value],
                    DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value:
                        entry[DexterEngineRunJournalEnum.BUSINESS_OWNER_ID.value],
                    DexterEngineRunJournalEnum.RUN_STATUS.value: entry[DexterEngineRunJournalEnum.RUN_STATUS.value],
                    DexterEngineRunJournalEnum.ALGORITHM_TYPE.value:
                        entry[DexterEngineRunJournalEnum.ALGORITHM_TYPE.value],
                    DexterEngineRunJournalEnum.START_TIMESTAMP.value:
                        entry[DexterEngineRunJournalEnum.START_TIMESTAMP.value],
                    DexterEngineRunJournalEnum.LEVEL.value: entry[DexterEngineRunJournalEnum.LEVEL.value],
                }
                self._journal_repository.update_one(search_query, update_query)

    def run_algorithm(self, search_query, time_interval, mongo_config):
        raise NotImplementedError
