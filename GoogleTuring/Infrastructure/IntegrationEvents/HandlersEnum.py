from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleTuring.Infrastructure.IntegrationEvents.GoogleUserPreferencesUpdatedEventHandler import \
    GoogleUserPreferencesUpdatedEventHandler


class HandlersEnum(EnumerationBase):
    GOOGLE_USER_PREFERENCES_UPDATED_EVENT = GoogleUserPreferencesUpdatedEventHandler
