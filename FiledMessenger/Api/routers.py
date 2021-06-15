import logging

import flask_restful
from flask import (
    request,
    render_template,
    session,
    copy_current_request_context,
    make_response,
)
from flask_socketio import emit, disconnect

from Core.flask_extensions import log_request
from FiledMessenger.Api import MessengerSocket
from FiledMessenger.Api.request_handlers import (
    MessageHandler,
    ConversationHandler,
    ConversationIDHandler,
)
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


class ConversationID(Resource):
    def get(self):
        sender = request.args.get("sender")
        recipient = request.args.get("recipient")

        response = ConversationIDHandler.get_conversation_id(sender, recipient)
        return response, 200

    def post(self):
        sender = request.args.get("sender")
        recipient = request.args.get("recipient")

        response = ConversationIDHandler.add_conversation_id(sender, recipient)
        return response, 201


socketio = MessengerSocket.socketio


class Chat(Resource):
    """
    Return HTML for testing in web browser

    Code referred from
    https://medium.com/swlh/implement-a-websocket-using-flask-and-socket-io-python-76afa5bbeae1
    https://stackoverflow.com/questions/19315567/returning-rendered-template-with-flask-restful-shows-html-in-browser/19316089#19316089
    """

    def get(self):
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template(
                "index.html",
                async_mode=socketio.async_mode,
            ),
            200,
            headers,
        )


@socketio.on("my_event", namespace="/test")
def test_message(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit("my_response", {"data": message["data"], "count": session["receive_count"]})


@socketio.on("my_broadcast_event", namespace="/test")
def test_broadcast_message(message):
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        broadcast=True,
    )


@socketio.on("disconnect_request", namespace="/test")
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "Disconnected!", "count": session["receive_count"]},
        callback=can_disconnect,
    )
