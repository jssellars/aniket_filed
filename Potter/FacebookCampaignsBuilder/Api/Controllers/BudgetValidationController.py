import json
import typing

import humps
from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Potter.FacebookCampaignsBuilder.Api.Queries.BudgetValidationQuery import BudgetValidationQuery
from Potter.FacebookCampaignsBuilder.Api.Startup import logger, startup


class BudgetValidationEndpoint(Resource):
    @jwt_required
    def get(self,
            business_owner_id: typing.AnyStr = None,
            account_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
        except Exception as e:
            pass

        try:
            response = BudgetValidationQuery.get(session=startup.session,
                                                 business_owner_id=business_owner_id,
                                                 account_id=account_id)
            response = json.dumps(humps.camelize(object_to_json(response)))
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="BudgetValidationEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")
