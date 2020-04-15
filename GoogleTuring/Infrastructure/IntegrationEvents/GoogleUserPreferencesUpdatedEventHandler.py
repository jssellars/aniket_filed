import typing

from GoogleTuring.Infrastructure.AdwordsAPIHandlers.AdwordsAPISyncStructuresHandler import AdwordsAPISyncStructuresHandler
from GoogleTuring.Infrastructure.IntegrationEvents.GoogleUserPreferencesUpdatedEvent import GoogleUserPreferencesUpdatedEvent
from GoogleTuring.Infrastructure.IntegrationEvents.GoogleUserPreferencesUpdatedEventMapping import GoogleUserPreferencesUpdatedEventMapping


class GoogleUserPreferencesUpdatedEventHandler:
    @classmethod
    def handle(cls, message: typing.Dict):
        mapping = GoogleUserPreferencesUpdatedEventMapping(GoogleUserPreferencesUpdatedEvent)
        request = mapping.load(message)

        AdwordsAPISyncStructuresHandler.handle(request)

    @classmethod
    def publish(cls, response):
        pass
