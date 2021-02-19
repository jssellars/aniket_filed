import logging
from datetime import datetime

import flask_restful
import humps
from flask import request

from Core.Web.Security.JWTTools import extract_user_filed_id
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Logging.Api.command_mappings import LoggingCommandMapping
from Logging.Api.commands import LoggingCommand
from Logging.Api.startup import config, fixtures
from Logging.Infrastructure.PersistenceLayer.LoggingMongoRepository import LoggingMongoRepository

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class Logging(Resource):
    @fixtures.authorize_jwt
    def post(self):
        try:
            # get business owner
            user_id = extract_user_filed_id()

            # get request
            request_json = request.get_json(force=True)
            request_json = humps.depascalize(request_json)

            # map request
            mapper = LoggingCommandMapping(target=LoggingCommand)
            command = mapper.load(request_json)
            command.user_id = user_id
            command.correlation_id = request.headers.get("CorrelationId")
            # === WARNING ===
            # === !! only activate these logs if they are really needed !! ===
            # business_owner_facebook_id = extract_business_owner_facebook_id(get_jwt())
            # business_owner_google_id = extract_business_owner_google_id(get_jwt())
            # command.business_owner_facebook_id = business_owner_facebook_id
            # command.business_owner_google_id = business_owner_google_id
            # command.jwt_token = request.headers.get('Authorization')
            # command.jwt_token = command.jwt_token.replace("Bearer ", "")
            command.timestamp = datetime.isoformat(datetime.now())

            # save request
            repository = LoggingMongoRepository(
                config=config.mongo,
                database_name=config.mongo.logging_database_name,
                collection_name=config.mongo.logging_collection_name,
            )
            repository.add_one(command)

            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to process request."}, 400
