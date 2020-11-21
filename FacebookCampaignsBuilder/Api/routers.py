import typing

import humps
from flask import request
from flask_restful import Resource

from Core.Tools.Logger.LoggerAPIRequestMessageBase import LoggerAPIRequestMessageBase
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from Core.Tools.Misc.ObjectSerializers import object_to_camelized_dict
from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.Web.Security.JWTTools import extract_business_owner_facebook_id
from Core.Web.Security.Permissions import CampaignBuilderPermissions
from FacebookCampaignsBuilder.Api import command_handlers, commands, dtos, mappings, queries
from FacebookCampaignsBuilder.Api.Startup import logger, startup


class AdCreativeAssetsImages(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.AdCreativeAssetsImages(
                session=startup.session,
                business_owner_id=business_owner_facebook_id,
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get(ad_account_id=ad_account_id))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="AdCreativeAssetsImagesEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdCreativeAssetsVideos(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, ad_account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.AdCreativeAssetsVideos(
                session=startup.session,
                business_owner_id=business_owner_facebook_id,
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get(ad_account_id=ad_account_id))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="AdCreativeAssetsImagesEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdCreativeAssetsPagePosts(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_facebook_id: typing.AnyStr = None, page_facebook_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.AdCreativeAssetsPagePosts(
                session=startup.session,
                business_owner_id=business_owner_facebook_id,
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get(page_facebook_id=page_facebook_id))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="AdCreativeAssetsImagesEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class AdPreview(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            mapper = mappings.AdPreviewCommand(commands.AdPreview)
            command = mapper.load(request_json)
            if not command.business_owner_id:
                command.business_owner_id = extract_business_owner_facebook_id()
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(command.business_owner_id)
            ad_preview_iframe = command_handlers.AdPreview.handle(
                command=command, facebook_config=startup.facebook_config, permanent_token=permanent_token
            )
            response = {"response": ad_preview_iframe}

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="AdPreviewEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="BadRequest_AdPreviewEndpoint")

            return response, 400


class AudienceSize(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self, account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = humps.depascalize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
            audience_size = command_handlers.AudienceSize.handle(
                permanent_token=permanent_token, account_id=account_id, audience_details=request_json
            )
            response = object_to_camelized_dict({"audience_size": audience_size})

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="AudienceSizeEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, "AudienceSizeEndpoint")

            return response, 400


class BudgetValidation(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, business_owner_id: typing.AnyStr = None, account_id: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            business_owner_id = extract_business_owner_facebook_id()
        except Exception as e:
            pass
        try:
            response = object_to_camelized_dict(
                queries.BudgetValidation.get(
                    session=startup.session, business_owner_id=business_owner_id, account_id=account_id
                )
            )

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="BudgetValidationEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class Version(Resource):
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        response = {
            "api_name": startup.api_name,
            "api_version": startup.api_version,
            "service_name": startup.service_name,
            "service_version": startup.service_version,
            "environment": startup.environment,
        }

        return response, 200


class HealthCheck(Resource):
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())

        return None, 200


class PublishCampaign(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def post(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            request_json = humps.decamelize(request.get_json(force=True))
            business_owner_id = extract_business_owner_facebook_id()
            permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)
            campaigns = command_handlers.PublishCampaign.handle(
                request=request_json,
                permanent_token=permanent_token,
                business_owner_id=business_owner_id,
                facebook_config=startup.facebook_config,
            )
        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="PublishCampaignEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="BadRequest_PublishCampaignEndpoint")

            return response, 400

        mapper = mappings.PublishCampaignResponseDto(target=dtos.PublishCampaignResponse)
        response = mapper.load(request_json)
        response.business_owner_facebook_id = business_owner_id
        response.campaigns = campaigns

        response = object_to_camelized_dict(response)

        return response, 200


class SmartCreateCats(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.SmartCreateCats()
            response = query.get()

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="GetCatalogsEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="BAD_REQUEST")

            return response, 400


class SmartCreateCatalogs(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.SMART_CREATE_VIEW)
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.SmartCreateCatalogs()
            response = query.get()

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="GetCatalogsEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsTree(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchInterestsTree(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchInterestsTreeEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchRegulatedInterests(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, categories: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchRegulatedInterests(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = query.get(regulated_categories=(categories.replace(" ", "").upper().split(",")))
            response = object_to_camelized_dict(response)

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchRegulatedInterestsEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsSearch(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchInterestsSearch(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchInterestsSearchEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchInterestsSuggestions(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchInterestsSuggestions(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchInterestsSuggestionsEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLocations(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchLocationsCountryGroups(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchLocationsEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLocationSearch(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self, query_string: typing.AnyStr = None):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchLocationsSearch(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.search(query_string=query_string))

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchLocationSearchEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400


class TargetingSearchLanguages(Resource):
    @startup.authorize_permission(permission=CampaignBuilderPermissions.CAN_ACCESS_CAMPAIGN_BUILDER)
    def get(self):
        logger.logger.info(LoggerAPIRequestMessageBase(request).to_dict())
        try:
            query = queries.TargetingSearchLanguages(
                session=startup.session,
                business_owner_id=extract_business_owner_facebook_id(),
                facebook_config=startup.facebook_config,
            )
            response = object_to_camelized_dict(query.get())

            return response, 200

        except Exception as e:
            log = LoggerMessageBase(
                mtype=LoggerMessageTypeEnum.ERROR,
                name="TargetingSearchLanguagesEndpoint",
                description=str(e),
                extra_data=LoggerAPIRequestMessageBase(request).request_details,
            )
            logger.logger.exception(log.to_dict())
            response = Tools.create_error(e, code="POTTER_BAD_REQUEST")

            return response, 400
