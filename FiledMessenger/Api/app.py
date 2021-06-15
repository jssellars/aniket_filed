# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

from flask_socketio import SocketIO

from FiledMessenger.Api import MessengerSocket
from FiledMessenger.Api.startup import config

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

import flask
import flask_cors
import flask_restful

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)
async_mode = None
MessengerSocket.socketio = SocketIO(app, async_mode=async_mode)
from FiledMessenger.Api import routers

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

if __name__ == "__main__":
    MessengerSocket.socketio.run(
        app=app,
        debug=config.logger_level == "DEBUG",
        host="localhost",
        port=config.port,
    )
