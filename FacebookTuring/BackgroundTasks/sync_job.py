# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from time import sleep

import schedule

from FacebookTuring.BackgroundTasks.Startup import startup
from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator
from FacebookTuring.Infrastructure.PersistenceLayer.TuringAdAccountJournalRepository import (
    TuringAdAccountJournalRepository,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


import logging

logger = logging.getLogger(__name__)


def sync():
    account_journal_repository = TuringAdAccountJournalRepository(
        config=startup.mongo_config,
        database_name=startup.mongo_config.accounts_journal_database_name,
        collection_name=startup.mongo_config.accounts_journal_collection_name,
    )
    insights_repository = TuringMongoRepository(
        config=startup.mongo_config, database_name=startup.mongo_config.insights_database_name
    )
    structures_repository = TuringMongoRepository(
        config=startup.mongo_config, database_name=startup.mongo_config.structures_database_name
    )
    try:
        (
            Orchestrator()
            .set_account_journal_repository(account_journal_repository)
            .set_insights_repository(insights_repository)
            .set_structures_repository(structures_repository)
            .run()
        )
    except Exception as e:
        logger.exception(f"Failed to sync data || {repr(e)}")


def main():
    schedule.every().day.at(startup.sync_time).do(sync)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == "__main__":
    main()
