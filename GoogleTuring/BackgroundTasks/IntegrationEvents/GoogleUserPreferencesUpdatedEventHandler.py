import typing

from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEvent import \
    GoogleUserPreferencesUpdatedEvent
from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEventMapping import \
    GoogleUserPreferencesUpdatedEventMapping
from GoogleTuring.BackgroundTasks.SyncJobs.Synchronizers.AdWordsAPIDataSyncHandler import \
    AdWordsAPIDataSyncHandler


class GoogleUserPreferencesUpdatedEventHandler:
    @classmethod
    def handle(cls, message: typing.Dict):
        mapping = GoogleUserPreferencesUpdatedEventMapping(GoogleUserPreferencesUpdatedEvent)
        request = mapping.load(message)

        AdWordsAPIDataSyncHandler.handle(request)

    @classmethod
    def publish(cls, response):
        pass
