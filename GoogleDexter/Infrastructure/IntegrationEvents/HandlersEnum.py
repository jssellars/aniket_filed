from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleDexter.Infrastructure.IntegrationEvents.GoogleTuringDataSyncCompletedEventHandler import \
    GoogleTuringDataSyncCompletedEventHandler


class HandlersEnum(EnumerationBase):
    TURING_DATA_SYNC_COMPLETED = GoogleTuringDataSyncCompletedEventHandler
