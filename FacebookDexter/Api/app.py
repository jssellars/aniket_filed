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

from FacebookDexter.Api.Controllers.HealthCheckController import HealthCheck, Version
from FacebookDexter.Api.Controllers.RecommendationsController import (
    GetRecommendationsPage,
    GetCountsByCategory,
    DismissRecommendation,
    ApplyRecommendation
)
from FacebookDexter.Api.Queries.DexterApiGetActionHistoryQuery import GetActionHistoryQuery
from FacebookDexter.Api.Queries.DexterApiGetCampaignsQuery import GetCampaignsQuery
from FacebookDexter.Api.Queries.DexterApiGetRecommendationQuery import GetRecommendationQuery
from FacebookDexter.Api.startup import config, fixtures

app = Flask(__name__)
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.url_map.strict_slashes = False


router_route_pairs = (
    (GetRecommendationsPage, 'GetRecommendationsPage'),
    (GetCampaignsQuery, 'GetCampaigns'),
    (GetActionHistoryQuery, 'GetActionHistory'),
    (GetRecommendationQuery, 'GetRecommendation'),
    (GetCountsByCategory, 'GetCountByCategory'),
    (DismissRecommendation, 'DismissRecommendation'),
    (ApplyRecommendation, 'ApplyRecommendation'),
    (HealthCheck, 'healthcheck'),
    (Version, 'version'),
)

for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")


if __name__ == '__main__':
    app.run(debug=config.logger_level == "DEBUG", host='localhost', port=config.port)
