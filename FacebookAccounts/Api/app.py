# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #

# WARNING: this must be imported first
from FacebookAccounts.Api.startup import config, fixtures

import flask
import flask_cors
import flask_restful

from FacebookAccounts.Api.Controllers.AdAccountController import (
    AdAccountInsightsEndpoint,
    AdAccountPagesEndpoint,
    AdAccountInstagramEndpoint,
    AdAccountPageInstagramEndpoint,
    AdAccountsAgGridViewEndpoint,
    AdAccountAgGridInsights,
)
from FacebookAccounts.Api.Controllers.BusinessOwnerController import (
    BusinessOwnerEndpoint,
    BusinessOwnerDeletePermissionsEndpoint,
)
from FacebookAccounts.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint


app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)


router_route_pairs = (
    (HealthCheckEndpoint, "healthcheck"),
    (VersionEndpoint, "version"),
    (BusinessOwnerEndpoint, "business-owner"),
    (BusinessOwnerDeletePermissionsEndpoint, "business-owner/<string:permissions>"),
    # TODO: Once V1 is fully implemented and deployed,
    #  this can be deleted along with the related controllers and handlers
    (AdAccountInsightsEndpoint, "facebook-accounts-insights"),
    (AdAccountPagesEndpoint, "pages/<string:account_id>"),
    (AdAccountInstagramEndpoint, "instagram-accounts/<string:account_id>"),
    (AdAccountPageInstagramEndpoint, "instagram-business-account/<string:page_id>"),
    (AdAccountsAgGridViewEndpoint, "accounts-ag-grid-view"),
    (AdAccountAgGridInsights, "accounts-ag-grid-insights"),
)

for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")


if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
