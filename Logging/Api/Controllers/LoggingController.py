import json
from datetime import datetime

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.Security.JWTTools import extract_field_user_id
from Logging.Api.Commands.LoggingCommand import LoggingCommand
from Logging.Api.Mappings.LoggingCommandMapping import LoggingCommandMapping
from Logging.Api.Startup import logger, startup
from Logging.Infrastructure.PersistenceLayer.LoggingMongoRepository import LoggingMongoRepository


class LoggingEndpoint(Resource):

    @jwt_required
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            # get business owner
            user_id = extract_field_user_id(get_jwt())

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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="LoggingEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')
