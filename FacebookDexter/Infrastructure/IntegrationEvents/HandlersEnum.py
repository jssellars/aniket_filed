from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookDexter.Infrastructure.IntegrationEvents.FacebookTuringDataSyncCompletedEventHandler import \
    FacebookTuringDataSyncCompletedEventHandler


class HandlersEnum(EnumerationBase):
    TURING_DATA_SYNC_COMPLETED = FacebookTuringDataSyncCompletedEventHandler
