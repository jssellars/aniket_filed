import json

from flask import request, Response
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Web.Security.Permissions import OptimizePermissions, AdsManagerPermissions
from FacebookDexter.Api.CommandHandlers.DexterApiApplyRecommendationCommandHandler import (
    DexterApiApplyRecommendationCommandHandler)
from FacebookDexter.Api.CommandHandlers.DexterApiDismissRecommendationCommandHandler import (
    DexterApiDismissRecommendationCommandHandler)
from FacebookDexter.Api.CommandHandlers.DexterApiGetCountsByCategoryCommandHandler import (
    DexterApiGetCountsByCategoryCommandHandler)
from FacebookDexter.Api.CommandHandlers.DexterApiGetRecommendationsPageCommandHandler import (
    DexterApiGetRecommendationsPageCommandHandler)
from FacebookDexter.Api.CommandValidators.DexterApiApplyRecommendationCommandValidator import (
    DexterApiApplyRecommendationCommandValidator)
from FacebookDexter.Api.CommandValidators.DexterApiDismissRecommendationCommandValidator import (
    DexterApiDismissRecommendationCommandValidator)
from FacebookDexter.Api.CommandValidators.DexterApiGetCountsByCategoryCommandValidator import (
    DexterApiGetCountsByCategoryCommandValidator)
from FacebookDexter.Api.CommandValidators.DexterApiGetRecommendationsPageCommandValidator import (
    DexterApiRecommendationsPageCommandValidator)
from FacebookDexter.Api.Commands.DexterApiApplyRecommendationCommand import DexterApiApplyRecommendationCommand
from FacebookDexter.Api.Commands.DexterApiDismissRecommendationCommand import DexterApiDismissRecommendationCommand
from FacebookDexter.Api.Commands.DexterApiGetCountsByCategoryCommand import DexterApiGetCountsByCategoryCommand
from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Api.Startup import startup


import logging

logger = logging.getLogger(__name__)


class GetRecommendationsPage(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        logger.info(request_as_log_dict(request))
        data = request.get_json()
        validator = DexterApiRecommendationsPageCommandValidator()
        valid, parameters_or_errors = validator.validate(data)
        if not valid:
            return Response(response=json.dumps(parameters_or_errors), status=400, mimetype='application/json')

        try:
            get_recommendations_page_command = (
                DexterApiGetRecommendationsPageCommand(parameters_or_errors.get('page_number'),
                                                       parameters_or_errors.get('page_size'),
                                                       parameters_or_errors.get('recommendations_filter'),
                                                       parameters_or_errors.get('recommendations_sort'),
                                                       parameters_or_errors.get('excluded_ids'))
            )

            handler = DexterApiGetRecommendationsPageCommandHandler()
            recommendations = handler.handle(get_recommendations_page_command)
            response = Response(response=json.dumps(recommendations), status=200, mimetype='application/json')
            return response

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class GetCountsByCategory(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        logger.info(request_as_log_dict(request))
        data = request.get_json()
        validator = DexterApiGetCountsByCategoryCommandValidator()
        valid, parameters_or_errors = validator.validate(data)

        if not valid:
            return Response(response=json.dumps(parameters_or_errors), status=400, mimetype='application/json')

        try:
            get_counts_by_category_command = DexterApiGetCountsByCategoryCommand(
                parameters_or_errors.get("channel"),
                parameters_or_errors.get("campaign_ids")
            )

            handler = DexterApiGetCountsByCategoryCommandHandler()
            counts = handler.handle(get_counts_by_category_command)
            response = Response(response=json.dumps(counts), status=200, mimetype='application/json')
            return response
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class DismissRecommendation(Resource):
    @startup.authorize_permission(permission=OptimizePermissions.OPTIMIZE_DELETE)
    def patch(self):
        logger.info(request_as_log_dict(request))
        data = request.args
        validator = DexterApiDismissRecommendationCommandValidator()
        valid, parameters_or_errors = validator.validate(data)
        if not valid:
            return Response(response=json.dumps(parameters_or_errors), status=400, mimetype='application/json')

        dismiss_recommendation_command = DexterApiDismissRecommendationCommand(parameters_or_errors.get('id'))
        try:
            handler = DexterApiDismissRecommendationCommandHandler()
            response = handler.handle(dismiss_recommendation_command)
            return response
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class ApplyRecommendation(Resource):
    @startup.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def patch(self):
        logger.info(request_as_log_dict(request))
        data = request.args
        headers = request.headers
        validator = DexterApiApplyRecommendationCommandValidator()
        valid, parameters_or_errors = validator.validate(data, headers)
        if not valid:
            return Response(response=json.dumps(parameters_or_errors), status=400, mimetype='application/json')

        apply_recommendation_command = DexterApiApplyRecommendationCommand(parameters_or_errors.get("id"),
                                                                           parameters_or_errors.get("token"))
        try:
            handler = DexterApiApplyRecommendationCommandHandler()
            return handler.handle(apply_recommendation_command)
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')

