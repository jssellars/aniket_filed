import logging

import flask_restful
from flask import request

from Core.flask_extensions import log_request
from FiledMessenger.Api.request_handlers import MessageHandler, ConversationHandler
from FiledMessenger.Api.startup import config

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class Message(Resource):
    def post(self):
        sender = request.args.get("sender")
        recipient = request.args.get("recipient")
        message = request.args.get("message")
        response = MessageHandler.add_message(sender, recipient, message)
        return response, 201

    def get(self):
        sender = request.args.get("sender")
        recipient = request.args.get("recipient")

        response = MessageHandler.get_message(sender, recipient)
        return response, 200


class Conversation(Resource):
    def get(self):
        sender = request.args.get("sender")
        recipient = request.args.get("recipient")

        response = ConversationHandler.get_conversation(sender, recipient)
        return response, 200
