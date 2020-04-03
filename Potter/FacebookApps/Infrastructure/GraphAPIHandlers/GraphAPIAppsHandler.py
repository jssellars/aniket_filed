import typing

from facebook_business.adobjects.adaccount import AdAccount

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookApps.BackgroundTasks import Startup
from Potter.FacebookApps.Infrastructure.Domain.App import App
from Potter.FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppDto import GraphAPIAppDto
from Potter.FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppFields import GraphAPIAppFields
from Potter.FacebookApps.Infrastructure.GraphAPIMappings.GraphAPIAppMapping import GraphAPIAppMapping


class GraphAPIAppsHandler:

    @classmethod
    def get_apps(cls,
                 permanent_token: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 startup: Startup = None) -> typing.Tuple[typing.List[App], typing.List[typing.Dict]]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(startup.facebook_config, permanent_token)

        # get apps
        errors = []
        try:
            apps = cls.get_apps_base(account_id=account_id)
        except Exception as e:
            apps = []
            errors.append(Tools.create_error(e, "GraphAPIAppsHandler.get_apps()"))

        return apps, errors

    @classmethod
    def get_apps_base(cls,
                      account_id: typing.AnyStr = None):
        ad_account = AdAccount(fbid=account_id)
        apps = ad_account.get_applications(fields=GraphAPIAppFields.get_values())
        mapper = GraphAPIAppMapping(target=GraphAPIAppDto)
        apps = mapper.load(apps, many=True)

        return apps
