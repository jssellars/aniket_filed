import typing

import humps
from flask import request
from flask_restful import Resource

from Core.logging_config import request_as_log_dict
from Core.Tools.Misc.ObjectSerializers import object_to_camelized_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import CampaignBuilderPermissions
from FacebookCampaignsBuilder.Api import command_handlers, commands, dtos, mappings, queries
from FacebookCampaignsBuilder.Api.startup import config, fixtures


import logging

logger = logging.getLogger(__name__)


class AdCreativeAssetsImages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.AdCreativeAssetsImages(
                business_owner_id=business_owner_facebook_id,
            )
            response = object_to_camelized_dict(query.get(ad_account_id=ad_account_id))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdCreativeAssetsVideos(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.AdCreativeAssetsVideos(
                business_owner_id=business_owner_facebook_id,
            )
            response = object_to_camelized_dict(query.get(ad_account_id=ad_account_id))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdCreativeAssetsPagePosts(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, page_facebook_id: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.AdCreativeAssetsPagePosts(
                business_owner_id=business_owner_facebook_id,
            )
            response = object_to_camelized_dict(query.get(page_facebook_id=page_facebook_id))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdPreview(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        logger.info(request_as_log_dict(request))
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            mapper = mappings.AdPreviewCommand(commands.AdPreview)
            command = mapper.load(request_json)
            if not command.business_owner_id:
                command.business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(command.business_owner_id)
            ad_preview_iframe = command_handlers.AdPreview.handle(
                command=command, facebook_config=config.facebook, permanent_token=permanent_token
            )
            response = {"response": ad_preview_iframe}

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="BadRequest_AdPreviewEndpoint")

            return response, 400


class AudienceSize(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self, account_id: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            audience_size = command_handlers.AudienceSize.handle(
                permanent_token=permanent_token, account_id=account_id, audience_details=request_json
            )
            response = object_to_camelized_dict({"audience_size": audience_size})

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, "AudienceSizeEndpoint")

            return response, 400


class BudgetValidation(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_id: typing.AnyStr = None, account_id: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            business_owner_id = extract_business_owner_facebook_id()
        except:
            pass
        try:
            response = object_to_camelized_dict(
                queries.BudgetValidation.get(
                    business_owner_id=business_owner_id, account_id=account_id
                )
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class Version(Resource):
    def get(self):
        logger.info(request_as_log_dict(request))
        response = {"app_name": config.name, "app_version": config.version, "environment": config.environment}

        return response, 200


class HealthCheck(Resource):
    def get(self):
        logger.info(request_as_log_dict(request))

        return None, 200


class PublishCampaign(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        logger.info(request_as_log_dict(request))
        try:
            request_json = humps.decamelize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            campaigns = command_handlers.CampaignBuilderPublish.handle(
                request=request_json,
                permanent_token=permanent_token,
                business_owner_id=business_owner_id,
            )
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="BadRequest_PublishCampaignEndpoint")

            return response, 400

        mapper = mappings.PublishCampaignResponseDto(target=dtos.PublishCampaignResponse)
        response = mapper.load(request_json)
        response.business_owner_facebook_id = business_owner_id
        response.campaigns = campaigns

        response = object_to_camelized_dict(response)

        return response, 200


class SmartCreatePublish(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def post(self):
        logger.info(request_as_log_dict(request))

        try:
            request_json = humps.decamelize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            campaigns = command_handlers.SmartCreatePublish.handle(
                request=request_json,
                permanent_token=permanent_token,
                business_owner_id=business_owner_id,
                facebook_config=config.facebook,
            )
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="BadRequest_PublishSmartCreateEndpoint")
            return response, 400

        mapper = mappings.PublishCampaignResponseDto(target=dtos.PublishCampaignResponse)
        response = mapper.load(request_json)
        response.business_owner_facebook_id = business_owner_id
        response.campaigns = campaigns

        response = object_to_camelized_dict(response)

        return response, 200


class SmartCreateCats(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.SmartCreateCats()
            response = query.get()

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="BAD_REQUEST")

            return response, 400


class SmartCreateCatalogs(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.SmartCreateCatalogs()
            response = query.get()

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsTree(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchInterestsTree(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchRegulatedInterests(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, categories: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchRegulatedInterests(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = query.get(regulated_categories=(categories.replace(" ", "").upper().split(",")))
            response = object_to_camelized_dict(response)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsSearch(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchInterestsSearch(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsSuggestions(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchInterestsSuggestions(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLocations(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchLocationsCountryGroups(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLocationSearch(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchLocationsSearch(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLanguages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.info(request_as_log_dict(request))
        try:
            query = queries.TargetingSearchLanguages(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400
