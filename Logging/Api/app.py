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

from Logging.Api.startup import config
from Logging.Api import routers

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.Logging, "log"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
