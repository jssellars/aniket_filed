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

from GoogleDexter.BackgroundTasks import routers
from Core.Dexter.PersistanceLayer.DexterJournalMongoRepository import DexterJournalMongoRepository
from Core.Dexter.PersistanceLayer.DexterRecommendationsMongoRepository import DexterRecommendationsMongoRepository
from GoogleDexter.BackgroundTasks.startup import config, fixtures
from GoogleDexter.Infrastructure.IntegrationEvents.HandlersEnum import HandlersEnum
from GoogleDexter.Infrastructure.IntegrationEvents.MessageTypeEnum import RequestTypeEnum
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info(getattr(properties, "type", ""), extra={"rabbitmq": body})
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        message_type = getattr(properties, "type", None)
        request_handler_name = RequestTypeEnum.get_by_value(message_type)
        request_handler = HandlersEnum.get_enum_by_name(request_handler_name).value
    except Exception as e:
        logger.exception(f"Failed to initialise processing || {repr(e)}")

        return

    try:
        # data_repository = GoogleDexterMongoRepository(config=config.mongo)
        recommendations_repository = DexterRecommendationsMongoRepository(
            config=config.mongo,
            database_name=config.mongo.recommendations_database_name,
            collection_name=config.mongo.recommendations_collection_name,
        )
        journal_repository = DexterJournalMongoRepository(
            config=config.mongo,
            database_name=config.mongo.journal_database_name,
            collection_name=config.mongo.journal_collection_name,
        )
        (
            request_handler.set_config(config)
            # .set_data_repository(data_repository)
            .set_journal_repository(journal_repository)
            .set_recommendations_repository(recommendations_repository)
            .handle(body)
        )
    except Exception as e:
        logger.exception(repr(e), extra={"message_type": message_type, "integration_event_body": body})


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
