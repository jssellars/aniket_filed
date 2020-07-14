import json

from flask import Response, request
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Potter.FacebookCampaignsBuilder.Api.Queries.SmartCreateCatalogsQuery import SmartCreateCatalogsQuery
from Potter.FacebookCampaignsBuilder.Api.Startup import logger


class SmartCreateCatalogsEndpoint(Resource):
    @jwt_required
    def get(self):
        try:
            query = SmartCreateCatalogsQuery()

            return Response(response=json.dumps(query.get()),
                            status=200,
                            mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="GetCatalogsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            response = json.dumps(Tools.create_error(e, code="POTTER_BAD_REQUEST"))
            return Response(response=response, status=400, mimetype="application/json")
