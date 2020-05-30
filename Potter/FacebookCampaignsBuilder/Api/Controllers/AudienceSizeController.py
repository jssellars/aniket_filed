import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookCampaignsBuilder.Api.CommandHandlers.AudienceSizeCommandHandler import AudienceSizeCommandHandler
from Potter.FacebookCampaignsBuilder.Api.Startup import logger, startup


class AudienceSizeEndpoint(Resource):

    @jwt_required
    def post(self, account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            request_json = humps.depascalize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
            audience_size = AudienceSizeCommandHandler.handle(permanent_token=permanent_token, account_id=account_id,
                                                              audience_details=request_json)
            response = {'audience_size': audience_size}
            response = json.dumps(humps.camelize(object_to_json(response)))

            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AudienceSizeEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, "AudienceSizeEndpoint"))
            return Response(response=response, status=400, mimetype="application/json")
