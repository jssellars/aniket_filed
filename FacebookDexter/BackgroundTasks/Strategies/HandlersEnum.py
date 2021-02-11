from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookDexter.BackgroundTasks.Strategies.FacebookTuringSyncDoneHandler import FacebookTuringSyncDoneHandler


class HandlersEnum(EnumerationBase):
    # TURING_DATA_SYNC_COMPLETED = FacebookTuringDataSyncCompletedEventHandler
    TURING_DATA_SYNC_COMPLETED = FacebookTuringSyncDoneHandler
