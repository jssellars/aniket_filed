import json
from datetime import datetime

import humps
from flask import request, Response
from flask_restful import Resource

from Core.logging_legacy import request_as_log_dict, request_as_log_dict_nested, log_message_as_dict
from Core.Web.Security.JWTTools import extract_field_user_id
from Logging.Api.Commands.LoggingCommand import LoggingCommand
from Logging.Api.Mappings.LoggingCommandMapping import LoggingCommandMapping
from Logging.Api.Startup import logger, startup
from Logging.Infrastructure.PersistenceLayer.LoggingMongoRepository import LoggingMongoRepository


import logging

logger_native = logging.getLogger(__name__)


class LoggingEndpoint(Resource):
    @startup.authorize_jwt
    def post(self):
        logger.logger.info(request_as_log_dict_nested(request))
        try:
            # get business owner
            user_id = extract_field_user_id()

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
            repository = LoggingMongoRepository(config=startup.mongo_config,
                                                database_name=startup.mongo_config.logging_database_name,
                                                collection_name=startup.mongo_config.logging_collection_name,
                                                logger=logger)
            repository.add_one(command)

            return Response(status=200, mimetype='application/json')
        except Exception as e:
            logger.logger.exception(log_message_as_dict(mtype=logging.ERROR,
                                      name="LoggingEndpoint",
                                      description=str(e),
                                      extra_data=request_as_log_dict(request)))
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')
