import logging

import flask_restful
import humps
from flask import Response, request

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import AdsManagerPermissions, OptimizePermissions
from FacebookDexter.Api.CommandHandlers import (
    DexterApiGetCountsByCategoryCommandHandler,
    DexterApiGetRecommendationsPageCommandHandler,
    RecommendationsHandlers,
)
from FacebookDexter.Api.CommandHandlers.DexterApiApplyRecommendationCommandHandler import (
    DexterApiApplyRecommendationCommandHandler,
)
from FacebookDexter.Api.CommandHandlers.DexterApiDismissRecommendationCommandHandler import (
    DexterApiDismissRecommendationCommandHandler,
)
from FacebookDexter.Api.Commands.DexterApiApplyRecommendationCommand import DexterApiApplyRecommendationCommand
from FacebookDexter.Api.Commands.DexterApiDismissRecommendationCommand import DexterApiDismissRecommendationCommand
from FacebookDexter.Api.Commands.DexterApiGetCountsByCategoryCommand import DexterApiGetCountsByCategoryCommand
from FacebookDexter.Api.Commands.DexterApiGetRecommendationsPageCommand import DexterApiGetRecommendationsPageCommand
from FacebookDexter.Api.Commands.RecommendationPageCommand import (
    ApplyRecommendationCommand,
    ApplyRecommendationMapping,
    NumberOfPagesCommand,
    NumberOfPagesCommandMapping,
    RecommendationPageCommand,
    RecommendationPageCommandMapping,
)
from FacebookDexter.Api.CommandValidators.DexterApiApplyRecommendationCommandValidator import (
    DexterApiApplyRecommendationCommandValidator,
)
from FacebookDexter.Api.CommandValidators.DexterApiDismissRecommendationCommandValidator import (
    DexterApiDismissRecommendationCommandValidator,
)
from FacebookDexter.Api.CommandValidators.DexterApiGetCountsByCategoryCommandValidator import (
    DexterApiGetCountsByCategoryCommandValidator,
)
from FacebookDexter.Api.CommandValidators.DexterApiGetRecommendationsPageCommandValidator import (
    DexterApiRecommendationsPageCommandValidator,
)
from FacebookDexter.Api.QueryParamsValidators import DexterApiGetCampaignsQueryValidator
from FacebookDexter.Api.startup import config, fixtures
from FacebookDexter.Infrastructure.PersistanceLayer.RecommendationsRepository import RecommendationsRepository

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class GetActionHistoryQuery(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            structure_id = request.args.get("structureId")
            if structure_id is None:
                return "Please provide structure id", 400

            recommendation_repository = RecommendationsRepository(config.mongo)

            return recommendation_repository.get_action_history(structure_id), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class GetCampaignsQuery(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:
            logger.info(request_as_log_dict(request))
            request_args = request.args
            error_response_or_paramaters = DexterApiGetCampaignsQueryValidator.validate(request_args)

            if isinstance(error_response_or_paramaters, Response):
                return error_response_or_paramaters

            recommendation_repository = RecommendationsRepository(config.mongo)
            campaigns = recommendation_repository.get_campaigns(
                error_response_or_paramaters["ad_account_id"], error_response_or_paramaters["channel"]
            )

            return campaigns, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class GetRecommendationQuery(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def get(self):
        try:

            logger.info(request_as_log_dict(request))
            recommendation_id = request.args.get("id")
            if recommendation_id is None:
                return "Please provide a recommendation id", 400

            recommendation_repository = RecommendationsRepository(config.mongo)
            recommendation = recommendation_repository.get_recommendation_by_id(recommendation_id)

            return recommendation, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class OldApplyRecommendation(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def patch(self):
        data = request.args
        headers = request.headers
        validator = DexterApiApplyRecommendationCommandValidator()
        valid, parameters_or_errors = validator.validate(data, headers)
        if not valid:
            return parameters_or_errors, 400

        apply_recommendation_command = DexterApiApplyRecommendationCommand(
            parameters_or_errors.get("id"), parameters_or_errors.get("token")
        )
        try:
            handler = DexterApiApplyRecommendationCommandHandler()

            return handler.handle(apply_recommendation_command)

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class GetRecommendationsPage(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        data = request.get_json()
        validator = DexterApiRecommendationsPageCommandValidator()
        valid, parameters_or_errors = validator.validate(data)
        if not valid:
            return parameters_or_errors, 400

        try:
            get_recommendations_page_command = DexterApiGetRecommendationsPageCommand(
                parameters_or_errors.get("page_number"),
                parameters_or_errors.get("page_size"),
                parameters_or_errors.get("recommendations_filter"),
                parameters_or_errors.get("recommendations_sort"),
                parameters_or_errors.get("excluded_ids"),
            )
            handler = DexterApiGetRecommendationsPageCommandHandler.get_recommendations_page(
                get_recommendations_page_command
            )

            return handler.handle(get_recommendations_page_command), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class GetCountsByCategory(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        data = request.get_json()
        validator = DexterApiGetCountsByCategoryCommandValidator()
        valid, parameters_or_errors = validator.validate(data)

        if not valid:
            return parameters_or_errors, 400

        try:
            get_counts_by_category_command = DexterApiGetCountsByCategoryCommand(
                parameters_or_errors.get("channel"), parameters_or_errors.get("campaign_ids")
            )
            handler = DexterApiGetCountsByCategoryCommandHandler.get_categories_count(get_counts_by_category_command)

            return handler.handle(get_counts_by_category_command), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class OldDismissRecommendation(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.OPTIMIZE_DELETE)
    def patch(self):
        data = request.args
        validator = DexterApiDismissRecommendationCommandValidator()
        valid, parameters_or_errors = validator.validate(data)
        if not valid:
            return parameters_or_errors, 400

        dismiss_recommendation_command = DexterApiDismissRecommendationCommand(parameters_or_errors.get("id"))
        try:
            handler = DexterApiDismissRecommendationCommandHandler()

            return handler.handle(dismiss_recommendation_command)

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return "An error occurred", 400


class GetRecommendations(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        data = humps.decamelize(request.get_json(force=True))
        mapping = RecommendationPageCommandMapping(target=RecommendationPageCommand)
        command = mapping.load(data)

        try:
            business_owner_id = extract_business_owner_facebook_id()
            result = RecommendationsHandlers.read_recommendations_page(command, business_owner_id)
            return result, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to retrieve recommendations."}, 400


class GetNumberOfPages(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.CAN_ACCESS_OPTIMIZE)
    def post(self):
        data = humps.decamelize(request.get_json(force=True))
        mapping = NumberOfPagesCommandMapping(target=NumberOfPagesCommand)
        command = mapping.load(data)

        try:
            business_owner_id = extract_business_owner_facebook_id()
            result = RecommendationsHandlers.get_number_of_pages(command, business_owner_id)
            return result, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to get recommendation's number of pages"}, 400


class DismissRecommendation(Resource):
    @fixtures.authorize_permission(permission=OptimizePermissions.OPTIMIZE_DELETE)
    def put(self, recommendation_id: str):

        try:
            RecommendationsHandlers.dismiss_recommendation(recommendation_id)
            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": "Failed to dismiss recommendation"}, 400


class ApplyRecommendation(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def put(self, recommendation_id: str):

        try:
            # Todo: Refactor in the Future.
            data = humps.decamelize(request.get_json())
            data = {} if data == "none" else data
            mapping = ApplyRecommendationMapping(target=ApplyRecommendationCommand)
            command = mapping.load(data)

            business_owner_id = extract_business_owner_facebook_id()
            return (
                RecommendationsHandlers.apply_recommendation(
                    recommendation_id, business_owner_id, request.headers, command
                ),
                200,
            )

        except Exception as e:
            logger.exception(f"Failed to apply recommendation || {repr(e)}")

            return {"message": "Failed to apply recommendation"}, 400
