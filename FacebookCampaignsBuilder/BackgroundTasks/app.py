# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import atexit
import logging

import flask
import flask_cors
import flask_restful
from apscheduler.schedulers.background import BackgroundScheduler

from FacebookCampaignsBuilder.BackgroundTasks import routers
from FacebookCampaignsBuilder.BackgroundTasks.request_handlers import HandlersEnum
from FacebookCampaignsBuilder.BackgroundTasks.startup import config, fixtures
from FacebookCampaignsBuilder.BackgroundTasks.sync_job import clean_publish_feedback
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.events import RequestTypeEnum

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info(getattr(properties, "type", ""), extra={"rabbitmq": body})
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        request_handler.handle(body)
    except Exception as e:
        logger.exception(repr(e), extra={"message_type": getattr(properties, "type", None), "event_body": body})


app = flask.Flask(__name__)
app.url_map.strict_slashes = False
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
api = flask_restful.Api(app)

router_route_pairs = (
    (routers.HealthCheck, "healthcheck"),
    (routers.Version, "version"),
)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    fixtures.rabbitmq_adapter.register_callback(callback)
    .register_consumer(config.rabbitmq.consumer_name)
    .start_consuming
)

hour, minute = config.sync_time.split(":")
scheduler.add_job(clean_publish_feedback, "cron", hour=hour, minute=minute)

atexit.register(lambda: scheduler.shutdown())

for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")

if __name__ == "__main__":
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port, use_reloader=False)
