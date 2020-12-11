import typing

from facebook_business.adobjects.user import User

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookAccounts.Api.startup import config, fixtures


class BusinessOwnerDeletePermissionsCommandHandler:

    @classmethod
    def handle(cls,
               business_owner_id: typing.AnyStr = None,
               permissions: typing.AnyStr = None) -> typing.Dict:

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        user = User(fbid=business_owner_id)
        response = {
            'successful': [],
            'failed': []
        }
        permissions = permissions.split(",")
        for permission in permissions:
            try:
                fb_response = user.delete_permissions(params={"permission": permission})
                if fb_response:
                    response['successful'].append(permission)
            except:
                response['failed'].append(permission)

        return response
