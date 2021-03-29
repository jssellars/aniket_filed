import concurrent.futures
import json
import logging
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime
from queue import Queue
from threading import Thread
from typing import AnyStr, Callable, Dict, List, Optional, Tuple, Union

import humps
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from Core.facebook.sdk_adapter.smart_create import ad_builder, adset_builder, campaign_builder, mappings
from Core.facebook.sdk_adapter.smart_create.ad_builder import get_ad_creative_id, get_tracking_specs
from Core.facebook.sdk_adapter.smart_create.structures import CampaignSplit
from Core.facebook.sdk_adapter.smart_create.targeting import FlexibleTargeting, Location, Targeting
from Core.facebook.sdk_adapter.validations import PLATFORM_X_POSITIONS
from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookRequestError
from FacebookCampaignsBuilder.BackgroundTasks import dtos
from FacebookCampaignsBuilder.BackgroundTasks.startup import config, fixtures
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.events import (
    CampaignCreatedEvent,
    CampaignCreatedEventMapping,
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
    def delete_incomplete_campaigns(campaign_tree):
        for campaign in campaign_tree:
            SmartCreateOperations.delete_campaign(campaign["facebook_id"])
            for ad_set in campaign["ad_sets"]:
                SmartCreateOperations.delete_ad_set(ad_set["facebook_id"])
                for ad_facebook_id in ad_set["ads"]:
                    SmartCreateOperations.delete_ad(ad_facebook_id)

    @staticmethod
    def delete_campaign(facebook_id):
        try:
            campaign = Campaign(fbid=facebook_id)
            campaign.api_delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ad_set(facebook_id):
        try:
            ad_set = AdSet(fbid=facebook_id)
            ad_set.api_delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ad(facebook_id):
        try:
            ad = Ad(fbid=facebook_id)
            ad.api_delete()
        except Exception as e:
            raise e

    @classmethod
    def publish(cls, publish_finished_event, sync_campaign_event=None):
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
    def clean_and_publish_response(campaign_tree, error_message, feedback_data, publish_response, template_id):
        SmartCreatePublish.update_feedback_database(
            feedback_data, template_id, PublishStatus.FAILED.value, error=error_message
        )
        SmartCreateOperations.delete_incomplete_campaigns(campaign_tree)
        publish_response.publish_status_id = PublishStatus.FAILED.value
        SmartCreateOperations.publish(publish_response)

    @staticmethod
    def build_campaign_event(ad_account_id, business_owner_id, campaign_tree):
        mapper = CampaignCreatedEventMapping(target=CampaignCreatedEvent)
        response = mapper.load(campaign_tree)
        response.business_owner_id = business_owner_id
        response.account_id = ad_account_id
        return response

    @staticmethod
    def update_feedback_database(feedback_data, template_id, status, error=None):
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
    def build_campaign_hierarchy(request: dtos.SmartCreatePublishRequest):
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
    def populate_missing_adset_fields(campaign_facebook_id: str, ad_set: Dict, parent_campaign: CampaignSplit):
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
    ):
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
    def get_gender_age_split(step_four: Dict, targeting: Dict):
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
    def get_location_device(step_four: Dict, targeting: Dict):
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

        campaign_tree = SmartEditPublish.process_structures_concurrently(
            SmartEditPublish.edit_campaigns, campaigns, Level.CAMPAIGN.value
        )
        adset_tree = SmartEditPublish.process_structures_concurrently(
            SmartEditPublish.edit_adsets, adsets, Level.ADSET.value
        )
        ad_tree = SmartEditPublish.update_ads(ads, ad_account)

        response = list()
        response.append({"campaigns": campaign_tree})
        response.append({"ad_sets": adset_tree})
        response.append({"ads": ad_tree})

        edit_event = SmartEditPublish.build_edit_event(request.ad_account_id, business_owner_id, campaign_tree)
        SmartCreateOperations.publish(publish_response, edit_event)

        return response

    @staticmethod
    def process_structures_concurrently(function: Callable, structures: List, level: str):
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
    def set_adset_budget(adset: Dict, params: Dict):
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
    def set_targeting(adset: Dict, params: Dict):
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

        publisher_platforms, positions = SmartEditPublish.get_platform_positions(adset)

        adset_targeting.publisher_platforms = publisher_platforms

        if positions:
            for key, value in positions.items():
                adset_targeting.__setattr__(key, value)

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

        facebook_campaign = Campaign(fbid=campaign.get("campaign_id"))
        facebook_campaign.api_update(params=params)

        return facebook_campaign

    @staticmethod
    def update_ads(ads: Dict, ad_account_id: AnyStr) -> List[Dict]:
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
                    step_three=ad,
                    objective=Optional[None],
                )
                param[FacebookEditField.Ad.ad_creative.value] = {"creative_id": ad_creative_id}

            if "pixel_id" in ad or "pixel_app_event_id" in ad:
                param[FacebookEditField.Ad.tracking_specs.value] = get_tracking_specs(ad)

            facebook_ads = Ad(ad_id)
            facebook_ads.api_update(params=param)
            updated_ad["ad_id"] = ad_id
            updated_ads.append(updated_ad)

        return updated_ads

    @staticmethod
    def add_feedback_to_queue(level: str):
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
    def update_db():
        while True:
            feedback_data = SmartEditPublish.queue.get()
            if feedback_data:
                SmartEditPublish.update_feedback_database(feedback_data)
                if feedback_data["publish_status"] != PublishStatus.IN_PROGRESS.value:
                    return

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

        SmartEditPublish.feedback_repository.update_many({"user_filed_id": feedback_data["user_filed_id"]}, query)

    @staticmethod
    def build_edit_event(ad_account_id, business_owner_id, structure_tree):
        mapper = StructureEditedEventMapping(target=StructureEditedEvent)
        response = mapper.load(structure_tree)
        response.business_owner_id = business_owner_id
        response.account_id = ad_account_id
        return response


class HandlersEnum(EnumerationBase):
    SMART_CREATE_PUBLISH_REQUEST = SmartCreatePublish
    SMART_EDIT_PUBLISH_REQUEST = SmartEditPublish
