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
from GoogleTuring.Api.Startup import startup
from GoogleTuring.Api.Controllers.AdAccountInsightsController import AdAccountInsightsEndpoint
from GoogleTuring.Api.Controllers.AdsManagerCatalogsController import AdsManagerReportsEndpoint, \
    AdsManagerDimensionsEndpoint, \
    AdsManagerMetricsEndpoint, AdsManagerBreakdownsEndpoint
from GoogleTuring.Api.Controllers.AdsManagerController import AdsManagerEndpoint, AdsManagerGetStructuresEndpoint, \
    AdsManagerFilteredStructuresEndpoint, OptimizeGetStructuresEndpoint
from GoogleTuring.Api.Controllers.AdsManagerInsightsController import AdsManagerInsightsWithTotalsEndpoint, \
    AccountsReportInsightsEndpoint, OptimizeReportInsightsEndpoint, \
    AdsManagerReportInsightsEndpoint, ReportsReportInsightsEndpoint
from GoogleTuring.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint

app = Flask(__name__)
app.url_map.strict_slashes = False

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
insights_controller = '{base_url}/accounts/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AccountsReportInsightsEndpoint, insights_controller)

# Insights
insights_controller = '{base_url}/optimize/reports'.format(base_url=startup.base_url.lower())
api.add_resource(OptimizeReportInsightsEndpoint, insights_controller)

# Insights
insights_controller = '{base_url}/ads-manager/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportInsightsEndpoint, insights_controller)

# Insights
insights_controller = '{base_url}/reports/reports'.format(base_url=startup.base_url.lower())
api.add_resource(ReportsReportInsightsEndpoint, insights_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

# AdsManager Structures
structures_controller = "{base_url}/ads-manager/<string:level>s/<string:account_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerGetStructuresEndpoint, structures_controller)

# Optimize Structures
structures_controller = "{base_url}/optimize/<string:level>s/<string:account_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(OptimizeGetStructuresEndpoint, structures_controller)

filtered_structures_controller = "{base_url}/filtered-structures/<string:level>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerFilteredStructuresEndpoint, filtered_structures_controller)

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
    app.run(debug=startup.logger_level == "DEBUG", host="localhost", port=startup.port)
