from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequestHandler import \
    GetAllAudiencesMessageRequestHandler


class HandlersEnum(EnumerationBase):
    GET_ALL_AUDIENCES_REQUEST_HANDLER = GetAllAudiencesMessageRequestHandler
