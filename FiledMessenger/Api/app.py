# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

import flask
import flask_cors
import flask_restful
import flask_socketio

from Core.logging_config import request_as_log_dict
from FiledMessenger.Api import routers
from FiledMessenger.Api.startup import config

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)
async_mode = None

socketio = flask_socketio.SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.Message, "message"),
    (routers.Conversation, "conversation"),
    (routers.ConversationID, "conversation-id"),
    (routers.Chat, "chat"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

namespace_chat = f"{config.base_url.lower()}/chat"
socketio.on_namespace(routers.SocketChat(namespace_chat))


# Unfortunately, namespace based error handling is not available, yet :)
@socketio.on_error(namespace=namespace_chat)
def chat_error_handler(e):
    routers.logger.exception(repr(e), extra=request_as_log_dict(flask.request))


if __name__ == "__main__":
    socketio.run(
        app=app,
        debug=config.logger_level == "DEBUG",
        host="localhost",
        port=config.port,
    )
