import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_restful import Api

from Turing.Api.Controllers import AdsManagerCatalogsController, AdsManagerInsightsController, AdsManagerController
from Turing.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from Turing.Api.Startup import startup

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else startup.jwt_secret_key
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

# Insights 
insights_controller = '{base_url}/insights'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerInsightsEndpoint, insights_controller)

insights_with_totals_controller = '{base_url}/insights-with-totals'.format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerInsightsController.AdsManagerInsightsWithTotalsEndpoint, insights_with_totals_controller)

views_controller = "{base_url}/views".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsEndpoint, views_controller)

views_by_level_controller = "{base_url}/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsByLevelEndpoint, views_by_level_controller)

metacolumns_controller = "{base_url}/metacolumns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsMetacolumnsEndpoint, metacolumns_controller)

breakdowns_controller = "{base_url}/breakdowns".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsBreakdownsEndpoint, breakdowns_controller)

breakdowns_combinations_controller = "{base_url}/breakdowns-combinations".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsBreakdownsCombinationsEndpoint, breakdowns_combinations_controller)

# Structures
structures_controller = "{base_url}/campaigns/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetCampaignsEndpoint, structures_controller)

structures_controller = "{base_url}/adsets/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetAdSetsEndpoint, structures_controller)

structures_controller = "{base_url}/ads/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerGetAdsEndpoint, structures_controller)

# Campaign Tree
campaign_tree_structure_controller = "{base_url}/campaign-structure-tree/<string:level>/<string:facebook_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerCampaignTreeStructureEndpoint, campaign_tree_structure_controller)

# Structure details + updates
structure_details_controller = "{base_url}/<string:level>/<string:facebook_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerEndpoint, structure_details_controller)

# Duplicate
duplicate_structure_controller = "{base_url}/<string:level>/<string:facebook_id>/duplicate".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerDuplicateStructureEndpoint, duplicate_structure_controller)

# Drafts
update_draft_controller = "{base_url}/<string:level>/<string:facebook_id>/draft".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerController.AdsManagerUpdateStructureDraftEndpoint, update_draft_controller)


if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
