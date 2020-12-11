import copy
import typing

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.application import Application

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppDto import GraphAPIAppDto
from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto
from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppFields import GraphAPIAppFields
from FacebookApps.Infrastructure.GraphAPIDtos.GraphApiAppEventTypeFields import GraphAPIAppEventTypeFields
from FacebookApps.Infrastructure.GraphAPIMappings.GraphAPIAppEventTypesMapping import \
    GraphAPIAppEventTypesMapping
from FacebookApps.Infrastructure.GraphAPIMappings.GraphAPIAppMapping import GraphAPIAppMapping


class GraphAPIAppsHandler:

    @classmethod
    def get_apps(cls,
                 permanent_token: typing.AnyStr = None,
                 account_id: typing.AnyStr = None,
                 config=None) -> typing.Tuple[typing.List[GraphAPIAppDto], typing.List[typing.Dict]]:
        # initialize GraphAPI SDK
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        # get apps
        errors = []
        try:
            apps, errors = cls.__get_apps_base(account_id=account_id)
        except Exception as e:
            apps = []
            errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))

        return apps, errors

    @classmethod
    def __get_apps_base(cls, account_id: typing.AnyStr = None) -> typing.Tuple[typing.List[GraphAPIAppDto], typing.List[typing.Dict]]:
        errors = []
        try:
            ad_account = AdAccount(fbid=account_id)
            response = ad_account.get_applications(fields=GraphAPIAppFields.get_values())
            mapper = GraphAPIAppMapping(target=GraphAPIAppDto)
            fb_apps = mapper.load(response, many=True)
        except Exception as e:
            errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))
            return [], errors

        for fb_app in fb_apps:
            try:
                fb_app.app_event_types = cls.__get_app_event_types(fb_app.id)
            except Exception as e:
                errors.append(copy.deepcopy(Tools.create_error(e, code="IntegrationEventError")))
        return fb_apps, errors

    @classmethod
    def __get_app_event_types(cls, facebook_id: typing.AnyStr = None) -> typing.List[GraphAPIAppEventTypeDto]:
        application = Application(fbid=facebook_id)
        fb_app_event_types = application.get_app_event_types(fields=GraphAPIAppEventTypeFields.get_values())
        mapper = GraphAPIAppEventTypesMapping(target=GraphAPIAppEventTypeDto)
        app_event_types = mapper.load(fb_app_event_types, many=True)
        return app_event_types
