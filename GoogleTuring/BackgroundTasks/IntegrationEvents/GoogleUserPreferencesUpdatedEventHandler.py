import typing

from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEvent import \
    GoogleUserPreferencesUpdatedEvent
from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEventMapping import \
    GoogleUserPreferencesUpdatedEventMapping
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.AdWordsAPIDataSyncHandler import \
    AdWordsAPIDataSyncHandler


class GoogleUserPreferencesUpdatedEventHandler:
    @classmethod
    def handle(cls, message: typing.Dict, logger=None):
        mapping = GoogleUserPreferencesUpdatedEventMapping(GoogleUserPreferencesUpdatedEvent)
        request = mapping.load(message)

        AdWordsAPIDataSyncHandler.handle(request, logger=logger)

    @classmethod
    def publish(cls, response):
        pass
