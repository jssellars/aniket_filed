import concurrent.futures
import json
import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import Callable, Dict, List, Optional, Tuple, Union

import humps
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookRequestError

from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from Core.facebook.sdk_adapter.smart_create import ad_builder, adset_builder, campaign_builder, mappings
from Core.facebook.sdk_adapter.smart_create.ad_builder import get_ad_creative_id
from Core.facebook.sdk_adapter.smart_create.adset_builder import get_placement_positions
from Core.facebook.sdk_adapter.smart_create.structures import CampaignSplit
from Core.facebook.sdk_adapter.smart_create.targeting import FlexibleTargeting, Location, Targeting
from Core.facebook.sdk_adapter.validations import PLATFORM_X_POSITIONS
from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import get_sdk_structures
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToGraphAPIStructure
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookCampaignsBuilder.BackgroundTasks import dtos
from FacebookCampaignsBuilder.BackgroundTasks.startup import config, fixtures
from FacebookCampaignsBuilder.Infrastructure.Domain.fe_structure_models import CreateAds, CreateAdSet
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.events import (
    AddAdsetAdEvent,
    AddAdsetAdEventMapping,
    AddAdsetAdPublishResponseEvent,
    CampaignCreatedEvent,
    CampaignCreatedEventMapping,
    PublishResponseEvent,
    SmartCreatePublishResponseEvent,
    SmartEditPublishResponseEvent,
    StructureEditedEvent,
    StructureEditedEventMapping,
)
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import PublishStatus
from FacebookCampaignsBuilder.Infrastructure.Mappings.SmartEditField import FacebookEditField

logger = logging.getLogger(__name__)
# TODO: Add the rest of location options into keys
LOCATION_OPTIONS = dict(city="cities", country="countries", geo_market="geo_markets", region="regions", zip="zips")


class SmartCreateOperations:
    @staticmethod
    def delete_incomplete_campaigns(campaign_tree: List[Dict]) -> None:
        for campaign in campaign_tree:
            SmartCreateOperations.delete_campaign(campaign["facebook_id"])
            for ad_set in campaign["ad_sets"]:
                SmartCreateOperations.delete_ad_set(ad_set["facebook_id"])
                for ad_facebook_id in ad_set["ads"]:
                    SmartCreateOperations.delete_ad(ad_facebook_id)

    @staticmethod
    def delete_campaign(facebook_id: str) -> None:
        try:
            campaign = Campaign(fbid=facebook_id)
            campaign.api_delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ad_set(facebook_id: str) -> None:
        try:
            ad_set = AdSet(fbid=facebook_id)
            ad_set.api_delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ad(facebook_id: str) -> None:
        try:
            ad = Ad(fbid=facebook_id)
            ad.api_delete()
        except Exception as e:
            raise e

    @classmethod
    def publish(cls, publish_finished_event: PublishResponseEvent, sync_campaign_event: Union[List, Dict] = None):
        rabbitmq_adapter = fixtures.rabbitmq_adapter
        rabbitmq_adapter.publish(publish_finished_event)
        logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(publish_finished_event)})

        if sync_campaign_event:
            rabbitmq_adapter.publish(sync_campaign_event, on_secondary=True)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(sync_campaign_event)})


class SmartCreatePublish:
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    @staticmethod
    def handle(message_body: Union[str, bytes]) -> List[Dict]:
        body = humps.decamelize(json.loads(message_body))
        request_mapper = mappings.SmartCreatePublishRequest(dtos.SmartCreatePublishRequest)
        request = request_mapper.load(body)

        business_owner_id = request.business_owner_facebook_id
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=config.facebook)

        campaign_tree = []
        campaign_response = {"facebook_id": None, "name": None, "ad_sets": []}

        campaigns, ad_sets, ads = SmartCreatePublish.build_campaign_hierarchy(request)
        ad_account = AdAccount(fbid=request.ad_account_id)

        is_campaign_using_cbo = (
            "campaign_budget_optimization" in request.step_one_details
            and request.step_one_details["campaign_budget_optimization"] is not None
        )
        is_adset_using_cbo = (
            "budget_optimization" in request.step_two_details
            and request.step_two_details["budget_optimization"] is not None
        )
        is_budget_split_evenly = request.step_four_details.get("is_budget_split_evenly")
        budget_allocation = request.step_four_details.get("budget_allocation", {})
        adset_budget_allocation = budget_allocation.get("ad_sets_budget") if budget_allocation else None

        publish_response = SmartCreatePublishResponseEvent(request.template_id)

        feedback_data = dict(
            user_filed_id=request.user_filed_id,
            start_date=datetime.now(),
            ad_account=request.ad_account_id,
            template_id=request.template_id,
            publish_status=PublishStatus.IN_PROGRESS.value,
            published_structures=0,
            published_campaigns=0,
            published_adsets=0,
            published_ads=0,
            total_structures=len(campaigns) + len(campaigns) * len(ad_sets) + len(campaigns) * len(ad_sets) * len(ads),
        )

        SmartCreatePublish.feedback_repository.add_one(feedback_data)

        for campaign_index, campaign in enumerate(campaigns):
            try:
                # Publish campaign
                campaign_budget_type = campaign_builder.get_budget_allocated_type(campaign.campaign_template)
                if is_campaign_using_cbo and is_budget_split_evenly:
                    campaign.campaign_template[campaign_budget_type] /= len(campaigns)

                facebook_campaign = ad_account.create_campaign(params=campaign.campaign_template)
                campaign_facebook_id = facebook_campaign.get_id()
                campaign_name = campaign.campaign_template.get("name")

                feedback_data["published_structures"] += 1
                feedback_data["published_campaigns"] += 1

                # Add new campaign to response
                campaign_tree.append(deepcopy(campaign_response))
                campaign_tree[campaign_index]["facebook_id"] = campaign_facebook_id
                campaign_tree[campaign_index]["name"] = campaign_name

                for ad_set_index, ad_set in enumerate(ad_sets):
                    SmartCreatePublish.populate_missing_adset_fields(campaign_facebook_id, ad_set, campaign)

                    adset_budget_type = (
                        AdSet.Field.lifetime_budget
                        if AdSet.Field.lifetime_budget in ad_set
                        else AdSet.Field.daily_budget
                    )
                    if is_adset_using_cbo:
                        initial_budget = int(request.step_two_details["budget_optimization"]["amount"]) * 100
                        total_adsets = len(campaigns) * len(ad_sets)
                        if is_budget_split_evenly:
                            ad_set[adset_budget_type] = round(initial_budget / total_adsets)
                        elif adset_budget_allocation:
                            ad_set[adset_budget_type] = SmartCreatePublish.allocate_adset_budget(
                                ad_set,
                                adset_budget_allocation,
                                request.step_four_details,
                            )

                    facebook_ad_set = ad_account.create_ad_set(params=ad_set)
                    ad_set_facebook_id = facebook_ad_set.get_id()
                    ad_set_name = ad_set.get("name")

                    feedback_data["published_structures"] += 1
                    feedback_data["published_adsets"] += 1

                    # Add new adset to response
                    ad_set_response = {"facebook_id": ad_set_facebook_id, "name": ad_set_name, "ads": []}
                    campaign_tree[campaign_index]["ad_sets"].append(deepcopy(ad_set_response))

                    for ad_index, ad in enumerate(ads):
                        ad = asdict(ad)
                        [
                            tracking_spec.update({"action.type": tracking_spec.pop("action_type")})
                            for tracking_spec in ad["tracking_specs"]
                        ]

                        ad["tracking_specs"] = [
                            {k: v for k, v in tracking_spec.items() if v is not None}
                            for tracking_spec in ad["tracking_specs"]
                        ]

                        ad.update({Ad.Field.adset_id: ad_set_facebook_id, Ad.Field.adset: ad_set_facebook_id})
                        ad = ad_account.create_ad(params=ad)
                        ad_facebook_id = ad.get_id()
                        campaign_tree[campaign_index]["ad_sets"][ad_set_index]["ads"].append(ad_facebook_id)

                        feedback_data["published_structures"] += 1
                        feedback_data["published_ads"] += 1
                    else:
                        SmartCreatePublish.update_feedback_database(
                            feedback_data,
                            request.template_id,
                            PublishStatus.IN_PROGRESS.value,
                        )

                else:
                    SmartCreatePublish.update_feedback_database(
                        feedback_data,
                        request.template_id,
                        PublishStatus.IN_PROGRESS.value,
                    )
            except FacebookRequestError as e:
                error_message = e.body().get("error", {}).get("error_user_msg") or e.get_message()
                SmartCreatePublish.clean_and_publish_response(
                    campaign_tree=campaign_tree,
                    error_message=error_message,
                    feedback_data=feedback_data,
                    publish_response=publish_response,
                    template_id=request.template_id,
                )
                raise

            except Exception:
                SmartCreatePublish.clean_and_publish_response(
                    campaign_tree=campaign_tree,
                    error_message="Something went wrong!",
                    feedback_data=feedback_data,
                    publish_response=publish_response,
                    template_id=request.template_id,
                )
                raise
        else:
            SmartCreatePublish.update_feedback_database(feedback_data, request.template_id, PublishStatus.SUCCESS.value)

        campaign_event = SmartCreatePublish.build_campaign_event(
            request.ad_account_id, business_owner_id, campaign_tree
        )
        SmartCreateOperations.publish(publish_response, campaign_event)

        return campaign_tree

    @staticmethod
    def clean_and_publish_response(
        campaign_tree: List[Dict],
        error_message: str,
        feedback_data: Dict,
        publish_response: PublishResponseEvent,
        template_id: str,
    ) -> None:
        SmartCreatePublish.update_feedback_database(
            feedback_data, template_id, PublishStatus.FAILED.value, error=error_message
        )
        SmartCreateOperations.delete_incomplete_campaigns(campaign_tree)
        publish_response.publish_status_id = PublishStatus.FAILED.value
        SmartCreateOperations.publish(publish_response)

    @staticmethod
    def build_campaign_event(
        ad_account_id: str, business_owner_id: str, campaign_tree: List[Dict]
    ) -> Union[List, Dict]:
        mapper = CampaignCreatedEventMapping(target=CampaignCreatedEvent)
        response = mapper.load(campaign_tree)
        response.business_owner_id = business_owner_id
        response.account_id = ad_account_id
        return response

    @staticmethod
    def update_feedback_database(
        feedback_data: Dict, template_id: str, status: PublishStatus, error: str = None
    ) -> None:
        update_fields = {
            "published_structures": feedback_data.get("published_structures", 0),
            "published_campaigns": feedback_data.get("published_campaigns", 0),
            "published_adsets": feedback_data.get("published_adsets", 0),
            "published_ads": feedback_data.get("published_ads", 0),
            "publish_status": status,
        }

        if error:
            update_fields["error"] = error

        query = {MongoOperator.SET.value: update_fields}

        SmartCreatePublish.feedback_repository.update_many({"template_id": template_id}, query)

    @staticmethod
    def build_campaign_hierarchy(request: dtos.SmartCreatePublishRequest) -> Tuple[List, List, List]:
        destination_type = request.step_one_details.get("destination_type")
        is_using_conversions = request.step_one_details["objective"] == "CONVERSIONS"
        is_using_cbo = (
            "campaign_budget_optimization" in request.step_one_details
            and request.step_one_details["campaign_budget_optimization"] is not None
        )

        # Build campaigns
        campaigns = campaign_builder.build_campaigns(
            step_one=request.step_one_details,
            step_two=request.step_two_details,
            step_four=request.step_four_details,
        )

        # Build ad_sets
        ad_sets = adset_builder.build_ad_sets(
            step_one=request.step_one_details,
            step_two=request.step_two_details,
            step_three=request.step_three_details,
            step_four=request.step_four_details,
            is_using_cbo=is_using_cbo,
            is_using_conversions=is_using_conversions,
            destination_type=destination_type,
        )

        # Build ads
        ads = ad_builder.build_ads(
            request.ad_account_id,
            request.step_two_details,
            request.step_three_details,
            request.step_one_details["objective"],
        )

        return campaigns, ad_sets, ads

    @staticmethod
    def populate_missing_adset_fields(campaign_facebook_id: str, ad_set: Dict, parent_campaign: CampaignSplit) -> None:
        ad_set["campaign_id"] = campaign_facebook_id
        if parent_campaign.location:
            ad_set["targeting"]["geo_locations"] = SmartCreatePublish.process_geo_location([parent_campaign.location])
        else:
            ad_set["targeting"]["geo_locations"] = SmartCreatePublish.process_geo_location(
                parent_campaign.all_locations
            )

        if parent_campaign.device:
            ad_set["targeting"]["device_platforms"] = [parent_campaign.device]

    @staticmethod
    def process_geo_location(locations: List[Location]) -> Dict:
        result = defaultdict(list)

        for location in locations:
            if location.type == "country":
                result[LOCATION_OPTIONS[location.type]].append(location.country_code)
            else:
                result[LOCATION_OPTIONS[location.type]].append({"key": location.key})

        return result

    @staticmethod
    def allocate_adset_budget(
        adset_create_template: Dict,
        adset_budget_allocation: Dict,
        step_four: Dict,
    ) -> Union[int, float]:
        targeting = adset_create_template["targeting"]

        device, location = SmartCreatePublish.get_location_device(step_four, targeting)
        campaign_split_fields = dict(location=location, device=device)

        age_split, gender = SmartCreatePublish.get_gender_age_split(step_four, targeting)
        adset_split_fields = dict(gender=gender, age_split=age_split)

        for allocation in adset_budget_allocation:
            allocation_location = allocation.get("location")
            if isinstance(allocation_location, list):
                location = set(allocation_location)
            else:
                location = allocation_location
            allocation_location_device = dict(location=location, device=allocation.get("device"))

            if campaign_split_fields == allocation_location_device:
                adset_allocations = allocation.get("ad_sets")

                for adset_allocation in adset_allocations:
                    if "budget" in adset_allocation:
                        budget = adset_allocation.pop("budget")
                        adset_allocation.pop("ad_set_name", None)
                    else:
                        continue

                    if adset_split_fields == adset_allocation:
                        return budget * 100
                    else:
                        adset_allocation.setdefault("budget", budget)

    @staticmethod
    def get_gender_age_split(step_four: Dict, targeting: Dict) -> Tuple[Dict, str]:
        # FE will send gender:null if adsets aren't split by genders
        targeting_genders = targeting["genders"]
        gender = targeting_genders if step_four.get("is_split_by_gender_selected") else None
        if isinstance(gender, list):
            gender = gender[0]

        # FE will send age_split:null if adsets aren't split by age
        age_split = (
            dict(
                min=targeting["age_min"],
                max=targeting["age_max"],
            )
            if step_four.get("is_split_age_range_selected")
            else None
        )

        return age_split, gender

    @staticmethod
    def get_location_device(step_four: Dict, targeting: Dict) -> Tuple[Optional[str], List]:
        # Refer to SmartCreate.process_geo_location for how location is encoded inside targeting
        location = []
        if step_four.get("is_split_by_location"):
            for _, location_type in LOCATION_OPTIONS.items():
                geo_locations = targeting["geo_locations"].get(location_type)
                if not geo_locations:
                    continue
                elif isinstance(geo_locations, list):
                    if location_type == "countries":
                        location.extend(geo_locations)
                    else:
                        location.extend([loc.get("key") for loc in geo_locations])
                else:
                    if location_type == "countries":
                        location.append(geo_locations)
                    else:
                        location.append(geo_locations.get("key"))

            if len(location) == 1:
                location = location[0]
            else:
                location = set(location)
        else:
            location = None

        # FE will send device:null if campaigns aren't split by devices
        # BE represents no device split as device:['desktop','mobile']
        device_platforms = targeting["device_platforms"]
        device = device_platforms[0] if len(device_platforms) == 1 else None

        return device, location


class SmartEditPublish:
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )
    feedback_data = dict()
    queue = Queue()

    @staticmethod
    def handle(message_body: Union[str, bytes]) -> List[Dict]:
        body = humps.decamelize(json.loads(message_body))
        request_mapper = mappings.SmartEditPublishRequest(dtos.SmartEditPublishRequest)
        request = request_mapper.load(body)

        business_owner_id = request.business_owner_facebook_id
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=config.facebook)
        publish_response = SmartEditPublishResponseEvent()

        ad_account = request.ad_account_id

        campaigns = request.campaigns
        adsets = request.adsets
        ads = request.ads

        SmartEditPublish.feedback_data = dict(
            user_filed_id=request.user_filed_id,
            start_date=datetime.now(),
            ad_account=ad_account,
            publish_status=PublishStatus.IN_PROGRESS.value,
            published_structures=0,
            published_campaigns=0,
            published_adsets=0,
            published_ads=0,
            # TODO: this might change if we add the publish children part
            total_structures=len(campaigns) + len(adsets) + len(ads),
        )

        SmartEditPublish.feedback_repository.add_one(SmartEditPublish.feedback_data)

        db_updater_thread = Thread(target=SmartEditPublish.update_db, args=())
        db_updater_thread.start()

        structures = {}

        try:
            structures["campaign_tree"] = SmartEditPublish.process_structures_concurrently(
                SmartEditPublish.edit_campaigns, campaigns, Level.CAMPAIGN.value
            )
            structures["adset_tree"] = SmartEditPublish.process_structures_concurrently(
                SmartEditPublish.edit_adsets, adsets, Level.ADSET.value
            )
            structures["ad_tree"] = SmartEditPublish.process_structures_concurrently(
                SmartEditPublish.edit_ads, ads, Level.AD.value)
        except FacebookRequestError as e:
            error_message = e.body().get("error", {}).get("error_user_msg") or e.get_message()
            SmartEditPublish.feedback_data["error"] = error_message
            SmartEditPublish.feedback_data["publish_status"] = PublishStatus.FAILED.value
            SmartEditPublish.queue.put(SmartEditPublish.feedback_data)
            SmartEditPublish.update_feedback_database(SmartEditPublish.feedback_data)

        response = list()
        response.append({"campaigns": structures.get("campaign_tree")})
        response.append({"ad_sets": structures.get("adset_tree")})
        response.append({"ads": structures.get("ad_tree")})

        edit_event = SmartEditPublish.build_edit_event(request.ad_account_id, business_owner_id, structures.get("campaign_tree"))
        SmartCreateOperations.publish(publish_response, edit_event)

        return response

    @staticmethod
    def process_structures_concurrently(function: Callable, structures: List, level: str) -> List[Dict]:
        structure_tree = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(function, structure): structure for structure in structures}

            for future in concurrent.futures.as_completed(futures):
                structure_tree.append(future.result())
                SmartEditPublish.add_feedback_to_queue(level)
        return structure_tree

    @staticmethod
    def edit_adsets(adset: Dict) -> Dict:
        adset_response = {"ad_set_id": None, "ads": []}

        try:
            # TODO add logic for creating ads to existing adsets
            additional_ads = adset.pop("ads", None)

            facebook_adset = SmartEditPublish.update_adset(adset)
            # Add updated adset to response
            adset_facebook_id = facebook_adset.get_id()
            adset_response["ad_set_id"] = adset_facebook_id
        except FacebookRequestError as e:
            raise e
        except Exception:
            raise

        return adset_response

    @staticmethod
    def update_adset(adset: Dict) -> AdSet:
        params = {
            AdSet.Field.name: adset.get("ad_set_name"),
        }
        opt_and_delivery = adset.get("optimization_and_delivery")
        if opt_and_delivery:
            params[AdSet.Field.optimization_goal] = opt_and_delivery["optimization_goal"]
            params[AdSet.Field.billing_event] = opt_and_delivery["billing_event"]

        date = adset.get("date")
        if date:
            # TODO discuss with FE about not being able to edit start date when it's already passed
            params[AdSet.Field.start_time] = date.get("start_date")
            params[AdSet.Field.end_time] = date.get("end_date")

        SmartEditPublish.set_adset_budget(adset, params)
        SmartEditPublish.set_targeting(adset, params)

        facebook_adset = AdSet(fbid=adset.get("ad_set_id"))
        facebook_adset.api_update(params=params)

        return facebook_adset

    @staticmethod
    def set_adset_budget(adset: Dict, params: Dict) -> None:
        budget_opt = adset.get("budget_optimization")
        if not budget_opt:
            return

        amount = int(budget_opt["amount"]) * 100
        if budget_opt["budget_allocated_type_id"] == 0:
            params[AdSet.Field.lifetime_budget] = amount
        else:
            params[AdSet.Field.daily_budget] = amount

        # TODO discuss with FE regarding bid control not allowed with LOWEST_COST_WITHOUT_CAP bid strategy
        params[AdSet.Field.bid_amount] = budget_opt.get("bid_control")
        params[AdSet.Field.bid_strategy] = budget_opt.get("bid_strategy")
        params[AdSet.Field.pacing_type] = [budget_opt.get("delivery_type")]

    @staticmethod
    def set_targeting(adset: Dict, params: Dict) -> None:
        targeting_request = adset.get("targeting")
        if not targeting_request:
            return

        languages = targeting_request.get("languages", [])
        if languages:
            languages = [language["key"] for language in languages]

        included_interests, excluded_interests, narrow_interests = adset_builder.extract_interests(targeting_request)
        included_custom_audiences, excluded_custom_audiences = adset_builder.extract_custom_audiences(targeting_request)

        flexible_spec = [FlexibleTargeting(included_interests)]
        adset_targeting = Targeting(
            flexible_spec,
            custom_audiences=included_custom_audiences,
            excluded_custom_audiences=excluded_custom_audiences,
            exclusions=FlexibleTargeting(interests=excluded_interests),
            locales=languages,
        )
        age_range = targeting_request.get("age_range")
        if age_range:
            adset_targeting.age_min = age_range["min_age"]
            adset_targeting.age_max = age_range["max_age"]

        gender = targeting_request.get("gender")
        if gender:
            adset_targeting.genders = [gender]

        geo_locations = targeting_request.get("locations")
        if geo_locations:
            location_objects = []
            for geo_location in geo_locations:
                location_objects.append(Location(**geo_location))

            adset_targeting.geo_locations = dict(SmartCreatePublish.process_geo_location(location_objects))

        devices = adset.get("devices")
        if devices:
            request_device_platforms = list(map(str.lower, devices.get("device_platforms")))
            request_user_os = devices.get("user_os")
            request_user_device = devices.get("user_device")
            if request_device_platforms:
                device_platforms = [
                    x.name_sdk
                    for x in DevicePlatform.contexts[Contexts.SMART_CREATE].items
                    if x.name_sdk in request_device_platforms
                ]
                adset_targeting.device_platforms = device_platforms
            if request_user_os:
                adset_targeting.user_os = request_user_os
            if request_user_device:
                adset_targeting.user_device = request_user_device

        placements = adset.get("placements")
        if placements:
            publisher_platforms, platform_positions = get_placement_positions(placements)

            adset_targeting.publisher_platforms = publisher_platforms

            if platform_positions:
                for platform_position, positions in platform_positions.items():
                    adset_targeting.__setattr__(platform_position, positions)

        params[AdSet.Field.targeting] = asdict(adset_targeting)

    @staticmethod
    def get_platform_positions(adset: Dict) -> Optional[Tuple[List[str], Dict]]:
        placements = adset.get("placements")
        result_positions = defaultdict(list)
        publisher_platforms = []
        if not placements:
            return
        for placement in placements:
            for platform, positions in PLATFORM_X_POSITIONS.items():
                if placement["name"] != platform.name:
                    continue
                publisher_platforms.append(platform.value.name_sdk.lower())
                request_positions = placement.get("positions")
                if not request_positions:
                    continue
                for request_position in request_positions:
                    for key, value in positions.items():
                        if isinstance(key, str):
                            continue
                        if request_position == key.name:
                            result_positions[f"{platform.name.lower()}_positions"].append(value)
        return publisher_platforms, result_positions

    @staticmethod
    def edit_campaigns(campaign: Dict) -> Dict:
        campaign_response = {"campaign_id": None, "ad_sets": [], "ads": []}

        try:
            # TODO add logic for creating adsets and ads to existing campaign
            additional_adsets = campaign.pop("adsets", {})
            additional_ads = additional_adsets.pop("ads", None)

            facebook_campaign = SmartEditPublish.update_campaign(campaign)

            # Add updated campaign to response
            campaign_facebook_id = facebook_campaign.get_id()
            campaign_response["campaign_id"] = campaign_facebook_id
        except FacebookRequestError as e:
            raise e
        except Exception:
            raise

        return campaign_response

    @staticmethod
    def update_campaign(campaign: Dict) -> Campaign:
        special_ad_categories = []
        params = {
            Campaign.Field.name: campaign.get("campaign_name"),
            Campaign.Field.buying_type: campaign.get(Campaign.Field.buying_type),
            Campaign.Field.objective: campaign.get(Campaign.Field.objective),
            Campaign.Field.special_ad_categories: special_ad_categories.append(
                campaign.get(Campaign.Field.special_ad_category)
            ),
        }

        budget = campaign.get("campaign_budget_optimization")
        if budget:
            campaign_builder.set_budget_optimization(params, budget)

        budget_optimization = campaign.get("budget_optimization")
        if budget_optimization:
            SmartEditPublish.disable_cbo(budget_optimization, params)

        facebook_campaign = Campaign(fbid=campaign.get("campaign_id"))
        facebook_campaign.api_update(params=params)

        return facebook_campaign

    @staticmethod
    def disable_cbo(budget_optimization: Dict, params: Dict) -> None:
        adset_budgets = budget_optimization.get("adset_budget_amounts")
        if adset_budgets:
            adset_budgets_templates = list()
            for adset in adset_budgets:
                adset_budget_template = {"adset_id": adset.get("ad_set_id")}
                SmartEditPublish.set_budget_optimization(adset_budget_template, adset)
                adset_budgets_templates.append(adset_budget_template)
            params["adset_budgets"] = adset_budgets_templates

        adset_bids = budget_optimization.get("adset_bid_amounts")
        if adset_bids:
            params["bid_strategy"] = Campaign.BidStrategy.lowest_cost_with_bid_cap
            params["adset_bid_amounts"] = adset_bids
        else:
            params["bid_strategy"] = Campaign.BidStrategy.lowest_cost_without_cap

        return None

    @staticmethod
    def set_budget_optimization(adset_budget_template: Dict, budget_opt: Dict) -> None:
        amount = int(budget_opt["amount"]) * 100
        if budget_opt["budget_allocated_type_id"] == 0:
            adset_budget_template[Campaign.Field.lifetime_budget] = amount
        else:
            adset_budget_template[Campaign.Field.daily_budget] = amount
        return None

    @staticmethod
    def edit_ads(ad: Dict) -> Dict:
        ad_response = {"ad_id": None}

        try:
            facebook_ad = SmartEditPublish.update_ad(ad)
            # Add updated ad to response
            ad_facebook_id = facebook_ad.get_id()
            ad_response["ad_id"] = ad_facebook_id
        except FacebookRequestError as e:
            raise e
        except Exception:
            raise

        return ad_response

    @staticmethod
    def update_ad(ad: Dict) -> Ad:
        facebook_ad = Ad(ad.get("ad_id"))
        params = {
            Ad.Field.name: ad.get("ad_name"),
        }

        for key in ad:
            if key in FacebookEditField.Ad.__members__:
                params[FacebookEditField.Ad[key].value] = ad[key]

        if "adverts" in ad:
            facebook_ad.api_get(fields=[Ad.Field.campaign, Ad.Field.account_id])
            facebook_campaign = facebook_ad.get(Ad.Field.campaign)
            objective = facebook_campaign.api_get(fields=[Campaign.Field.objective]).get(Campaign.Field.objective)
            ad_creative_id = get_ad_creative_id(
                ad_creative_type=int(ad["ad_format_type"]),
                ad_account_id=f"act_{facebook_ad.get(Ad.Field.account_id)}",
                step_two=ad,
                adverts=ad["adverts"],
                objective=objective
            )
            params[FacebookEditField.Ad.ad_creative.value] = {"creative_id": ad_creative_id}

        if "pixel_id" in ad or "pixel_app_event_id" in ad:
            ad = [asdict(tracking_spec) for tracking_spec in CreateAds.get_tracking_specs(ad)]

            # Facebook requires "action.type" instead of "action_type"
            [tracking_spec.update({"action.type": tracking_spec.pop("action_type")}) for tracking_spec in ad]
            # Removing null fields
            ad = [{k: v for k, v in tracking_spec.items() if v is not None} for tracking_spec in ad]

            params[FacebookEditField.Ad.tracking_specs.value] = ad

        facebook_ad.api_update(params=params)

        return facebook_ad

    @staticmethod
    def update_ads(ads: Dict, ad_account_id: str) -> List[Dict]:
        updated_ads = []

        for ad in ads:
            param = {}
            updated_ad = {}
            ad_id = ad.pop("ad_id")
            for key in ad:
                if key in FacebookEditField.Ad.__members__:
                    param[FacebookEditField.Ad[key].value] = ad[key]

            if "adverts" in ad:
                ad_creative_id = get_ad_creative_id(
                    ad_creative_type=int(ad["ad_format_type"]),
                    ad_account_id=ad_account_id,
                    step_two=ad,
                    adverts=ad["adverts"],
                    objective=Optional[None],
                )
                param[FacebookEditField.Ad.ad_creative.value] = {"creative_id": ad_creative_id}

            if "pixel_id" in ad or "pixel_app_event_id" in ad:
                ad = [asdict(tracking_spec) for tracking_spec in CreateAds.get_tracking_specs(ad)]

                # Facebook requires "action.type" instead of "action_type"
                [tracking_spec.update({"action.type": tracking_spec.pop("action_type")}) for tracking_spec in ad]
                # Removing null fields
                ad = [{k: v for k, v in tracking_spec.items() if v is not None} for tracking_spec in ad]

                param[FacebookEditField.Ad.tracking_specs.value] = ad

            facebook_ads = Ad(ad_id)
            facebook_ads.api_update(params=param)
            updated_ad["ad_id"] = ad_id
            updated_ads.append(updated_ad)

        return updated_ads

    @staticmethod
    def add_feedback_to_queue(level: str) -> None:
        feedback_data_list = list(SmartEditPublish.queue.queue)
        if len(feedback_data_list) == 0:
            feedback_data = deepcopy(SmartEditPublish.feedback_data)
        else:
            feedback_data = deepcopy(feedback_data_list[-1])

        feedback_data["published_structures"] += 1

        if level == Level.AD.value:
            feedback_data["published_ads"] += 1
        elif level == Level.ADSET.value:
            feedback_data["published_adsets"] += 1
        elif level == Level.CAMPAIGN.value:
            feedback_data["published_campaigns"] += 1

        if feedback_data["total_structures"] == feedback_data["published_structures"]:
            feedback_data["publish_status"] = PublishStatus.SUCCESS.value

        SmartEditPublish.queue.put(feedback_data)
        SmartEditPublish.feedback_data = feedback_data

    @staticmethod
    def update_db() -> None:
        while True:
            feedback_data = SmartEditPublish.queue.get()
            if feedback_data:
                SmartEditPublish.update_feedback_database(feedback_data)
                if feedback_data["publish_status"] != PublishStatus.IN_PROGRESS.value:
                    return

    @staticmethod
    def update_feedback_database(feedback_data: Dict) -> None:
        update_fields = {
            "published_structures": feedback_data.get("published_structures", 0),
            "published_campaigns": feedback_data.get("published_campaigns", 0),
            "published_adsets": feedback_data.get("published_adsets", 0),
            "published_ads": feedback_data.get("published_ads", 0),
            "publish_status": feedback_data.get("publish_status"),
        }

        if "error" in feedback_data:
            update_fields["error"] = feedback_data.get("error")

        query = {MongoOperator.SET.value: update_fields}

        SmartEditPublish.feedback_repository.update_many({"user_filed_id": feedback_data["user_filed_id"]}, query)

    @staticmethod
    def build_edit_event(ad_account_id: str, business_owner_id: str, structure_tree: List[Dict]) -> Dict:
        if not structure_tree:
            return {}
        mapper = StructureEditedEventMapping(target=StructureEditedEvent)
        response = mapper.load(structure_tree)
        response.business_owner_id = business_owner_id
        response.account_id = ad_account_id
        return response


class AddStructuresToParent:
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    que = Queue()
    feedback_data = dict()

    @staticmethod
    def handle(message_body: Union[str, bytes]) -> Dict[str, List]:
        body = humps.decamelize(json.loads(message_body))
        request_mapper = mappings.AddAdsetAdPublishRequest(dtos.AddAdsetAdPublishRequest)
        request = request_mapper.load(body)

        business_owner_id = request.business_owner_facebook_id
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=config.facebook)

        account_id = request.ad_account_id
        user_filed_id = request.user_filed_id
        child_level = request.child_level
        parent_level = request.parent_level
        parent_ids = request.parent_ids
        child_ids = request.child_ids
        request = asdict(request)

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

        campaign_event = AddStructuresToParent.build_add_adset_ad_event(account_id, business_owner_id, new_structures)
        publish_response = AddAdsetAdPublishResponseEvent()
        SmartCreateOperations.publish(publish_response, campaign_event)

        return {child_level: new_structures}

    @staticmethod
    def get_number_of_parent_and_child(parent_ids, child_ids, request: Dict) -> Tuple[int, int]:
        if len(child_ids) > 0:
            return len(parent_ids), len(child_ids)
        elif "ads" in request and len(request["ads"]) > 0:
            return len(parent_ids), len(request["ads"])
        elif "adsets" in request and len(request["adsets"]) > 0:
            n_child = len(request["adsets"])
            for adset in request["adsets"]:
                if "ads" in adset:
                    n_child += len(adset["ads"])
            return len(parent_ids), n_child

    @staticmethod
    def update_db() -> None:
        while True:
            feedback_data = AddStructuresToParent.que.get()
            if feedback_data:
                AddStructuresToParent.update_feedback_database(feedback_data)
                if feedback_data["publish_status"] != PublishStatus.IN_PROGRESS.value:
                    return

    @staticmethod
    def get_all_adsets_from_campaign(account_id: str, campaign_ids: List[str]) -> Tuple[Level, List[str]]:
        fields = [FieldsMetadata.id.name, FieldsMetadata.campaign_id.name]
        response = get_sdk_structures(account_id, Level.ADSET, fields)
        response = [entry.export_all_data() for entry in response]

        adset_parent_ids = [adset["id"] for adset in response if adset["campaign_id"] in campaign_ids]

        return Level.ADSET.value, adset_parent_ids

    @staticmethod
    def create_queue(child_level: str) -> None:
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
    def _publish_structures_from_ids(
        parent_level: str, child_level: str, child_ids: List[str], parent_ids: List[str]
    ) -> List[Dict]:
        results = []

        if (parent_level, child_level) == (Level.CAMPAIGN.value, Level.ADSET.value):
            clones_map = {}
            for campaign_id in parent_ids:
                for adset_id in child_ids:
                    new_adset_id = AddStructuresToParent._duplicate_structure_on_facebook(
                        parent_level, child_level, adset_id, campaign_id
                    )["adset_ids"][0]

                    orig_fb_adset = AdSet(fbid=adset_id)
                    ad_ids = [ad.get_id() for ad in (orig_fb_adset.get_ads(fields=["id"]))]
                    clones_map[new_adset_id] = ad_ids
                    # Update feedback data and database
                    AddStructuresToParent.create_queue(child_level)
                    AddStructuresToParent.feedback_data["total_structures"] += len(ad_ids)
                    AddStructuresToParent.que.put(AddStructuresToParent.feedback_data)
                    AddStructuresToParent.update_feedback_database(AddStructuresToParent.feedback_data)

            for new_adset_id, ad_ids in clones_map.items():
                if not ad_ids:
                    continue
                new_ad_ids = AddStructuresToParent.make_copies(
                    ad_ids, Level.AD.value, [new_adset_id], Level.ADSET.value
                )

                results.append(
                    {
                        new_adset_id: new_ad_ids,
                    }
                )
        else:
            results.append(AddStructuresToParent.make_copies(child_ids, child_level, parent_ids, parent_level))

        return results

    @staticmethod
    def make_copies(child_ids: List, child_level: str, parent_ids: List, parent_level: str):
        new_copies = []
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
                new_copies.extend(future.result()[f"{child_level}_ids"])
                AddStructuresToParent.create_queue(child_level)

            return new_copies

    @staticmethod
    def _duplicate_structure_on_facebook(parent_level: str, child_level: str, facebook_id: str, parent_id: str) -> dict:
        structure_ids = {
            f"{child_level}_ids": []
        }
        try:
            structure = LevelToGraphAPIStructure.get(child_level, facebook_id)
            params = AddStructuresToParent._create_duplicate_parameters(parent_level, child_level, parent_id)
            new_structure_id = structure.create_copy(params=params)
            new_structure_id = Tools.convert_to_json(new_structure_id)
            # Reference https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/copies/#async
            if "ad_object_ids" in new_structure_id:
                structure_ids[f"{child_level}_ids"].append(new_structure_id["ad_object_ids"][0]["copied_id"])
            elif "copied_ad_id" in new_structure_id:
                structure_ids[f"{child_level}_ids"].append(new_structure_id["copied_ad_id"])
            else:
                raise ValueError("Invalid duplicated structure id.")
        except FacebookRequestError as e:
            error_message = e.body().get("error", {}).get("error_user_msg") or e.get_message()
            structure_ids["error_message"] = error_message
            AddStructuresToParent.feedback_data["error"] = error_message
            AddStructuresToParent.feedback_data["publish_status"] = PublishStatus.FAILED.value
            AddStructuresToParent.que.put(AddStructuresToParent.feedback_data)
            AddStructuresToParent.update_feedback_database(AddStructuresToParent.feedback_data)

        return structure_ids

    @staticmethod
    def _create_duplicate_parameters(parent_level: str, child_level: str, parent_id: str) -> Dict:
        if parent_level == Level.CAMPAIGN.value and child_level == Level.ADSET.value:
            return AddStructuresToParent._duplicate_adset_parameters(parent_id)
        elif parent_level == Level.ADSET.value and child_level == Level.AD.value:
            return AddStructuresToParent._duplicate_ad_parameters(parent_id)
        else:
            raise ValueError(f"Unknown child_level supplied: {child_level}. Please try again using adset or ad")

    @staticmethod
    def _duplicate_adset_parameters(parent_id: str) -> Dict:
        parameters = {
            "campaign_id": parent_id,
            "deep_copy": False,
            "status_option": AdSet.StatusOption.paused,
        }
        return parameters

    @staticmethod
    def _duplicate_ad_parameters(parent_id: str) -> Dict:
        parameters = {"adset_id": parent_id, "status_option": Ad.StatusOption.paused}
        return parameters

    @staticmethod
    def update_feedback_database(feedback_data: Dict) -> None:
        update_fields = {
            "published_structures": feedback_data.get("published_structures", 0),
            "published_campaigns": feedback_data.get("published_campaigns", 0),
            "published_adsets": feedback_data.get("published_adsets", 0),
            "published_ads": feedback_data.get("published_ads", 0),
            "publish_status": feedback_data.get("publish_status"),
            "total_structures": feedback_data.get("total_structures"),
        }

        if "error" in feedback_data:
            update_fields["error"] = feedback_data.get("error")

        query = {MongoOperator.SET.value: update_fields}

        AddStructuresToParent.feedback_repository.update_many({"user_filed_id": feedback_data["user_filed_id"]}, query)

    @staticmethod
    def _publish_children_to_parents(
        callback: Callable, ad_account_id: str, requests: List, parent_ids: List, child_level: str
    ) -> List:
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
    def _publish_adset_to_campaigns(ad_account_id: str, adset_requests: List, parent_ids: List) -> List:
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
    def _publish_ad_to_adsets(ad_account_id: str, ad_requests: List, parent_ids: List) -> List:
        """
        Take a list of ads and publish them for the provided list of adset ids.
        """
        results = AddStructuresToParent._publish_children_to_parents(
            AddStructuresToParent._create_ad_for_adset, ad_account_id, ad_requests, parent_ids, Level.AD.value
        )
        return results

    @staticmethod
    def _create_adset_for_campaign(ad_account_id: str, adset_request: dict, campaign_id: str) -> dict:
        """
        Take an adset request object, and create an adset in the parent campaign.
        Finally return the dictionary of 1. created adset id, and 2. list of ad ids (if any).
        NOTE: If Parent Campaign CBO is on, Adset budget will not be set.
        """
        ad_account = AdAccount(fbid=ad_account_id)

        structure_ids = {}

        try:
            ad_set_template = CreateAdSet(
                tune_for_category=adset_request.get(AdSet.Field.tune_for_category, AdSet.TuneForCategory.none),
                name=adset_request.get("ad_set_name"),
                billing_event=adset_request["optimization_and_delivery"].get("billing_event"),
                optimization_goal=adset_request["optimization_and_delivery"].get("optimization_goal"),
                campaign_id=campaign_id,
            )

            adset_builder.set_statuses_dto(ad_set_template)
            adset_builder.set_date_interval_dto(ad_set_template, adset_request["date"])
            # TODO: Check if conversions is required here!
            objective = adset_request.get("objective")
            ad_set_template.set_promoted_object_fields(
                adset_builder.get_promoted_object(objective, adset_request, adset_request.get("facebook_page_id"))
            )

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
                bid_control = int(budget_opt.get("bid_control", 0))
                if bid_control:
                    ad_set_template.bid_amount = bid_control * 100
                    ad_set_template.bid_strategy = Campaign.BidStrategy.lowest_cost_with_bid_cap
                else:
                    ad_set_template.bid_strategy = Campaign.BidStrategy.lowest_cost_without_cap
                ad_set_template.set_budget_opt(budget_opt["amount"], budget_opt["budget_allocated_type_id"])

            targeting_request = adset_request.get("targeting")
            ad_set_template.targeting = AddStructuresToParent._set_targeting(adset_request, targeting_request)
            ad_set_template = asdict(ad_set_template)

            facebook_ad_set = ad_account.create_ad_set(params=ad_set_template)
            structure_ids = {
                "adset_id": facebook_ad_set.get_id(),
                "ad_ids": AddStructuresToParent._publish_ad_to_adsets(
                    ad_account_id, adset_request["ads"], [facebook_ad_set.get_id()]
                )
                if "ads" in adset_request
                else [],
            }
        except FacebookRequestError as e:
            error_message = e.body().get("error", {}).get("error_user_msg") or e.get_message()
            structure_ids["error_message"] = error_message
            AddStructuresToParent.feedback_data["error"] = error_message
            AddStructuresToParent.feedback_data["publish_status"] = PublishStatus.FAILED.value
            AddStructuresToParent.que.put(AddStructuresToParent.feedback_data)
            AddStructuresToParent.update_feedback_database(AddStructuresToParent.feedback_data)

        return structure_ids

    @staticmethod
    def _create_ad_for_adset(ad_account_id: str, ad_request: Dict, adset_id: str) -> dict:
        ad_account = AdAccount(fbid=ad_account_id)
        # TODO: Modify build_ads function to accept a single argument for necessary fields
        #  as opposed to per step fields

        ads = ad_builder.build_ads(ad_account_id, ad_request, {"ads": [ad_request]})

        structure_ids = {
            "ad_ids": []
        }
        for ad in ads:
            try:
                ad = asdict(ad)

                [
                    tracking_spec.update({"action.type": tracking_spec.pop("action_type")})
                    for tracking_spec in ad["tracking_specs"]
                ]

                ad["tracking_specs"] = [
                    {k: v for k, v in tracking_spec.items() if v is not None} for tracking_spec in ad["tracking_specs"]
                ]

                ad.update({Ad.Field.adset_id: adset_id, Ad.Field.adset: adset_id})
                ad = ad_account.create_ad(params=ad)
                structure_ids["ad_ids"].append(ad.get_id())

            except FacebookRequestError as e:
                error_message = e.body().get("error", {}).get("error_user_msg") or e.get_message()
                structure_ids["error_message"] = error_message
                AddStructuresToParent.feedback_data["error"] = error_message
                AddStructuresToParent.feedback_data["publish_status"] = PublishStatus.FAILED.value
                AddStructuresToParent.que.put(AddStructuresToParent.feedback_data)
                AddStructuresToParent.update_feedback_database(AddStructuresToParent.feedback_data)

            return structure_ids

    @staticmethod
    def _set_targeting(request: dict, targeting_request: dict) -> dict:
        languages = targeting_request.get("languages", [])
        if languages:
            languages = [language["key"] for language in languages]

        locations = targeting_request.get("locations")
        if locations:
            locations = [Location(**location) for location in locations]

        included_interests, excluded_interests, narrow_interests = adset_builder.extract_interests(targeting_request)
        included_custom_audiences, excluded_custom_audiences = adset_builder.extract_custom_audiences(targeting_request)

        placements = request.get("placements")
        (
            publisher_platforms,
            positions,
        ) = get_placement_positions(placements)

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
            geo_locations=dict(SmartCreatePublish.process_geo_location(locations)),
            locales=languages,
            # facebook_positions=result_positions["facebook_positions"],
            # instagram_positions=result_positions["instagram_positions"],
            # audience_network_positions=result_positions["audience_network_positions"],
            publisher_platforms=publisher_platforms,
            device_platforms=device_platforms,
            user_device=user_device,
            user_os=user_os,
        )

        if positions:
            for key, value in positions.items():
                targeting.__setattr__(key, value)

        return asdict(targeting)

    @staticmethod
    def build_add_adset_ad_event(
        ad_account_id: str, business_owner_id: str, structure_tree: List[Dict]
    ) -> Union[List, Dict]:
        mapper = AddAdsetAdEventMapping(target=AddAdsetAdEvent)
        response = mapper.load(structure_tree)
        response.business_owner_id = business_owner_id
        response.account_id = ad_account_id
        return response


class HandlersEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_REQUEST = SmartCreatePublish
    SMART_EDIT_PUBLISH_REQUEST = SmartEditPublish
    AAA_PUBLISH_REQUEST = AddStructuresToParent
