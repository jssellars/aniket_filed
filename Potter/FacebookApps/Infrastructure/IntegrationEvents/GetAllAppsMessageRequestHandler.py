import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookApps.BackgroundTasks.Startup import startup
from Potter.FacebookApps.Infrastructure.GraphAPIHandlers.GraphAPIAppsHandler import GraphAPIAppsHandler
from Potter.FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequest import GetAllAppsMessageRequest
from Potter.FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageRequestMapping import \
    GetAllAppsMessageRequestMapping
from Potter.FacebookApps.Infrastructure.IntegrationEvents.GetAllAppsMessageResponse import GetAllAppsMessageResponse


class GetAllAppsMessageRequestHandler:

    @classmethod
    def handle(cls, message_body: typing.MutableMapping) -> typing.NoReturn:
        #  load message
        message_mapper = GetAllAppsMessageRequestMapping(target=GetAllAppsMessageRequest)
        message = message_mapper.load(message_body)

        # get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(
            message.business_owner_facebook_id)

        # get audiences
        apps, errors = GraphAPIAppsHandler.get_apps(permanent_token=permanent_token, account_id=message.ad_account_id,
                                                    startup=startup)

        #  Publish response details to audiences outbound queue
        # todo: use below after c# changes ErrorMessage
        # replace errors=[] with errors returned by get_apps()
        response = GetAllAppsMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                             ad_account_id=message.ad_account_id,
                                             apps=apps,
                                             errors=[])

        cls.__publish(response)

    @classmethod
    def __publish(cls, response: GetAllAppsMessageResponse) -> typing.NoReturn:
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(response)
        except Exception as e:
            raise e
