from Core.Tools.Misc.EnumerationBase import EnumerationBase
from PotterFacebookAudiences.Infrastructure.IntegrationEvents.GetAllAudiencesMessageRequestHandler import \
    GetAllAudiencesMessageRequestHandler


class HandlersEnum(EnumerationBase):
    GET_ALL_AUDIENCES_REQUEST_HANDLER = GetAllAudiencesMessageRequestHandler
