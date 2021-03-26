import logging
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import asdict
from functools import lru_cache
from typing import List

from facebook_business.adobjects.abstractcrudobject import AbstractCrudObject
from facebook_business.adobjects.ad import Ad as FacebookAd
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.flexibletargeting import FlexibleTargeting
from facebook_business.adobjects.targeting import Targeting

from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter, get_sdk_structures
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookGender, FacebookMiscFields, Gender
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level, LevelToFacebookIdKeyMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureMapping import StructureFields
from Core.Web.FacebookGraphAPI.search import GraphAPICountryGroupsLegend, GraphAPILanguagesHandler
from FacebookCampaignsBuilder.Api.startup import config, fixtures
from FacebookCampaignsBuilder.Infrastructure.Domain.fe_structure_models import Ad, AdSet, Campaign, Interest

logger = logging.getLogger(__name__)

LOCATION_TYPES_TO_SINGULAR = {
    "countries": "country",
    "regions": "region",
    "geo_markets": "geo_market",
    "cities": "city",
    "zips": "zip",
    "electoral_districts": "electoral_district",
}


class CampaignTreesStructure:
    @staticmethod
    def get(account_id, level, structure_ids, business_owner_facebook_id):
        level_enum = Level(level)
        campaign_tree_builder = CampaignTreeBuilder(account_id, level_enum, structure_ids, business_owner_facebook_id)
        result = campaign_tree_builder.create_campaign_trees()
        return result


class GetStructure:
    @staticmethod
    def get(account_id, level, structure_ids, business_owner_facebook_id):
        level_enum = Level(level)
        get_structure = CampaignTreeBuilder(account_id, level_enum, structure_ids, business_owner_facebook_id)

        return get_structure.get_exact_structure()


class CampaignTreeBuilder:
    languages = None
    countries = None

    def __init__(self, account_id, level_enum, structure_ids, business_owner_facebook_id):
        self.account_id = account_id
        self.level = level_enum
        self.structure_ids = structure_ids
        self.business_owner_facebook_id = business_owner_facebook_id

        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id)
        GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=config.facebook)

    @property
    def _languages(self):
        if not CampaignTreeBuilder.languages:
            CampaignTreeBuilder.languages = {
                language["key"]: language for language in GraphAPILanguagesHandler().get_all()
            }

        return CampaignTreeBuilder.languages

    @property
    def _countries(self):
        if not CampaignTreeBuilder.countries:
            CampaignTreeBuilder.countries = {
                country["country_code"]: country for country in GraphAPICountryGroupsLegend().countries
            }

        return CampaignTreeBuilder.countries

    def get_exact_structure(self):
        # get structure id key
        if self.level == Level.AD:
            structure_id_key = LevelToFacebookIdKeyMapping.AD.value.replace("_", ".")
            map_structure = self.__map_ads
        elif self.level == Level.ADSET:
            structure_id_key = LevelToFacebookIdKeyMapping.ADSET.value.replace("_", ".")
            map_structure = self.__map_adsets
        else:
            raise ValueError("Incorrect level provided!")
        # map the structure
        structures = []
        for structure_id in self.structure_ids:
            raw_structures = self.__get_raw_structures_by_id(self.level, structure_id_key, structure_id)
            [mapped_structure] = map_structure(raw_structures)
            structures.append(asdict(mapped_structure))

        return structures

    def create_campaign_trees(self):
        if self.level == Level.CAMPAIGN:
            campaigns_ids = self.structure_ids
        else:
            campaigns_ids = self.__get_structures_campaign_ids()

        raw_campaigns = self.__get_campaigns(campaigns_ids)
        campaigns = self.__map_campaigns(raw_campaigns)
        campaigns_trees = self.__build_campaign_trees(campaigns)

        return list(map(asdict, campaigns_trees))

    def __build_campaign_trees(self, campaigns: List[Campaign]):
        for campaign in campaigns:
            level = Level.ADSET
            campaign_id_key = LevelToFacebookIdKeyMapping.CAMPAIGN.value.replace("_", ".")
            raw_adsets = self.__get_raw_structures_by_id(level, campaign_id_key, campaign.id)

            adsets = self.__map_adsets(raw_adsets)
            with ThreadPoolExecutor() as executor:
                ads = executor.map(self.__get_ads, adsets)

            campaign.adsets = list(ads)

        return campaigns

    def __get_ads(self, adset: AdSet):
        level = Level.AD
        adset_id_key = LevelToFacebookIdKeyMapping.ADSET.value.replace("_", ".")
        raw_ads = self.__get_raw_structures_by_id(level, adset_id_key, adset.id)
        adset.ads = self.__map_ads(raw_ads)
        return adset

    def __get_campaigns(self, campaign_ids):
        facebook_structure_key = LevelToFacebookIdKeyMapping.CAMPAIGN.value.replace("_", ".")
        structures_filter = {
            "filtering": [create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, campaign_ids)]
        }
        structure_fields = StructureFields.get(Level.CAMPAIGN.value).structure_fields
        fields = [field.facebook_fields[0] for field in structure_fields]

        return get_sdk_structures(self.account_id, Level.CAMPAIGN, fields=fields, params=structures_filter)

    def __get_structures_campaign_ids(self):
        facebook_structure_key = LevelToFacebookIdKeyMapping[self.level.value.upper()].value.replace("_", ".")
        structures_filter = {
            "filtering": [create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, self.structure_ids)]
        }
        fields = [Level.CAMPAIGN.value]
        response = get_sdk_structures(self.account_id, self.level, fields=fields, params=structures_filter)

        return [item[Level.CAMPAIGN.value][FacebookMiscFields.id] for item in response]

    def __get_raw_structures_by_id(self, level, structure_key, structure_id):
        structures_filter = {
            "filtering": [create_facebook_filter(structure_key, AgGridFacebookOperator.EQUAL, structure_id)]
        }
        structure_fields = StructureFields.get(level.value).structure_fields
        fields = [field.facebook_fields[0] for field in structure_fields]

        response = get_sdk_structures(self.account_id, level, fields=fields, params=structures_filter)
        return [item for item in response]

    @staticmethod
    def __map_campaigns(raw_campaigns) -> List[Campaign]:
        campaigns = []
        for raw_campaign in raw_campaigns:
            campaign = Campaign(
                id=raw_campaign[GraphAPIInsightsFields.structure_id],
                name=raw_campaign[GraphAPIInsightsFields.name],
                status=raw_campaign[GraphAPIInsightsFields.status],
                objective=raw_campaign[GraphAPIInsightsFields.objective],
                buying_type=raw_campaign[GraphAPIInsightsFields.buying_type],
                special_ad_category=raw_campaign[GraphAPIInsightsFields.special_ad_category],
                bid_strategy=raw_campaign.get(GraphAPIInsightsFields.bid_strategy, None),
            )

            campaign.set_budget_opt(
                daily_budget=raw_campaign.get(GraphAPIInsightsFields.daily_budget, None),
                lifetime_budget=raw_campaign.get(GraphAPIInsightsFields.lifetime_budget, None),
            )
            campaigns.append(campaign)

        return campaigns

    def __map_adsets(self, raw_adsets) -> List[AdSet]:
        adsets = []
        for raw_adset in raw_adsets:
            targeting = raw_adset[GraphAPIInsightsFields.targeting]
            promoted_object = raw_adset.get(GraphAPIInsightsFields.promoted_object)

            adset = AdSet(
                id=raw_adset[GraphAPIInsightsFields.structure_id],
                name=raw_adset[GraphAPIInsightsFields.name],
                status=raw_adset[GraphAPIInsightsFields.status],
                destination_type=raw_adset[GraphAPIInsightsFields.destination_type],
                optimization_goal=raw_adset[GraphAPIInsightsFields.optimization_goal],
                billing_event=raw_adset[GraphAPIInsightsFields.billing_event],
                publisher_platforms=targeting.get(Targeting.Field.publisher_platforms),
                min_age=targeting[Targeting.Field.age_min],
                max_age=targeting[Targeting.Field.age_max],
                start_time=raw_adset[GraphAPIInsightsFields.start_time],
                end_time=raw_adset.get(GraphAPIInsightsFields.end_time),
            )

            if promoted_object:
                adset.set_promoted_object_fields(promoted_object)

            bid_control = raw_adset.get(GraphAPIInsightsFields.bid_amount)
            if bid_control:
                adset.bid_control = bid_control / 100

            if Targeting.Field.genders in targeting:
                genders = targeting[Targeting.Field.genders]

                if len(genders) == 1:
                    if genders[0] == FacebookGender.MEN.value:
                        adset.gender = Gender.MEN.value
                    else:
                        adset.gender = Gender.WOMEN.value

                adset.device_platforms = targeting.get(Targeting.Field.device_platforms, ["mobile", "desktop"])

            self.__map_adset_interests(adset, targeting)
            self.__map_adset_locations(adset, targeting)
            self.__map_adset_languages(adset, targeting)

            adset.facebook_positions = targeting.get(Targeting.Field.facebook_positions, [])
            adset.instagram_positions = targeting.get(Targeting.Field.instagram_positions, [])
            adset.audience_network_positions = targeting.get(Targeting.Field.audience_network_positions, [])

            adset.custom_audiences = [
                audience["id"] for audience in targeting.get(Targeting.Field.custom_audiences, [])
            ]
            adset.excluded_custom_audiences = [
                audience["id"] for audience in targeting.get(Targeting.Field.excluded_custom_audiences, [])
            ]

            adset.set_budget_opt(
                daily_budget=raw_adset.get(GraphAPIInsightsFields.daily_budget),
                lifetime_budget=raw_adset.get(GraphAPIInsightsFields.lifetime_budget),
            )
            adset.set_mobile_fields(
                user_os=targeting.get(Targeting.Field.user_os, []),
                user_device=targeting.get(Targeting.Field.user_device, []),
            )

            adsets.append(adset)

        return adsets

    def __map_adset_interests(self, adset, targeting):
        if Targeting.Field.flexible_spec in targeting:
            flexible_spec = targeting[Targeting.Field.flexible_spec]
            flexible_targeting = flexible_spec[0]
            for interest in flexible_targeting.get(FlexibleTargeting.Field.interests, []):
                self.__try_add_interest_to_adset(adset.interests, interest)

            # TODO: for now we are intersecting just 2 audiences, we might extend this in the near future
            if len(flexible_spec) > 1:
                flexible_targeting = flexible_spec[1]
                for interest in flexible_targeting.get(FlexibleTargeting.Field.interests, []):
                    self.__try_add_interest_to_adset(adset.narrow_interests, interest)
        else:
            for interest in targeting.get(FlexibleTargeting.Field.interests, []):
                self.__try_add_interest_to_adset(adset.interests, interest)

        for interest in targeting.get(Targeting.Field.exclusions, {}).get(FlexibleTargeting.Field.interests, []):
            self.__try_add_interest_to_adset(adset.excluded_interests, interest)

    def __try_add_interest_to_adset(self, adset_interests, interest):
        _interest = self.__get_interest(interest["id"])
        if _interest:
            adset_interests.append(_interest)

    @staticmethod
    @lru_cache(maxsize=1024)  # TODO: this can be changed and extracted as a constant
    def __get_interest(interest_id):
        try:
            interest_obj = AbstractCrudObject()
            fb_api = interest_obj.get_api()
            interest = fb_api.call(method="GET", path=(interest_id,))
            return Interest(**interest.json())
        except Exception as e:
            # Some interests might be removed from facebook
            logger.exception(repr(e))
            return None

    @staticmethod
    def __map_ads(raw_ads) -> List[Ad]:
        ads = []
        for raw_ad in raw_ads:
            tracking_specs = raw_ad.get(GraphAPIInsightsFields.tracking_specs, [])

            fields_string = GraphAPIInsightsFields.adcreatives
            fields_string = fields_string[fields_string.find("{") + 1 : fields_string.find("}")]
            fields = fields_string.split(",")

            ad_id = raw_ad[GraphAPIInsightsFields.structure_id]
            ad_account = FacebookAd(ad_id)
            ad_creative_data = ad_account.get_ad_creatives(fields=fields)
            ad_creative_data = [item for item in ad_creative_data][0]

            adcreative_fields = GraphAPIInsightsFields.adcreatives_fields.split(",")
            ad_creative = AdCreative(ad_creative_data["id"])
            ad_creative_fields_data = ad_creative.api_get(fields=adcreative_fields)

            ad_creative_data.update(ad_creative_fields_data)

            ad = Ad.from_ad_details(
                raw_ad[GraphAPIInsightsFields.structure_id],
                raw_ad[GraphAPIInsightsFields.name],
                raw_ad[GraphAPIInsightsFields.status],
                ad_creative_data,
                tracking_specs,
            )
            ads.append(ad)

        return ads

    def __map_adset_locations(self, adset: AdSet, targeting):
        if Targeting.Field.geo_locations in targeting:
            geo_locations = targeting[Targeting.Field.geo_locations]

            for location_type, locations in geo_locations.items():
                _locations = []
                if location_type == Targeting.Field.countries:
                    _locations = [self._countries[country_code] for country_code in locations]
                elif location_type in LOCATION_TYPES_TO_SINGULAR:
                    _locations = locations

                for _location in _locations:
                    _location["type"] = LOCATION_TYPES_TO_SINGULAR[location_type]

                    if Targeting.Field.country in _location:
                        _location["country_name"] = self._countries[_location["country"]]["name"]

                adset.locations.extend(_locations)

    def __map_adset_languages(self, adset: AdSet, targeting):
        if Targeting.Field.locales in targeting:
            adset.languages.extend(
                [self._languages[key] for key in targeting[Targeting.Field.locales] if key in self._languages]
            )
