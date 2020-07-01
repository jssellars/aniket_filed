# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

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
from GoogleTuring.Api.Controllers.AdAccountInsightsController import AdAccountInsightsEndpoint
from GoogleTuring.Api.Controllers.AdsManagerCatalogsController import AdsManagerReportsEndpoint, \
    AdsManagerDimensionsEndpoint, \
    AdsManagerMetricsEndpoint, AdsManagerBreakdownsEndpoint
from GoogleTuring.Api.Controllers.AdsManagerController import AdsManagerEndpoint, AdsManagerGetAdsEndpoint, \
    AdsManagerGetAdGroupsEndpoint, \
    AdsManagerGetCampaignsEndpoint, AdsManagerGetKeywordsEndpoint
from GoogleTuring.Api.Controllers.AdsManagerInsightsController import AdsManagerReportInsightsEndpoint, \
    AdsManagerInsightsWithTotalsEndpoint
from GoogleTuring.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint

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
reports_controller = "{base_url}/get-reports".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportsEndpoint, reports_controller)

dimensions_controller = "{base_url}/get-dimensions".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerDimensionsEndpoint, dimensions_controller)

metrics_controller = "{base_url}/get-metrics".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerMetricsEndpoint, metrics_controller)

breakdowns_controller = "{base_url}/get-breakdowns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerBreakdownsEndpoint, breakdowns_controller)

ad_account_insights_controller = "{base_url}/google-accounts-insights".format(base_url=startup.base_url.lower())
api.add_resource(AdAccountInsightsEndpoint, ad_account_insights_controller)

# Insights
insights_controller = '{base_url}/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportInsightsEndpoint, insights_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

# Structures
structures_controller = "{base_url}/campaigns/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerGetCampaignsEndpoint, structures_controller)

structures_controller = "{base_url}/adgroups/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerGetAdGroupsEndpoint, structures_controller)

structures_controller = "{base_url}/ads/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerGetAdsEndpoint, structures_controller)

structures_controller = "{base_url}/keywords/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerGetKeywordsEndpoint, structures_controller)

# Structure updates
structure_details_controller = "{base_url}/<int:account_id>/<string:level>/<int:structure_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerEndpoint, structure_details_controller)

# Version / Healthcheck
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
