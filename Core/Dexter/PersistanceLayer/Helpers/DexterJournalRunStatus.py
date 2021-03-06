from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import DexterEngineRunJournalEnum, \
    RunStatusDexterEngineJournal


class DexterJournalRunStatus:

    @staticmethod
    def is_completed_or_failed(doc):
        return doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.COMPLETED.value or \
               doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.FAILED.value

    @staticmethod
    def is_pending(doc):
        return doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.PENDING.value

    @staticmethod
    def is_in_progress(doc):
        return doc[DexterEngineRunJournalEnum.RUN_STATUS.value] == RunStatusDexterEngineJournal.IN_PROGRESS.value
