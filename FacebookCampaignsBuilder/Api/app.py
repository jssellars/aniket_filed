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

from FacebookCampaignsBuilder.Api import routers
from FacebookCampaignsBuilder.Api.Startup import startup

app = Flask(__name__)
app.config.update(
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", startup.jwt_secret_key),
    JWT_TOKEN_LOCATION="headers",
    JWT_HEADER_NAME="Authorization",
    JWT_HEADER_TYPE="Bearer",
    JWT_DECODE_AUDIENCE="Filed-Client-Apps",
)
app.url_map.strict_slashes = False
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

base_url = startup.base_url.lower()
router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
    (routers.PublishCampaign, "campaign"),
    (routers.AudienceSize, "audience-size/<string:account_id>"),
    (routers.AdCreativeAssetsImages, "assets/<string:business_owner_facebook_id>/ad-images/<string:ad_account_id>"),
    (routers.AdCreativeAssetsVideos, "assets/<string:business_owner_facebook_id>/ad-videos/<string:ad_account_id>"),
    (
        routers.AdCreativeAssetsPagePosts,
        "assets/<string:business_owner_facebook_id>/page-posts/<string:page_facebook_id>",
    ),
    (routers.AdPreview, "advert-preview"),
    (routers.TargetingSearchInterestsTree, "targeting-search/interests/tree"),
    (routers.TargetingSearchRegulatedInterests, "targeting-search/regulated-interests/categories=<string:categories>"),
    (routers.TargetingSearchInterestsSearch, "targeting-search/interests/search/<string:query_string>"),
    (routers.TargetingSearchInterestsSuggestions, "targeting-search/interests/suggestions/<string:query_string>"),
    (routers.TargetingSearchLocations, "targeting-search/locations/country-groups"),
    (routers.TargetingSearchLocationSearch, "targeting-search/locations/search/<string:query_string>"),
    (routers.TargetingSearchLanguages, "targeting-search/languages"),
    (routers.BudgetValidation, "budget-validation/<string:business_owner_id>/<string:account_id>"),
    (routers.SmartCreateCats, "smart-create/cats"),
    (routers.SmartCreateCatalogs, "smart-create/catalogs"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{base_url}/{route}")


if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
