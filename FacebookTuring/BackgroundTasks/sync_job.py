# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from time import sleep

import schedule

from Core.logging_legacy import log_message_as_dict
from FacebookTuring.BackgroundTasks.Startup import startup, logger, rabbit_logger
from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


import logging

logger_native = logging.getLogger(__name__)


def sync():
    account_journal_repository = TuringAdAccountJournalRepository(
        config=startup.mongo_config,
        database_name=startup.mongo_config.accounts_journal_database_name,
        collection_name=startup.mongo_config.accounts_journal_collection_name,
        logger=logger,
    )
    insights_repository = TuringMongoRepository(
        config=startup.mongo_config, database_name=startup.mongo_config.insights_database_name, logger=logger
    )
    structures_repository = TuringMongoRepository(
        config=startup.mongo_config, database_name=startup.mongo_config.structures_database_name, logger=logger
    )
    try:
        (
            Orchestrator()
            .set_account_journal_repository(account_journal_repository)
            .set_insights_repository(insights_repository)
            .set_logger(logger)
            .set_rabbit_logger(rabbit_logger)
            .set_structures_repository(structures_repository)
            .run()
        )
    except Exception as e:
        logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
            name="Facebook Turing Daily Sync Error",
            description="Failed to sync data. Reason: %s" % str(e),
        ))


def main():
    schedule.every().day.at(startup.sync_time).do(sync)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == "__main__":
    main()
