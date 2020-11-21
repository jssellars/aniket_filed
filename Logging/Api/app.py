# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from Logging.Api.Controllers.HealthcheckController import HealthCheckEndpoint, VersionEndpoint
from Logging.Api.Controllers.LoggingController import LoggingEndpoint
from Logging.Api.Startup import startup

app = Flask(__name__)

cors = CORS(app, resources={r"*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck 
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

# Logging controller
logging_endpoint = "{base_url}/log".format(base_url=startup.base_url.lower())
api.add_resource(LoggingEndpoint, logging_endpoint)

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
