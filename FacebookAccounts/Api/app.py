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

from FacebookAccounts.Api.Controllers.AdAccountController import AdAccountInsightsEndpoint, \
    AdAccountPagesEndpoint, AdAccountInstagramEndpoint, AdAccountPageInstagramEndpoint, AdAccountsAgGridViewEndpoint, AdAccountAgGridInsights
from FacebookAccounts.Api.Controllers.BusinessOwnerController import BusinessOwnerEndpoint, \
    BusinessOwnerDeletePermissionsEndpoint
from FacebookAccounts.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from FacebookAccounts.Api.Startup import startup

app = Flask(__name__)
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck 
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

# Business owner controller
business_owner_controller = "{base_url}/business-owner".format(base_url=startup.base_url.lower())
api.add_resource(BusinessOwnerEndpoint, business_owner_controller)

business_owner_delete_permissions_controller = "{base_url}/business-owner/<string:permissions>".format(
    base_url=startup.base_url.lower())
api.add_resource(BusinessOwnerDeletePermissionsEndpoint, business_owner_delete_permissions_controller)

# Insights controller
# TODO: Once V1 is fully implemented and deployed, this can be deleted along with the related controllers and handlers
ad_account_insights_controller = "{base_url}/facebook-accounts-insights".format(base_url=startup.base_url.lower())
api.add_resource(AdAccountInsightsEndpoint, ad_account_insights_controller)

# Pages controller
ad_account_pages_controller = "{base_url}/pages/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdAccountPagesEndpoint, ad_account_pages_controller)

# Instagram accounts controller
ad_account_instagram_controller = "{base_url}/instagram-accounts/<string:account_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdAccountInstagramEndpoint, ad_account_instagram_controller)

# Instagram business account controller
ad_account_page_instagram_controller = "{base_url}/instagram-business-account/<string:page_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdAccountPageInstagramEndpoint, ad_account_page_instagram_controller)

# Accounts tab view for AgGrid
ag_grid_view = "{base_url}/accounts-ag-grid-view/".format(base_url=startup.base_url.lower())
api.add_resource(AdAccountsAgGridViewEndpoint, ag_grid_view)

# Accounts insights for V1
ag_grid_insights = "{base_url}/accounts-ag-grid-insights/".format(base_url=startup.base_url.lower())
api.add_resource(AdAccountAgGridInsights, ag_grid_insights)


if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
