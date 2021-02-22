# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
from time import sleep

import schedule

from FacebookTuring.BackgroundTasks.startup import config
from FacebookTuring.BackgroundTasks.Orchestrators.Orchestrator import Orchestrator

import logging

logger = logging.getLogger(__name__)


def sync():

    try:
        Orchestrator().run()
    except Exception as e:
        logger.exception(f"Failed to sync data || {repr(e)}")


def main():
    schedule.every().day.at(config.sync_time).do(sync)

    while True:
        schedule.run_pending()
        sleep(5)


if __name__ == "__main__":
    main()
