import logging
from dataclasses import asdict
from typing import List

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import (
    FacebookGender, Gender)
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.search import (GraphAPICountryGroupsLegend,
                                              GraphAPILanguagesHandler)
# from facebook_business.adobjects.adsinterest import AdsInterest TODO: find a way to cache all the interest without using this class
from facebook_business.adobjects.flexibletargeting import FlexibleTargeting
from facebook_business.adobjects.targeting import Targeting
from FacebookTuring.Api.startup import config, fixtures
from FacebookTuring.Infrastructure.Domain.fe_structure_models import (Ad,
                                                                      AdSet,
                                                                      Campaign)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import \
    TuringMongoRepository

logger = logging.getLogger(__name__)


class CampaignKeyMap:
    id = "campaign_id"
    name = "campaign_name"


class AdSetKeyMap:
    id = "adset_id"
    name = "adset_name"


class AdKeyMap:
    id = "ad_id"
    name = "ad_name"


LOCATION_TYPES_TO_SINGULAR = {
    "countries": "country",
    "regions": "region",
    "geo_markets": "geo_market",
    "cities": "city",
    "zips": "zip",
    "electoral_districts": "electoral_district",
}

LEVEL_TO_NAME_KEY = {Level.CAMPAIGN: CampaignKeyMap.name, Level.ADSET: AdSetKeyMap.name, Level.AD: AdKeyMap.name}

LEVEL_TO_ID_KEY = {Level.CAMPAIGN: CampaignKeyMap.id, Level.ADSET: AdSetKeyMap.id, Level.AD: AdKeyMap.id}


class CampaignTreesStructure:
    @staticmethod
    def get(level, structure_ids, business_owner_facebook_id):
        level_enum = Level(level)
        campaign_tree_builder = CampaignTreeBuilder(level_enum, structure_ids, business_owner_facebook_id)
        result = campaign_tree_builder.create_campaign_trees()
        return result


class CampaignTreeBuilder:
    languages = None
    countries = None

    def __init__(self, level_enum, structure_ids, business_owner_facebook_id):
        self.level = level_enum
        self.structure_ids = structure_ids
        self.business_owner_facebook_id = business_owner_facebook_id
        self.repository = TuringMongoRepository(
            config=config.mongo, database_name=config.mongo.structures_database_name, collection_name=self.level.value
        )

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

    def create_campaign_trees(self):
        if self.level == Level.CAMPAIGN:
            campaigns_ids = self.structure_ids
        else:
            campaigns_ids = self.__get_structures_campaign_ids()

        raw_campaigns = self.__get_campaigns_from_db(campaigns_ids)
        campaigns = self.__map_campaigns(raw_campaigns)
        campaigns_trees = self.__build_campaign_trees(campaigns)
        return list(map(asdict, campaigns_trees))

    def __build_campaign_trees(self, campaigns: List[Campaign]):
        for campaign in campaigns:
            self.repository.collection = Level.ADSET.value
            campaign_id_key = LEVEL_TO_ID_KEY[Level.CAMPAIGN]
            raw_adsets = self.__get_raw_structures_by_id(campaign_id_key, campaign.id)

            campaign.adsets = self.__map_adsets(raw_adsets)
            for adset in campaign.adsets:
                self.repository.collection = Level.AD.value
                adset_id_key = LEVEL_TO_ID_KEY[Level.ADSET]
                raw_ads = self.__get_raw_structures_by_id(adset_id_key, adset.id)

                adset.ads = self.__map_ads(raw_ads)

        return campaigns

    def __get_campaigns_from_db(self, campaign_ids):
        self.repository.collection = Level.CAMPAIGN.value
        return self.repository.get_bo_structures_by_ids(
            self.business_owner_facebook_id, LEVEL_TO_ID_KEY[Level.CAMPAIGN], campaign_ids
        )

    def __get_structures_campaign_ids(self):
        return self.repository.get_bo_unique_campaign_ids(
            self.business_owner_facebook_id, LEVEL_TO_ID_KEY[self.level], self.structure_ids
        )

    def __get_raw_structures_by_id(self, structure_key, ids):
        return self.repository.get_bo_structures_by_id(self.business_owner_facebook_id, structure_key, ids)

    @staticmethod
    def __map_campaigns(raw_campaigns) -> List[Campaign]:
        campaigns = []
        for raw_campaign in raw_campaigns:
            details = raw_campaign["details"]
            campaign = Campaign(
                id=raw_campaign["campaign_id"],
                name=raw_campaign["campaign_name"],
                status=raw_campaign["status"],
                objective=raw_campaign["objective"],
                buying_type=details["buying_type"],
                special_ad_category=details["special_ad_category"],
                bid_strategy=details.get("bid_strategy"),
            )

            campaign.set_budget_opt(
                daily_budget=raw_campaign["daily_budget"], lifetime_budget=raw_campaign["lifetime_budget"]
            )
            campaigns.append(campaign)

        return campaigns

    def __map_adsets(self, raw_adsets) -> List[AdSet]:
        adsets = []
        for raw_adset in raw_adsets:
            details = raw_adset["details"]
            targeting = details["targeting"]
            promoted_object = details.get("promoted_object")

            adset = AdSet(
                id=raw_adset["adset_id"],
                name=raw_adset["adset_name"],
                status=raw_adset["status"],
                destination_type=details["destination_type"],
                optimization_goal=details["optimization_goal"],
                billing_event=details["billing_event"],
                publisher_platforms=targeting.get(Targeting.Field.publisher_platforms),
                min_age=targeting[Targeting.Field.age_min],
                max_age=targeting[Targeting.Field.age_max],
                start_time=raw_adset["start_time"],
                end_time=raw_adset["end_time"],
            )

            if promoted_object:
                adset.set_promoted_object_fields(promoted_object)

            bid_control = details.get("bid_amount")
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

            # TODO: Uncomment when the interests issue is solved
            # self.__map_adset_interests(adset, targeting)
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

            adset.set_budget_opt(daily_budget=raw_adset["daily_budget"], lifetime_budget=raw_adset["lifetime_budget"])
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

    # @staticmethod
    # @lru_cache(maxsize=1024)  # TODO: this can be changed and extracted as a constant
    # def __get_interest(interest_id):
    #     try:
    #         graph_interest = AdsInterest(interest_id)
    #         _interest = Interest(**dict(graph_interest.api_get()))
    #         return _interest
    #     except Exception as e:
    #         # Some interests might be removed from facebook
    #         logger.exception(repr(e))
    #         return None

    @staticmethod
    def __map_ads(raw_ads) -> List[Ad]:
        ads = []
        for raw_ad in raw_ads:
            details = raw_ad["details"]
            tracking_specs = details.get("tracking_specs", [])

            if "adcreatives" not in details:
                # TODO: check for sync problems
                logger.debug("adcreatives key not found in details")
                continue

            ad_creative_data = details["adcreatives"]["data"][0]

            ad = Ad.from_ad_details(
                raw_ad["ad_id"], raw_ad["ad_name"], raw_ad["status"], ad_creative_data, tracking_specs
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
