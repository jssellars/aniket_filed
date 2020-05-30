import typing

from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIRequests.GraphAPIRequestAudienceSize import GraphAPIRequestAudienceSize


class AudienceSizeCommandHandler(object):

    @classmethod
    def handle(cls,
               permanent_token: typing.AnyStr = None,
               account_id: typing.AnyStr = None,
               audience_details: typing.AnyStr = None):
        try:
            audience_size_request = GraphAPIRequestAudienceSize(access_token=permanent_token,
                                                                account_id=account_id,
                                                                audience_details=audience_details)
            response, _ = HTTPRequestBase.get(audience_size_request.url)
        except Exception as e:
            raise e

        if isinstance(response, Exception):
            raise response

        audience_size_estimate = response[0].get('estimate_mau', None)
        return audience_size_estimate
