import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from flask_restful import Api

from FacebookDexter.Api.Controllers.HealthCheckController import DexterApiHealthCheck, DexterApiVersion
from FacebookDexter.Api.Controllers.RecommendationsController import (DexterApiGetRecommendationsPage,
                                                                      DexterApiGetCountsByCategory,
                                                                      DexterApiDismissRecommendation,
                                                                      DexterApiApplyRecommendation)
from FacebookDexter.Api.Queries.DexterApiGetActionHistoryQuery import DexterApiGetActionHistoryQuery
from FacebookDexter.Api.Queries.DexterApiGetCampaignsQuery import DexterApiGetCampaignsQuery
from FacebookDexter.Api.Queries.DexterApiGetRecommendationQuery import DexterApiGetRecommendationQuery
from FacebookDexter.Api.Startup import startup

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ[
    "JWT_SECRET_KEY"] if "JWT_SECRET_KEY" in os.environ.keys() else startup.jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_DECODE_AUDIENCE"] = "Filed-Client-Apps"
app.url_map.strict_slashes = False

jwt = JWTManager(app)

CORS(app)
api = Api(app)
app.url_map.strict_slashes = False

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

base_url = startup.base_url

api.add_resource(DexterApiGetRecommendationsPage, f'{base_url}/GetRecommendationsPage')
api.add_resource(DexterApiGetCampaignsQuery, f'{base_url}/GetCampaigns')
api.add_resource(DexterApiGetActionHistoryQuery, f'{base_url}/GetActionHistory')
api.add_resource(DexterApiGetRecommendationQuery, f'{base_url}/GetRecommendation')
api.add_resource(DexterApiGetCountsByCategory, f'{base_url}/GetCountByCategory')
api.add_resource(DexterApiDismissRecommendation, f'{base_url}/DismissRecommendation')
api.add_resource(DexterApiApplyRecommendation, f'{base_url}/ApplyRecommendation')
api.add_resource(DexterApiHealthCheck, f'{base_url}/HealthCheck')
api.add_resource(DexterApiVersion, f'{base_url}/Version')

if __name__ == '__main__':
    app.run(debug=startup.debug,
            host='localhost',
            port=startup.port)

