import logging
import typing
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Optional

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestBase import HTTPRequestBase
from FacebookCampaignsBuilder.Api import commands
from FacebookCampaignsBuilder.Api.startup import config, fixtures
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdBuilderHandler import (
    GraphAPIAdBuilderHandler,
)
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdPreviewBuilderHandler import (
    GraphAPIAdPreviewBuilderHandler,
)
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdSetBuilderHandler import (
    GraphAPIAdSetBuilderHandler,
)
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPICampaignBuilderHandler import (
    GraphAPICampaignBuilderHandler,
)
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create import campaign_builder
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.ad_builder import AdBuilder
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create import adset_builder
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.structures import CampaignSplit
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.targeting import Location
from FacebookCampaignsBuilder.Infrastructure.GraphAPIRequests.GraphAPIRequestAudienceSize import (
    GraphAPIRequestAudienceSize,
)
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.CampaignCreatedEvent import CampaignCreatedEvent
from FacebookCampaignsBuilder.Infrastructure.IntegrationEvents.CampaignCreatedEventMapping import (
    CampaignCreatedEventMapping,
)

logger = logging.getLogger(__name__)


class AdPreview:
    @classmethod
    def handle(
        cls,
        command: commands.AdPreview = None,
        facebook_config: typing.Any = None,
        permanent_token: typing.AnyStr = None,
    ) -> Optional[str]:
        ad_builder = GraphAPIAdPreviewBuilderHandler(facebook_config=facebook_config, permanent_token=permanent_token)
        ad_builder.build_ad_creative(
            account_id=command.account_id,
            ad_template=command.ad_template,
            page_facebook_id=command.page_facebook_id,
            instagram_facebook_id=command.instagram_facebook_id,
        )
        params = {"ad_format": command.ad_format, "creative": ad_builder.ad_creative_details}
        ad_account = AdAccount(fbid=command.account_id)
        ad_preview = ad_account.get_generate_previews(params=params)

        if ad_preview:
            return ad_preview[0].export_all_data()["body"].replace('scrolling="yes"', 'scrolling="no"')

        return None


class AudienceSize:
    @classmethod
    def handle(
        cls,
        permanent_token: typing.AnyStr = None,
        account_id: typing.AnyStr = None,
        audience_details: typing.AnyStr = None,
    ):
        try:
            audience_size_request = GraphAPIRequestAudienceSize(
                access_token=permanent_token, account_id=account_id, audience_details=audience_details
            )
            response, _ = HTTPRequestBase.get(audience_size_request.url)
        except Exception as e:
            raise e

        if isinstance(response, Exception):
            raise response

        audience_size_estimate = response[0].get("estimate_mau", None)
        return audience_size_estimate


class CampaignPublish:
    @staticmethod
    def delete_incomplete_campaigns(campaign_tree):
        for campaign in campaign_tree:
            CampaignPublish.delete_campaign(campaign["facebook_id"])
            for ad_set in campaign["ad_sets"]:
                CampaignPublish.delete_ad_set(ad_set["facebook_id"])
                for ad_facebook_id in ad_set["ads"]:
                    CampaignPublish.delete_ad(ad_facebook_id)

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

    @staticmethod
    def publish_response(response):
        try:
            rabbitmq_client = RabbitMqClient(
                startup.rabbitmq_config, startup.exchange_details.name, startup.exchange_details.outbound_queue.key
            )
            rabbitmq_client.publish(response)
            logger.info({"rabbitmq": rabbitmq_client.serialize_message(response)})
        except Exception as e:
            raise e


class CampaignBuilderPublish:
    @staticmethod
    def handle(
        request: typing.Dict = None,
        business_owner_id: typing.AnyStr = None,
        facebook_config: typing.Any = None,
        permanent_token: str = None,
    ) -> typing.List[typing.Dict]:

        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        campaign_structure = request["campaign_optimization_details"]["campaign_structure"]
        campaign_template = request["campaign_template"]

        ad_set_template = request["ad_set_template"]
        ad_set_budget_template = request["campaign_optimization_details"]["budget_template"]

        ad_template = request["advert_template"]

        # Check if automated structure is required
        if campaign_structure["use_recommended_campaign_structure"]:
            campaign_structure["split_by_device"] = True
            campaign_structure["split_by_location"] = True
            campaign_structure["split_by_gender"] = True
            campaign_structure["split_by_age_range"] = False

        # Build campaigns
        campaign_builder = GraphAPICampaignBuilderHandler()

        # If 'geo_locations' or 'countries' are not set at ad set level, set them to [None]
        ad_set_template = CampaignBuilderPublish._set_default_location_targeting(ad_set_template)

        # Build all campaigns generated by the split
        campaign_builder.build_campaigns(
            campaign_structure,
            campaign_template,
            ad_set_template["targeting"]["device_platforms"],
            ad_set_template["targeting"]["geo_locations"]["countries"],
        )

        # Build adsets
        ad_set_builder = GraphAPIAdSetBuilderHandler()
        if (
            "campaign_budget_optimization" in campaign_template.keys()
            and campaign_template["campaign_budget_optimization"]
        ):
            is_using_campaign_budget_optimization = True
        else:
            is_using_campaign_budget_optimization = False
        ad_set_builder.build_ad_sets_full(
            campaign_structure, ad_set_template, ad_set_budget_template, is_using_campaign_budget_optimization
        )

        # Build adverts
        ad_builder = GraphAPIAdBuilderHandler()

        # Publish on Facebook
        campaign_tree = []
        campaign_response = {"facebook_id": None, "ad_sets": []}

        ad_account = AdAccount(fbid=request["ad_account_id"])
        for campaign_index, campaign in enumerate(campaign_builder.campaigns):
            try:
                # Publish campaign
                facebook_campaign = ad_account.create_campaign(params=campaign)
                campaign_facebook_id = facebook_campaign.get_id()

                # Add new campaign to response
                campaign_tree.append(deepcopy(campaign_response))
                campaign_tree[campaign_index]["facebook_id"] = campaign_facebook_id

                for ad_set_index, ad_set in enumerate(ad_set_builder.ad_sets):
                    ad_set["campaign_id"] = campaign_facebook_id
                    # remove array of [None] from countries
                    if (
                        "geo_locations" in ad_set["targeting"].keys()
                        and "countries" in ad_set["targeting"]["geo_locations"]
                        and ad_set["targeting"]["geo_locations"]["countries"] == [None]
                    ):
                        del ad_set["targeting"]["geo_locations"]["countries"]
                    ad_set["debug"] = "all"
                    facebook_ad_set = ad_account.create_ad_set(params=ad_set)
                    ad_set_facebook_id = facebook_ad_set.get_id()

                    # Add new adset to response
                    ad_set_response = {"facebook_id": ad_set_facebook_id, "ads": []}
                    campaign_tree[campaign_index]["ad_sets"].append(deepcopy(ad_set_response))

                    # Publish ad
                    for ad_index, ad_template_details in enumerate(ad_template["details"]["generated_adverts"]):
                        current_ad_template = {}
                        current_ad_template.update(ad_template_details)
                        current_ad_template["ad_format"] = ad_template["ad_format"]
                        ad_builder.build_ad(
                            request["ad_account_id"],
                            ad_set_facebook_id,
                            current_ad_template,
                            ad_template["details"]["page_facebook_id"],
                            ad_template["details"]["instagram_account_facebook_id"],
                        )
                        ad_builder.ad[Ad.Field.name] = ad_set["name"] + " - Ad - " + str(ad_index + 1)
                        ad = ad_account.create_ad(params=ad_builder.ad)
                        ad_facebook_id = ad.get_id()

                        # Add new ad to response
                        campaign_tree[campaign_index]["ad_sets"][ad_set_index]["ads"].append(ad_facebook_id)
            except Exception as e:
                CampaignPublish.delete_incomplete_campaigns(campaign_tree)
                raise e

        try:
            mapper = CampaignCreatedEventMapping(target=CampaignCreatedEvent)
            response = mapper.load(campaign_tree)
            response.business_owner_id = business_owner_id
            response.account_id = request["ad_account_id"]
            CampaignPublish.publish_response(response)
        except Exception as e:
            raise e

        return campaign_tree

    @staticmethod
    def _set_default_location_targeting(ad_set_template):
        if "geo_locations" not in ad_set_template["targeting"].keys():
            ad_set_template["targeting"]["geo_locations"] = {"countries": [None]}

        if "countries" not in ad_set_template["targeting"]["geo_locations"].keys():
            ad_set_template["targeting"]["geo_locations"]["countries"] = [None]

        return ad_set_template


class SmartCreatePublish:
    @staticmethod
    def handle(
        request: typing.Dict = None,
        business_owner_id: typing.AnyStr = None,
        facebook_config: typing.Any = None,
        permanent_token: str = None,
    ) -> typing.List[typing.Dict]:

        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=facebook_config)

        campaign_tree = []
        campaign_response = {"facebook_id": None, "ad_sets": []}

        campaigns, ad_sets, ads = SmartCreatePublish.build_campaign_hierarchy(request)
        ad_account = AdAccount(fbid=request["ad_account_id"])

        step_two = request["step_two_details"]
        is_adset_using_cbo = (
            "campaign_budget_optimization" in step_two and step_two["campaign_budget_optimization"] is not None
        )

        for campaign_index, campaign in enumerate(campaigns):
            try:
                # Publish campaign
                facebook_campaign = ad_account.create_campaign(params=campaign.campaign_template)
                campaign_facebook_id = facebook_campaign.get_id()

                # Add new campaign to response
                campaign_tree.append(deepcopy(campaign_response))
                campaign_tree[campaign_index]["facebook_id"] = campaign_facebook_id
                adset_budgets = []

                for ad_set_index, ad_set in enumerate(ad_sets):
                    SmartCreatePublish.populate_missing_adset_fields(campaign_facebook_id, ad_set, campaign)

                    # This is needed because we cannot have budget on both campaign + adsets
                    adset_create_template = deepcopy(ad_set)
                    adset_budget_type, budget = SmartCreatePublish.extract_budget_from_adset(adset_create_template)

                    facebook_ad_set = ad_account.create_ad_set(params=adset_create_template)
                    ad_set_facebook_id = facebook_ad_set.get_id()

                    # Add new adset to response
                    ad_set_response = {"facebook_id": ad_set_facebook_id, "ads": []}
                    campaign_tree[campaign_index]["ad_sets"].append(deepcopy(ad_set_response))
                    adset_budgets.append({"adset_id": ad_set_facebook_id, adset_budget_type: budget})

                if is_adset_using_cbo:
                    SmartCreatePublish.add_adsets_budget(
                        campaign_facebook_id, adset_budgets, campaign.campaign_template
                    )

            except Exception as e:
                CampaignPublish.delete_incomplete_campaigns(campaign_tree)
                raise e

        return campaign_tree

    @staticmethod
    def build_campaign_hierarchy(request):
        step_one = request["step_one_details"]
        step_two = request["step_two_details"]
        step_three = request["step_three_details"]
        step_four = request["step_four_details"]

        # Flags used for adset builder
        destination_type = step_one.get("destination_type")
        is_using_conversions = step_one["objective"] == "CONVERSIONS"
        is_using_cbo = (
            "campaign_budget_optimization" in step_one and step_one["campaign_budget_optimization"] is not None
        )

        # Build campaigns
        campaigns = campaign_builder.build_campaigns(
            step_one=step_one,
            step_two=step_two,
            step_four=step_four,
        )

        # Build ad_sets
        ad_sets = adset_builder.build_ad_sets(
            step_two=step_two,
            step_three=step_three,
            step_four=step_four,
            is_using_cbo=is_using_cbo,
            is_using_conversions=is_using_conversions,
            destination_type=destination_type,
        )

        # Build ads
        ads = AdBuilder.build_ads()

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

    @classmethod
    def publish_response(cls, response):
        try:
            rabbitmq_adapter = fixtures.rabbitmq_adapter
            rabbitmq_adapter.publish(response)
            logger.info({"rabbitmq": rabbitmq_adapter.serialize_message(response)})
        except Exception as e:
            raise e

    @staticmethod
    def process_geo_location(locations: List[Location]) -> Dict:
        keys = dict(city="cities", country="countries", geo_market="geo_markets", region="regions", zip="zips")
        result = defaultdict(list)

        for location in locations:
            result[keys[location.type]].append({"key": location.key})

        return result

    @staticmethod
    def add_adsets_budget(campaign_facebook_id: str, adset_budgets: List[Dict], campaign_template: Dict):
        fb_campaign = Campaign(campaign_facebook_id)
        campaign_template.update({"adset_budgets": adset_budgets})
        campaign_template.pop(Campaign.Field.bid_strategy, None)
        campaign_template.pop(Campaign.Field.pacing_type, None)
        # Is either lifetime_budget or daily_budget
        campaign_template.pop(AdSet.Field.lifetime_budget, None)
        campaign_template.pop(AdSet.Field.daily_budget, None)
        fb_campaign.api_update(params=campaign_template)

    @staticmethod
    def extract_budget_from_adset(ad_set: Dict):
        if AdSet.Field.lifetime_budget in ad_set:
            adset_budget_type = AdSet.Field.lifetime_budget
            budget = ad_set.pop(AdSet.Field.lifetime_budget)
            return adset_budget_type, budget
        elif AdSet.Field.daily_budget in ad_set:
            adset_budget_type = AdSet.Field.daily_budget
            budget = ad_set.pop(AdSet.Field.daily_budget)
            return adset_budget_type, budget

        return None, None
