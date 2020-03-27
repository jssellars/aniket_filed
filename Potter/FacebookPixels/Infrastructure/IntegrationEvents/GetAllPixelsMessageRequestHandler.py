import typing

from Core.Tools.RabbitMQ.RabbitMqClient import RabbitMqClient
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookPixels.BackgroundTasks.Startup import startup
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsHandler import GraphAPIPixelHandler
from Potter.FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageRequest import GetAllPixelsMessageRequest
from Potter.FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageRequestMapping import GetAllPixelsMessageRequestMapping
from Potter.FacebookPixels.Infrastructure.IntegrationEvents.GetAllPixelsMessageResponse import GetAllPixelsMessageResponse


class GetAllPixelsMessageRequestHandler:

    @classmethod
    def handle(cls, message_body: typing.Dict) -> typing.NoReturn:
        #  load message
        message_mapper = GetAllPixelsMessageRequestMapping(target=GetAllPixelsMessageRequest)
        message = message_mapper.load(message_body)

        #  get permanent token
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(message.business_owner_facebook_id)

        pixels, errors = GraphAPIPixelHandler.get_pixels(permanent_token=permanent_token, account_id=message.ad_account_id, startup=startup)

        #  Publish pixel details to pixels outbound queue
        # todo: use below after c# changes ErrorMessage
        # response = GetAllPixelsMessageResponse(ad_account_id=message.ad_account_id, pixels=pixels, errors=errors)
        response = GetAllPixelsMessageResponse(business_owner_facebook_id=message.business_owner_facebook_id,
                                               ad_account_id=message.ad_account_id,
                                               pixels=pixels,
                                               errors=[])
        cls.__publish(response)

    @classmethod
    def __publish(cls, pixels):
        try:
            rabbitmq_client = RabbitMqClient(startup.rabbitmq_config,
                                             startup.exchange_details.name,
                                             startup.exchange_details.outbound_queue.key)
            rabbitmq_client.publish(pixels)
        except Exception as e:
            raise e