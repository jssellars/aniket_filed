import typing

from facebook_business.adobjects.user import User

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookAccounts.Api.Startup import startup


class BusinessOwnerDeletePermissionsCommandHandler:

    @classmethod
    def handle(cls,
               business_owner_id: typing.AnyStr = None,
               permissions: typing.AnyStr = None) -> typing.Dict:

        # get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)

        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(startup.facebook_config, permanent_token)

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
            except Exception as e:
                response['failed'].append(permission)

        return response
