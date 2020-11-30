# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import time

import schedule

from GoogleTuring.BackgroundTasks.SyncJobs.DailySyncJob import daily_sync_job
from GoogleTuring.BackgroundTasks.Startup import startup


def main():
    schedule.every().day.at(startup.sync_time).do(daily_sync_job)
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":
    main()
