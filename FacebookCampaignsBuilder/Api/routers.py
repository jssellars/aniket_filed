import json
import logging
import typing
from distutils.util import strtobool

import flask_restful
import humps
from Core.facebook.sdk_adapter.smart_create import mappings
from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict
from Core.Tools.Misc.ObjectSerializers import object_to_camelized_dict
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id, extract_user_filed_id
from Core.Web.Security.Permissions import AdsManagerPermissions, CampaignBuilderPermissions
from FacebookCampaignsBuilder.Api import command_handlers, commands, queries
from FacebookCampaignsBuilder.Api.command_handlers import PublishProgress, PublishRequestToMessageQueue, DeliveryEstimateHandler
from FacebookCampaignsBuilder.Api.Queries.campaign_trees_structure import CampaignTreesStructure, GetStructure
from FacebookCampaignsBuilder.Api.startup import config, fixtures
from flask import request

from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.events import PublishAddAdsetAdEvent, PublishSmartEditEvent

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
            query = queries.AdCreativeAssetsImages(
                business_owner_id=business_owner_facebook_id,
            )

            return object_to_camelized_dict(query.get(ad_account_id=ad_account_id)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdCreativeAssetsVideos(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        try:
            is_instagram_eligible = bool(strtobool(request.args.get("instagramEligible", "False")))
            query = queries.AdCreativeAssetsVideos(business_owner_id=business_owner_facebook_id)

            return (
                object_to_camelized_dict(
                    query.get(ad_account_id=ad_account_id, is_instagram_eligible=is_instagram_eligible)
                ),
                200,
            )

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdCreativeAssetsPagePosts(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, page_facebook_id: typing.AnyStr = None):
        try:
            query = queries.AdCreativeAssetsPagePosts(
                business_owner_id=business_owner_facebook_id,
            )

            return query.get(page_facebook_id=page_facebook_id), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class AdPreview(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        try:
            uploaded_image = None
            if request.files:
                uploaded_image = request.files["image"]
                request_json = humps.depascalize(json.load(request.files["data"]))
            else:
                request_json = humps.depascalize(request.get_json(force=True))
            mapper = mappings.AdPreviewCommand(commands.AdPreview)
            command = mapper.load(request_json)
            if not command.business_owner_id:
                command.business_owner_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(command.business_owner_id)
            ad_preview_iframe = command_handlers.AdPreview.handle(
                command=command,
                facebook_config=config.facebook,
                permanent_token=permanent_token,
                uploaded_image=uploaded_image,
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
    def get(self, account_id: typing.AnyStr = None):

        business_owner_id = extract_business_owner_facebook_id()

        try:
            fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id=business_owner_id)
            query = queries.BudgetValidation.get(account_id=account_id)

            return object_to_camelized_dict(query), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


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
            query = queries.TargetingSearchInterestsTree(
                business_owner_id=extract_business_owner_facebook_id(),
            )

            return object_to_camelized_dict(query.get()), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchRegulatedInterests(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, categories: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchRegulatedInterests(
                business_owner_id=extract_business_owner_facebook_id(),
            )
            response = query.get(regulated_categories=(categories.replace(" ", "").upper().split(",")))

            return object_to_camelized_dict(response), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchInterestsSearch(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchInterestsSearch(
                business_owner_id=extract_business_owner_facebook_id(),
            )

            return object_to_camelized_dict(query.search(query_string=query_string)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchInterestsSuggestions(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        try:
            query = queries.TargetingSearchInterestsSuggestions(
                business_owner_id=extract_business_owner_facebook_id(),
            )

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
            query = queries.TargetingSearchLocationsSearch(
                business_owner_id=extract_business_owner_facebook_id(),
            )

            return object_to_camelized_dict(query.search(query_string=query_string)), 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class TargetingSearchLanguages(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        try:
            query = queries.TargetingSearchLanguages(
                business_owner_id=extract_business_owner_facebook_id(),
            )

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


class SmartCreatePublishProgress(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        try:
            user_filed_id = extract_user_filed_id()
            response = PublishProgress.get_publish_feedback(int(user_filed_id))

            if response:
                return object_to_camelized_dict(response), 200

            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, code="POTTER_BAD_REQUEST"), 400


class SmartEditCampaignTreesStructure(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, account_id, level, structure_ids):
        try:
            structure_ids = structure_ids.split(",")
            business_owner_facebook_id = extract_business_owner_facebook_id()
            return (
                humps.camelize(
                    CampaignTreesStructure.get(account_id, level, structure_ids, business_owner_facebook_id)
                ),
                200,
            )

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return {"message": f"Could not retrieve tree for {structure_ids}"}, 400


class AddAnAdAdsetGetStructure(Resource):
    @fixtures.authorize_permission(permission=AdsManagerPermissions.ADS_MANAGER_EDIT)
    def get(self, account_id, level, structure_ids):
        try:
            structure_ids = structure_ids.split(",")
            business_owner_facebook_id = extract_business_owner_facebook_id()
            return (
                humps.camelize(GetStructure.get(account_id, level, structure_ids, business_owner_facebook_id)),
                200,
            )
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": f"Could not retrieve structure for {structure_ids}"}, 400


class AddAnAdAdsetPublishStructure(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            request_json["business_owner_facebook_id"] = extract_business_owner_facebook_id()
            request_json["user_filed_id"] = extract_user_filed_id()
            publish_request = PublishAddAdsetAdEvent(**request_json)
            PublishRequestToMessageQueue.publish(publish_request)

            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, "AddAnAdAdsetEndpoint"), 400


class SmartEditPublishStructure(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            request_json["business_owner_facebook_id"] = extract_business_owner_facebook_id()
            request_json["user_filed_id"] = extract_user_filed_id()
            publish_request = PublishSmartEditEvent(**request_json)
            PublishRequestToMessageQueue.publish(publish_request)

            return None, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, "SmartEditPublishEndpoint"), 400


class DeliveryEstimate(Resource):
    @fixtures.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            business_owner_facebook_id = extract_business_owner_facebook_id()
            permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id)
            response = DeliveryEstimateHandler.handle(request_json, permanent_token)

            return response, 200

        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))

            return Tools.create_error(e, "DeliveryEstimateEndpoint"), 400
