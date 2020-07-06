import json

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookCampaignsBuilder.Api.CommandHandlers.AdPreviewCommandHandler import AdPreviewCommandHandler
from Potter.FacebookCampaignsBuilder.Api.Commands.AdPreviewCommand import AdPreviewCommand
from Potter.FacebookCampaignsBuilder.Api.Mappings.AdPreviewCommandMapping import AdPreviewCommandMapping
from Potter.FacebookCampaignsBuilder.Api.Startup import logger, startup


class AdPreviewEndpoint(Resource):

    @jwt_required
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            request_json = humps.depascalize(request.get_json(force=True))
            mapper = AdPreviewCommandMapping(AdPreviewCommand)
            command = mapper.load(request_json)
            if not command.business_owner_id:
                command.business_owner_id = extract_business_owner_facebook_id(get_jwt())
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(command.business_owner_id)
            ad_preview_iframe = AdPreviewCommandHandler.handle(command=command,
                                                               facebook_config=startup.facebook_config,
                                                               permanent_token=permanent_token)
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdPreviewEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="BadRequest_AdPreviewEndpoint"))
            return Response(response=response, status=400, mimetype="application/json")

        response = json.dumps({'response': ad_preview_iframe})
        return Response(response=response, status=200, mimetype='application/json')
