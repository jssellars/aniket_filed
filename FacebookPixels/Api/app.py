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

from FacebookPixels.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from FacebookPixels.Api.startup import config, fixtures
from FacebookPixels.Api.Controllers.PixelsInsightsCatalogsController import \
    CustomConversionsInsightsCatalogsEndpoint, PixelsInsightsCatalogsEndpoint
from FacebookPixels.Api.Controllers.PixelsInsightsController import PixelsInsightsEndpoint

app = Flask(__name__)
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck
healthcheck_controller = "{base_url}/healthcheck".format(base_url=config.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=config.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

# Pixel insights catalogs controller
pixel_insights_catalogs_controller = "{base_url}/pixels/catalogs".format(base_url=config.base_url.lower())
api.add_resource(PixelsInsightsCatalogsEndpoint, pixel_insights_catalogs_controller)

custom_conversions_insights_catalogs_controller = "{base_url}/customconversions/catalogs".format(
    base_url=config.base_url.lower())
api.add_resource(CustomConversionsInsightsCatalogsEndpoint, custom_conversions_insights_catalogs_controller)

# Pixel insights controller
pixel_insights_controller = "{base_url}/<string:level>/insights".format(base_url=config.base_url.lower())
api.add_resource(PixelsInsightsEndpoint, pixel_insights_controller)

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
