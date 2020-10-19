import hashlib
import json
import typing
from datetime import datetime

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from PotterFacebookApps.BackgroundTasks.Startup import startup
from PotterFacebookApps.Infrastructure.Domain.App import App
from PotterFacebookApps.Infrastructure.Domain.AppStateEnum import AppStateEnum
from PotterFacebookApps.Infrastructure.Domain.Event import Event
from PotterFacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppDto import GraphAPIAppDto
from PotterFacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto
from PotterFacebookApps.Infrastructure.GraphAPIHandlers.GraphAPIAppsHandler import GraphAPIAppsHandler
from PotterFacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequest import GetAllAppsMessageRequest
from PotterFacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequestMapping import \
    GetAllAppsMessageRequestMapping
from PotterFacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageResponse import GetAllAppsMessageResponse


class GetAllAppsMessageRequestHandler:
    __rabbit_logger = None

    @classmethod
    def set_rabbit_logger(cls, logger: typing.Any):
        cls.__rabbit_logger = logger
        return cls

    @classmethod
    def handle(cls, message_body: typing.AnyStr) -> typing.NoReturn:
        # get apps
        try:
            #  load message
            body = json.loads(message_body)
            message_mapper = GetAllAppsMessageRequestMapping(target=GetAllAppsMessageRequest)
            message = message_mapper.load(body)

            # get permanent token
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
                message.business_owner_facebook_id)

            graph_api_apps_dtos, errors = GraphAPIAppsHandler.get_apps(permanent_token=permanent_token,
                                                                       account_id=message.ad_account_id,
                                                                       startup=startup)
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

            cls.__publish(response)
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
    def __publish(cls, response: GetAllAppsMessageResponse) -> typing.NoReturn:
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.INTEGRATION_EVENT,
                                    name=response.message_type,
                                    extra_data={"event_body": rabbitmq_client.serialize_message(response)})
            cls.__rabbit_logger.logger.info(log.to_dict())
        except Exception as e:
            raise e
