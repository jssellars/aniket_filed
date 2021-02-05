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

from FacebookCampaignsBuilder.Api import routers
from FacebookCampaignsBuilder.Api.startup import config

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

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
    (routers.SmartCreatePublish, "smart-create/publish"),
    (routers.SmartCreateAccountAdvertisableApps, "smart-create/account-advertisable-apps/<string:account_id>"),
    (routers.AdsManagerAccountAdvertisableApps, "ads-manager/account-advertisable-apps/<string:account_id>"),
    (routers.AdsManagerAddStructuresToParent, "add-structures-to-parent/<string:level>"),
    (routers.SmartCreatePublishProgress, "smart-create/publish-progress/<string:template_id>"),
)
for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port)
