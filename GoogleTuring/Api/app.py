from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from GoogleTuring.Api.Controllers import AdsManagerCatalogsController
from GoogleTuring.Api.Startup import startup

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)
views_controller = "{base_url}/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsMetaColumnsEndpoint, views_controller)

views_by_level_controller = "{base_url}/views/views/<string:level>".format(base_url=startup.base_url.lower())
api.add_resource(AdsManagerCatalogsController.AdsManagerCatalogsViewsByLevelEndpoint, views_by_level_controller)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="41000")
