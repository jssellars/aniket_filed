import concurrent.futures
import logging
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Any, Dict, Optional

from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from Core.facebook.sdk_adapter.smart_create import ad_builder, adset_builder
from Core.facebook.sdk_adapter.smart_create.targeting import (
    FlexibleTargeting, Location, Targeting)
from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from Core.Tools.Misc.FiledAdFormatEnum import FiledAdFormatEnum
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import \
    get_sdk_structures
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    Level, LevelToGraphAPIStructure)
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from FacebookCampaignsBuilder.Api import commands
from FacebookCampaignsBuilder.Api.startup import config
# TODO move AddStructuresToParent Class to BackgroundTasks
from FacebookCampaignsBuilder.BackgroundTasks.request_handlers import \
    SmartCreatePublish
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import \
    PublishStatus
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
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    que = Queue()
    feedback_data = dict()

    @staticmethod
    def publish_structures_to_parent(
        request: Dict = None,
        permanent_token: str = None,
        user_filed_id: str = None,
        facebook_config: Any = None,
    ):
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        account_id = request.get("ad_account_id", None)
        child_level = request.get("child_level", None)
        parent_level = request.get("parent_level", None)
        parent_ids = request.get("parent_ids", None)
        child_ids = request.get("child_ids", None)

        if parent_level == Level.CAMPAIGN.value and child_level == Level.AD.value:
            parent_level, parent_ids = AddStructuresToParent.get_all_adsets_from_campaign(account_id, parent_ids)

        n_parent, n_child = AddStructuresToParent.get_number_of_parent_and_child(parent_ids, child_ids, request)

        AddStructuresToParent.feedback_data = dict(
            user_filed_id=user_filed_id,
            start_date=datetime.now(),
            ad_account=account_id,
            publish_status=PublishStatus.IN_PROGRESS.value,
            published_structures=0,
            published_adsets=0,
            published_ads=0,
            total_structures=n_parent * n_child,
        )

        AddStructuresToParent.feedback_repository.add_one(AddStructuresToParent.feedback_data)

        db_updater_thread = Thread(target=AddStructuresToParent.update_db, args=())
        db_updater_thread.start()

        if child_ids and parent_ids:
            new_structures = AddStructuresToParent._publish_structures_from_ids(
                parent_level, child_level, child_ids, parent_ids
            )
        elif child_level == Level.ADSET.value and "adsets" in request and parent_ids:
            new_structures = AddStructuresToParent._publish_adset_to_campaigns(
                request["ad_account_id"], request["adsets"], parent_ids
            )
        elif child_level == Level.AD.value and "ads" in request and parent_ids:
            new_structures = AddStructuresToParent._publish_ad_to_adsets(
                request["ad_account_id"], request["ads"], parent_ids
            )
        else:
            raise ValueError("No valid existing keys found in request. Or list of Ids is empty.")
        return {child_level: new_structures}

    @staticmethod
    def get_number_of_parent_and_child(parent_ids, child_ids, request):
        if len(child_ids) > 0:
            return len(parent_ids), len(child_ids)
        elif "ads" in request.keys():
            return len(parent_ids), len(request["ads"])
        elif "adsets" in request.keys():
            n_child = len(request["adsets"])
            for adset in request["adsets"]:
                if "ads" in adset:
                    n_child += len(adset["ads"])
            return len(parent_ids), n_child

    @staticmethod
    def update_db():
        while True:
            feedback_data = AddStructuresToParent.que.get()
            if feedback_data:
                AddStructuresToParent.update_feedback_database(feedback_data)
                if feedback_data["publish_status"] != PublishStatus.IN_PROGRESS.value:
                    return

    @staticmethod
    def get_all_adsets_from_campaign(account_id, campaign_ids):
        adset_parent_ids = []
        fields = [FieldsMetadata.id.name, FieldsMetadata.campaign_id.name]
        response = get_sdk_structures(account_id, Level.ADSET, fields)
        response = [entry.export_all_data() for entry in response]

        for campaign_id in campaign_ids:
            adset_ids = [adset["id"] for adset in response if int(adset["campaign_id"]) == campaign_id]
            adset_parent_ids.extend(adset_ids)

        return Level.ADSET.value, adset_parent_ids

    @staticmethod
    def create_queue(child_level):
        feedback_data_list = list(AddStructuresToParent.que.queue)
        if len(feedback_data_list) == 0:
            feedback_data = deepcopy(AddStructuresToParent.feedback_data)
        else:
            feedback_data = deepcopy(feedback_data_list[-1])

        feedback_data["published_structures"] += 1

        if child_level == Level.AD.value:
            feedback_data["published_ads"] += 1
        elif child_level == Level.ADSET.value:
            feedback_data["published_adsets"] += 1

        if feedback_data["total_structures"] == feedback_data["published_structures"]:
            feedback_data["publish_status"] = PublishStatus.SUCCESS.value

        AddStructuresToParent.que.put(feedback_data)
        AddStructuresToParent.feedback_data = feedback_data

    @staticmethod
    def _publish_structures_from_ids(parent_level, child_level, child_ids, parent_ids):
        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for parent_id in parent_ids:
                for child_id in child_ids:
                    futures.append(
                        executor.submit(
                            AddStructuresToParent._duplicate_structure_on_facebook,
                            parent_level,
                            child_level,
                            child_id,
                            parent_id,
                        )
                    )

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                AddStructuresToParent.create_queue(child_level)

        return results

    @staticmethod
    def _duplicate_structure_on_facebook(parent_level, child_level, facebook_id, parent_id=None):
        structure = LevelToGraphAPIStructure.get(child_level, facebook_id)
        params = AddStructuresToParent._create_duplicate_parameters(parent_level, child_level, parent_id)
        new_structure_id = structure.create_copy(params=params)
        new_structure_id = Tools.convert_to_json(new_structure_id)
        if "ad_object_ids" in new_structure_id:
            return new_structure_id["ad_object_ids"][0]["copied_id"]
        elif "copied_ad_id" in new_structure_id:
            return new_structure_id["copied_ad_id"]
        else:
            raise ValueError("Invalid duplicated structure id.")

    @staticmethod
    def _create_duplicate_parameters(parent_level, child_level, parent_id=None):
        if parent_level == Level.CAMPAIGN.value and child_level == Level.ADSET.value:
            return AddStructuresToParent._duplicate_adset_parameters(parent_id)
        elif parent_level == Level.ADSET.value and child_level == Level.AD.value:
            return AddStructuresToParent._duplicate_ad_parameters(parent_id)
        else:
            raise ValueError(f"Unknown child_level supplied: {child_level}. Please try again using adset or ad")

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
    def update_feedback_database(feedback_data):
        update_fields = {
            "published_structures": feedback_data.get("published_structures", 0),
            "published_campaigns": feedback_data.get("published_campaigns", 0),
            "published_adsets": feedback_data.get("published_adsets", 0),
            "published_ads": feedback_data.get("published_ads", 0),
            "publish_status": feedback_data.get("publish_status"),
        }

        query = {MongoOperator.SET.value: update_fields}

        AddStructuresToParent.feedback_repository.update_many({"user_filed_id": feedback_data["user_filed_id"]}, query)

    @staticmethod
    def _publish_children_to_parents(callback, ad_account_id, requests, parent_ids, child_level):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for parent_id in parent_ids:
                for request in requests:
                    futures.append(executor.submit(callback, ad_account_id, request, parent_id))

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                AddStructuresToParent.create_queue(child_level)

        return results

    @staticmethod
    def _publish_adset_to_campaigns(ad_account_id, adset_requests, parent_ids):
        """
        Take a list of adsets and publish them for the provided list of campaign ids.
        """
        results = AddStructuresToParent._publish_children_to_parents(
            AddStructuresToParent._create_adset_for_campaign,
            ad_account_id,
            adset_requests,
            parent_ids,
            Level.ADSET.value,
        )
        return results

    @staticmethod
    def _publish_ad_to_adsets(ad_account_id, ad_requests, parent_ids):
        """
        Take a list of ads and publish them for the provided list of adset ids.
        """
        results = AddStructuresToParent._publish_children_to_parents(
            AddStructuresToParent._create_ad_for_adset, ad_account_id, ad_requests, parent_ids, Level.AD.value
        )
        return results

    @staticmethod
    def _create_adset_for_campaign(ad_account_id, adset_request, campaign_id):
        """
        Take a list of adSets from request, and for each adSet, create an ad set in the parent campaign.
        Finally return the list of created ad sets.
        NOTE: If Parent Campaign CBO is on, Adset budget will not be set.
        """
        ad_account = AdAccount(fbid=ad_account_id)
        ad_set_template = {
            AdSet.Field.tune_for_category: adset_request.get(AdSet.Field.tune_for_category, AdSet.TuneForCategory.none),
            AdSet.Field.name: adset_request.get("ad_set_name"),
            AdSet.Field.billing_event: adset_request["optimization_and_delivery"].get("billing_event"),
            AdSet.Field.optimization_goal: adset_request["optimization_and_delivery"].get("optimization_goal"),
            AdSet.Field.campaign_id: campaign_id,
        }

        adset_builder.set_statuses(ad_set_template)
        adset_builder.set_date_interval(ad_set_template, adset_request, adset_request)
        # TODO: Check if conversions is required here!
        is_using_conversions = adset_request.get("objective") == "CONVERSIONS"
        adset_builder.set_promoted_object(ad_set_template, is_using_conversions, adset_request, adset_request)

        # Fetch Parent Campaign CBO information to check
        parent_campaign_cbo_info = LevelToGraphAPIStructure.get(Level.CAMPAIGN.value, campaign_id).api_get(
            fields=[FieldsMetadata.daily_budget.name, FieldsMetadata.lifetime_budget.name]
        )
        parent_campaign_not_has_cbo = not (
            parent_campaign_cbo_info.get(FieldsMetadata.daily_budget.name)
            or parent_campaign_cbo_info.get(FieldsMetadata.lifetime_budget.name)
        )

        # If Parent Campaign has CBO, then don't add adset budget
        if parent_campaign_not_has_cbo and ("budget_optimization" in adset_request):
            budget_opt = adset_request.get("budget_optimization")
            # TODO: Discuss proper mapping of bidAmount and bidControl wit FE
            # TODO: Validate Bid Strategy and Bid Control Pairing
            ad_set_template[AdSet.Field.bid_amount] = int(budget_opt.get("bid_control", 0))
            ad_set_template[AdSet.Field.bid_strategy] = budget_opt.get("bid_strategy")

            amount = int(budget_opt["amount"]) * 100
            if budget_opt["budget_allocated_type_id"] == 0:
                ad_set_template[AdSet.Field.lifetime_budget] = amount
            else:
                ad_set_template[AdSet.Field.daily_budget] = amount

        targeting_request = adset_request.get("targeting")
        AddStructuresToParent._set_targeting(ad_set_template, adset_request, targeting_request)
        facebook_ad_set = ad_account.create_ad_set(params=ad_set_template)

        return {
            "adset_id": facebook_ad_set.get_id(),
            "ad_ids": AddStructuresToParent._publish_ad_to_adsets(
                ad_account_id, adset_request["ads"], [facebook_ad_set.get_id()]
            )
            if "ads" in adset_request
            else [],
        }

    @staticmethod
    def _create_ad_for_adset(ad_account_id, ad_request, adset_id):
        ad_account = AdAccount(fbid=ad_account_id)
        # TODO: Modify build_ads function to accept a single argument for necessary fields
        #  as opposed to per step fields

        ads = ad_builder.build_ads(ad_account_id, ad_request, ad_request)

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

        device_platforms, user_device, user_os = [], [], []
        devices = request.get("devices")

        if devices:
            request_device_platforms = list(map(str.lower, devices.get("device_platforms")))
            if request_device_platforms:
                device_platforms = [
                    x.name_sdk
                    for x in DevicePlatform.contexts[Contexts.SMART_CREATE].items
                    if x.name_sdk in request_device_platforms
                ]

            user_device = devices.get("user_device", [])
            user_os = devices.get("user_os", [])

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
            device_platforms=device_platforms,
            user_device=user_device,
            user_os=user_os,
        )

        ad_set_template["targeting"] = asdict(targeting)

        locations = targeting_request.get("locations")
        all_locations = [Location(**location) for location in locations]
        ad_set_template["targeting"]["geo_locations"] = SmartCreatePublish.process_geo_location(all_locations)


class PublishProgress:
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    @staticmethod
    def get_publish_feedback(user_filed_id: int):
        date_key = "start_date"
        query = {"user_filed_id": {MongoOperator.EQUALS.value: user_filed_id}}
        sort_query = [(date_key, -1)]

        feedback_docs = PublishProgress.feedback_repository.get_sorted(query=query, sort_query=sort_query)
        if not feedback_docs:
            return

        feedback = feedback_docs[0]
        if feedback["publish_status"] != PublishStatus.IN_PROGRESS.value:
            PublishProgress.feedback_repository.delete_many({"user_filed_id": user_filed_id})

        feedback[date_key] = feedback[date_key].isoformat()
        feedback.pop("_id")

        return feedback
