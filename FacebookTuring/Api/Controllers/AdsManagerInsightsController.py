import json

from flask import request, Response
from flask_jwt_simple import jwt_required, get_jwt
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from FacebookTuring.Api.Commands.AdsManagerInsightsCommand import AdsManagerInsightsCommandEnum
from FacebookTuring.Api.CommandsHandlers.AdsManagerInsightsCommandHandler import AdsManagerInsightsCommandHandler
from FacebookTuring.Api.Startup import logger


class AdsManagerInsightsEndpoint(Resource):

    @jwt_required
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            response = (AdsManagerInsightsCommandHandler.
                        handle(handler_type=AdsManagerInsightsCommandEnum.INSIGHTS,
                               query_json=request_json,
                               business_owner_id=business_owner_id))
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AdsManagerInsightsWithTotalsEndpoint(Resource):

    @jwt_required
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            response = (AdsManagerInsightsCommandHandler.
                        handle(handler_type=AdsManagerInsightsCommandEnum.INSIGHTS_WITH_TOTALS,
                               query_json=request_json,
                               business_owner_id=business_owner_id))
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerInsightsWithTotalsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AdsManagerAgGridInsightsEndpoint(Resource):

    @jwt_required
    def post(self, level):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            response = (AdsManagerInsightsCommandHandler.handle(
                handler_type=AdsManagerInsightsCommandEnum.AG_GRID_INSIGHTS,
                query_json=request_json,
                business_owner_id=business_owner_id,
                level=level)
            )
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            import traceback
            traceback.print_exc()
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerInsightsWithTotalsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')


class AdsManagerReportInsightsEndpoint(Resource):

    @jwt_required
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = request.get_json(force=True)
            business_owner_id = extract_business_owner_facebook_id(get_jwt())
            response = (AdsManagerInsightsCommandHandler.
                        handle(handler_type=AdsManagerInsightsCommandEnum.REPORTS,
                               query_json=request_json,
                               business_owner_id=business_owner_id))
            return response
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerReportInsightsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to process request."}), status=400,
                            mimetype='application/json')
