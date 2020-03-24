from Algorithms.Tools.Columns import RunStatusDexterEngineJournal, DexterEngineRunJournalEnum


class RunStatusChecker:

    @staticmethod
    def is_run_status_failed_or_completed(doc):
        if doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.COMPLETED.value:
            return 1
        elif doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.FAILED.value:
            return 1

        return 0

    @staticmethod
    def is_run_status_pending(doc):
        if doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.PENDING.value:
            return 1

        return 0

    @staticmethod
    def is_run_status_in_progress(doc):
        if doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.IN_PROGRESS.value:
            return 1

        return 0
