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
from FacebookTuring.Api.Controllers.AdsManagerInsightsController import AdsManagerInsightsWithTotalsEndpoint, \
    AdsManagerReportInsightsEndpoint, AccountsReportInsightsEndpoint, OptimizeReportInsightsEndpoint, \
    ReportsReportInsightsEndpoint, AdsManagerAgGridInsightsEndpoint, AdsManagerAgGridTrendEndpoint, \
    AccountsAgGridTrendEndpoint
from FacebookTuring.Api.Controllers.AdsManagerController import AdsManagerGetStructuresEndpoint, \
    AdsManagerFilteredStructuresEndpoint, AdsManagerCampaignTreeStructureEndpoint, \
    AdsManagerEndpoint, \
    AdsManagerDuplicateStructureEndpoint, AdsManagerUpdateStructureDraftEndpoint, OptimizeGetStructuresEndpoint
from FacebookTuring.Api.Controllers.AdsManagerCatalogsController import AdsManagerCatalogsViewsEndpoint, \
    AdsManagerCatalogsViewsByLevelEndpoint, AdsManagerCatalogsMetacolumnsEndpoint, \
    AdsManagerCatalogsBreakdownsEndpoint, \
    AdsManagerCatalogsBreakdownsCombinationsEndpoint, AdsManagerCatalogsViewsAgGrid, AccountsElementsViews, \
    AdsManagerElementsViews

from FacebookTuring.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Api.Controllers.AdsManagerCatalogsReportsController import AdsManagerReportsEndpoint, \
    AdsManagerReportsDimensionsEndpoint, AdsManagerReportsMetricsEndpoint, AdsManagerReportsBreakdownsEndpoint

app = Flask(__name__)
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

# Accounts Insights
insights_controller = '{base_url}/accounts/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AccountsReportInsightsEndpoint, insights_controller)

# Optimize Insights
insights_controller = '{base_url}/optimize/reports'.format(base_url=startup.base_url.lower())
api.add_resource(OptimizeReportInsightsEndpoint, insights_controller)

ads_manager_ag_grid_period_trend_controller = '{base_url}/ads-manager/ag-grid-insights-trend/<string:level>'.\
    format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerAgGridTrendEndpoint, ads_manager_ag_grid_period_trend_controller)

accounts_ag_grid_period_trend_controller = '{base_url}/accounts/ag-grid-insights-trend/<string:level>'.\
    format(base_url=startup.base_url.lower())
api.add_resource(AccountsAgGridTrendEndpoint, accounts_ag_grid_period_trend_controller)

# AdsManager Insights
insights_controller = '{base_url}/ads-manager/reports'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerReportInsightsEndpoint, insights_controller)

# Reports Insights
insights_controller = '{base_url}/reports/reports'.format(base_url=startup.base_url.lower())
api.add_resource(ReportsReportInsightsEndpoint, insights_controller)
ag_grid_insights_controller = '{base_url}/ag-grid-insights/<string:level>'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerAgGridInsightsEndpoint, ag_grid_insights_controller)

views_controller = "{base_url}/views".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsViewsEndpoint, views_controller)

views_by_level_controller = "{base_url}/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsViewsByLevelEndpoint, views_by_level_controller)

ag_grid_views = "{base_url}/ag-grid-views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsViewsAgGrid, ag_grid_views)

accounts_element_cards_views = "{base_url}/accounts/elements-cards-views".format(base_url=startup.base_url.lower())
api.add_resource(AccountsElementsViews, accounts_element_cards_views)

ads_manager_element_cards_views = "{base_url}/ads-manager/elements-cards-views".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerElementsViews, ads_manager_element_cards_views)

metacolumns_controller = "{base_url}/metacolumns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsMetacolumnsEndpoint, metacolumns_controller)

breakdowns_controller = "{base_url}/breakdowns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsBreakdownsEndpoint, breakdowns_controller)

breakdowns_combinations_controller = "{base_url}/breakdowns-combinations".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsBreakdownsCombinationsEndpoint,
                 breakdowns_combinations_controller)

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

# Campaign Tree
campaign_tree_structure_controller = "{base_url}/campaign-structure-tree/<string:level>/<string:facebook_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerCampaignTreeStructureEndpoint, campaign_tree_structure_controller)

# Structure details + updates
structure_details_controller = "{base_url}/<string:level>/<string:facebook_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerEndpoint, structure_details_controller)

# Duplicate
duplicate_structure_controller = "{base_url}/<string:level>/<string:facebook_id>/duplicate".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerDuplicateStructureEndpoint, duplicate_structure_controller)

# Drafts
update_draft_controller = "{base_url}/<string:level>/<string:facebook_id>/draft".format(
    base_url=startup.base_url.lower())
api.add_resource(AdsManagerUpdateStructureDraftEndpoint, update_draft_controller)

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
