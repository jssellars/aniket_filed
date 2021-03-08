import logging
from dataclasses import asdict
from typing import Any, Dict, Optional

from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from Core.facebook.sdk_adapter.smart_create import ad_builder, adset_builder
from Core.facebook.sdk_adapter.smart_create.targeting import FlexibleTargeting, Location, Targeting
from Core.Tools.Misc.FiledAdFormatEnum import FiledAdFormatEnum
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from FacebookCampaignsBuilder.Api import commands
from FacebookCampaignsBuilder.Api.request_handlers import SmartCreatePublish
from FacebookCampaignsBuilder.Api.startup import config
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


class AdPreview:
    @classmethod
    def handle(
        cls,
        command: commands.AdPreview = None,
        facebook_config: Any = None,
        permanent_token: str = None,
        uploaded_image: FileStorage = None,
    ) -> Optional[str]:
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        ad_creative = None
        ad_account = AdAccount(fbid=command.account_id)
        page_ids = dict(
            facebook_page_id=command.page_facebook_id,
            instagram_page_id=command.instagram_facebook_id,
        )
        if command.ad_template["ad_format"] == FiledAdFormatEnum.IMAGE.value:
            ad_creative = ad_builder.build_image_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective, uploaded_image
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.VIDEO.value:
            ad_creative = ad_builder.build_video_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.CAROUSEL.value:
            ad_creative = ad_builder.build_carousel_ad_creative(
                page_ids, command.ad_template, ad_account, command.objective
            )
        elif command.ad_template["ad_format"] == FiledAdFormatEnum.EXISTING_POST.value:
            ad_creative = ad_builder.build_existing_ad_creative(ad_account, command.ad_template["post_id"])

        params = {"ad_format": command.ad_format, "creative": ad_creative}
        ad_preview = ad_account.get_generate_previews(params=params)

        if ad_preview:
            return ad_preview[0].export_all_data()["body"].replace('scrolling="yes"', 'scrolling="no"')

        return None


class AudienceSize:
    @classmethod
    def handle(
        cls,
        permanent_token: str = None,
        account_id: str = None,
        audience_details: Dict = None,
    ):
        _ = GraphAPISdkBase(config.facebook, permanent_token)

        try:
            account = AdAccount(account_id)
            response = account.get_delivery_estimate(fields=["estimate_mau"], params=audience_details)

        except Exception as e:
            raise e

        if isinstance(response, Exception):
            raise response

        audience_size_estimate = response[0].get("estimate_mau", None)
        return audience_size_estimate


class AddStructuresToParent:
    @staticmethod
    def publish_structures_to_parent(
        level: str,
        request: Dict = None,
        permanent_token: str = None,
        facebook_config: Any = None,
    ):
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        parent_ids = request.get("parent_ids", None)
        child_ids = request.get("child_ids", None)
        if child_ids and parent_ids:
            new_structures = AddStructuresToParent._publish_structures_from_ids(level, child_ids, parent_ids)
        elif level == Level.ADSET.value and "ad_set_name" in request and parent_ids:
            new_structures = AddStructuresToParent._publish_adset_to_campaigns(request, parent_ids)
        elif level == Level.AD.value and "ad_name" in request and parent_ids:
            new_structures = AddStructuresToParent._publish_ad_to_adsets(request, parent_ids)
        else:
            raise ValueError("No valid existing keys found in request. Or list of Ids is empty.")
        return {level: new_structures}

    @staticmethod
    def _publish_structures_from_ids(level, child_ids, parent_ids):
        results = []
        for parent_id in parent_ids:
            for child_id in child_ids:
                results.append(AddStructuresToParent._duplicate_structure_on_facebook(level, child_id, parent_id))
        return results

    @staticmethod
    def _duplicate_structure_on_facebook(level, facebook_id, parent_id=None):
        structure = LevelToGraphAPIStructure.get(level, facebook_id)
        params = AddStructuresToParent._create_duplicate_parameters(level, parent_id)
        new_structure_id = structure.create_copy(params=params)
        new_structure_id = Tools.convert_to_json(new_structure_id)
        if "ad_object_ids" in new_structure_id:
            return new_structure_id["ad_object_ids"][0]["copied_id"]
        elif "copied_ad_id" in new_structure_id:
            return new_structure_id["copied_ad_id"]
        else:
            raise ValueError("Invalid duplicated structure id.")

    @staticmethod
    def _create_duplicate_parameters(level, parent_id=None):
        if level == Level.ADSET.value:
            return AddStructuresToParent._duplicate_adset_parameters(parent_id)
        elif level == Level.AD.value:
            return AddStructuresToParent._duplicate_ad_parameters(parent_id)
        else:
            raise ValueError(f"Unknown level supplied: {level}. Please try again using adset or ad")

    @staticmethod
    def _duplicate_adset_parameters(parent_id):
        parameters = {
            "campaign_id": parent_id,
            "deep_copy": False,
            "status_option": AdSet.StatusOption.paused,
        }
        return parameters

    @staticmethod
    def _duplicate_ad_parameters(parent_id):
        parameters = {"adset_id": parent_id, "status_option": Ad.StatusOption.paused}
        return parameters

    @staticmethod
    def _publish_adset_to_campaigns(request, parent_ids):
        results = []
        for parent_id in parent_ids:
            results.append(AddStructuresToParent._create_adset_for_campaign(request, parent_id))
        return results

    @staticmethod
    def _publish_ad_to_adsets(request, parent_ids):
        results = []
        for parent_id in parent_ids:
            results.append(AddStructuresToParent._create_ad_for_adset(request, parent_id))
        return results

    @staticmethod
    def _create_adset_for_campaign(request, campaign_id):
        ad_account = AdAccount(fbid=request["ad_account_id"])

        ad_set_template = {
            AdSet.Field.tune_for_category: request.get(AdSet.Field.tune_for_category, AdSet.TuneForCategory.none),
            AdSet.Field.name: request.get("ad_set_name", None),
            AdSet.Field.destination_type: request.get("destination_type", None),
            AdSet.Field.billing_event: request.get("budget_billing_event", None),
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.bid_amount: request.get("bid_amount", None),
            AdSet.Field.bid_strategy: request.get("bid_strategy", None),
        }

        adset_builder.set_statuses(ad_set_template)
        adset_builder.set_date_interval(ad_set_template, request)
        is_using_conversions = request["objective"] == "CONVERSIONS"
        adset_builder.set_promoted_object(ad_set_template, is_using_conversions, request, request)

        if "campaign_budget_optimization" in request:
            budget_opt = request["campaign_budget_optimization"]
            amount = budget_opt["amount"] * 100
            if budget_opt["budget_allocated_type_id"] == 0:
                ad_set_template[AdSet.Field.lifetime_budget] = amount
            else:
                ad_set_template[AdSet.Field.daily_budget] = amount

        targeting_request = request.get("targeting", None)
        AddStructuresToParent._set_targeting(ad_set_template, request, targeting_request)
        facebook_ad_set = ad_account.create_ad_set(params=ad_set_template)

        return facebook_ad_set.get_id()

    @staticmethod
    def _create_ad_for_adset(request, adset_id):
        ad_account_id = request["ad_account_id"]
        ad_account = AdAccount(fbid=request["ad_account_id"])
        # TODO: Modify build_ads function to accept a single argument for necessary fields
        #  as opposed to per step fields
        ads = ad_builder.build_ads(ad_account_id, request, request)

        for ad in ads:
            ad.update({Ad.Field.adset_id: adset_id, Ad.Field.adset: adset_id})
            ad = ad_account.create_ad(params=ad)
            return ad.get_id()

    @staticmethod
    def _set_targeting(ad_set_template, request, targeting_request):
        languages = targeting_request.get("languages", [])

        if languages:
            languages = [language["key"] for language in languages]

        included_interests, excluded_interests, narrow_interests = adset_builder.extract_interests(targeting_request)
        included_custom_audiences, excluded_custom_audiences = adset_builder.extract_custom_audiences(targeting_request)

        (
            facebook_positions,
            instagram_positions,
            audience_network_positions,
            publisher_platforms,
        ) = adset_builder.add_placement_positions(request)

        flexible_spec = [FlexibleTargeting(included_interests)]
        # TODO: check if this is valid, maybe we should include the narrow interests into the
        #  included interests
        if narrow_interests:
            flexible_spec.append(FlexibleTargeting(narrow_interests))

        age_range = targeting_request.get("age_range", None)

        targeting = Targeting(
            flexible_spec,
            age_min=age_range["min_age"],
            age_max=age_range["max_age"],
            custom_audiences=included_custom_audiences,
            excluded_custom_audiences=excluded_custom_audiences,
            genders=[targeting_request.get("gender", None)],
            exclusions=FlexibleTargeting(interests=excluded_interests),
            locales=languages,
            facebook_positions=facebook_positions,
            instagram_positions=instagram_positions,
            audience_network_positions=audience_network_positions,
            publisher_platforms=publisher_platforms,
            device_platforms=[x.name_sdk for x in DevicePlatform.contexts[Contexts.SMART_CREATE].items],
        )

        ad_set_template["targeting"] = asdict(targeting)

        locations = targeting_request.get("locations")
        all_locations = [Location(**location) for location in locations]
        ad_set_template["targeting"]["geo_locations"] = SmartCreatePublish.process_geo_location(all_locations)
