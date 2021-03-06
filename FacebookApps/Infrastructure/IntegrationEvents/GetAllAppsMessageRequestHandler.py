import hashlib
import json
import typing
from datetime import datetime

from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookApps.Infrastructure.Domain.App import App
from FacebookApps.Infrastructure.Domain.AppStateEnum import AppStateEnum
from FacebookApps.Infrastructure.Domain.Event import Event
from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppDto import GraphAPIAppDto
from FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto
from FacebookApps.Infrastructure.GraphAPIHandlers.GraphAPIAppsHandler import GraphAPIAppsHandler
from FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequest import GetAllAppsMessageRequest
from FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequestMapping import \
    GetAllAppsMessageRequestMapping
from FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageResponse import GetAllAppsMessageResponse


import logging

logger = logging.getLogger(__name__)


class GetAllAppsMessageRequestHandler:
    @classmethod
    def handle(cls, message_body: typing.AnyStr, config, fixtures) -> typing.NoReturn:
        # get apps
        try:
            body = json.loads(message_body)
            message_mapper = GetAllAppsMessageRequestMapping(target=GetAllAppsMessageRequest)
            message = message_mapper.load(body)

            permanent_token = fixtures.business_owner_repository.get_permanent_token(message.business_owner_facebook_id)

            graph_api_apps_dtos, errors = GraphAPIAppsHandler.get_apps(permanent_token=permanent_token,
                                                                       account_id=message.ad_account_id,
                                                                       config=config)
        except Exception as e:
            raise e

        try:
            # map GraphAPIAppsDto to App model
            apps = [cls.__map_graph_api_dto(fb_app) for fb_app in graph_api_apps_dtos]
        except Exception as e:
            raise e

        try:
            response = GetAllAppsMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                                 ad_account_id=message.ad_account_id,
                                                 apps=apps,
                                                 errors=errors)

            cls.__publish(response, fixtures)
        except Exception as e:
            raise e

    @classmethod
    def __map_graph_api_dto(cls, fb_app: GraphAPIAppDto = None) -> App:
        events = [cls.__map_graph_api_app_event_type_dto(fb_app.id, event) for event in fb_app.app_event_types]
        app = App(id=fb_app.id,
                  name=fb_app.name,
                  date_created=fb_app.created_time,
                  last_updated=datetime.now().strftime('%y-%m-%d %H:%M:%S'),
                  details_as_json=object_to_json(fb_app),
                  state=AppStateEnum.ACTIVE.value,
                  events=events)

        return app

    @classmethod
    def __map_graph_api_app_event_type_dto(cls, app_id: typing.AnyStr = None,
                                           fb_app_event: GraphAPIAppEventTypeDto = None) -> Event:
        event_id = app_id + fb_app_event.event_name
        event_id = hashlib.sha1(event_id.encode('utf-8')).hexdigest()

        event = Event(id=event_id,
                      name=fb_app_event.event_name,
                      display_name=fb_app_event.display_name,
                      details_as_json=object_to_json(fb_app_event),
                      last_updated=datetime.now().strftime('%y-%m-%d %H:%M:%S'),
                      state=AppStateEnum.ACTIVE.value)

        return event

    @classmethod
    def __publish(cls, response: GetAllAppsMessageResponse, fixtures) -> typing.NoReturn:
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(response)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(response)})
        except Exception as e:
            raise e
