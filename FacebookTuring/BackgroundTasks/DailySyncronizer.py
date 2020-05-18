from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.BackgroundTasks.Startup import startup, logger
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import \
    TuringAdAccountJournalRepository
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


def run_daily_sync():
    #  Initialize mongo repositories for accounts journal, insights and structures
    account_journal_repository = TuringAdAccountJournalRepository(config=startup.mongo_config,
                                                                  database_name=startup.mongo_config.accounts_journal_database_name,
                                                                  collection_name=startup.mongo_config.accounts_journal_collection_name)
    insights_repository = TuringMongoRepository(config=startup.mongo_config,
                                                database_name=startup.mongo_config.insights_database_name)
    structures_repository = TuringMongoRepository(config=startup.mongo_config,
                                                  database_name=startup.mongo_config.structures_database_name)

    try:
        orchestrator = Orchestrator(). \
            set_account_journal_repository(account_journal_repository). \
            set_insights_repository(insights_repository). \
            set_structures_reposiotry(structures_repository)
        orchestrator.run()
    except:
        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                name="Facebook Turing Daily Sync Error",
                                description="Failed to sync data.")
        logger.logger.exception(log.to_dict())
        return
