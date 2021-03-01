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

from FacebookTuring.Api import routers
from FacebookTuring.Api.startup import config

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.AccountsReportInsights, "accounts/reports"),
    (routers.OptimizeReportInsights, "optimize/reports"),
    (routers.AdsManagerAgGridTrend, "ads-manager/ag-grid-insights-trend/<string:level>"),
    (routers.AccountsAgGridTrend, "accounts/ag-grid-insights-trend/<string:level>"),
    (routers.AdsManagerReportInsights, "ads-manager/reports"),
    (routers.ReportsReportInsights, "reports/reports"),
    (routers.AdsManagerAgGridInsights, "ag-grid-insights/<string:level>"),
    (routers.AdsManagerCatalogsViews, "views"),
    (routers.AdsManagerCatalogsViewsByLevel, "views/<string:level>"),
    (routers.AdsManagerCatalogsViewsAgGrid, "ag-grid-views/<string:level>"),
    (routers.AccountsElementsViews, "accounts/elements-cards-views"),
    (routers.AdsManagerElementsViews, "ads-manager/elements-cards-views"),
    (routers.AdsManagerCatalogsMetacolumns, "metacolumns"),
    (routers.AdsManagerCatalogsBreakdowns, "breakdowns"),
    (routers.AdsManagerCatalogsBreakdownsCombinations, "breakdowns-combinations"),
    (routers.AdsManagerGetStructures, "ads-manager/<string:level>s/<string:account_id>"),
    (routers.OptimizeGetStructures, "optimize/<string:level>s/<string:account_id>"),
    (routers.AdsManagerFilteredStructures, "filtered-structures/<string:level>"),
    (routers.AdsManagerCampaignTreeStructure, "campaign-structure-tree/<string:level>/<string:facebook_id>"),
    (
        routers.SmartEditCampaignTreesStructure,
        "campaign-trees-structure/<string:account_id>/<string:level>/<string:structure_ids>",
    ),
    (routers.AdsManager, "<string:level>/<string:facebook_id>"),
    (routers.AdsManagerDuplicateStructure, "<string:level>/<string:facebook_id>/duplicate"),
    (routers.AdsManagerReports, "get-reports"),
    (routers.AdsManagerReportsDimensions, "get-dimensions"),
    (routers.AdsManagerReportsMetrics, "get-metrics"),
    (routers.AdsManagerReportsBreakdowns, "get-breakdowns"),
    (routers.AdsManagerAgGridStructuresPerformance, "ag-grid-structures-performance/<string:level>"),
    (routers.AdsManagerAgGridStructuresPerformanceViews, "ag-grid-structures-performance-views/<string:level>"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
