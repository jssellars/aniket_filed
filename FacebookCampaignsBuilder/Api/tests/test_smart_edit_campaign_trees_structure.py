import json
from enum import Enum

import pytest

from Core.test_config import STRUCTURE_IDS


class SmartEditCampaignTreesStructureField(Enum):
    ID = "id"
    NAME = "name"
    STATUS = "status"
    OBJECTIVE = "objective"
    SPECIAL_AD_CATEGORY = "specialAdCategory"
    BUYING_TYPE = "buyingType"
    BID_STRATEGY = "bidStrategy"
    CAMPAIGN_BUDGET_OPTIMIZATION = "campaignBudgetOptimization"
    ADSETS = "adsets"
    DESTINATION_TYPE = "destinationType"
    OPTIMIZATION_GOAL = "optimizationGoal"
    BILLING_EVENT = "billingEvent"
    PUBLISHER_PLATFORMS = "publisherPlatforms"
    MIN_AGE = "minAge"
    MAX_AGE = "maxAge"
    START_TIME = "startTime"
    BID_CONTROL = "bidControl"
    PAGE_ID = "pageId"
    PIXEL_ID = "pixelId"
    CUSTOM_EVENT_TYPE = "customEventType"
    INTERESTS = "interests"
    EXCLUDED_INTERESTS = "excludedInterests"
    NARROW_INTERESTS = "narrowInterests"
    GENDER = "gender"
    LOCATIONS = "locations"
    LANGUAGES = "languages"
    CUSTOM_AUDIENCES = "customAudiences"
    EXCLUDED_CUSTOM_AUDIENCES = "excludedCustomAudiences"
    FACEBOOK_POSITIONS = "facebookPositions"
    INSTAGRAM_POSITIONS = "instagramPositions"
    AUDIENCE_NETWORK_POSITIONS = "audienceNetworkPositions"
    DEVICE_PLATFORMS = "devicePlatforms"
    MOBILE_OS = "mobileOs"
    MOBILE_DEVICES = "mobileDevices"
    END_TIME = "endTime"
    ADSET_BUDGET_OPTIMIZATION = "adsetBudgetOptimization"
    AMOUNT = "amount"
    BUDGET_ALLOCATED_TYPE_ID = "budgetAllocatedTypeId"
    ADS = "ads"
    KEY = "key"
    TYPE = "type"
    COUNTRY = "country"
    COUNTRY_CODE = "countryCode"
    COUNTRY_NAME = "countryName"
    REGION = "region"
    REGION_ID = "regionId"
    SUPPORTS_REGION = "supportsRegion"
    SUPPORTS_CITY = "supportsCity"
    CITY_OR_COUNTRY_NAME = "cityOrCountryName"
    SELECTED_LOCATION = "selectedLocationString"
    DISTANCE_UNIT = "distanceUnit"
    AD_FORMAT_TYPE = "adFormatType"
    FACEBOOK_PAGE_ID = "facebookPageId"
    INSTAGRAM_PAGE_ID = "instagramPageId"
    POST_ID = "postId"
    PIXEL_APP_EVENT_ID = "pixelAppEventId"
    ADVERT = "advert"
    MEDIA_URL = "mediaUrl"
    PRIMARY_TEXT = "primaryText"
    HEADLINE = "headline"
    DESCRIPTION = "description"
    WEBSITE_URL = "websiteUrl"
    CALL_TO_ACTION = "callToAction"
    DISPLAY_LINK = "displayLink"
    MEDIA_TYPE = "mediaType"
    CARDS = "cards"
    PICTURE = "picture"
    VIDEO_ID = "video_id"
    ADD_CARD_WITH_PAGE_PROFILE = "addCardWithPageProfile"


class TestSmartEditCampaignTreesStructure:
    @pytest.fixture(scope="session")
    def response(self, client, config):
        url = f"/api/v1/campaign-trees-structure/{config['account_id']}/campaign/{STRUCTURE_IDS}"
        return client.get(url, headers=config["headers"])

    @pytest.fixture(scope="session")
    def response_json(self, response):
        data = response.data.decode("UTF-8")
        return json.loads(data)

    def test_status_code_200(self, response):
        assert response.status_code == 200

    def test_return_type_is_list(self, response_json):
        assert isinstance(response_json, list)

    ##  Campaign tests ##

    def test_id_is_non_empty_string(self, response_json):
        for response in response_json:
            id_ = response.get(SmartEditCampaignTreesStructureField.ID.value)
            assert isinstance(id_, str)
            assert len(id_) > 0

    def test_name_is_non_empty_string(self, response_json):
        for response in response_json:
            name = response.get(SmartEditCampaignTreesStructureField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    def test_status_is_non_empty_string(self, response_json):
        for response in response_json:
            status = response.get(SmartEditCampaignTreesStructureField.STATUS.value)
            assert isinstance(status, str)
            assert len(status) > 0

    def test_objective_is_non_empty_string(self, response_json):
        for response in response_json:
            objective = response.get(SmartEditCampaignTreesStructureField.OBJECTIVE.value)
            assert isinstance(objective, str)
            assert len(objective) > 0

    def test_special_ad_category_is_non_empty_string(self, response_json):
        for response in response_json:
            special_ad_category = response.get(SmartEditCampaignTreesStructureField.SPECIAL_AD_CATEGORY.value)
            assert isinstance(special_ad_category, str)
            assert len(special_ad_category) > 0

    def test_buying_type_is_non_empty_string(self, response_json):
        for response in response_json:
            buying_type = response.get(SmartEditCampaignTreesStructureField.BUYING_TYPE.value)
            assert isinstance(buying_type, str)
            assert len(buying_type) > 0

    def test_bid_strategy_is_non_empty_string(self, response_json):
        for response in response_json:
            bid_strategy = response.get(SmartEditCampaignTreesStructureField.BID_STRATEGY.value)
            if bid_strategy:
                assert isinstance(bid_strategy, str)
                assert len(bid_strategy) > 0

    def test_campaign_budget_optimization(self, response_json):
        for response in response_json:
            campaign_budget_optimization = response.get(
                SmartEditCampaignTreesStructureField.CAMPAIGN_BUDGET_OPTIMIZATION.value
            )
            if campaign_budget_optimization:
                assert isinstance(campaign_budget_optimization, dict)
                assert len(campaign_budget_optimization) > 0

    def test_adsets_is_list(self, response_json):
        for response in response_json:
            adsets = response.get(SmartEditCampaignTreesStructureField.ADSETS.value)
            assert isinstance(adsets, list)

    ##  Adset tests ##

    @pytest.fixture(scope="session")
    def adset_data(self, response_json):
        data = []
        for response in response_json:
            campaign_budget_optimization = response.get(
                SmartEditCampaignTreesStructureField.CAMPAIGN_BUDGET_OPTIMIZATION.value
            )
            adsets = [
                dict(adset, cbo=True if campaign_budget_optimization else False)
                for adset in response.get(SmartEditCampaignTreesStructureField.ADSETS.value)
            ]
            data.extend(adsets)
        return data

    def test_adset_id_is_non_empty_string(self, adset_data):
        for response in adset_data:
            id_ = response.get(SmartEditCampaignTreesStructureField.ID.value)
            assert isinstance(id_, str)
            assert len(id_) > 0

    def test_adset_name_is_non_empty_string(self, adset_data):
        for response in adset_data:
            name = response.get(SmartEditCampaignTreesStructureField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    def test_adset_status_is_non_empty_string(self, adset_data):
        for response in adset_data:
            status = response.get(SmartEditCampaignTreesStructureField.STATUS.value)
            assert isinstance(status, str)
            assert len(status) > 0

    def test_adset_destination_type_is_non_empty_string(self, adset_data):
        for response in adset_data:
            destination_type = response.get(SmartEditCampaignTreesStructureField.DESTINATION_TYPE.value)
            assert isinstance(destination_type, str)
            assert len(destination_type) > 0

    def test_billing_event_is_non_empty_string(self, adset_data):
        for response in adset_data:
            billing_event = response.get(SmartEditCampaignTreesStructureField.BILLING_EVENT.value)
            assert isinstance(billing_event, str)
            assert len(billing_event) > 0

    def test_publisher_platforms_is_non_empty_list(self, adset_data):
        for response in adset_data:
            publisher_platforms = response.get(SmartEditCampaignTreesStructureField.PUBLISHER_PLATFORMS.value)
            if publisher_platforms:
                assert isinstance(publisher_platforms, list)
                assert len(publisher_platforms) > 0

    def test_min_age(self, adset_data):
        for response in adset_data:
            min_age = response.get(SmartEditCampaignTreesStructureField.MIN_AGE.value)
            assert isinstance(min_age, int)
            assert min_age >= 13

    def test_max_age(self, adset_data):
        for response in adset_data:
            min_age = response.get(SmartEditCampaignTreesStructureField.MIN_AGE.value)
            max_age = response.get(SmartEditCampaignTreesStructureField.MAX_AGE.value)
            assert isinstance(max_age, int)
            assert max_age >= min_age

    def test_start_time_is_non_empty_string(self, adset_data):
        for response in adset_data:
            start_time = response.get(SmartEditCampaignTreesStructureField.START_TIME.value)
            assert isinstance(start_time, str)
            assert len(start_time) > 0

    def test_bid_control_is_int_if_exists(self, adset_data):
        for response in adset_data:
            bid_control = response.get(SmartEditCampaignTreesStructureField.BID_CONTROL.value)
            if bid_control:
                assert isinstance(bid_control, int)
                assert bid_control > 0

    def test_page_id_is_non_empty_string(self, adset_data):
        for response in adset_data:
            page_id = response.get(SmartEditCampaignTreesStructureField.PAGE_ID.value)
            if page_id:
                assert isinstance(page_id, str)
                assert len(page_id) > 0

    def test_pixel_id_is_non_empty_string_if_exists(self, adset_data):
        for response in adset_data:
            pixel_id = response.get(SmartEditCampaignTreesStructureField.PIXEL_ID.value)
            if pixel_id:
                assert isinstance(pixel_id, str)
                assert len(pixel_id) > 0

    def test_custom_event_type_is_non_empty_string_if_exists(self, adset_data):
        for response in adset_data:
            custom_event_type = response.get(SmartEditCampaignTreesStructureField.CUSTOM_EVENT_TYPE.value)
            if custom_event_type:
                assert isinstance(custom_event_type, str)
                assert len(custom_event_type) > 0

    def test_interests_is_list(self, adset_data):
        for response in adset_data:
            interests = response.get(SmartEditCampaignTreesStructureField.INTERESTS.value)
            assert isinstance(interests, list)

    def test_excluded_interests_is_list(self, adset_data):
        for response in adset_data:
            excluded_interests = response.get(SmartEditCampaignTreesStructureField.EXCLUDED_INTERESTS.value)
            assert isinstance(excluded_interests, list)

    def test_narrow_interests_is_list(self, adset_data):
        for response in adset_data:
            narrow_interests = response.get(SmartEditCampaignTreesStructureField.NARROW_INTERESTS.value)
            assert isinstance(narrow_interests, list)

    def test_gender(self, adset_data):
        for response in adset_data:
            gender = response.get(SmartEditCampaignTreesStructureField.GENDER.value)
            assert isinstance(gender, int)
            assert gender in range(0, 3)

    def test_locations_is_list(self, adset_data):
        for response in adset_data:
            locations = response.get(SmartEditCampaignTreesStructureField.LOCATIONS.value)
            assert isinstance(locations, list)

    def test_languages_is_list(self, adset_data):
        for response in adset_data:
            languages = response.get(SmartEditCampaignTreesStructureField.LANGUAGES.value)
            assert isinstance(languages, list)

    def test_custom_audiences_is_list(self, adset_data):
        for response in adset_data:
            custom_audiences = response.get(SmartEditCampaignTreesStructureField.CUSTOM_AUDIENCES.value)
            assert isinstance(custom_audiences, list)

    def test_excluded_custom_audiences_is_list(self, adset_data):
        for response in adset_data:
            excluded_custom_audiences = response.get(
                SmartEditCampaignTreesStructureField.EXCLUDED_CUSTOM_AUDIENCES.value
            )
            assert isinstance(excluded_custom_audiences, list)

    def test_facebook_positions_audiences_is_list(self, adset_data):
        for response in adset_data:
            publisher_platforms = response.get(SmartEditCampaignTreesStructureField.PUBLISHER_PLATFORMS.value)
            facebook_positions = response.get(SmartEditCampaignTreesStructureField.FACEBOOK_POSITIONS.value)
            if facebook_positions:
                assert isinstance(facebook_positions, list)
                if "facebook" in publisher_platforms:
                    assert len(facebook_positions) > 0

    def test_instagram_positions_audiences_is_list(self, adset_data):
        for response in adset_data:
            publisher_platforms = response.get(SmartEditCampaignTreesStructureField.PUBLISHER_PLATFORMS.value)
            instagram_positions = response.get(SmartEditCampaignTreesStructureField.FACEBOOK_POSITIONS.value)
            if instagram_positions:
                assert isinstance(instagram_positions, list)
                if "instagram" in publisher_platforms:
                    assert len(instagram_positions) > 0

    def test_audience_network_positions_is_list(self, adset_data):
        for response in adset_data:
            audience_network_positions = response.get(
                SmartEditCampaignTreesStructureField.AUDIENCE_NETWORK_POSITIONS.value
            )
            assert isinstance(audience_network_positions, list)

    def test_device_platforms_is_list(self, adset_data):
        for response in adset_data:
            device_platforms = response.get(SmartEditCampaignTreesStructureField.DEVICE_PLATFORMS.value)
            assert isinstance(device_platforms, list)

    def test_mobile_os_is_non_empty_string(self, adset_data):
        for response in adset_data:
            mobile_os = response.get(SmartEditCampaignTreesStructureField.MOBILE_OS.value)
            assert isinstance(mobile_os, str)
            assert len(mobile_os) > 0

    def test_mobile_devices_is_list(self, adset_data):
        for response in adset_data:
            mobile_devices = response.get(SmartEditCampaignTreesStructureField.MOBILE_DEVICES.value)
            assert isinstance(mobile_devices, list)

    def test_end_time_is_non_empty_string(self, adset_data):
        for response in adset_data:
            end_time = response.get(SmartEditCampaignTreesStructureField.END_TIME.value)
            if end_time:
                assert isinstance(end_time, str)
                assert len(end_time) > 0

    def test_adset_budget_optimization(self, adset_data):
        for response in adset_data:
            adset_budget_optimization = response.get(
                SmartEditCampaignTreesStructureField.ADSET_BUDGET_OPTIMIZATION.value
            )
            if not response["cbo"]:
                assert isinstance(adset_budget_optimization, dict)
            else:
                assert adset_budget_optimization is None

    def test_adset_budget_optimization_amount_is_float(self, adset_data):
        for response in adset_data:
            adset_budget_optimization = response.get(
                SmartEditCampaignTreesStructureField.ADSET_BUDGET_OPTIMIZATION.value
            )

            if adset_budget_optimization is not None:
                amount = adset_budget_optimization.get(SmartEditCampaignTreesStructureField.AMOUNT.value)
                assert isinstance(amount, float)
                assert amount > 0

    def test_adset_budget_allocated_type_id_is_int(self, adset_data):
        for response in adset_data:
            adset_budget_optimization = response.get(
                SmartEditCampaignTreesStructureField.ADSET_BUDGET_OPTIMIZATION.value
            )

            if adset_budget_optimization is not None:
                budget_allocated_type_id = adset_budget_optimization.get(
                    SmartEditCampaignTreesStructureField.BUDGET_ALLOCATED_TYPE_ID.value
                )
                assert isinstance(budget_allocated_type_id, int)
                assert budget_allocated_type_id > 0

    def test_ads_is_list(self, adset_data):
        for response in adset_data:
            ads = response.get(SmartEditCampaignTreesStructureField.ADS.value)
            assert isinstance(ads, list)

    ##  Location data tests ##

    @pytest.fixture(scope="session")
    def location_data(self, adset_data):
        data = []
        for response in adset_data:
            locations = response.get(SmartEditCampaignTreesStructureField.LOCATIONS.value)
            data.extend(locations)
        return data

    def test_location_key_is_non_empty_string(self, location_data):
        for response in location_data:
            key = response.get(SmartEditCampaignTreesStructureField.KEY.value)
            assert isinstance(key, str)
            assert len(key) > 0

    def test_location_name_is_non_empty_string(self, location_data):
        for response in location_data:
            name = response.get(SmartEditCampaignTreesStructureField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    def test_location_type_is_non_empty_string(self, location_data):
        for response in location_data:
            type_ = response.get(SmartEditCampaignTreesStructureField.TYPE.value)
            assert isinstance(type_, str)
            assert len(type_) > 0

    def test_location_country_code_is_non_empty_string(self, location_data):
        for response in location_data:
            country_code = response.get(SmartEditCampaignTreesStructureField.COUNTRY_CODE.value)
            if country_code:
                assert isinstance(country_code, str)
                assert len(country_code) > 0

    def test_location_supports_region_is_bool(self, location_data):
        for response in location_data:
            supports_region = response.get(SmartEditCampaignTreesStructureField.SUPPORTS_REGION.value)
            if supports_region:
                assert isinstance(supports_region, bool)

    def test_location_supports_city_is_bool(self, location_data):
        for response in location_data:
            supports_city = response.get(SmartEditCampaignTreesStructureField.SUPPORTS_CITY.value)
            if supports_city:
                assert isinstance(supports_city, bool)

    def test_location_distance_unit_is_non_empty_string(self, location_data):
        for response in location_data:
            distance_unit = response.get(SmartEditCampaignTreesStructureField.DISTANCE_UNIT.value)
            if distance_unit:
                assert isinstance(distance_unit, str)
                assert len(distance_unit) > 0

    def test_location_country_is_non_empty_string(self, location_data):
        for response in location_data:
            country = response.get(SmartEditCampaignTreesStructureField.COUNTRY.value)
            if country:
                assert isinstance(country, str)
                assert len(country) > 0

    def test_region_is_non_empty_string(self, location_data):
        for response in location_data:
            region = response.get(SmartEditCampaignTreesStructureField.REGION.value)
            if region:
                assert isinstance(region, str)
                assert len(region) > 0

    def test_region_id_is_non_empty_string(self, location_data):
        for response in location_data:
            region_id = response.get(SmartEditCampaignTreesStructureField.REGION_ID.value)
            if region_id:
                assert isinstance(region_id, str)
                assert len(region_id) > 0

    def test_country_name_is_non_empty_string(self, location_data):
        for response in location_data:
            country_name = response.get(SmartEditCampaignTreesStructureField.COUNTRY_NAME.value)
            if country_name:
                assert isinstance(country_name, str)
                assert len(country_name) > 0

    def test_city_or_country_name_is_non_empty_string(self, location_data):
        for response in location_data:
            city_country_name = response.get(SmartEditCampaignTreesStructureField.CITY_OR_COUNTRY_NAME.value)
            if city_country_name:
                assert isinstance(city_country_name, str)
                assert len(city_country_name) > 0

    def test_selected_location_is_non_empty_string(self, location_data):
        for response in location_data:
            selected_location = response.get(SmartEditCampaignTreesStructureField.SELECTED_LOCATION.value)
            if selected_location:
                assert isinstance(selected_location, str)
                assert len(selected_location) > 0

    ##  Ad tests ##

    @pytest.fixture(scope="session")
    def ad_data(self, adset_data):
        data = []
        for response in adset_data:
            ads = response.get(SmartEditCampaignTreesStructureField.ADS.value)
            data.extend(ads)
        return data

    def test_ad_id_is_non_empty_string(self, ad_data):
        for response in ad_data:
            id_ = response.get(SmartEditCampaignTreesStructureField.ID.value)
            assert isinstance(id_, str)
            assert len(id_) > 0

    def test_ad_name_is_non_empty_string(self, ad_data):
        for response in ad_data:
            name = response.get(SmartEditCampaignTreesStructureField.NAME.value)
            assert isinstance(name, str)
            assert len(name) > 0

    def test_ad_status_is_non_empty_string(self, ad_data):
        for response in ad_data:
            status = response.get(SmartEditCampaignTreesStructureField.STATUS.value)
            assert isinstance(status, str)
            assert len(status) > 0

    def test_ad_format_type_is_int(self, ad_data):
        for response in ad_data:
            ad_format_type = response.get(SmartEditCampaignTreesStructureField.AD_FORMAT_TYPE.value)
            if ad_format_type:
                assert isinstance(ad_format_type, int)
                assert ad_format_type in range(1, 7)

    def test_fb_id_is_non_empty_string(self, ad_data):
        for response in ad_data:
            fb_id = response.get(SmartEditCampaignTreesStructureField.FACEBOOK_PAGE_ID.value)
            if fb_id:
                assert isinstance(fb_id, str)
                assert len(fb_id) > 0

    def test_ig_id_is_non_empty_string(self, ad_data):
        for response in ad_data:
            ig_id = response.get(SmartEditCampaignTreesStructureField.INSTAGRAM_PAGE_ID.value)
            if ig_id:
                assert isinstance(ig_id, str)
                assert len(ig_id) > 0

    def test_post_id_is_non_empty_string(self, ad_data):
        for response in ad_data:
            post_id = response.get(SmartEditCampaignTreesStructureField.POST_ID.value)
            if post_id:
                assert isinstance(post_id, str)
                assert len(post_id) > 0

    def test_ad_pixel_id_is_non_empty_string(self, ad_data):
        for response in ad_data:
            pixel_id = response.get(SmartEditCampaignTreesStructureField.PIXEL_ID.value)
            if pixel_id:
                assert isinstance(pixel_id, str)
                assert len(pixel_id) > 0

    def test_ad_pixel_app_event_is_non_empty_string(self, ad_data):
        for response in ad_data:
            pixel_app_event = response.get(SmartEditCampaignTreesStructureField.PIXEL_APP_EVENT_ID.value)
            if pixel_app_event:
                assert isinstance(pixel_app_event, str)
                assert len(pixel_app_event) > 0

    def test_advert_is_dict(self, ad_data):
        for response in ad_data:
            advert = response.get(SmartEditCampaignTreesStructureField.ADVERT.value)
            if advert:
                assert isinstance(advert, dict)

    ##  Advert tests ##

    @pytest.fixture(scope="session")
    def advert_data(self, ad_data):
        data = []
        for response in ad_data:
            advert = response.get(SmartEditCampaignTreesStructureField.ADVERT.value)
            data.append(advert)
        return data

    def test_advert_media_url_is_non_empty_string(self, advert_data):
        for response in advert_data:
            media_url = response.get(SmartEditCampaignTreesStructureField.MEDIA_URL.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and media_url:
                assert isinstance(media_url, str)
                assert len(media_url) > 0

    def test_advert_primary_text_is_non_empty_string(self, advert_data):
        for response in advert_data:
            primary_text = response.get(SmartEditCampaignTreesStructureField.PRIMARY_TEXT.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and primary_text:
                assert isinstance(primary_text, str)
                assert len(primary_text) > 0

    def test_advert_headline_is_non_empty_string(self, advert_data):
        for response in advert_data:
            headline = response.get(SmartEditCampaignTreesStructureField.HEADLINE.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and headline:
                assert isinstance(headline, str)
                assert len(headline) > 0

    def test_advert_description_is_non_empty_string(self, advert_data):
        for response in advert_data:
            description = response.get(SmartEditCampaignTreesStructureField.DESCRIPTION.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and description:
                assert isinstance(description, str)
                assert len(description) > 0

    def test_advert_website_url_is_non_empty_string(self, advert_data):
        for response in advert_data:
            website_url = response.get(SmartEditCampaignTreesStructureField.WEBSITE_URL.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and website_url:
                assert isinstance(website_url, str)
                assert len(website_url) > 0

    def test_advert_call_to_action_is_non_empty_string_or_dict(self, advert_data):
        for response in advert_data:
            call_to_action = response.get(SmartEditCampaignTreesStructureField.CALL_TO_ACTION.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and call_to_action:
                assert isinstance(call_to_action, str) or isinstance(call_to_action, dict)
                assert len(call_to_action) > 0

    def test_advert_display_link_is_non_empty_string(self, advert_data):
        for response in advert_data:
            display_link = response.get(SmartEditCampaignTreesStructureField.CALL_TO_ACTION.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and display_link:
                assert isinstance(display_link, str)
                assert len(display_link) > 0

    def test_media_type(self, advert_data):
        for response in advert_data:
            media_type = response.get(SmartEditCampaignTreesStructureField.MEDIA_TYPE.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and media_type:
                assert isinstance(media_type, int)
                assert media_type in range(1, 7)

    def test_picture_is_non_empty_string(self, advert_data):
        for response in advert_data:
            picture = response.get(SmartEditCampaignTreesStructureField.PICTURE.value)
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if not cards and picture:
                assert isinstance(picture, list)

    def test_cards_is_list(self, advert_data):
        for response in advert_data:
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if cards:
                assert isinstance(cards, list)

    def test_add_card_page_is_bool(self, advert_data):
        for response in advert_data:
            add_card_page = response.get(SmartEditCampaignTreesStructureField.ADD_CARD_WITH_PAGE_PROFILE.value)
            if add_card_page:
                assert isinstance(add_card_page, bool)

    ##  Carasoul tests ##

    @pytest.fixture(scope="session")
    def card_data(self, advert_data):
        data = []
        for response in advert_data:
            cards = response.get(SmartEditCampaignTreesStructureField.CARDS.value)
            if cards:
                data.append(cards)
        return data

    def test_cards_media_type(self, card_data):
        for response in card_data:
            media_type = response.get(SmartEditCampaignTreesStructureField.MEDIA_TYPE.value)
            if media_type:
                assert isinstance(media_type, int)
                assert media_type in range(1, 7)

    def test_card_description_is_non_empty_string(self, card_data):
        for response in card_data:
            description = response.get(SmartEditCampaignTreesStructureField.DESCRIPTION.value)
            assert isinstance(description, str)
            assert len(description) > 0

    def test_card_headline_is_non_empty_string(self, card_data):
        for response in card_data:
            headline = response.get(SmartEditCampaignTreesStructureField.HEADLINE.value)
            assert isinstance(headline, str)
            assert len(headline) > 0

    def test_card_video_id_is_non_empty_string(self, card_data):
        for response in card_data:
            video_id = response.get(SmartEditCampaignTreesStructureField.VIDEO_ID.value)
            if video_id:
                assert isinstance(video_id, str)
                assert len(video_id) > 0

    def test_card_picture_is_non_empty_string(self, card_data):
        for response in card_data:
            picture = response.get(SmartEditCampaignTreesStructureField.PICTURE.value)
            if picture:
                assert isinstance(picture, str)
                assert len(picture) > 0
