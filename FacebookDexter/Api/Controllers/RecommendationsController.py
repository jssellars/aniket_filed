import json

from flask import request, Response
from flask_jwt_simple import jwt_required
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageTypeEnum, LoggerMessageBase
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
from FacebookDexter.Api.Startup import logger


class DexterApiGetRecommendationsPage(Resource):
    @jwt_required
    def post(self):
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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApiGetRecommendationsPageEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class DexterApiGetCountsByCategory(Resource):
    @jwt_required
    def post(self):
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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApiGetCountsByCategoryEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class DexterApiDismissRecommendation(Resource):
    @jwt_required
    def patch(self):
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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApplyRecommendationEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')


class DexterApiApplyRecommendation(Resource):
    @jwt_required
    def patch(self):
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
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                    name="DexterApplyRecommendationEndpoint",
                                    description=str(e),
                                    extra_data=LoggerAPIRequestMessageBase(request).request_details)
            logger.logger.exception(log.to_dict())
            return Response(response=json.dumps('An error occurred'), status=500, mimetype='application/json')

