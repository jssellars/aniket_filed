from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleTuring.BackgroundTasks.IntegrationEvents.GoogleUserPreferencesUpdatedEventHandler import \
    GoogleUserPreferencesUpdatedEventHandler


class HandlersEnum(EnumerationBase):
    GOOGLE_USER_PREFERENCES_UPDATED_EVENT = GoogleUserPreferencesUpdatedEventHandler
