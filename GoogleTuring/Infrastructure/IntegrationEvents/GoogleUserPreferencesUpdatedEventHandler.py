import typing

from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIDataSyncHandler import \
    AdWordsAPIDataSyncHandler
from GoogleTuring.Infrastructure.IntegrationEvents.GoogleUserPreferencesUpdatedEvent import \
    GoogleUserPreferencesUpdatedEvent
from GoogleTuring.Infrastructure.IntegrationEvents.GoogleUserPreferencesUpdatedEventMapping import \
    GoogleUserPreferencesUpdatedEventMapping


class GoogleUserPreferencesUpdatedEventHandler:
    @classmethod
    def handle(cls, message: typing.Dict):
        mapping = GoogleUserPreferencesUpdatedEventMapping(GoogleUserPreferencesUpdatedEvent)
        request = mapping.load(message)

        AdWordsAPIDataSyncHandler.handle(request)

    @classmethod
    def publish(cls, response):
        pass
