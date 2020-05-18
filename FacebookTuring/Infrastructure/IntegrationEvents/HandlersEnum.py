from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookTuring.Infrastructure.IntegrationEvents.BusinessOwnerPreferencesChangedEventHandler import \
    BusinessOwnerPreferencesChangedEventHandler


class HandlersEnum(EnumerationBase):
    BUSINESS_OWNER_UPDATE_EVENT = BusinessOwnerPreferencesChangedEventHandler
