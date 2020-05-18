from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Potter.FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageRequestHandler import \
    GetAllPixelsMessageRequestHandler


class HandlersEnum(EnumerationBase):
    GET_ALL_PIXELS_REQUEST_HANDLER = GetAllPixelsMessageRequestHandler
