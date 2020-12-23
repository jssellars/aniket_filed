import logging
import typing

import flask_restful
import humps
from flask import request

from Core.Tools.Misc.ObjectSerializers import object_to_camelized_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import CampaignBuilderPermissions, AdsManagerPermissions
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from FacebookCampaignsBuilder.Api import command_handlers, commands, dtos, mappings, queries
from FacebookCampaignsBuilder.Api.startup import config, fixtures

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class HealthCheck(Resource):
    def get(self):
        return None, 200


class Version(Resource):
    def get(self):
        return config.version_endpoint_payload, 200


class AdCreativeAssetsImages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        try:
            query = queries.AdCreativeAssetsImages(business_owner_id=business_owner_facebook_id, )

            return object_to_camelized_dict(query.get(ad_account_id=ad_account_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdCreativeAssetsVideos(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        try:
            query = queries.AdCreativeAssetsVideos(business_owner_id=business_owner_facebook_id, )

            return object_to_camelized_dict(query.get(ad_account_id=ad_account_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdCreativeAssetsPagePosts(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, page_facebook_id: typing.AnyStr = None):
        try:
            query = queries.AdCreativeAssetsPagePosts(business_owner_id=business_owner_facebook_id, )

            return object_to_camelized_dict(query.get(page_facebook_id=page_facebook_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdPreview(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
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

            return {"response": ad_preview_iframe}, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="BadRequest_AdPreviewEndpoint"), 400


class AudienceSize(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self, account_id: typing.AnyStr = None):
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            audience_size = command_handlers.AudienceSize.handle(
                permanent_token=permanent_token, account_id=account_id, audience_details=request_json
            )

            return object_to_camelized_dict({"audience_size": audience_size}), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, "AudienceSizeEndpoint"), 400


class BudgetValidation(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_id: typing.AnyStr = None, account_id: typing.AnyStr = None):
        try:
            business_owner_id = extract_business_owner_facebook_id()
        except:
            pass
        try:
            query = queries.BudgetValidation.get(business_owner_id=business_owner_id, account_id=account_id)

            return object_to_camelized_dict(query), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class PublishCampaign(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        try:
            request_json = humps.decamelize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            campaigns = command_handlers.CampaignBuilderPublish.handle(
                request=request_json, permanent_token=permanent_token, business_owner_id=business_owner_id,
            )
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="BadRequest_PublishCampaignEndpoint"), 400

        mapper = mappings.PublishCampaignResponseDto(target=dtos.PublishCampaignResponse)
        response = mapper.load(request_json)
        response.business_owner_facebook_id = business_owner_id
        response.campaigns = campaigns

        return object_to_camelized_dict(response), 200


class SmartCreatePublish(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def post(self):

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

            return Tools.create_error(e, code="BadRequest_PublishSmartCreateEndpoint"), 400

        mapper = mappings.PublishCampaignResponseDto(target=dtos.PublishCampaignResponse)
        response = mapper.load(request_json)
        response.business_owner_facebook_id = business_owner_id
        response.campaigns = campaigns

        return object_to_camelized_dict(response), 200


class SmartCreateCats(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        try:
            return queries.SmartCreateCats().get(), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="BAD_REQUEST"), 400


class SmartCreateCatalogs(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        try:
            return queries.SmartCreateCatalogs().get(), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="BAD_REQUEST"), 400


class TargetingSearchInterestsTree(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        try:
            query = queries.TargetingSearchInterestsTree(business_owner_id=extract_business_owner_facebook_id(), )

            return object_to_camelized_dict(query.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchRegulatedInterests(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, categories: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchRegulatedInterests(business_owner_id=extract_business_owner_facebook_id(), )
            response = query.get(regulated_categories=(categories.replace(" ", "").upper().split(",")))

            return object_to_camelized_dict(response), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchInterestsSearch(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchInterestsSearch(business_owner_id=extract_business_owner_facebook_id(), )

            return object_to_camelized_dict(query.search(query_string=query_string)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchInterestsSuggestions(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchInterestsSuggestions(business_owner_id=extract_business_owner_facebook_id(), )

            return object_to_camelized_dict(query.search(query_string=query_string)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchLocations(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        try:
            query = queries.TargetingSearchLocationsCountryGroups(
                business_owner_id=extract_business_owner_facebook_id(),
            )

            return object_to_camelized_dict(query.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchLocationSearch(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchLocationsSearch(business_owner_id=extract_business_owner_facebook_id(), )

            return object_to_camelized_dict(query.search(query_string=query_string)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchLanguages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        try:
            query = queries.TargetingSearchLanguages(business_owner_id=extract_business_owner_facebook_id(), )

            return object_to_camelized_dict(query.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AccountAdvertisableApps:
    @staticmethod
    def get(account_id: str):
        try:
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
            apps = queries.get_account_advertisable_apps(account_id, permanent_token, config)
            return object_to_camelized_dict(apps), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="BAD_REQUEST"), 400


class SmartCreateAccountAdvertisableApps(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self, account_id: str):
        return AccountAdvertisableApps.get(account_id)


class AdsManagerAccountAdvertisableApps(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, account_id: str):
        return AccountAdvertisableApps.get(account_id)


class AdsManagerAddStructuresToParent(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def post(self, level):
        try:
            raw_request = humps.decamelize(request.get_json(force=True))
            business_owner_facebook_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id)
            response = command_handlers.AddStructuresToParent.publish_structures_to_parent(
                level=level,
                request=raw_request,
                permanent_token=permanent_token,
                facebook_config=config.facebook
            )

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to process request."}, 400


