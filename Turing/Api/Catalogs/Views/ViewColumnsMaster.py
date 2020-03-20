from Core.Tools.Misc.Autoincrement import Autoincrement
from Turing.Api.Catalogs.Columns.MetadataColumnsPool import MetadataColumnsPool
from Turing.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from Turing.Api.Catalogs.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Turing.Api.Catalogs.Columns.ViewColumns.ViewColumnType import ViewColumnType

id = Autoincrement(0)


class ViewColumnsMaster:
        effective_status = ViewColumn(id.increment_as_string(), display_name="MongoRepositoryStatusBase", primary_value=MetadataColumnsPool.effective_status, type_id=ViewColumnType.button.id, category_id=ViewColumnCategory.common.id, is_fixed=True)

        delivery = ViewColumn(id.increment_as_string(), display_name="Delivery", primary_value=MetadataColumnsPool.effective_status, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id, is_fixed=True)

        ad_account_id = ViewColumn(id.increment_as_string(), display_name="Ad account id", primary_value=MetadataColumnsPool.ad_account_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        account_name = ViewColumn(id.increment_as_string(), display_name="Account name", primary_value=MetadataColumnsPool.account_name, secondary_value=MetadataColumnsPool.ad_account_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        ad_id = ViewColumn(id.increment_as_string(), display_name="Ad id", primary_value=MetadataColumnsPool.ad_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        ad_name = ViewColumn(id.increment_as_string(), display_name="Ad name", primary_value=MetadataColumnsPool.ad_name, secondary_value=MetadataColumnsPool.ad_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        adset_id = ViewColumn(id.increment_as_string(), display_name="Adset id", primary_value=MetadataColumnsPool.adset_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        adset_name = ViewColumn(id.increment_as_string(), display_name="Adset name", primary_value=MetadataColumnsPool.adset_name, secondary_value=MetadataColumnsPool.adset_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        buying_type = ViewColumn(id.increment_as_string(), display_name="Buying type", primary_value=MetadataColumnsPool.buying_type, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        campaign_id = ViewColumn(id.increment_as_string(), display_name="Campaign id", primary_value=MetadataColumnsPool.campaign_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        campaign_name = ViewColumn(id.increment_as_string(), display_name="Campaign name", primary_value=MetadataColumnsPool.campaign_name, secondary_value=MetadataColumnsPool.campaign_id, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        tags = ViewColumn(id.increment_as_string(), display_name="Tags", primary_value=MetadataColumnsPool.tags, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        objective = ViewColumn(id.increment_as_string(), display_name="Objective", primary_value=MetadataColumnsPool.objective, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        created_at = ViewColumn(id.increment_as_string(), display_name="Date created", primary_value=MetadataColumnsPool.created_at, type_id=ViewColumnType.date.id, category_id=ViewColumnCategory.settings.id)

        last_significant_edit = ViewColumn(id.increment_as_string(), display_name="Last significant edit", primary_value=MetadataColumnsPool.last_significant_edit, type_id=ViewColumnType.date.id, category_id=ViewColumnCategory.settings.id)

        start_date = ViewColumn(id.increment_as_string(), display_name="Start date", primary_value=MetadataColumnsPool.start_date, type_id=ViewColumnType.date.id, category_id=ViewColumnCategory.settings.id)

        end_date = ViewColumn(id.increment_as_string(), display_name="End date", primary_value=MetadataColumnsPool.end_date, type_id=ViewColumnType.date.id, category_id=ViewColumnCategory.settings.id)

        bid_strategy = ViewColumn(id.increment_as_string(), display_name="Bid stategy", primary_value=MetadataColumnsPool.bid_strategy, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        amount_spent_percentage = ViewColumn(id.increment_as_string(), display_name="Amount spent percentage", primary_value=MetadataColumnsPool.amount_spent_percentage, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.settings.id)

        budget = ViewColumn(id.increment_as_string(), display_name="Budget", primary_value=MetadataColumnsPool.budget, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.settings.id)

        budget_remaining = ViewColumn(id.increment_as_string(), display_name="Budget remaining", primary_value=MetadataColumnsPool.budget_remaining, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.settings.id)

        bid_cap = ViewColumn(id.increment_as_string(), display_name="Bid cap", primary_value=MetadataColumnsPool.bid_cap, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.settings.id)

        location = ViewColumn(id.increment_as_string(), display_name="Location", primary_value=MetadataColumnsPool.location, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        age = ViewColumn(id.increment_as_string(), display_name="Age", primary_value=MetadataColumnsPool.age, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        gender = ViewColumn(id.increment_as_string(), display_name="Gender", primary_value=MetadataColumnsPool.gender, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        included_custom_audiences = ViewColumn(id.increment_as_string(), display_name="Included custom audiences", primary_value=MetadataColumnsPool.included_custom_audiences, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        excluded_custom_audiences = ViewColumn(id.increment_as_string(), display_name="Excluded custom audiences", primary_value=MetadataColumnsPool.excluded_custom_audiences, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        page_name = ViewColumn(id.increment_as_string(), display_name="Page name", primary_value=MetadataColumnsPool.page_name, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        headline = ViewColumn(id.increment_as_string(), display_name="Headline", primary_value=MetadataColumnsPool.headline, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        body = ViewColumn(id.increment_as_string(), display_name="Body", primary_value=MetadataColumnsPool.body, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        link = ViewColumn(id.increment_as_string(), display_name="Link", primary_value=MetadataColumnsPool.link, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        destination = ViewColumn(id.increment_as_string(), display_name="Destination", primary_value=MetadataColumnsPool.destination, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        url_parameters = ViewColumn(id.increment_as_string(), display_name="Url parameters", primary_value=MetadataColumnsPool.url_parameters, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        pixel = ViewColumn(id.increment_as_string(), display_name="Pixel", primary_value=MetadataColumnsPool.pixel, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        app_event = ViewColumn(id.increment_as_string(), display_name="App event", primary_value=MetadataColumnsPool.app_event, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        offline_event = ViewColumn(id.increment_as_string(), display_name="Offline event", primary_value=MetadataColumnsPool.offline_event, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.settings.id)

        canvas_avg_view_percentage = ViewColumn(id.increment_as_string(), display_name="Canvas avg view percent", primary_value=MetadataColumnsPool.canvas_avg_view_percent, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.common.id)

        canvas_avg_view_time = ViewColumn(id.increment_as_string(), display_name="Canvas avg view time", primary_value=MetadataColumnsPool.canvas_avg_view_time, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.common.id)

        clicks = ViewColumn(id.increment_as_string(), display_name="Clicks", primary_value=MetadataColumnsPool.clicks, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        conversion_rate_ranking = ViewColumn(id.increment_as_string(), display_name="Conversion rate ranking", primary_value=MetadataColumnsPool.conversion_rate_ranking, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.performance.id)

        cost_per_estimated_ad_recallers = ViewColumn(id.increment_as_string(), display_name="Cost per estimated ad recall lift (people)", primary_value=MetadataColumnsPool.cost_per_estimated_ad_recallers, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        # costPerInlineLinkClick = ViewColumn(id.increment_as_string(), display_name="Cost per inline link click", primary_value=MetadataColumnsPool.costPerInlineLinkClick, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.performance.id)

        # costPerInlinePostEngagement = ViewColumn(id.increment_as_string(), display_name="Cost per inline post engagement", primary_value=MetadataColumnsPool.costPerInlinePostEngagement, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_unique_click = ViewColumn(id.increment_as_string(), display_name="Cost per unique click", primary_value=MetadataColumnsPool.cost_per_unique_click, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        # costPerUniqueInlineLinkClick = ViewColumn(id.increment_as_string(), display_name="Cost per unique inline link click", primary_value=MetadataColumnsPool.costPerUniqueInlineLinkClick, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cpc = ViewColumn(id.increment_as_string(), display_name="CPC", primary_value=MetadataColumnsPool.cpc, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.performance.id)

        cpm = ViewColumn(id.increment_as_string(), display_name="CPM", primary_value=MetadataColumnsPool.cpm, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.performance.id)

        cpp = ViewColumn(id.increment_as_string(), display_name="CPP", primary_value=MetadataColumnsPool.cpp, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.performance.id)

        ctr = ViewColumn(id.increment_as_string(), display_name="CTR", primary_value=MetadataColumnsPool.ctr, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.performance.id)

        date_start = ViewColumn(id.increment_as_string(), display_name="Date", primary_value=MetadataColumnsPool.date_start, type_id=ViewColumnType.date.id, category_id=ViewColumnCategory.common.id)

        # date_stop = ViewColumn(id.increment_as_string(), display_name="Date stop", primary_value=MetadataColumnsPool.date_stop, field_type=ViewColumnType.date.id, category_id=ViewColumnCategory.common.id)

        engagement_rate_ranking = ViewColumn(id.increment_as_string(), display_name="Engagement rate ranking", primary_value=MetadataColumnsPool.engagement_rate_ranking, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.performance.id)

        estimated_ad_recall_rate = ViewColumn(id.increment_as_string(), display_name="Estimated ad recall rate", primary_value=MetadataColumnsPool.estimated_ad_recall_rate, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        estimated_ad_recallers = ViewColumn(id.increment_as_string(), display_name="Estimated ad recallers", primary_value=MetadataColumnsPool.estimated_ad_recallers, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        frequency = ViewColumn(id.increment_as_string(), display_name="Frequency", primary_value=MetadataColumnsPool.frequency, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        full_view_impressions = ViewColumn(id.increment_as_string(), display_name="Full view impressions", primary_value=MetadataColumnsPool.full_view_impressions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        full_view_reach = ViewColumn(id.increment_as_string(), display_name="Full view reach", primary_value=MetadataColumnsPool.full_view_reach, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        impressions = ViewColumn(id.increment_as_string(), display_name="Impressions", primary_value=MetadataColumnsPool.impressions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        # inlineLinkClickCtr = ViewColumn(id.increment_as_string(), display_name="Inline link click CTR", primary_value=MetadataColumnsPool.inlineLinkClickCtr, field_type=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        # inlineLinkClicks = ViewColumn(id.increment_as_string(), display_name="Inline link clicks", primary_value=MetadataColumnsPool.inlineLinkClicks, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # inlinePostEngagement = ViewColumn(id.increment_as_string(), display_name="Inline post engagement", primary_value=MetadataColumnsPool.inlinePostEngagement, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        instant_experience_clicks_to_open = ViewColumn(id.increment_as_string(), display_name="Instant experience clicks to open", primary_value=MetadataColumnsPool.instant_experience_clicks_to_open, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        instant_experience_clicks_to_start = ViewColumn(id.increment_as_string(), display_name="Instant experience clicks to start", primary_value=MetadataColumnsPool.instant_experience_clicks_to_start, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        instant_experience_outbound_clicks = ViewColumn(id.increment_as_string(), display_name="Instant experience outbound clicks", primary_value=MetadataColumnsPool.instant_experience_outbound_clicks, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # placePageName = ViewColumn(id.increment_as_string(), display_name="Place page name", primary_value=MetadataColumnsPool.placePageName, field_type=ViewColumnType.text.id, category_id=ViewColumnCategory.engagement.id)

        quality_ranking = ViewColumn(id.increment_as_string(), display_name="Quality ranking", primary_value=MetadataColumnsPool.quality_ranking, type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.performance.id)

        reach = ViewColumn(id.increment_as_string(), display_name="Reach", primary_value=MetadataColumnsPool.reach, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        social_spend = ViewColumn(id.increment_as_string(), display_name="Social spend", primary_value=MetadataColumnsPool.social_spend, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        spend = ViewColumn(id.increment_as_string(), display_name="Amount spent", primary_value=MetadataColumnsPool.spend, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        unique_clicks = ViewColumn(id.increment_as_string(), display_name="Unique clicks", primary_value=MetadataColumnsPool.unique_clicks, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        unique_ctr = ViewColumn(id.increment_as_string(), display_name="Unique CTR", primary_value=MetadataColumnsPool.unique_ctr, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        # uniqueInlineLinkClickCtr = ViewColumn(id.increment_as_string(), display_name="Unique inline link click CTR", primary_value=MetadataColumnsPool.uniqueInlineLinkClickCtr, field_type=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        # uniqueInlineLinkClicks = ViewColumn(id.increment_as_string(), display_name="Unique inline link clicks", primary_value=MetadataColumnsPool.uniqueInlineLinkClicks, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        unique_link_clicks_ctr = ViewColumn(id.increment_as_string(), display_name="Unique link clicks CTR", primary_value=MetadataColumnsPool.unique_link_clicks_ctr, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        page_engagement = ViewColumn(id.increment_as_string(), display_name="Page engagement", primary_value=MetadataColumnsPool.page_engagement, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        like = ViewColumn(id.increment_as_string(), display_name="Page likes", primary_value=MetadataColumnsPool.like, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        comment = ViewColumn(id.increment_as_string(), display_name="Comment", primary_value=MetadataColumnsPool.comment, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        post_engagement = ViewColumn(id.increment_as_string(), display_name="post engagement", primary_value=MetadataColumnsPool.post_engagement, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        post_reaction = ViewColumn(id.increment_as_string(), display_name="post reaction", primary_value=MetadataColumnsPool.post_reaction, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # onsiteConversion = ViewColumn(id.increment_as_string(), display_name="Onsite conversion", primary_value=MetadataColumnsPool.onsiteConversion, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        post_share = ViewColumn(id.increment_as_string(), display_name="post share", primary_value=MetadataColumnsPool.post_share, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        photo_view = ViewColumn(id.increment_as_string(), display_name="Photo view", primary_value=MetadataColumnsPool.photo_view, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        event_responses = ViewColumn(id.increment_as_string(), display_name="Event response", primary_value=MetadataColumnsPool.event_responses, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # effectShare = ViewColumn(id.increment_as_string(), display_name="Effect share", primary_value=MetadataColumnsPool.effectShare, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_page_engagement = ViewColumn(id.increment_as_string(), display_name="Cost per page engagement", primary_value=MetadataColumnsPool.cost_per_page_engagement, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_like = ViewColumn(id.increment_as_string(), display_name="Cost per like", primary_value=MetadataColumnsPool.cost_per_like, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_post_engagement = ViewColumn(id.increment_as_string(), display_name="Cost per post engagement", primary_value=MetadataColumnsPool.cost_per_post_engagement, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_event_response = ViewColumn(id.increment_as_string(), display_name="Cost per event response", primary_value=MetadataColumnsPool.cost_per_event_response, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        link_click_website_ctr = ViewColumn(id.increment_as_string(), display_name="Link click website CTR", primary_value=MetadataColumnsPool.link_click_website_ctr, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        website_purchase_roas = ViewColumn(id.increment_as_string(), display_name="Website purchase ROAS", primary_value=MetadataColumnsPool.website_purchase_roas, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.performance.id)

        purchase_roas = ViewColumn(id.increment_as_string(), display_name="Purchase ROAS", primary_value=MetadataColumnsPool.purchase_roas, type_id=ViewColumnType.percentage.id, category_id=ViewColumnCategory.performance.id)

        link_click = ViewColumn(id.increment_as_string(), display_name="Link click", primary_value=MetadataColumnsPool.link_click, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        unique_link_click = ViewColumn(id.increment_as_string(), display_name="Unique link click", primary_value=MetadataColumnsPool.unique_link_click, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        outbound_click = ViewColumn(id.increment_as_string(), display_name="Outbound click", primary_value=MetadataColumnsPool.outbound_click, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        unique_outbound_click = ViewColumn(id.increment_as_string(), display_name="Unique outbound click", primary_value=MetadataColumnsPool.unique_outbound_click, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # outboundCtr = ViewColumn(id.increment_as_string(), display_name="Outbound CTR", primary_value=MetadataColumnsPool.outboundCtr, field_type=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        # uniqueOutboundCtr = ViewColumn(id.increment_as_string(), display_name="Unique outbound CTR", primary_value=MetadataColumnsPool.uniqueOutboundCtr, field_type=ViewColumnType.percentage.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_outbound_click = ViewColumn(id.increment_as_string(), display_name="Cost per outbound click", primary_value=MetadataColumnsPool.cost_per_outbound_click, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_unique_outbound_click = ViewColumn(id.increment_as_string(), display_name="Cost per unique outbound click", primary_value=MetadataColumnsPool.cost_per_unique_outbound_click, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.engagement.id)

        # offsiteConversionFbPixelAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Website add payment info", primary_value=MetadataColumnsPool.offsiteConversionFbPixelAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # addPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Add payment info", primary_value=MetadataColumnsPool.addPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # omniAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Omni add payment info", primary_value=MetadataColumnsPool.omniAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # mobileAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Mobile add payment info", primary_value=MetadataColumnsPool.mobileAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # uniqueOffsiteConversionFbPixelAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Unique add payment info", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # uniqueAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Unique add payment info", primary_value=MetadataColumnsPool.uniqueAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # uniqueOmniAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Unique omni add payment info", primary_value=MetadataColumnsPool.uniqueOmniAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # uniqueMobileAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Unique mobile add payment info", primary_value=MetadataColumnsPool.uniqueMobileAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # valueOffsiteConversionFbPixelAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Value website add payment info", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # valueAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Value add payment info", primary_value=MetadataColumnsPool.valueAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # valueOmniAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Value omni add payment info", primary_value=MetadataColumnsPool.valueOmniAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # valueMobileAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Value mobile add payment info", primary_value=MetadataColumnsPool.valueMobileAddPaymentInfo, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # costOffsiteConversionFbPixelAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost website add payment info", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost add payment info", primary_value=MetadataColumnsPool.costAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costOmniAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost omni add payment info", primary_value=MetadataColumnsPool.costOmniAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costMobileAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost mobile add payment info", primary_value=MetadataColumnsPool.costMobileAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costPerUniqueOffsiteConversionFbPixelAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost per unique website add payment info", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costPerUniqueAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost per unique add payment info", primary_value=MetadataColumnsPool.costPerUniqueAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costPerUniqueOmniAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni add payment info", primary_value=MetadataColumnsPool.costPerUniqueOmniAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # costPerUniqueMobileAddPaymentInfo = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile add payment info", primary_value=MetadataColumnsPool.costPerUniqueMobileAddPaymentInfo, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)

        # offsiteConversionFbPixelAddToCart = ViewColumn(id.increment_as_string(), display_name="Website add to cart", primary_value=MetadataColumnsPool.offsiteConversionFbPixelAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # addToCart = ViewColumn(id.increment_as_string(), display_name="Add to cart", primary_value=MetadataColumnsPool.addToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # omniAddToCart = ViewColumn(id.increment_as_string(), display_name="Omni add to cart", primary_value=MetadataColumnsPool.omniAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileAddToCart = ViewColumn(id.increment_as_string(), display_name="Mobile add to cart", primary_value=MetadataColumnsPool.mobileAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelAddToCart = ViewColumn(id.increment_as_string(), display_name="Unique website add to cart", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueAddToCart = ViewColumn(id.increment_as_string(), display_name="Unique add to cart", primary_value=MetadataColumnsPool.uniqueAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniAddToCart = ViewColumn(id.increment_as_string(), display_name="Unique omni add to cart", primary_value=MetadataColumnsPool.uniqueOmniAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileAddToCart = ViewColumn(id.increment_as_string(), display_name="Unique mobile add to cart", primary_value=MetadataColumnsPool.uniqueMobileAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelAddToCart = ViewColumn(id.increment_as_string(), display_name="Value website add to cart", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueAddToCart = ViewColumn(id.increment_as_string(), display_name="Value add to cart", primary_value=MetadataColumnsPool.valueAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniAddToCart = ViewColumn(id.increment_as_string(), display_name="Value omni add to cart", primary_value=MetadataColumnsPool.valueOmniAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileAddToCart = ViewColumn(id.increment_as_string(), display_name="Value mobile add to cart", primary_value=MetadataColumnsPool.valueMobileAddToCart, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost website add to cart", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost add to cart", primary_value=MetadataColumnsPool.costAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost omni add to cart", primary_value=MetadataColumnsPool.costOmniAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost mobile add to cart", primary_value=MetadataColumnsPool.costMobileAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost per unique website add to cart", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost per unique add to cart", primary_value=MetadataColumnsPool.costPerUniqueAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni add to cart", primary_value=MetadataColumnsPool.costPerUniqueOmniAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileAddToCart = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile add to cart", primary_value=MetadataColumnsPool.costPerUniqueMobileAddToCart, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Website add to wishlist", primary_value=MetadataColumnsPool.offsiteConversionFbPixelAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # addToWishlist = ViewColumn(id.increment_as_string(), display_name="Add to wishlist", primary_value=MetadataColumnsPool.addToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Omni add to wishlist", primary_value=MetadataColumnsPool.omniAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Mobile add to wishlist", primary_value=MetadataColumnsPool.mobileAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Unique website add to wishlist", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Unique add to wishlist", primary_value=MetadataColumnsPool.uniqueAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Unique omni add to wishlist", primary_value=MetadataColumnsPool.uniqueOmniAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Unique mobile add to wishlist", primary_value=MetadataColumnsPool.uniqueMobileAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Value website add to wishlist", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Value add to wishlist", primary_value=MetadataColumnsPool.valueAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Value omni add to wishlist", primary_value=MetadataColumnsPool.valueOmniAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Value mobile add to wishlist", primary_value=MetadataColumnsPool.valueMobileAddToWishlist, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost website add to wishlist", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost add to wishlist", primary_value=MetadataColumnsPool.costAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost omni add to wishlist", primary_value=MetadataColumnsPool.costOmniAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost mobile add to wishlist", primary_value=MetadataColumnsPool.costMobileAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost per unique website add to wishlist", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost per unique add to wishlist", primary_value=MetadataColumnsPool.costPerUniqueAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni add to wishlist", primary_value=MetadataColumnsPool.costPerUniqueOmniAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileAddToWishlist = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile add to wishlist", primary_value=MetadataColumnsPool.costPerUniqueMobileAddToWishlist, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Website complete registration", primary_value=MetadataColumnsPool.offsiteConversionFbPixelCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # completeRegistration = ViewColumn(id.increment_as_string(), display_name="Complete registration", primary_value=MetadataColumnsPool.completeRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Omni complete registration", primary_value=MetadataColumnsPool.omniCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Mobile complete registration", primary_value=MetadataColumnsPool.mobileCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Unique website complete registration", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Unique complete registration", primary_value=MetadataColumnsPool.uniqueCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Unique omni complete registration", primary_value=MetadataColumnsPool.uniqueOmniCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Unique mobile complete registration", primary_value=MetadataColumnsPool.uniqueMobileCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Value website complete registration", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Value complete registration", primary_value=MetadataColumnsPool.valueCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Value omni complete registration", primary_value=MetadataColumnsPool.valueOmniCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Value mobile complete registration", primary_value=MetadataColumnsPool.valueMobileCompleteRegistration, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost website complete registration", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost complete registration", primary_value=MetadataColumnsPool.costCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost omni complete registration", primary_value=MetadataColumnsPool.costOmniCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost mobile complete registration", primary_value=MetadataColumnsPool.costMobileCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost per unique website complete registration", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost per unique complete registration", primary_value=MetadataColumnsPool.costPerUniqueCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni complete registration", primary_value=MetadataColumnsPool.costPerUniqueOmniCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileCompleteRegistration = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile complete registration", primary_value=MetadataColumnsPool.costPerUniqueMobileCompleteRegistration, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelContact = ViewColumn(id.increment_as_string(), display_name="Website contact", primary_value=MetadataColumnsPool.offsiteConversionFbPixelContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # contact = ViewColumn(id.increment_as_string(), display_name="Contact", primary_value=MetadataColumnsPool.contact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniContact = ViewColumn(id.increment_as_string(), display_name="Omni contact", primary_value=MetadataColumnsPool.omniContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileContact = ViewColumn(id.increment_as_string(), display_name="Mobile contact", primary_value=MetadataColumnsPool.mobileContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelContact = ViewColumn(id.increment_as_string(), display_name="Unique website contact", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueContact = ViewColumn(id.increment_as_string(), display_name="Unique contact", primary_value=MetadataColumnsPool.uniqueContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniContact = ViewColumn(id.increment_as_string(), display_name="Unique omni contact", primary_value=MetadataColumnsPool.uniqueOmniContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileContact = ViewColumn(id.increment_as_string(), display_name="Unique mobile contact", primary_value=MetadataColumnsPool.uniqueMobileContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelContact = ViewColumn(id.increment_as_string(), display_name="Value website contact", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueContact = ViewColumn(id.increment_as_string(), display_name="Value contact", primary_value=MetadataColumnsPool.valueContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniContact = ViewColumn(id.increment_as_string(), display_name="Value omni contact", primary_value=MetadataColumnsPool.valueOmniContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileContact = ViewColumn(id.increment_as_string(), display_name="Value mobile contact", primary_value=MetadataColumnsPool.valueMobileContact, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelContact = ViewColumn(id.increment_as_string(), display_name="Cost website contact", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costContact = ViewColumn(id.increment_as_string(), display_name="Cost contact", primary_value=MetadataColumnsPool.costContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniContact = ViewColumn(id.increment_as_string(), display_name="Cost omni contact", primary_value=MetadataColumnsPool.costOmniContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileContact = ViewColumn(id.increment_as_string(), display_name="Cost mobile contact", primary_value=MetadataColumnsPool.costMobileContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelContact = ViewColumn(id.increment_as_string(), display_name="Cost per unique website contact", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueContact = ViewColumn(id.increment_as_string(), display_name="Cost per unique contact", primary_value=MetadataColumnsPool.costPerUniqueContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniContact = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni contact", primary_value=MetadataColumnsPool.costPerUniqueOmniContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileContact = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile contact", primary_value=MetadataColumnsPool.costPerUniqueMobileContact, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Website customize product", primary_value=MetadataColumnsPool.offsiteConversionFbPixelCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # customizeProduct = ViewColumn(id.increment_as_string(), display_name="Customize product", primary_value=MetadataColumnsPool.customizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Omni customize product", primary_value=MetadataColumnsPool.omniCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Mobile customize product", primary_value=MetadataColumnsPool.mobileCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Unique website customize product", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Unique customize product", primary_value=MetadataColumnsPool.uniqueCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Unique omni customize product", primary_value=MetadataColumnsPool.uniqueOmniCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Unique mobile customize product", primary_value=MetadataColumnsPool.uniqueMobileCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Value website customize product", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Value customize product", primary_value=MetadataColumnsPool.valueCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Value omni customize product", primary_value=MetadataColumnsPool.valueOmniCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Value mobile customize product", primary_value=MetadataColumnsPool.valueMobileCustomizeProduct, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost website customize product", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost customize product", primary_value=MetadataColumnsPool.costCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost omni customize product", primary_value=MetadataColumnsPool.costOmniCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost mobile customize product", primary_value=MetadataColumnsPool.costMobileCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost per unique website customize product", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost per unique customize product", primary_value=MetadataColumnsPool.costPerUniqueCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni customize product", primary_value=MetadataColumnsPool.costPerUniqueOmniCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileCustomizeProduct = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile customize product", primary_value=MetadataColumnsPool.costPerUniqueMobileCustomizeProduct, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelDonate = ViewColumn(id.increment_as_string(), display_name="Website donate", primary_value=MetadataColumnsPool.offsiteConversionFbPixelDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # donate = ViewColumn(id.increment_as_string(), display_name="Donate", primary_value=MetadataColumnsPool.donate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniDonate = ViewColumn(id.increment_as_string(), display_name="Omni donate", primary_value=MetadataColumnsPool.omniDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileDonate = ViewColumn(id.increment_as_string(), display_name="Mobile donate", primary_value=MetadataColumnsPool.mobileDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelDonate = ViewColumn(id.increment_as_string(), display_name="Unique website donate", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueDonate = ViewColumn(id.increment_as_string(), display_name="Unique donate", primary_value=MetadataColumnsPool.uniqueDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniDonate = ViewColumn(id.increment_as_string(), display_name="Unique omni donate", primary_value=MetadataColumnsPool.uniqueOmniDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileDonate = ViewColumn(id.increment_as_string(), display_name="Unique mobile donate", primary_value=MetadataColumnsPool.uniqueMobileDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelDonate = ViewColumn(id.increment_as_string(), display_name="Value website donate", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueDonate = ViewColumn(id.increment_as_string(), display_name="Value donate", primary_value=MetadataColumnsPool.valueDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniDonate = ViewColumn(id.increment_as_string(), display_name="Value omni donate", primary_value=MetadataColumnsPool.valueOmniDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileDonate = ViewColumn(id.increment_as_string(), display_name="Value mobile donate", primary_value=MetadataColumnsPool.valueMobileDonate, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelDonate = ViewColumn(id.increment_as_string(), display_name="Cost website donate", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costDonate = ViewColumn(id.increment_as_string(), display_name="Cost donate", primary_value=MetadataColumnsPool.costDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniDonate = ViewColumn(id.increment_as_string(), display_name="Cost omni donate", primary_value=MetadataColumnsPool.costOmniDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileDonate = ViewColumn(id.increment_as_string(), display_name="Cost mobile donate", primary_value=MetadataColumnsPool.costMobileDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelDonate = ViewColumn(id.increment_as_string(), display_name="Cost per unique website donate", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueDonate = ViewColumn(id.increment_as_string(), display_name="Cost per unique donate", primary_value=MetadataColumnsPool.costPerUniqueDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniDonate = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni donate", primary_value=MetadataColumnsPool.costPerUniqueOmniDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileDonate = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile donate", primary_value=MetadataColumnsPool.costPerUniqueMobileDonate, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelFindLocation = ViewColumn(id.increment_as_string(), display_name="Website find location", primary_value=MetadataColumnsPool.offsiteConversionFbPixelFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # findLocation = ViewColumn(id.increment_as_string(), display_name="get location", primary_value=MetadataColumnsPool.findLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniFindLocation = ViewColumn(id.increment_as_string(), display_name="Omni find location", primary_value=MetadataColumnsPool.omniFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileFindLocation = ViewColumn(id.increment_as_string(), display_name="Mobile find location", primary_value=MetadataColumnsPool.mobileFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelFindLocation = ViewColumn(id.increment_as_string(), display_name="Unique website find location", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueFindLocation = ViewColumn(id.increment_as_string(), display_name="Unique find location", primary_value=MetadataColumnsPool.uniqueFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniFindLocation = ViewColumn(id.increment_as_string(), display_name="Unique omni find location", primary_value=MetadataColumnsPool.uniqueOmniFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileFindLocation = ViewColumn(id.increment_as_string(), display_name="Unique mobile find location", primary_value=MetadataColumnsPool.uniqueMobileFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelFindLocation = ViewColumn(id.increment_as_string(), display_name="Value website find location", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueFindLocation = ViewColumn(id.increment_as_string(), display_name="Value find location", primary_value=MetadataColumnsPool.valueFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniFindLocation = ViewColumn(id.increment_as_string(), display_name="Value omni find location", primary_value=MetadataColumnsPool.valueOmniFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileFindLocation = ViewColumn(id.increment_as_string(), display_name="Value mobile find location", primary_value=MetadataColumnsPool.valueMobileFindLocation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost website find location", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost find location", primary_value=MetadataColumnsPool.costFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost omni find location", primary_value=MetadataColumnsPool.costOmniFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost mobile find location", primary_value=MetadataColumnsPool.costMobileFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost per unique website find location", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost per unique find location", primary_value=MetadataColumnsPool.costPerUniqueFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni find location", primary_value=MetadataColumnsPool.costPerUniqueOmniFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileFindLocation = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile find location", primary_value=MetadataColumnsPool.costPerUniqueMobileFindLocation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Website initiate checkout", primary_value=MetadataColumnsPool.offsiteConversionFbPixelInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # initiateCheckout = ViewColumn(id.increment_as_string(), display_name="Initiate checkout", primary_value=MetadataColumnsPool.initiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Omni initiate checkout", primary_value=MetadataColumnsPool.omniInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Mobile initiate checkout", primary_value=MetadataColumnsPool.mobileInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Unique website initiate checkout", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Unique initiate checkout", primary_value=MetadataColumnsPool.uniqueInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Unique omni initiate checkout", primary_value=MetadataColumnsPool.uniqueOmniInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Unique mobile initiate checkout", primary_value=MetadataColumnsPool.uniqueMobileInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Value website initiate checkout", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Value initiate checkout", primary_value=MetadataColumnsPool.valueInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Value omni initiate checkout", primary_value=MetadataColumnsPool.valueOmniInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Value mobile initiate checkout", primary_value=MetadataColumnsPool.valueMobileInitiateCheckout, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost website initiate checkout", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost initiate checkout", primary_value=MetadataColumnsPool.costInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost omni initiate checkout", primary_value=MetadataColumnsPool.costOmniInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost mobile initiate checkout", primary_value=MetadataColumnsPool.costMobileInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost per unique website initiate checkout", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost per unique initiate checkout", primary_value=MetadataColumnsPool.costPerUniqueInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni initiate checkout", primary_value=MetadataColumnsPool.costPerUniqueOmniInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileInitiateCheckout = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile initiate checkout", primary_value=MetadataColumnsPool.costPerUniqueMobileInitiateCheckout, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelLead = ViewColumn(id.increment_as_string(), display_name="Website lead", primary_value=MetadataColumnsPool.offsiteConversionFbPixelLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # lead = ViewColumn(id.increment_as_string(), display_name="Lead", primary_value=MetadataColumnsPool.lead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniLead = ViewColumn(id.increment_as_string(), display_name="Omni lead", primary_value=MetadataColumnsPool.omniLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileLead = ViewColumn(id.increment_as_string(), display_name="Mobile lead", primary_value=MetadataColumnsPool.mobileLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelLead = ViewColumn(id.increment_as_string(), display_name="Unique website lead", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueLead = ViewColumn(id.increment_as_string(), display_name="Unique lead", primary_value=MetadataColumnsPool.uniqueLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniLead = ViewColumn(id.increment_as_string(), display_name="Unique omni lead", primary_value=MetadataColumnsPool.uniqueOmniLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileLead = ViewColumn(id.increment_as_string(), display_name="Unique mobile lead", primary_value=MetadataColumnsPool.uniqueMobileLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelLead = ViewColumn(id.increment_as_string(), display_name="Value website lead", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueLead = ViewColumn(id.increment_as_string(), display_name="Value lead", primary_value=MetadataColumnsPool.valueLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniLead = ViewColumn(id.increment_as_string(), display_name="Value omni lead", primary_value=MetadataColumnsPool.valueOmniLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileLead = ViewColumn(id.increment_as_string(), display_name="Value mobile lead", primary_value=MetadataColumnsPool.valueMobileLead, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelLead = ViewColumn(id.increment_as_string(), display_name="Cost website lead", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costLead = ViewColumn(id.increment_as_string(), display_name="Cost lead", primary_value=MetadataColumnsPool.costLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniLead = ViewColumn(id.increment_as_string(), display_name="Cost omni lead", primary_value=MetadataColumnsPool.costOmniLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileLead = ViewColumn(id.increment_as_string(), display_name="Cost mobile lead", primary_value=MetadataColumnsPool.costMobileLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelLead = ViewColumn(id.increment_as_string(), display_name="Cost per unique website lead", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueLead = ViewColumn(id.increment_as_string(), display_name="Cost per unique lead", primary_value=MetadataColumnsPool.costPerUniqueLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniLead = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni lead", primary_value=MetadataColumnsPool.costPerUniqueOmniLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileLead = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile lead", primary_value=MetadataColumnsPool.costPerUniqueMobileLead, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelPurchase = ViewColumn(id.increment_as_string(), display_name="Website purchase", primary_value=MetadataColumnsPool.offsiteConversionFbPixelPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # purchase = ViewColumn(id.increment_as_string(), display_name="Purchase", primary_value=MetadataColumnsPool.purchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniPurchase = ViewColumn(id.increment_as_string(), display_name="Omni purchase", primary_value=MetadataColumnsPool.omniPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobilePurchase = ViewColumn(id.increment_as_string(), display_name="Mobile purchase", primary_value=MetadataColumnsPool.mobilePurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelPurchase = ViewColumn(id.increment_as_string(), display_name="Unique website purchase", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniquePurchase = ViewColumn(id.increment_as_string(), display_name="Unique purchase", primary_value=MetadataColumnsPool.uniquePurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniPurchase = ViewColumn(id.increment_as_string(), display_name="Unique omni purchase", primary_value=MetadataColumnsPool.uniqueOmniPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobilePurchase = ViewColumn(id.increment_as_string(), display_name="Unique mobile purchase", primary_value=MetadataColumnsPool.uniqueMobilePurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelPurchase = ViewColumn(id.increment_as_string(), display_name="Value website purchase", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valuePurchase = ViewColumn(id.increment_as_string(), display_name="Value purchase", primary_value=MetadataColumnsPool.valuePurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniPurchase = ViewColumn(id.increment_as_string(), display_name="Value omni purchase", primary_value=MetadataColumnsPool.valueOmniPurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobilePurchase = ViewColumn(id.increment_as_string(), display_name="Value mobile purchase", primary_value=MetadataColumnsPool.valueMobilePurchase, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelPurchase = ViewColumn(id.increment_as_string(), display_name="Cost website purchase", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelPurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPurchase = ViewColumn(id.increment_as_string(), display_name="Cost purchase", primary_value=MetadataColumnsPool.costPurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniPurchase = ViewColumn(id.increment_as_string(), display_name="Cost omni purchase", primary_value=MetadataColumnsPool.costOmniPurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobilePurchase = ViewColumn(id.increment_as_string(), display_name="Cost mobile purchase", primary_value=MetadataColumnsPool.costMobilePurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelPurchase = ViewColumn(id.increment_as_string(), display_name="Cost per unique website purchase", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelPurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniquePurchase = ViewColumn(id.increment_as_string(), display_name="Cost per unique purchase", primary_value=MetadataColumnsPool.costPerUniquePurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniPurchase = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni purchase", primary_value=MetadataColumnsPool.costPerUniqueOmniPurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobilePurchase = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile purchase", primary_value=MetadataColumnsPool.costPerUniqueMobilePurchase, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelSchedule = ViewColumn(id.increment_as_string(), display_name="Website schedule", primary_value=MetadataColumnsPool.offsiteConversionFbPixelSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # schedule = ViewColumn(id.increment_as_string(), display_name="Schedule", primary_value=MetadataColumnsPool.schedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniSchedule = ViewColumn(id.increment_as_string(), display_name="Omni schedule", primary_value=MetadataColumnsPool.omniSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileSchedule = ViewColumn(id.increment_as_string(), display_name="Mobile schedule", primary_value=MetadataColumnsPool.mobileSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelSchedule = ViewColumn(id.increment_as_string(), display_name="Unique website schedule", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueSchedule = ViewColumn(id.increment_as_string(), display_name="Unique schedule", primary_value=MetadataColumnsPool.uniqueSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniSchedule = ViewColumn(id.increment_as_string(), display_name="Unique omni schedule", primary_value=MetadataColumnsPool.uniqueOmniSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileSchedule = ViewColumn(id.increment_as_string(), display_name="Unique mobile schedule", primary_value=MetadataColumnsPool.uniqueMobileSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelSchedule = ViewColumn(id.increment_as_string(), display_name="Value website schedule", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueSchedule = ViewColumn(id.increment_as_string(), display_name="Value schedule", primary_value=MetadataColumnsPool.valueSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniSchedule = ViewColumn(id.increment_as_string(), display_name="Value omni schedule", primary_value=MetadataColumnsPool.valueOmniSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileSchedule = ViewColumn(id.increment_as_string(), display_name="Value mobile schedule", primary_value=MetadataColumnsPool.valueMobileSchedule, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelSchedule = ViewColumn(id.increment_as_string(), display_name="Cost website schedule", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costSchedule = ViewColumn(id.increment_as_string(), display_name="Cost schedule", primary_value=MetadataColumnsPool.costSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniSchedule = ViewColumn(id.increment_as_string(), display_name="Cost omni schedule", primary_value=MetadataColumnsPool.costOmniSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileSchedule = ViewColumn(id.increment_as_string(), display_name="Cost mobile schedule", primary_value=MetadataColumnsPool.costMobileSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelSchedule = ViewColumn(id.increment_as_string(), display_name="Cost per unique website schedule", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueSchedule = ViewColumn(id.increment_as_string(), display_name="Cost per unique schedule", primary_value=MetadataColumnsPool.costPerUniqueSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniSchedule = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni schedule", primary_value=MetadataColumnsPool.costPerUniqueOmniSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileSchedule = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile schedule", primary_value=MetadataColumnsPool.costPerUniqueMobileSchedule, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelSearch = ViewColumn(id.increment_as_string(), display_name="Website search", primary_value=MetadataColumnsPool.offsiteConversionFbPixelSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # search = ViewColumn(id.increment_as_string(), display_name="Search", primary_value=MetadataColumnsPool.search, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniSearch = ViewColumn(id.increment_as_string(), display_name="Omni search", primary_value=MetadataColumnsPool.omniSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileSearch = ViewColumn(id.increment_as_string(), display_name="Mobile search", primary_value=MetadataColumnsPool.mobileSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelSearch = ViewColumn(id.increment_as_string(), display_name="Unique website search", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueSearch = ViewColumn(id.increment_as_string(), display_name="Unique search", primary_value=MetadataColumnsPool.uniqueSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniSearch = ViewColumn(id.increment_as_string(), display_name="Unique omni search", primary_value=MetadataColumnsPool.uniqueOmniSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileSearch = ViewColumn(id.increment_as_string(), display_name="Unique mobile search", primary_value=MetadataColumnsPool.uniqueMobileSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelSearch = ViewColumn(id.increment_as_string(), display_name="Value website search", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueSearch = ViewColumn(id.increment_as_string(), display_name="Value search", primary_value=MetadataColumnsPool.valueSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniSearch = ViewColumn(id.increment_as_string(), display_name="Value omni search", primary_value=MetadataColumnsPool.valueOmniSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileSearch = ViewColumn(id.increment_as_string(), display_name="Value mobile search", primary_value=MetadataColumnsPool.valueMobileSearch, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelSearch = ViewColumn(id.increment_as_string(), display_name="Cost website search", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costSearch = ViewColumn(id.increment_as_string(), display_name="Cost search", primary_value=MetadataColumnsPool.costSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniSearch = ViewColumn(id.increment_as_string(), display_name="Cost omni search", primary_value=MetadataColumnsPool.costOmniSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileSearch = ViewColumn(id.increment_as_string(), display_name="Cost mobile search", primary_value=MetadataColumnsPool.costMobileSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelSearch = ViewColumn(id.increment_as_string(), display_name="Cost per unique website search", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueSearch = ViewColumn(id.increment_as_string(), display_name="Cost per unique search", primary_value=MetadataColumnsPool.costPerUniqueSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniSearch = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni search", primary_value=MetadataColumnsPool.costPerUniqueOmniSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileSearch = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile search", primary_value=MetadataColumnsPool.costPerUniqueMobileSearch, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelStartTrial = ViewColumn(id.increment_as_string(), display_name="Website start trial", primary_value=MetadataColumnsPool.offsiteConversionFbPixelStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # startTrial = ViewColumn(id.increment_as_string(), display_name="Start trial", primary_value=MetadataColumnsPool.startTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniStartTrial = ViewColumn(id.increment_as_string(), display_name="Omni start trial", primary_value=MetadataColumnsPool.omniStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileStartTrial = ViewColumn(id.increment_as_string(), display_name="Mobile start trial", primary_value=MetadataColumnsPool.mobileStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelStartTrial = ViewColumn(id.increment_as_string(), display_name="Unique website start trial", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueStartTrial = ViewColumn(id.increment_as_string(), display_name="Unique start trial", primary_value=MetadataColumnsPool.uniqueStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniStartTrial = ViewColumn(id.increment_as_string(), display_name="Unique omni start trial", primary_value=MetadataColumnsPool.uniqueOmniStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileStartTrial = ViewColumn(id.increment_as_string(), display_name="Unique mobile start trial", primary_value=MetadataColumnsPool.uniqueMobileStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelStartTrial = ViewColumn(id.increment_as_string(), display_name="Value website start trial", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueStartTrial = ViewColumn(id.increment_as_string(), display_name="Value start trial", primary_value=MetadataColumnsPool.valueStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniStartTrial = ViewColumn(id.increment_as_string(), display_name="Value omni start trial", primary_value=MetadataColumnsPool.valueOmniStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileStartTrial = ViewColumn(id.increment_as_string(), display_name="Value mobile start trial", primary_value=MetadataColumnsPool.valueMobileStartTrial, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost website start trial", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost start trial", primary_value=MetadataColumnsPool.costStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost omni start trial", primary_value=MetadataColumnsPool.costOmniStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost mobile start trial", primary_value=MetadataColumnsPool.costMobileStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost per unique website start trial", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost per unique start trial", primary_value=MetadataColumnsPool.costPerUniqueStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni start trial", primary_value=MetadataColumnsPool.costPerUniqueOmniStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileStartTrial = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile start trial", primary_value=MetadataColumnsPool.costPerUniqueMobileStartTrial, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Website submit application", primary_value=MetadataColumnsPool.offsiteConversionFbPixelSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # submitApplication = ViewColumn(id.increment_as_string(), display_name="Submit application", primary_value=MetadataColumnsPool.submitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Omni submit application", primary_value=MetadataColumnsPool.omniSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Mobile submit application", primary_value=MetadataColumnsPool.mobileSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Unique website submit application", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Unique submit application", primary_value=MetadataColumnsPool.uniqueSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Unique omni submit application", primary_value=MetadataColumnsPool.uniqueOmniSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Unique mobile submit application", primary_value=MetadataColumnsPool.uniqueMobileSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Value website submit application", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Value submit application", primary_value=MetadataColumnsPool.valueSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Value omni submit application", primary_value=MetadataColumnsPool.valueOmniSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Value mobile submit application", primary_value=MetadataColumnsPool.valueMobileSubmitApplication, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost website submit application", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost submit application", primary_value=MetadataColumnsPool.costSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost omni submit application", primary_value=MetadataColumnsPool.costOmniSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost mobile submit application", primary_value=MetadataColumnsPool.costMobileSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost per unique website submit application", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost per unique submit application", primary_value=MetadataColumnsPool.costPerUniqueSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni submit application", primary_value=MetadataColumnsPool.costPerUniqueOmniSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileSubmitApplication = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile submit application", primary_value=MetadataColumnsPool.costPerUniqueMobileSubmitApplication, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelSubscribe = ViewColumn(id.increment_as_string(), display_name="Website subscribe", primary_value=MetadataColumnsPool.offsiteConversionFbPixelSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # subscribe = ViewColumn(id.increment_as_string(), display_name="Subscribe", primary_value=MetadataColumnsPool.subscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniSubscribe = ViewColumn(id.increment_as_string(), display_name="Omni subscribe", primary_value=MetadataColumnsPool.omniSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileSubscribe = ViewColumn(id.increment_as_string(), display_name="Mobile subscribe", primary_value=MetadataColumnsPool.mobileSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelSubscribe = ViewColumn(id.increment_as_string(), display_name="Unique website subscribe", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueSubscribe = ViewColumn(id.increment_as_string(), display_name="Unique subscribe", primary_value=MetadataColumnsPool.uniqueSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniSubscribe = ViewColumn(id.increment_as_string(), display_name="Unique omni subscribe", primary_value=MetadataColumnsPool.uniqueOmniSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileSubscribe = ViewColumn(id.increment_as_string(), display_name="Unique mobile subscribe", primary_value=MetadataColumnsPool.uniqueMobileSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelSubscribe = ViewColumn(id.increment_as_string(), display_name="Value website subscribe", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueSubscribe = ViewColumn(id.increment_as_string(), display_name="Value subscribe", primary_value=MetadataColumnsPool.valueSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniSubscribe = ViewColumn(id.increment_as_string(), display_name="Value omni subscribe", primary_value=MetadataColumnsPool.valueOmniSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileSubscribe = ViewColumn(id.increment_as_string(), display_name="Value mobile subscribe", primary_value=MetadataColumnsPool.valueMobileSubscribe, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost website subscribe", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost subscribe", primary_value=MetadataColumnsPool.costSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost omni subscribe", primary_value=MetadataColumnsPool.costOmniSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost mobile subscribe", primary_value=MetadataColumnsPool.costMobileSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost per unique website subscribe", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost per unique subscribe", primary_value=MetadataColumnsPool.costPerUniqueSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni subscribe", primary_value=MetadataColumnsPool.costPerUniqueOmniSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileSubscribe = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile subscribe", primary_value=MetadataColumnsPool.costPerUniqueMobileSubscribe, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # offsiteConversionFbPixelViewContent = ViewColumn(id.increment_as_string(), display_name="Website view content", primary_value=MetadataColumnsPool.offsiteConversionFbPixelViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # viewContent = ViewColumn(id.increment_as_string(), display_name="View content", primary_value=MetadataColumnsPool.viewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniViewContent = ViewColumn(id.increment_as_string(), display_name="Omni view content", primary_value=MetadataColumnsPool.omniViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileViewContent = ViewColumn(id.increment_as_string(), display_name="Mobile view content", primary_value=MetadataColumnsPool.mobileViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOffsiteConversionFbPixelViewContent = ViewColumn(id.increment_as_string(), display_name="Unique website view content", primary_value=MetadataColumnsPool.uniqueOffsiteConversionFbPixelViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueViewContent = ViewColumn(id.increment_as_string(), display_name="Unique view content", primary_value=MetadataColumnsPool.uniqueViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueOmniViewContent = ViewColumn(id.increment_as_string(), display_name="Unique omni view content", primary_value=MetadataColumnsPool.uniqueOmniViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileViewContent = ViewColumn(id.increment_as_string(), display_name="Unique mobile view content", primary_value=MetadataColumnsPool.uniqueMobileViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOffsiteConversionFbPixelViewContent = ViewColumn(id.increment_as_string(), display_name="Value website view content", primary_value=MetadataColumnsPool.valueOffsiteConversionFbPixelViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueViewContent = ViewColumn(id.increment_as_string(), display_name="Value view content", primary_value=MetadataColumnsPool.valueViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueOmniViewContent = ViewColumn(id.increment_as_string(), display_name="Value omni view content", primary_value=MetadataColumnsPool.valueOmniViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileViewContent = ViewColumn(id.increment_as_string(), display_name="Value mobile view content", primary_value=MetadataColumnsPool.valueMobileViewContent, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOffsiteConversionFbPixelViewContent = ViewColumn(id.increment_as_string(), display_name="Cost website view content", primary_value=MetadataColumnsPool.costOffsiteConversionFbPixelViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costViewContent = ViewColumn(id.increment_as_string(), display_name="Cost view content", primary_value=MetadataColumnsPool.costViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costOmniViewContent = ViewColumn(id.increment_as_string(), display_name="Cost omni view content", primary_value=MetadataColumnsPool.costOmniViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileViewContent = ViewColumn(id.increment_as_string(), display_name="Cost mobile view content", primary_value=MetadataColumnsPool.costMobileViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOffsiteConversionFbPixelViewContent = ViewColumn(id.increment_as_string(), display_name="Cost per unique website view content", primary_value=MetadataColumnsPool.costPerUniqueOffsiteConversionFbPixelViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueViewContent = ViewColumn(id.increment_as_string(), display_name="Cost per unique view content", primary_value=MetadataColumnsPool.costPerUniqueViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueOmniViewContent = ViewColumn(id.increment_as_string(), display_name="Cost per unique omni view content", primary_value=MetadataColumnsPool.costPerUniqueOmniViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileViewContent = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile view content", primary_value=MetadataColumnsPool.costPerUniqueMobileViewContent, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Mobile app activation", primary_value=MetadataColumnsPool.mobileAppActivation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Unique mobile app activation", primary_value=MetadataColumnsPool.uniqueMobileAppActivation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Value mobile app activation", primary_value=MetadataColumnsPool.valueMobileAppActivation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Cost mobile app activation", primary_value=MetadataColumnsPool.costMobileAppActivation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile app activation", primary_value=MetadataColumnsPool.costPerUniqueMobileAppActivation, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniMobileAppActivation = ViewColumn(id.increment_as_string(), display_name="Omni mobile app activation", primary_value=MetadataColumnsPool.omniMobileAppActivation, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # mobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Mobile app install", primary_value=MetadataColumnsPool.mobileAppInstall, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # uniqueMobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Unique mobile app install", primary_value=MetadataColumnsPool.uniqueMobileAppInstall, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # valueMobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Value mobile app install", primary_value=MetadataColumnsPool.valueMobileAppInstall, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costMobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Cost mobile app install", primary_value=MetadataColumnsPool.costMobileAppInstall, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # costPerUniqueMobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Cost per unique mobile app install", primary_value=MetadataColumnsPool.costPerUniqueMobileAppInstall, field_type=ViewColumnType.currency.id, category_id=ViewColumnCategory.conversion.id)
        #
        # omniMobileAppInstall = ViewColumn(id.increment_as_string(), display_name="Omni mobile app install", primary_value=MetadataColumnsPool.omniMobileAppInstall, field_type=ViewColumnType.number.id, category_id=ViewColumnCategory.conversion.id)

        # Video engagement

        total_video_p25_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video 25% watched actions", primary_value=MetadataColumnsPool.total_video_p25_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        total_video_p50_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video 50% watched actions", primary_value=MetadataColumnsPool.total_video_p50_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        total_video_p75_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video 75% watched actions", primary_value=MetadataColumnsPool.total_video_p75_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        total_video_p95_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video 95% watched actions", primary_value=MetadataColumnsPool.total_video_p95_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        total_video_p100_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video 100% watched actions", primary_value=MetadataColumnsPool.total_video_p100_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        total_video_thruplay_watched_actions = ViewColumn(id.increment_as_string(), display_name="Total video thruplay watched actions", primary_value=MetadataColumnsPool.video_thruplay_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        cost_per_total_video_thruplay_watched_actions = ViewColumn(id.increment_as_string(), display_name="Cost per thruplay", primary_value=MetadataColumnsPool.cost_per_video_thruplay_watched_actions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        # # Calculated columns

        cost_per_1000_people_reached = ViewColumn(id.increment_as_string(), display_name="Cost per 1000 people reached", primary_value=MetadataColumnsPool.cost_per_1000_people_reached, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.engagement.id)

        results = ViewColumn(id.increment_as_string(), display_name="Results", primary_value=MetadataColumnsPool.results, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        cost_per_result = ViewColumn(id.increment_as_string(), display_name="Cost per result", primary_value=MetadataColumnsPool.cost_per_result, type_id=ViewColumnType.currency.id, category_id=ViewColumnCategory.performance.id)

        conversions = ViewColumn(id.increment_as_string(), display_name="Conversions (All)", primary_value=MetadataColumnsPool.conversions, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)

        cost_per_conversion = ViewColumn(id.increment_as_string(), display_name="Cost per conversion (All)", primary_value=MetadataColumnsPool.cost_per_conversion, type_id=ViewColumnType.number.id, category_id=ViewColumnCategory.performance.id)