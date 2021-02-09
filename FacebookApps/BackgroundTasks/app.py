# ====== CONFIGURE PATH TO SOLUTION - DO NOT DELETE ====== #
import os
import sys

path = os.environ.get("PYTHON_SOLUTION_PATH")
if path:
    sys.path.append(path)
# ====== END OF CONFIG SECTION ====== #
import atexit
import flask
import flask_cors
import flask_restful
import logging

from FacebookApps.BackgroundTasks.startup import config, fixtures
from FacebookApps.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from FacebookApps.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from FacebookApps.BackgroundTasks import routers
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info(getattr(properties, "type", ""), extra={"rabbitmq": body})
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
        request_handler.handle(body, config, fixtures)
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
    fixtures.rabbitmq_adapter
    .register_callback(callback)
    .register_consumer(config.rabbitmq.consumer_name)
    .start_consuming
)
atexit.register(lambda: scheduler.shutdown())

for router, route in router_route_pairs:
    api.add_resource(router, f"{config.base_url.lower()}/{route}")


def main():
    app.run(debug=config.logger_level == "DEBUG", host="localhost", port=config.port, use_reloader=False)


if __name__ == "__main__":
    main()
