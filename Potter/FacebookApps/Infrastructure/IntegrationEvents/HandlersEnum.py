from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Potter.FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequestHandler import GetAllAppsMessageRequestHandler


class HandlersEnum(EnumerationBase):
    GET_ALL_APPS_REQUEST_HANDLER = GetAllAppsMessageRequestHandler
