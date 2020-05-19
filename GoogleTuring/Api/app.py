# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

from GoogleTuring.Api.Controllers.AdsManagerCatalogsController import AdsManagerCatalogsMetaColumnsEndpoint, \
    AdsManagerCatalogsViewsByLevelEndpoint
from GoogleTuring.Api.Controllers.AdsManagerController import AdsManagerEndpoint
from GoogleTuring.Api.Controllers.AdsManagerInsightsController import AdsManagerInsightsEndpoint, \
    AdsManagerInsightsWithTotalsEndpoint
from GoogleTuring.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append(r"D:\Filed\Python-Google Turing\Filed.Python")
# ====== END OF CONFIG SECTION ====== #

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_simple import JWTManager
from GoogleTuring.Api.Startup import startup

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ[
    "JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else startup.jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_DECODE_AUDIENCE"] = "Filed-Client-Apps"

jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck
healthcheck_controller = "{base_url}/turing/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/turing/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

views_controller = "{base_url}/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsMetaColumnsEndpoint, views_controller)

views_by_level_controller = "{base_url}/views/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsViewsByLevelEndpoint, views_by_level_controller)

# Insights
insights_controller = '{base_url}/insights'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsEndpoint, insights_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

# Structure updates
structure_details_controller = "{base_url}/<int:account_id>/<string:level>/<int:structure_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerEndpoint, structure_details_controller)

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
