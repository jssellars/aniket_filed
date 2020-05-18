# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python/")
# ====== END OF CONFIG SECTION ====== #

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_restful import Api

from Potter.FacebookPixels.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from Potter.FacebookPixels.Api.Startup import startup
from Potter.FacebookPixels.Api.Controllers.PixelsInsightsCatalogsController import \
    CustomConversionsInsightsCatalogsEndpoint, PixelsInsightsCatalogsEndpoint
from Potter.FacebookPixels.Api.Controllers.PixelsInsightsController import PixelsInsightsEndpoint

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
healthcheck_controller = "{base_url}/facebook-pixels/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/facebook-pixels/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

# Pixel insights catalogs controller
pixel_insights_catalogs_controller = "{base_url}/pixels/catalogs".format(base_url=startup.base_url.lower())
api.add_resource(PixelsInsightsCatalogsEndpoint, pixel_insights_catalogs_controller)

custom_conversions_insights_catalogs_controller = "{base_url}/customconversions/catalogs".format(
    base_url=startup.base_url.lower())
api.add_resource(CustomConversionsInsightsCatalogsEndpoint, custom_conversions_insights_catalogs_controller)

# Pixel insights controller
pixel_insights_controller = "{base_url}/<string:level>/insights".format(base_url=startup.base_url.lower())
api.add_resource(PixelsInsightsEndpoint, pixel_insights_controller)

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
