import json

import humps
from flask import Response, request
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import AdsManagerPermissions, AccountsPermissions
from FacebookTuring.Api.Dtos import ElementsCardViews
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsCombinationsDto import (
    AdsManagerCatalogsBreakdownsCombinationsDto,
)
from FacebookTuring.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsMetacolumnsDto import AdsManagerCatalogsMetacolumnsDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsAgGridDto import AdsManagerCatalogsViewsAgGridDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsByLevelDto import AdsManagerCatalogsViewsByLevelDto
from FacebookTuring.Api.Dtos.AdsManagerCatalogsViewsDto import AdsManagerCatalogsViewsDto
from FacebookTuring.Api.startup import config, fixtures


import logging

logger = logging.getLogger(__name__)


class AdsManagerCatalogsViewsEndpoint(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsViewsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve views."}), status=400, mimetype="application/json"
            )


class AdsManagerCatalogsViewsByLevelEndpoint(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self, level):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsViewsByLevelDto.get(level)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve views by level."}),
                status=400,
                mimetype="application/json",
            )


class AdsManagerCatalogsViewsAgGrid(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self, level):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsViewsAgGridDto.get(level)
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve ag grid views by level."}),
                status=400,
                mimetype="application/json",
            )


class ElementsViewsHandler:
    @staticmethod
    def get():
        logger.info(request_as_log_dict(request))
        try:
            response = ElementsCardViews.get_card_views()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve ag grid views by level."}),
                status=400,
                mimetype="application/json",
            )


class AdsManagerElementsViews(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_CAN_ACCESS_REPORTS_DATA)
    def get(self):
        return ElementsViewsHandler.get()


class AccountsElementsViews(Resource):
    @fixtures.authorize_permission(permission=AccountsPermissions.ACCOUNTS_CAN_ACCESS_REPORTS_DATA)
    def get(self):
        return ElementsViewsHandler.get()


class AdsManagerCatalogsMetacolumnsEndpoint(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsMetacolumnsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve meta columns."}),
                status=400,
                mimetype="application/json",
            )


class AdsManagerCatalogsBreakdownsEndpoint(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsBreakdownsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve breakdowns."}),
                status=400,
                mimetype="application/json",
            )


class AdsManagerCatalogsBreakdownsCombinationsEndpoint(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.CAN_ACCESS_ADS_MANAGER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            response = AdsManagerCatalogsBreakdownsCombinationsDto.get()
            response = humps.camelize(response)
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(
                response=json.dumps({"message": "Failed to retrieve breakdowns combinations columns."}),
                status=400,
                mimetype="application/json",
            )
