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

from FacebookAccounts.Api.startup import config
from FacebookAccounts.Api import routers

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.BusinessOwner, "business-owner"),
    (routers.BusinessOwnerDeletePermissions, "business-owner/<string:permissions>"),
    # TODO: Once V1 is fully implemented and deployed,
    #  this can be deleted along with the related controllers and handlers
    (routers.AdAccountPages, "pages/<string:account_id>"),
    (routers.AdAccountPageInstagram, "page-instagram-account/<string:page_id>"),
    (routers.AdAccountsAgGridView, "accounts-ag-grid-view"),
    (routers.AdAccountAgGridInsights, "accounts-ag-grid-insights"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
