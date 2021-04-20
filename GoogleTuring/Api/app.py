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

from GoogleTuring.Api import routers
from GoogleTuring.Api.startup import config

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.AdsManagerReports, "get-reports"),
    (routers.AdsManagerDimensions, "get-dimensions"),
    (routers.AdsManagerMetrics, "get-metrics"),
    (routers.AdsManagerBreakdowns, "get-breakdowns"),
    (routers.AdAccountInsights, "google-accounts-insights"),
    (routers.AccountsReportInsights, "accounts/reports"),
    (routers.OptimizeReportInsights, "optimize/reports"),
    (routers.AdsManagerReportInsights, "ads-manager/reports"),
    (routers.ReportsReportInsights, "reports/reports"),
    (routers.AdsManagerInsightsWithTotals, "insights-with-totals"),
    (routers.AdsManagerGetStructures, "ads-manager/<string:level>s/<string:account_id>"),
    (routers.OptimizeGetStructures, "optimize/<string:level>s/<string:account_id>"),
    (routers.AdsManagerFilteredStructures, "filtered-structures/<string:level>"),
    (routers.AdsManager, "<int:account_id>/<string:level>/<int:structure_id>"),
    (routers.AdsManagerAgGridStructuresPerformance, "ag-grid-structures-performance/<string:level>"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
