import json

import humps
from flask import Response, request
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsCombinationsDto import \
    AdsManagerCatalogsBreakdownsCombinationsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsMetacolumnsDto import AdsManagerCatalogsMetacolumnsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsByLevelDto import AdsManagerCatalogsViewsByLevelDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsAgGridDto import AdsManagerCatalogsViewsAgGridDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsDto import AdsManagerCatalogsViewsDto
from FacebookTuring.Api.Startup import logger


class AdsManagerCatalogsViewsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsViewsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve views."}), status=400,
                            mimetype='application/json')


class AdsManagerCatalogsViewsByLevelEndpoint(Resource):

    @jwt_required
    def get(self, level):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsViewsByLevelDto.get(level)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsByLevelEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve views by level."}), status=400,
                            mimetype='application/json')


class AdsManagerCatalogsViewsAgGrid(Resource):

    @jwt_required
    def get(self, level):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsViewsAgGridDto.get(level)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsAgGridEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve ag grid views by level."}), status=400,
                            mimetype='application/json')


class AdsManagerCatalogsMetacolumnsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsMetacolumnsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsByLevelEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve meta columns."}), status=400,
                            mimetype='application/json')


class AdsManagerCatalogsBreakdownsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsBreakdownsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsByLevelEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve breakdowns."}), status=400,
                            mimetype='application/json')


class AdsManagerCatalogsBreakdownsCombinationsEndpoint(Resource):

    @jwt_required
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            response = AdsManagerCatalogsBreakdownsCombinationsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype='application/json')
        except Exception as e:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="AdsManagerCatalogsViewsByLevelEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps({"message": "Failed to retrieve breakdowns combinations columns."}),
                            status=400, mimetype='application/json')
