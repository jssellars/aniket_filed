# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
else:
    sys.path.append("/Users/luchicla/Work/Filed/Source/Filed.Python/")
# ====== END OF CONFIG SECTION ====== #

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_restful import Api

from Potter.FacebookCampaignsBuilder.Api.Controllers.AudienceSizeController import AudienceSizeEndpoint
from Potter.FacebookCampaignsBuilder.Api.Controllers.HealthCheckController import HealthCheckEndpoint, VersionEndpoint
from Potter.FacebookCampaignsBuilder.Api.Controllers.PublishCampaignController import PublishCampaignEndpoint
from Potter.FacebookCampaignsBuilder.Api.Controllers.AdCreativeAssetsController import AdCreativeAssetsImagesEndpoint, \
    AdCreativeAssetsVideosEndpoint, AdCreativeAssetsPagePostsEndpoint
from Potter.FacebookCampaignsBuilder.Api.Controllers.AdPreviewController import AdPreviewEndpoint

from Potter.FacebookCampaignsBuilder.Api.Startup import startup

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ[
    "JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else startup.jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_DECODE_AUDIENCE"] = "Filed-Client-Apps"

jwt = JWTManager(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

# Version / Healthcheck
healthcheck_controller = "{base_url}/healthcheck".format(base_url=startup.base_url.lower())
api.add_resource(HealthCheckEndpoint, healthcheck_controller)

version_controller = "{base_url}/version".format(base_url=startup.base_url.lower())
api.add_resource(VersionEndpoint, version_controller)

#  Publish campaign controller
publish_campaign_controller = "{base_url}/campaign".format(base_url=startup.base_url.lower())
api.add_resource(PublishCampaignEndpoint, publish_campaign_controller)

#  Audience size controller
audience_size_controller = "{base_url}/audience-size/<string:account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AudienceSizeEndpoint, audience_size_controller)

#  Ad creative assets controller
ad_creative_assets_images_endpoint = "{base_url}/assets/<string:business_owner_facebook_id>/" \
                                     "ad-images/<string:ad_account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdCreativeAssetsImagesEndpoint, ad_creative_assets_images_endpoint)

ad_creative_assets_videos_endpoint = "{base_url}/assets/<string:business_owner_facebook_id>/" \
                                     "ad-videos/<string:ad_account_id>".format(base_url=startup.base_url.lower())
api.add_resource(AdCreativeAssetsVideosEndpoint, ad_creative_assets_videos_endpoint)

ad_creative_assets_page_posts_endpoint = "{base_url}/assets/<string:business_owner_facebook_id>/" \
                                         "page-posts/<string:page_facebook_id>".format(
    base_url=startup.base_url.lower())
api.add_resource(AdCreativeAssetsPagePostsEndpoint, ad_creative_assets_page_posts_endpoint)

# Generate preview controller
ad_preview_endpoint = "{base_url}/advert-preview".format(base_url=startup.base_url.lower())
api.add_resource(AdPreviewEndpoint, ad_preview_endpoint)

# Targeting search controller

if __name__ == "__main__":
    app.run(debug=startup.debug_mode, host="localhost", port=startup.port)
