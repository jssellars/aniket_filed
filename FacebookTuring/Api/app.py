# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_restful import Api

from FacebookTuring.Api.Controllers import AdsManagerCatalogsController, AdsManagerInsightsController, \
    AdsManagerController
from FacebookTuring.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Api.Controllers.AdsManagerCatalogsReportsController import AdsManagerReportsEndpoint, \
    AdsManagerReportsDimensionsEndpoint, AdsManagerReportsMetricsEndpoint, AdsManagerReportsBreakdownsEndpoint

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ[
    "JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else startup.jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_DECODE_AUDIENCE"] = "Filed-Client-Apps"
app.url_map.strict_slashes = False

jwt = JWTManager(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

# Insights 
insights_controller = '{base_url}/insights'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerInsightsEndpoint, insights_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

ag_grid_insights_controller = '{base_url}/ag-grid-insights/<string:level>'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerAgGridInsightsEndpoint, ag_grid_insights_controller)

ads_manager_ag_grid_period_trend_controller = '{base_url}/ads-manager/ag-grid-insights-trend/<string:level>'.\
    format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerAgGridTrendEndpoint, ads_manager_ag_grid_period_trend_controller)

accounts_ag_grid_period_trend_controller = '{base_url}/accounts/ag-grid-insights-trend/<string:level>'.\
    format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AccountsAgGridTrendEndpoint, accounts_ag_grid_period_trend_controller)

insights_controller = '{base_url}/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerReportInsightsEndpoint, insights_controller)

views_controller = "{base_url}/views".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsEndpoint, views_controller)

views_by_level_controller = "{base_url}/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsByLevelEndpoint, views_by_level_controller)

ag_grid_views = "{base_url}/ag-grid-views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsAgGrid, ag_grid_views)

metacolumns_controller = "{base_url}/metacolumns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsMetacolumnsEndpoint, metacolumns_controller)

breakdowns_controller = "{base_url}/breakdowns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsBreakdownsEndpoint, breakdowns_controller)

breakdowns_combinations_controller = "{base_url}/breakdowns-combinations".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsBreakdownsCombinationsEndpoint,
                 breakdowns_combinations_controller)

# Structures
structures_controller = "{base_url}/campaigns/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetCampaignsEndpoint, structures_controller)

structures_controller = "{base_url}/adsets/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetAdSetsEndpoint, structures_controller)

structures_controller = "{base_url}/ads/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetAdsEndpoint, structures_controller)

filtered_structures_controller = "{base_url}/filtered-structures/<string:level>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerFilteredStructuresEndpoint, filtered_structures_controller)

# Campaign Tree
campaign_tree_structure_controller = "{base_url}/campaign-structure-tree/<string:level>/<string:facebook_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerCampaignTreeStructureEndpoint, campaign_tree_structure_controller)

# Structure details + updates
structure_details_controller = "{base_url}/<string:level>/<string:facebook_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerEndpoint, structure_details_controller)

# Duplicate
duplicate_structure_controller = "{base_url}/<string:level>/<string:facebook_id>/duplicate".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerDuplicateStructureEndpoint, duplicate_structure_controller)

# Drafts
update_draft_controller = "{base_url}/<string:level>/<string:facebook_id>/draft".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerUpdateStructureDraftEndpoint, update_draft_controller)

# Report catalogs
reports_controller = "{base_url}/get-reports".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportsEndpoint, reports_controller)

dimensions_controller = "{base_url}/get-dimensions".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportsDimensionsEndpoint, dimensions_controller)

metrics_controller = "{base_url}/get-metrics".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportsMetricsEndpoint, metrics_controller)

reporting_breakdowns_controller = "{base_url}/get-breakdowns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportsBreakdownsEndpoint, reporting_breakdowns_controller)

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
