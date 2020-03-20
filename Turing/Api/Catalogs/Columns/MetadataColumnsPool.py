from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata
from Turing.Api.Catalogs.Columns.AggregationType import AggregationType
from Turing.Api.Catalogs.Columns.ColumnMetadata import ColumnMetadata
from Turing.Api.Catalogs.Columns.ColumnType import ColumnType


class MetadataColumnsPool():
    #  Structure fields and parameters
    #  Object names, IDs, statuses, and dates
    ad_account_id = ColumnMetadata(FacebookFieldsMetadata.ad_account_id.name, AggregationType.null, ColumnType.text)

    account_name = ColumnMetadata(FacebookFieldsMetadata.account_name.name, AggregationType.null, ColumnType.text)

    ad_id = ColumnMetadata(FacebookFieldsMetadata.ad_id.name, AggregationType.null, ColumnType.text)

    ad_name = ColumnMetadata(FacebookFieldsMetadata.ad_name.name, AggregationType.null, ColumnType.text)

    adset_id = ColumnMetadata(FacebookFieldsMetadata.adset_id.name, AggregationType.null, ColumnType.text)

    adset_name = ColumnMetadata(FacebookFieldsMetadata.adset_name.name, AggregationType.null, ColumnType.text)

    buying_type = ColumnMetadata(FacebookFieldsMetadata.buying_type.name, AggregationType.null, ColumnType.text)

    campaign_id = ColumnMetadata(FacebookFieldsMetadata.campaign_id.name, AggregationType.null, ColumnType.text)

    campaign_name = ColumnMetadata(FacebookFieldsMetadata.campaign_name.name, AggregationType.null, ColumnType.text)

    effective_status = ColumnMetadata(FacebookFieldsMetadata.effective_status.name, AggregationType.null, ColumnType.text)

    tags = ColumnMetadata(FacebookFieldsMetadata.tags.name, AggregationType.null, ColumnType.text)

    objective = ColumnMetadata(FacebookFieldsMetadata.objective.name, AggregationType.null, ColumnType.text)

    created_at = ColumnMetadata(FacebookFieldsMetadata.created_at.name, AggregationType.null, ColumnType.date)

    last_significant_edit = ColumnMetadata(FacebookFieldsMetadata.last_significant_edit.name, AggregationType.null, ColumnType.date)

    start_date = ColumnMetadata(FacebookFieldsMetadata.start_date.name, AggregationType.null, ColumnType.date)

    end_date = ColumnMetadata(FacebookFieldsMetadata.end_date.name, AggregationType.null, ColumnType.date)

    bid_strategy = ColumnMetadata(FacebookFieldsMetadata.bid_strategy.name, AggregationType.null, ColumnType.text)

    amount_spent_percentage = ColumnMetadata(FacebookFieldsMetadata.amount_spent_percentage.name, AggregationType.avg, ColumnType.number)

    bid_cap = ColumnMetadata(FacebookFieldsMetadata.bid_cap.name, AggregationType.avg, ColumnType.number)

    budget = ColumnMetadata(FacebookFieldsMetadata.budget.name, AggregationType.sum, ColumnType.number)

    budget_remaining = ColumnMetadata(FacebookFieldsMetadata.budget_remaining.name, AggregationType.sum, ColumnType.number)

    # Targeting

    location = ColumnMetadata(FacebookFieldsMetadata.location.name, AggregationType.null, ColumnType.text)

    age = ColumnMetadata(FacebookFieldsMetadata.age.name, AggregationType.null, ColumnType.text)

    gender = ColumnMetadata(FacebookFieldsMetadata.gender.name, AggregationType.null, ColumnType.text)

    included_custom_audiences = ColumnMetadata(FacebookFieldsMetadata.included_custom_audiences.name, AggregationType.null, ColumnType.text)

    excluded_custom_audiences = ColumnMetadata(FacebookFieldsMetadata.excluded_custom_audiences.name, AggregationType.null, ColumnType.text)

    # Ad creative

    page_name = ColumnMetadata(FacebookFieldsMetadata.page_name.name, AggregationType.null, ColumnType.text)

    headline = ColumnMetadata(FacebookFieldsMetadata.headline.name, AggregationType.null, ColumnType.text)

    body = ColumnMetadata(FacebookFieldsMetadata.body.name, AggregationType.null, ColumnType.text)

    link = ColumnMetadata(FacebookFieldsMetadata.link.name, AggregationType.null, ColumnType.text)

    destination = ColumnMetadata(FacebookFieldsMetadata.destination.name, AggregationType.null, ColumnType.text)

    # Tracking
    url_parameters = ColumnMetadata(FacebookFieldsMetadata.url_parameters.name, AggregationType.null, ColumnType.text)

    pixel = ColumnMetadata(FacebookFieldsMetadata.pixel.name, AggregationType.null, ColumnType.text)

    app_event = ColumnMetadata(FacebookFieldsMetadata.app_event.name, AggregationType.null, ColumnType.text)

    offline_event = ColumnMetadata(FacebookFieldsMetadata.offline_event.name, AggregationType.null, ColumnType.text)

    # TODO: Split test

    # TODO: Optimization

    # Insights fields and parameters

    canvas_avg_view_percent = ColumnMetadata(FacebookFieldsMetadata.instant_experience_view_percentage.name, AggregationType.avg, ColumnType.number)

    canvas_avg_view_time = ColumnMetadata(FacebookFieldsMetadata.instant_experience_view_time.name, AggregationType.avg, ColumnType.number)

    clicks = ColumnMetadata(FacebookFieldsMetadata.all_clicks.name, AggregationType.sum, ColumnType.number)

    conversion_rate_ranking = ColumnMetadata(FacebookFieldsMetadata.conversion_rate_ranking.name, AggregationType.null, ColumnType.text)

    cost_per_estimated_ad_recallers = ColumnMetadata(FacebookFieldsMetadata.cost_per_estimated_ad_recall_lift.name, AggregationType.avg, ColumnType.number)

    # costPerInlineLinkClick = ColumnMetadata(FacebookFieldsMetadata.costPerIn, AggregationType.avg, ColumnType.number)

    # costPerInlinePostEngagement = ColumnMetadata("cost_per_inline_post_engagement", AggregationType.avg, ColumnType.number)

    cost_per_unique_click = ColumnMetadata(FacebookFieldsMetadata.cost_per_unique_click_all.name, AggregationType.avg, ColumnType.number)

    # costPerUniqueInlineLinkClick = ColumnMetadata("cost_per_unique_inline_link_click", AggregationType.avg, ColumnType.number)

    cpc = ColumnMetadata(FacebookFieldsMetadata.all_cpc.name, AggregationType.avg, ColumnType.number)

    cpm = ColumnMetadata(FacebookFieldsMetadata.cpm.name, AggregationType.avg, ColumnType.number)

    cpp = ColumnMetadata(FacebookFieldsMetadata.all_cpp.name, AggregationType.avg, ColumnType.number)

    ctr = ColumnMetadata(FacebookFieldsMetadata.all_ctr.name, AggregationType.avg, ColumnType.number)

    date_start = ColumnMetadata(FacebookFieldsMetadata.date_start.name, AggregationType.null, ColumnType.date)

    date_stop = ColumnMetadata(FacebookFieldsMetadata.date_stop.name, AggregationType.null, ColumnType.date)

    engagement_rate_ranking = ColumnMetadata(FacebookFieldsMetadata.engagement_rate_ranking.name, AggregationType.null, ColumnType.text)

    estimated_ad_recall_rate = ColumnMetadata(FacebookFieldsMetadata.estimated_ad_recall_rate.name, AggregationType.avg, ColumnType.number)

    estimated_ad_recallers = ColumnMetadata(FacebookFieldsMetadata.estimated_ad_recall_lift.name, AggregationType.sum, ColumnType.number)

    frequency = ColumnMetadata(FacebookFieldsMetadata.frequency.name, AggregationType.avg, ColumnType.number)

    full_view_impressions = ColumnMetadata(FacebookFieldsMetadata.full_view_impressions.name, AggregationType.sum, ColumnType.number)

    full_view_reach = ColumnMetadata(FacebookFieldsMetadata.full_view_reach.name, AggregationType.sum, ColumnType.number)

    impressions = ColumnMetadata(FacebookFieldsMetadata.impressions.name, AggregationType.sum, ColumnType.number)

    # inlineLinkClickCtr = ColumnMetadata("inline_link_click_ctr", AggregationType.avg, ColumnType.number)

    # inlineLinkClicks = ColumnMetadata("inline_link_clicks", AggregationType.sum, ColumnType.number)

    # inlinePostEngagement = ColumnMetadata("inline_post_engagement", AggregationType.sum, ColumnType.number)

    instant_experience_clicks_to_open = ColumnMetadata(FacebookFieldsMetadata.instant_experience_click_to_open.name, AggregationType.sum, ColumnType.number)

    instant_experience_clicks_to_start = ColumnMetadata(FacebookFieldsMetadata.instant_experience_click_to_start.name, AggregationType.sum, ColumnType.number)

    instant_experience_outbound_clicks = ColumnMetadata(FacebookFieldsMetadata.instant_experience_outbound_click.name, AggregationType.sum, ColumnType.number)

    # placePageName = ColumnMetadata("place_page_name", AggregationType.null, ColumnType.text)

    quality_ranking = ColumnMetadata(FacebookFieldsMetadata.quality_ranking.name, AggregationType.null, ColumnType.text)

    reach = ColumnMetadata(FacebookFieldsMetadata.reach.name, AggregationType.sum, ColumnType.number)

    social_spend = ColumnMetadata(FacebookFieldsMetadata.social_spend.name, AggregationType.sum, ColumnType.number)

    spend = ColumnMetadata(FacebookFieldsMetadata.amount_spent.name, AggregationType.sum, ColumnType.number)

    unique_clicks = ColumnMetadata(FacebookFieldsMetadata.unique_click.name, AggregationType.sum, ColumnType.number)

    unique_ctr = ColumnMetadata(FacebookFieldsMetadata.unique_ctr.name, AggregationType.avg, ColumnType.number)

    # uniqueInlineLinkClickCtr = ColumnMetadata("unique_inline_link_click_ctr", AggregationType.avg, ColumnType.number)
    #
    # uniqueInlineLinkClicks = ColumnMetadata("unique_inline_link_clicks", AggregationType.sum, ColumnType.number)

    unique_link_clicks_ctr = ColumnMetadata(FacebookFieldsMetadata.unique_link_click_ctr.name, AggregationType.sum, ColumnType.number)

    # Page post

    page_engagement = ColumnMetadata(FacebookFieldsMetadata.page_engagement.name, AggregationType.sum, ColumnType.number)

    like = ColumnMetadata(FacebookFieldsMetadata.page_like.name, AggregationType.sum, ColumnType.number)

    comment = ColumnMetadata(FacebookFieldsMetadata.post_comment.name, AggregationType.sum, ColumnType.number)

    post_engagement = ColumnMetadata(FacebookFieldsMetadata.post_engagement.name, AggregationType.sum, ColumnType.number)

    post_reaction = ColumnMetadata(FacebookFieldsMetadata.post_reaction.name, AggregationType.sum, ColumnType.number)

    # onsiteConversion = ColumnMetadata("actions_onsite_conversion_post_save", AggregationType.sum, ColumnType.number)

    post_share = ColumnMetadata(FacebookFieldsMetadata.post_share.name, AggregationType.sum, ColumnType.number)

    photo_view = ColumnMetadata(FacebookFieldsMetadata.photo_view.name, AggregationType.sum, ColumnType.number)

    event_responses = ColumnMetadata(FacebookFieldsMetadata.event_responses.name, AggregationType.sum, ColumnType.number)

    # effectShare = ColumnMetadata("effect_share", AggregationType.sum, ColumnType.number)

    cost_per_page_engagement = ColumnMetadata(FacebookFieldsMetadata.cost_per_page_engagement.name, AggregationType.avg, ColumnType.number)

    cost_per_like = ColumnMetadata(FacebookFieldsMetadata.cost_per_page_like.name, AggregationType.avg, ColumnType.number)

    cost_per_post_engagement = ColumnMetadata(FacebookFieldsMetadata.cost_per_post_engagement.name, AggregationType.avg, ColumnType.number)

    cost_per_event_response = ColumnMetadata(FacebookFieldsMetadata.cost_per_event_response.name, AggregationType.avg, ColumnType.number)

    # Messaging

    messaging_block = ColumnMetadata(FacebookFieldsMetadata.blocked_messaging_connections.name, AggregationType.sum, ColumnType.number)

    messaging_conversation_started_7d = ColumnMetadata(FacebookFieldsMetadata.messaging_conversation_started_7d.name, AggregationType.sum, ColumnType.number)

    messaging_first_reply = ColumnMetadata(FacebookFieldsMetadata.new_messaging_connections.name, AggregationType.sum, ColumnType.number)

    # uniqueMessagingBlock = ColumnMetadata("unique_actions_onsite_conversion_messaging_block", AggregationType.sum, ColumnType.number)
    #
    # uniqueMessagingConversationStarted7d = ColumnMetadata("unique_actions_onsite_conversion_messaging_conversation_started_7d", AggregationType.sum, ColumnType.number)
    #
    # uniqueMessagingFirst_reply = ColumnMetadata("unique_actions_onsite_conversion_messaging_first_reply", AggregationType.sum, ColumnType.number)
    #
    # costPerMessagingBlock = ColumnMetadata("cost_per_action_type_onsite_conversion_messaging_block", AggregationType.sum, ColumnType.number)
    #
    # costPerMessagingConversationStarted7D = ColumnMetadata("cost_per_action_type_onsite_conversion_messaging_conversation_started_7d", AggregationType.sum, ColumnType.number)

    cost_per_messaging_first_reply = ColumnMetadata(FacebookFieldsMetadata.cost_per_new_messaging_connection.name, AggregationType.sum, ColumnType.number)

    # costPerUniqueMessagingBlock = ColumnMetadata("cost_per_unique_action_type_onsite_conversion_messaging_block", AggregationType.sum, ColumnType.number)
    #
    # costPerUniqueMessagingConversationStarted7D = ColumnMetadata("cost_per_unique_action_type_onsite_conversion_messaging_conversation_started_7d", AggregationType.sum, ColumnType.number)
    #
    # costPerUniqueMessagingFirstReply = ColumnMetadata("cost_per_unique_action_type_onsite_conversion_messaging_first_reply", AggregationType.sum, ColumnType.number)

    #  TODO: Media -- check with FB

    # video30SecWatchedActions = ColumnMetadata("video_30_sec_watched_actions_video_view", AggregationType.sum, ColumnType.number)

    # videoAvgTimeWatchedActions = ColumnMetadata("video_avg_time_watched_actions_video_view", AggregationType.sum, ColumnType.number)

    total_video_p100_watched_actions = ColumnMetadata(FacebookFieldsMetadata.total_video_100p_watched_actions.name, AggregationType.sum, ColumnType.number)

    total_video_p25_watched_actions = ColumnMetadata(FacebookFieldsMetadata.total_video_25p_watched_actions.name, AggregationType.sum, ColumnType.number)

    total_video_p50_watched_actions = ColumnMetadata(FacebookFieldsMetadata.total_video_50p_watched_actions.name, AggregationType.sum, ColumnType.number)

    total_video_p75_watched_actions = ColumnMetadata(FacebookFieldsMetadata.total_video_75p_watched_actions.name, AggregationType.sum, ColumnType.number)

    total_video_p95_watched_actions = ColumnMetadata(FacebookFieldsMetadata.total_video_95p_watched_actions.name, AggregationType.sum, ColumnType.number)

    video_play_actions = ColumnMetadata(FacebookFieldsMetadata.video_play.name, AggregationType.sum, ColumnType.number)

    video_thruplay_watched_actions = ColumnMetadata(FacebookFieldsMetadata.thruplay.name, AggregationType.sum, ColumnType.number)

    link_click_website_ctr = ColumnMetadata(FacebookFieldsMetadata.link_click_ctr.name, AggregationType.sum, ColumnType.number)

    website_purchase_roas = ColumnMetadata(FacebookFieldsMetadata.website_purchase_roas.name, AggregationType.sum, ColumnType.number)

    purchase_roas = ColumnMetadata(FacebookFieldsMetadata.purchase_roas.name, AggregationType.sum, ColumnType.number)

    #  Clicks

    link_click = ColumnMetadata(FacebookFieldsMetadata.link_click.name, AggregationType.sum, ColumnType.number)

    unique_link_click = ColumnMetadata(FacebookFieldsMetadata.unique_link_click.name, AggregationType.sum, ColumnType.number)

    outbound_click = ColumnMetadata(FacebookFieldsMetadata.outbound_click.name, AggregationType.sum, ColumnType.number)

    unique_outbound_click = ColumnMetadata(FacebookFieldsMetadata.unique_outbound_click.name, AggregationType.sum, ColumnType.number)

    outbound_link_click_ctr = ColumnMetadata(FacebookFieldsMetadata.outbound_link_click_ctr.name, AggregationType.avg, ColumnType.number)

    unique_outbound_link_click_ctr = ColumnMetadata(FacebookFieldsMetadata.unique_outbound_link_click_ctr.name, AggregationType.avg, ColumnType.number)

    cost_per_outbound_click = ColumnMetadata(FacebookFieldsMetadata.cost_per_outbound_link_click.name, AggregationType.avg, ColumnType.number)

    cost_per_unique_outbound_click = ColumnMetadata(FacebookFieldsMetadata.click_per_unique_outbound_link_click.name, AggregationType.avg, ColumnType.number)

    #  ====== Standard events ====== #
    # Add payment info

    # offsiteConversionFbPixelAddPaymentInfo = ColumnMetadata("actions_offsite_conversion_fb_pixel_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # addPaymentInfo = ColumnMetadata("add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # omniAddPaymentInfo = ColumnMetadata("omni_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # mobileAddPaymentInfo = ColumnMetadata("mobile_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelAddPaymentInfo = ColumnMetadata("unique_actions_offsite_conversion_fb_pixel_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # uniqueAddPaymentInfo = ColumnMetadata("unique.add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniAddPaymentInfo = ColumnMetadata("unique.omni_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileAddPaymentInfo = ColumnMetadata("unique.mobile_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelAddPaymentInfo = ColumnMetadata("action_values_offsite_conversion_fb_pixel_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # valueAddPaymentInfo = ColumnMetadata("value.add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # valueOmniAddPaymentInfo = ColumnMetadata("value.omni_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # valueMobileAddPaymentInfo = ColumnMetadata("value.mobile_add_payment_info", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelAddPaymentInfo = ColumnMetadata("cost_per_action_type_offsite_conversion_fb_pixel_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costAddPaymentInfo = ColumnMetadata("COST.add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costOmniAddPaymentInfo = ColumnMetadata("COST.omni_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costMobileAddPaymentInfo = ColumnMetadata("COST.mobile_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelAddPaymentInfo = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueAddPaymentInfo = ColumnMetadata("cost_per_unique.add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniAddPaymentInfo = ColumnMetadata("cost_per_unique.omni_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileAddPaymentInfo = ColumnMetadata("cost_per_unique.mobile_add_payment_info", AggregationType.avg, ColumnType.number)
    #
    # # Add to cart
    #
    # offsiteConversionFbPixelAddToCart = ColumnMetadata("offsite_conversion.fb_pixel_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # addToCart = ColumnMetadata("add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # omniAddToCart = ColumnMetadata("omni_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # mobileAddToCart = ColumnMetadata("mobile_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelAddToCart = ColumnMetadata("unique.offsite_conversion.fb_pixel_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # uniqueAddToCart = ColumnMetadata("unique.add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniAddToCart = ColumnMetadata("unique.omni_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileAddToCart = ColumnMetadata("unique.mobile_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelAddToCart = ColumnMetadata("value.offsite_conversion.fb_pixel_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # valueAddToCart = ColumnMetadata("value.add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # valueOmniAddToCart = ColumnMetadata("value.omni_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # valueMobileAddToCart = ColumnMetadata("value.mobile_add_to_cart", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelAddToCart = ColumnMetadata("COST.offsite_conversion.fb_pixel_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costAddToCart = ColumnMetadata("COST.add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costOmniAddToCart = ColumnMetadata("COST.omni_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costMobileAddToCart = ColumnMetadata("COST.mobile_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelAddToCart = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueAddToCart = ColumnMetadata("cost_per_unique.add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniAddToCart = ColumnMetadata("cost_per_unique.omni_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileAddToCart = ColumnMetadata("cost_per_unique.mobile_add_to_cart", AggregationType.avg, ColumnType.number)
    #
    # # Add to wishlist
    # offsiteConversionFbPixelAddToWishlist = ColumnMetadata("offsite_conversion.fb_pixel_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # addToWishlist = ColumnMetadata("add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # omniAddToWishlist = ColumnMetadata("omni_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # mobileAddToWishlist = ColumnMetadata("mobile_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelAddToWishlist= ColumnMetadata("unique.offsite_conversion.fb_pixel_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # uniqueAddToWishlist= ColumnMetadata("unique.add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniAddToWishlist= ColumnMetadata("unique.omni_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileAddToWishlist = ColumnMetadata("unique.mobile_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelAddToWishlist = ColumnMetadata("value.offsite_conversion.fb_pixel_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # valueAddToWishlist = ColumnMetadata("value.add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # valueOmniAddToWishlist = ColumnMetadata("value.omni_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # valueMobileAddToWishlist = ColumnMetadata("value.mobile_add_to_wishlist", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelAddToWishlist = ColumnMetadata("COST.offsite_conversion.fb_pixel_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costAddToWishlist = ColumnMetadata("COST.add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costOmniAddToWishlist = ColumnMetadata("COST.omni_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costMobileAddToWishlist = ColumnMetadata("COST.mobile_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelAddToWishlist = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueAddToWishlist = ColumnMetadata("cost_per_unique.add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniAddToWishlist = ColumnMetadata("cost_per_unique.omni_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileAddToWishlist = ColumnMetadata("cost_per_unique.mobile_add_to_wishlist", AggregationType.avg, ColumnType.number)
    #
    # # Complete registration
    # offsiteConversionFbPixelCompleteRegistration = ColumnMetadata("offsite_conversion.fb_pixel_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # completeRegistration = ColumnMetadata("complete_registration", AggregationType.sum, ColumnType.number)
    #
    # omniCompleteRegistration = ColumnMetadata("omni_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # mobileCompleteRegistration = ColumnMetadata("mobile_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelCompleteRegistration = ColumnMetadata("unique.offsite_conversion.fb_pixel_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # uniqueCompleteRegistration = ColumnMetadata("unique.complete_registration", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniCompleteRegistration = ColumnMetadata("unique.omni_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileCompleteRegistration = ColumnMetadata("unique.mobile_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelCompleteRegistration = ColumnMetadata("value.offsite_conversion.fb_pixel_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # valueCompleteRegistration = ColumnMetadata("value.complete_registration", AggregationType.sum, ColumnType.number)
    #
    # valueOmniCompleteRegistration = ColumnMetadata("value.omni_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # valueMobileCompleteRegistration = ColumnMetadata("value.mobile_complete_registration", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelCompleteRegistration = ColumnMetadata("COST.offsite_conversion.fb_pixel_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costCompleteRegistration = ColumnMetadata("COST.complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costOmniCompleteRegistration = ColumnMetadata("COST.omni_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costMobileCompleteRegistration = ColumnMetadata("COST.mobile_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelCompleteRegistration = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueCompleteRegistration = ColumnMetadata("cost_per_unique.complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniCompleteRegistration = ColumnMetadata("cost_per_unique.omni_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileCompleteRegistration = ColumnMetadata("cost_per_unique.mobile_complete_registration", AggregationType.avg, ColumnType.number)
    #
    # # Contact
    # offsiteConversionFbPixelContact = ColumnMetadata("offsite_conversion.fb_pixel_contact", AggregationType.sum, ColumnType.number)
    #
    # contact = ColumnMetadata("contact", AggregationType.sum, ColumnType.number)
    #
    # omniContact = ColumnMetadata("omni_contact", AggregationType.sum, ColumnType.number)
    #
    # mobileContact = ColumnMetadata("mobile_contact", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelContact = ColumnMetadata("unique.offsite_conversion.fb_pixel_contact", AggregationType.sum, ColumnType.number)
    #
    # uniqueContact = ColumnMetadata("unique.contact", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniContact = ColumnMetadata("unique.omni_contact", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileContact = ColumnMetadata("unique.mobile_contact", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelContact = ColumnMetadata("value.offsite_conversion.fb_pixel_contact", AggregationType.sum, ColumnType.number)
    #
    # valueContact = ColumnMetadata("value.contact", AggregationType.sum, ColumnType.number)
    #
    # valueOmniContact = ColumnMetadata("value.omni_contact", AggregationType.sum, ColumnType.number)
    #
    # valueMobileContact = ColumnMetadata("value.mobile_contact", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelContact = ColumnMetadata("COST.offsite_conversion.fb_pixel_contact", AggregationType.avg, ColumnType.number)
    #
    # costContact = ColumnMetadata("COST.contact", AggregationType.avg, ColumnType.number)
    #
    # costOmniContact = ColumnMetadata("COST.omni_contact", AggregationType.avg, ColumnType.number)
    #
    # costMobileContact = ColumnMetadata("COST.mobile_contact", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelContact = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_contact", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueContact = ColumnMetadata("cost_per_unique.contact", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniContact = ColumnMetadata("cost_per_unique.omni_contact", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileContact = ColumnMetadata("cost_per_unique.mobile_contact", AggregationType.avg, ColumnType.number)
    #
    # # Customise product
    # offsiteConversionFbPixelCustomizeProduct = ColumnMetadata("offsite_conversion.fb_pixel_customize_product", AggregationType.sum, ColumnType.number)
    #
    # customizeProduct = ColumnMetadata("customize_product", AggregationType.sum, ColumnType.number)
    #
    # omniCustomizeProduct = ColumnMetadata("omni_customize_product", AggregationType.sum, ColumnType.number)
    #
    # mobileCustomizeProduct = ColumnMetadata("mobile_customize_product", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelCustomizeProduct = ColumnMetadata("unique.offsite_conversion.fb_pixel_customize_product", AggregationType.sum, ColumnType.number)
    #
    # uniqueCustomizeProduct = ColumnMetadata("unique.customize_product", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniCustomizeProduct = ColumnMetadata("unique.omni_customize_product", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileCustomizeProduct = ColumnMetadata("unique.mobile_customize_product", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelCustomizeProduct = ColumnMetadata("value.offsite_conversion.fb_pixel_customize_product", AggregationType.sum, ColumnType.number)
    #
    # valueCustomizeProduct = ColumnMetadata("value.customize_product", AggregationType.sum, ColumnType.number)
    #
    # valueOmniCustomizeProduct = ColumnMetadata("value.omni_customize_product", AggregationType.sum, ColumnType.number)
    #
    # valueMobileCustomizeProduct = ColumnMetadata("value.mobile_customize_product", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelCustomizeProduct = ColumnMetadata("COST.offsite_conversion.fb_pixel_customize_product", AggregationType.avg, ColumnType.number)
    #
    # costCustomizeProduct = ColumnMetadata("COST.customize_product", AggregationType.avg, ColumnType.number)
    #
    # costOmniCustomizeProduct = ColumnMetadata("COST.omni_customize_product", AggregationType.avg, ColumnType.number)
    #
    # costMobileCustomizeProduct = ColumnMetadata("COST.mobile_customize_product", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelCustomizeProduct = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_customize_product", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueCustomizeProduct = ColumnMetadata("cost_per_unique.customize_product", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniCustomizeProduct = ColumnMetadata("cost_per_unique.omni_customize_product", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileCustomizeProduct = ColumnMetadata("cost_per_unique.mobile_customize_product", AggregationType.avg, ColumnType.number)
    #
    # # Donate
    # offsiteConversionFbPixelDonate = ColumnMetadata("offsite_conversion.fb_pixel_donate", AggregationType.sum, ColumnType.number)
    #
    # donate = ColumnMetadata("donate", AggregationType.sum, ColumnType.number)
    #
    # omniDonate = ColumnMetadata("omni_donate", AggregationType.sum, ColumnType.number)
    #
    # mobileDonate = ColumnMetadata("mobile_donate", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelDonate = ColumnMetadata("unique.offsite_conversion.fb_pixel_donate", AggregationType.sum, ColumnType.number)
    #
    # uniqueDonate = ColumnMetadata("unique.donate", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniDonate = ColumnMetadata("unique.omni_donate", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileDonate = ColumnMetadata("unique.mobile_donate", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelDonate = ColumnMetadata("value.offsite_conversion.fb_pixel_donate", AggregationType.sum, ColumnType.number)
    #
    # valueDonate = ColumnMetadata("value.donate", AggregationType.sum, ColumnType.number)
    #
    # valueOmniDonate = ColumnMetadata("value.omni_donate", AggregationType.sum, ColumnType.number)
    #
    # valueMobileDonate = ColumnMetadata("value.mobile_donate", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelDonate = ColumnMetadata("COST.offsite_conversion.fb_pixel_donate", AggregationType.avg, ColumnType.number)
    #
    # costDonate = ColumnMetadata("COST.donate", AggregationType.avg, ColumnType.number)
    #
    # costOmniDonate = ColumnMetadata("COST.omni_donate", AggregationType.avg, ColumnType.number)
    #
    # costMobileDonate = ColumnMetadata("COST.mobile_donate", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelDonate = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_donate", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueDonate = ColumnMetadata("cost_per_unique.donate", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniDonate = ColumnMetadata("cost_per_unique.omni_donate", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileDonate = ColumnMetadata("cost_per_unique.mobile_donate", AggregationType.avg, ColumnType.number)
    #
    # # get location
    # offsiteConversionFbPixelFindLocation = ColumnMetadata("offsite_conversion.fb_pixel_find_location", AggregationType.sum, ColumnType.number)
    #
    # findLocation = ColumnMetadata("find_location", AggregationType.sum, ColumnType.number)
    #
    # omniFindLocation = ColumnMetadata("omni_find_location", AggregationType.sum, ColumnType.number)
    #
    # mobileFindLocation = ColumnMetadata("mobile_find_location", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelFindLocation = ColumnMetadata("unique.offsite_conversion.fb_pixel_find_location", AggregationType.sum, ColumnType.number)
    #
    # uniqueFindLocation = ColumnMetadata("unique.find_location", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniFindLocation = ColumnMetadata("unique.omni_find_location", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileFindLocation = ColumnMetadata("unique.mobile_find_location", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelFindLocation = ColumnMetadata("value.offsite_conversion.fb_pixel_find_location", AggregationType.sum, ColumnType.number)
    #
    # valueFindLocation = ColumnMetadata("value.find_location", AggregationType.sum, ColumnType.number)
    #
    # valueOmniFindLocation = ColumnMetadata("value.omni_find_location", AggregationType.sum, ColumnType.number)
    #
    # valueMobileFindLocation = ColumnMetadata("value.mobile_find_location", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelFindLocation = ColumnMetadata("COST.offsite_conversion.fb_pixel_find_location", AggregationType.avg, ColumnType.number)
    #
    # costFindLocation = ColumnMetadata("COST.find_location", AggregationType.avg, ColumnType.number)
    #
    # costOmniFindLocation = ColumnMetadata("COST.omni_find_location", AggregationType.avg, ColumnType.number)
    #
    # costMobileFindLocation = ColumnMetadata("COST.mobile_find_location", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelFindLocation = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_find_location", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueFindLocation = ColumnMetadata("cost_per_unique.find_location", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniFindLocation = ColumnMetadata("cost_per_unique.omni_find_location", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileFindLocation = ColumnMetadata("cost_per_unique.mobile_find_location", AggregationType.avg, ColumnType.number)
    #
    # # Initiate checkout
    # offsiteConversionFbPixelInitiateCheckout = ColumnMetadata("offsite_conversion.fb_pixel_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # initiateCheckout = ColumnMetadata("initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # omniInitiateCheckout = ColumnMetadata("omni_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # mobileInitiateCheckout = ColumnMetadata("mobile_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelInitiateCheckout = ColumnMetadata("unique.offsite_conversion.fb_pixel_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # uniqueInitiateCheckout = ColumnMetadata("unique.initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniInitiateCheckout = ColumnMetadata("unique.omni_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileInitiateCheckout = ColumnMetadata("unique.mobile_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelInitiateCheckout = ColumnMetadata("value.offsite_conversion.fb_pixel_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # valueInitiateCheckout = ColumnMetadata("value.initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # valueOmniInitiateCheckout = ColumnMetadata("value.omni_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # valueMobileInitiateCheckout = ColumnMetadata("value.mobile_initiate_checkout", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelInitiateCheckout = ColumnMetadata("COST.offsite_conversion.fb_pixel_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costInitiateCheckout = ColumnMetadata("COST.initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costOmniInitiateCheckout = ColumnMetadata("COST.omni_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costMobileInitiateCheckout = ColumnMetadata("COST.mobile_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelInitiateCheckout = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueInitiateCheckout = ColumnMetadata("cost_per_unique.initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniInitiateCheckout = ColumnMetadata("cost_per_unique.omni_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileInitiateCheckout = ColumnMetadata("cost_per_unique.mobile_initiate_checkout", AggregationType.avg, ColumnType.number)
    #
    # # Lead
    # offsiteConversionFbPixelLead = ColumnMetadata("offsite_conversion.fb_pixel_lead", AggregationType.sum, ColumnType.number)
    #
    # lead = ColumnMetadata("lead", AggregationType.sum, ColumnType.number)
    #
    # omniLead = ColumnMetadata("omni_lead", AggregationType.sum, ColumnType.number)
    #
    # mobileLead = ColumnMetadata("mobile_lead", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelLead = ColumnMetadata("unique.offsite_conversion.fb_pixel_lead", AggregationType.sum, ColumnType.number)
    #
    # uniqueLead = ColumnMetadata("unique.lead", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniLead = ColumnMetadata("unique.omni_lead", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileLead = ColumnMetadata("unique.mobile_lead", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelLead = ColumnMetadata("value.offsite_conversion.fb_pixel_lead", AggregationType.sum, ColumnType.number)
    #
    # valueLead = ColumnMetadata("value.lead", AggregationType.sum, ColumnType.number)
    #
    # valueOmniLead = ColumnMetadata("value.omni_lead", AggregationType.sum, ColumnType.number)
    #
    # valueMobileLead = ColumnMetadata("value.mobile_lead", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelLead = ColumnMetadata("COST.offsite_conversion.fb_pixel_lead", AggregationType.avg, ColumnType.number)
    #
    # costLead = ColumnMetadata("COST.lead", AggregationType.avg, ColumnType.number)
    #
    # costOmniLead = ColumnMetadata("COST.omni_lead", AggregationType.avg, ColumnType.number)
    #
    # costMobileLead = ColumnMetadata("COST.mobile_lead", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelLead = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_lead", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueLead = ColumnMetadata("cost_per_unique.lead", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniLead = ColumnMetadata("cost_per_unique.omni_lead", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileLead = ColumnMetadata("cost_per_unique.mobile_lead", AggregationType.avg, ColumnType.number)
    #
    # # Purchase
    # offsiteConversionFbPixelPurchase = ColumnMetadata("offsite_conversion.fb_pixel_purchase", AggregationType.sum, ColumnType.number)
    #
    # purchase = ColumnMetadata("purchase", AggregationType.sum, ColumnType.number)
    #
    # omniPurchase = ColumnMetadata("omni_purchase", AggregationType.sum, ColumnType.number)
    #
    # mobilePurchase = ColumnMetadata("mobile_purchase", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelPurchase = ColumnMetadata("unique.offsite_conversion.fb_pixel_purchase", AggregationType.sum, ColumnType.number)
    #
    # uniquePurchase = ColumnMetadata("unique.purchase", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniPurchase = ColumnMetadata("unique.omni_purchase", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobilePurchase = ColumnMetadata("unique.mobile_purchase", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelPurchase = ColumnMetadata("value.offsite_conversion.fb_pixel_purchase", AggregationType.sum, ColumnType.number)
    #
    # valuePurchase = ColumnMetadata("value.purchase", AggregationType.sum, ColumnType.number)
    #
    # valueOmniPurchase = ColumnMetadata("value.omni_purchase", AggregationType.sum, ColumnType.number)
    #
    # valueMobilePurchase = ColumnMetadata("value.mobile_purchase", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelPurchase = ColumnMetadata("COST.offsite_conversion.fb_pixel_purchase", AggregationType.avg, ColumnType.number)
    #
    # costPurchase = ColumnMetadata("COST.purchase", AggregationType.avg, ColumnType.number)
    #
    # costOmniPurchase = ColumnMetadata("COST.omni_purchase", AggregationType.avg, ColumnType.number)
    #
    # costMobilePurchase = ColumnMetadata("COST.mobile_purchase", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelPurchase = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_purchase", AggregationType.avg, ColumnType.number)
    #
    # costPerUniquePurchase = ColumnMetadata("cost_per_unique.purchase", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniPurchase = ColumnMetadata("cost_per_unique.omni_purchase", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobilePurchase = ColumnMetadata("cost_per_unique.mobile_purchase", AggregationType.avg, ColumnType.number)
    #
    # # Schedule
    # offsiteConversionFbPixelSchedule = ColumnMetadata("offsite_conversion.fb_pixel_schedule", AggregationType.sum, ColumnType.number)
    #
    # schedule = ColumnMetadata("schedule", AggregationType.sum, ColumnType.number)
    #
    # omniSchedule = ColumnMetadata("omni_schedule", AggregationType.sum, ColumnType.number)
    #
    # mobileSchedule = ColumnMetadata("mobile_schedule", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelSchedule = ColumnMetadata("unique.offsite_conversion.fb_pixel_schedule", AggregationType.sum, ColumnType.number)
    #
    # uniqueSchedule = ColumnMetadata("unique.schedule", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniSchedule = ColumnMetadata("unique.omni_schedule", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileSchedule = ColumnMetadata("unique.mobile_schedule", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelSchedule = ColumnMetadata("value.offsite_conversion.fb_pixel_schedule", AggregationType.sum, ColumnType.number)
    #
    # valueSchedule = ColumnMetadata("value.schedule", AggregationType.sum, ColumnType.number)
    #
    # valueOmniSchedule = ColumnMetadata("value.omni_schedule", AggregationType.sum, ColumnType.number)
    #
    # valueMobileSchedule = ColumnMetadata("value.mobile_schedule", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelSchedule = ColumnMetadata("COST.offsite_conversion.fb_pixel_schedule", AggregationType.avg, ColumnType.number)
    #
    # costSchedule = ColumnMetadata("COST.schedule", AggregationType.avg, ColumnType.number)
    #
    # costOmniSchedule = ColumnMetadata("COST.omni_schedule", AggregationType.avg, ColumnType.number)
    #
    # costMobileSchedule = ColumnMetadata("COST.mobile_schedule", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelSchedule = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_schedule", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueSchedule = ColumnMetadata("cost_per_unique.schedule", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniSchedule = ColumnMetadata("cost_per_unique.omni_schedule", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileSchedule = ColumnMetadata("cost_per_unique.mobile_schedule", AggregationType.avg, ColumnType.number)
    #
    # # Search
    # offsiteConversionFbPixelSearch = ColumnMetadata("offsite_conversion.fb_pixel_search", AggregationType.sum, ColumnType.number)
    #
    # search = ColumnMetadata("search", AggregationType.sum, ColumnType.number)
    #
    # omniSearch = ColumnMetadata("omni_search", AggregationType.sum, ColumnType.number)
    #
    # mobileSearch = ColumnMetadata("mobile_search", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelSearch = ColumnMetadata("unique.offsite_conversion.fb_pixel_search", AggregationType.sum, ColumnType.number)
    #
    # uniqueSearch = ColumnMetadata("unique.search", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniSearch = ColumnMetadata("unique.omni_search", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileSearch = ColumnMetadata("unique.mobile_search", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelSearch = ColumnMetadata("value.offsite_conversion.fb_pixel_search", AggregationType.sum, ColumnType.number)
    #
    # valueSearch = ColumnMetadata("value.search", AggregationType.sum, ColumnType.number)
    #
    # valueOmniSearch = ColumnMetadata("value.omni_search", AggregationType.sum, ColumnType.number)
    #
    # valueMobileSearch = ColumnMetadata("value.mobile_search", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelSearch = ColumnMetadata("COST.offsite_conversion.fb_pixel_search", AggregationType.avg, ColumnType.number)
    #
    # costSearch = ColumnMetadata("COST.search", AggregationType.avg, ColumnType.number)
    #
    # costOmniSearch = ColumnMetadata("COST.omni_search", AggregationType.avg, ColumnType.number)
    #
    # costMobileSearch = ColumnMetadata("COST.mobile_search", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelSearch = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_search", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueSearch = ColumnMetadata("cost_per_unique.search", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniSearch = ColumnMetadata("cost_per_unique.omni_search", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileSearch = ColumnMetadata("cost_per_unique.mobile_search", AggregationType.avg, ColumnType.number)
    #
    # # Start trial
    # offsiteConversionFbPixelStartTrial = ColumnMetadata("offsite_conversion.fb_pixel_start_trial", AggregationType.sum, ColumnType.number)
    #
    # startTrial = ColumnMetadata("start_trial", AggregationType.sum, ColumnType.number)
    #
    # omniStartTrial = ColumnMetadata("omni_start_trial", AggregationType.sum, ColumnType.number)
    #
    # mobileStartTrial = ColumnMetadata("mobile_start_trial", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelStartTrial = ColumnMetadata("unique.offsite_conversion.fb_pixel_start_trial", AggregationType.sum, ColumnType.number)
    #
    # uniqueStartTrial = ColumnMetadata("unique.start_trial", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniStartTrial = ColumnMetadata("unique.omni_start_trial", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileStartTrial = ColumnMetadata("unique.mobile_start_trial", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelStartTrial = ColumnMetadata("value.offsite_conversion.fb_pixel_start_trial", AggregationType.sum, ColumnType.number)
    #
    # valueStartTrial = ColumnMetadata("value.start_trial", AggregationType.sum, ColumnType.number)
    #
    # valueOmniStartTrial = ColumnMetadata("value.omni_start_trial", AggregationType.sum, ColumnType.number)
    #
    # valueMobileStartTrial = ColumnMetadata("value.mobile_start_trial", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelStartTrial = ColumnMetadata("COST.offsite_conversion.fb_pixel_start_trial", AggregationType.avg, ColumnType.number)
    #
    # costStartTrial = ColumnMetadata("COST.start_trial", AggregationType.avg, ColumnType.number)
    #
    # costOmniStartTrial = ColumnMetadata("COST.omni_start_trial", AggregationType.avg, ColumnType.number)
    #
    # costMobileStartTrial = ColumnMetadata("COST.mobile_start_trial", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelStartTrial = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_start_trial", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueStartTrial = ColumnMetadata("cost_per_unique.start_trial", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniStartTrial = ColumnMetadata("cost_per_unique.omni_start_trial", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileStartTrial = ColumnMetadata("cost_per_unique.mobile_start_trial", AggregationType.avg, ColumnType.number)
    #
    # # Submit application
    # offsiteConversionFbPixelSubmitApplication = ColumnMetadata("offsite_conversion.fb_pixel_submit_application", AggregationType.sum, ColumnType.number)
    #
    # submitApplication = ColumnMetadata("submit_application", AggregationType.sum, ColumnType.number)
    #
    # omniSubmitApplication = ColumnMetadata("omni_submit_application", AggregationType.sum, ColumnType.number)
    #
    # mobileSubmitApplication = ColumnMetadata("mobile_submit_application", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelSubmitApplication = ColumnMetadata("unique.offsite_conversion.fb_pixel_submit_application", AggregationType.sum, ColumnType.number)
    #
    # uniqueSubmitApplication = ColumnMetadata("unique.submit_application", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniSubmitApplication = ColumnMetadata("unique.omni_submit_application", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileSubmitApplication = ColumnMetadata("unique.mobile_submit_application", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelSubmitApplication = ColumnMetadata("value.offsite_conversion.fb_pixel_submit_application", AggregationType.sum, ColumnType.number)
    #
    # valueSubmitApplication = ColumnMetadata("value.submit_application", AggregationType.sum, ColumnType.number)
    #
    # valueOmniSubmitApplication = ColumnMetadata("value.omni_submit_application", AggregationType.sum, ColumnType.number)
    #
    # valueMobileSubmitApplication = ColumnMetadata("value.mobile_submit_application", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelSubmitApplication = ColumnMetadata("COST.offsite_conversion.fb_pixel_submit_application", AggregationType.avg, ColumnType.number)
    #
    # costSubmitApplication = ColumnMetadata("COST.submit_application", AggregationType.avg, ColumnType.number)
    #
    # costOmniSubmitApplication = ColumnMetadata("COST.omni_submit_application", AggregationType.avg, ColumnType.number)
    #
    # costMobileSubmitApplication = ColumnMetadata("COST.mobile_submit_application", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelSubmitApplication = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_submit_application", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueSubmitApplication = ColumnMetadata("cost_per_unique.submit_application", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniSubmitApplication = ColumnMetadata("cost_per_unique.omni_submit_application", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileSubmitApplication = ColumnMetadata("cost_per_unique.mobile_submit_application", AggregationType.avg, ColumnType.number)
    #
    # # Subscribe
    # offsiteConversionFbPixelSubscribe = ColumnMetadata("offsite_conversion.fb_pixel_subscribe", AggregationType.sum, ColumnType.number)
    #
    # subscribe = ColumnMetadata("subscribe", AggregationType.sum, ColumnType.number)
    #
    # omniSubscribe = ColumnMetadata("omni_subscribe", AggregationType.sum, ColumnType.number)
    #
    # mobileSubscribe = ColumnMetadata("mobile_subscribe", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelSubscribe = ColumnMetadata("unique.offsite_conversion.fb_pixel_subscribe", AggregationType.sum, ColumnType.number)
    #
    # uniqueSubscribe = ColumnMetadata("unique.subscribe", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniSubscribe = ColumnMetadata("unique.omni_subscribe", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileSubscribe = ColumnMetadata("unique.mobile_subscribe", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelSubscribe = ColumnMetadata("value.offsite_conversion.fb_pixel_subscribe", AggregationType.sum, ColumnType.number)
    #
    # valueSubscribe = ColumnMetadata("value.subscribe", AggregationType.sum, ColumnType.number)
    #
    # valueOmniSubscribe = ColumnMetadata("value.omni_subscribe", AggregationType.sum, ColumnType.number)
    #
    # valueMobileSubscribe = ColumnMetadata("value.mobile_subscribe", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelSubscribe = ColumnMetadata("COST.offsite_conversion.fb_pixel_subscribe", AggregationType.avg, ColumnType.number)
    #
    # costSubscribe = ColumnMetadata("COST.subscribe", AggregationType.avg, ColumnType.number)
    #
    # costOmniSubscribe = ColumnMetadata("COST.omni_subscribe", AggregationType.avg, ColumnType.number)
    #
    # costMobileSubscribe = ColumnMetadata("COST.mobile_subscribe", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelSubscribe = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_subscribe", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueSubscribe = ColumnMetadata("cost_per_unique.subscribe", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniSubscribe = ColumnMetadata("cost_per_unique.omni_subscribe", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileSubscribe = ColumnMetadata("cost_per_unique.mobile_subscribe", AggregationType.avg, ColumnType.number)
    #
    # # View content
    # offsiteConversionFbPixelViewContent = ColumnMetadata("offsite_conversion.fb_pixel_view_content", AggregationType.sum, ColumnType.number)
    #
    # viewContent = ColumnMetadata("view_content", AggregationType.sum, ColumnType.number)
    #
    # omniViewContent = ColumnMetadata("omni_view_content", AggregationType.sum, ColumnType.number)
    #
    # mobileViewContent = ColumnMetadata("mobile_view_content", AggregationType.sum, ColumnType.number)
    #
    # uniqueOffsiteConversionFbPixelViewContent = ColumnMetadata("unique.offsite_conversion.fb_pixel_view_content", AggregationType.sum, ColumnType.number)
    #
    # uniqueViewContent = ColumnMetadata("unique.view_content", AggregationType.sum, ColumnType.number)
    #
    # uniqueOmniViewContent = ColumnMetadata("unique.omni_view_content", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileViewContent = ColumnMetadata("unique.mobile_view_content", AggregationType.sum, ColumnType.number)
    #
    # valueOffsiteConversionFbPixelViewContent = ColumnMetadata("value.offsite_conversion.fb_pixel_view_content", AggregationType.sum, ColumnType.number)
    #
    # valueViewContent = ColumnMetadata("value.view_content", AggregationType.sum, ColumnType.number)
    #
    # valueOmniViewContent = ColumnMetadata("value.omni_view_content", AggregationType.sum, ColumnType.number)
    #
    # valueMobileViewContent = ColumnMetadata("value.mobile_view_content", AggregationType.sum, ColumnType.number)
    #
    # costOffsiteConversionFbPixelViewContent = ColumnMetadata("COST.offsite_conversion.fb_pixel_view_content", AggregationType.avg, ColumnType.number)
    #
    # costOmniViewContent = ColumnMetadata("COST.omni_view_content", AggregationType.avg, ColumnType.number)
    #
    # costViewContent = ColumnMetadata("COST.view_content", AggregationType.avg, ColumnType.number)
    #
    # costMobileViewContent = ColumnMetadata("COST.mobile_view_content", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOffsiteConversionFbPixelViewContent = ColumnMetadata("cost_per_unique.offsite_conversion.fb_pixel_view_content", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueViewContent = ColumnMetadata("cost_per_unique.view_content", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueOmniViewContent = ColumnMetadata("cost_per_unique.omni_view_content", AggregationType.avg, ColumnType.number)
    #
    # costPerUniqueMobileViewContent = ColumnMetadata("cost_per_unique.mobile_view_content", AggregationType.avg, ColumnType.number)
    #
    # # TODO: check with FB
    # # Mobile app activation & install
    # mobileAppActivation = ColumnMetadata("mobile_app_activation", AggregationType.sum, ColumnType.number)
    # uniqueMobileAppActivation = ColumnMetadata("unique.mobile_app_activation", AggregationType.sum, ColumnType.number)
    #
    # valueMobileAppActivation = ColumnMetadata("value.mobile_app_activation", AggregationType.sum, ColumnType.number)
    #
    # costMobileAppActivation = ColumnMetadata("COST.mobile_app_activation", AggregationType.sum, ColumnType.number)
    #
    # costPerUniqueMobileAppActivation = ColumnMetadata("cost_per_unique.mobile_app_activation", AggregationType.sum, ColumnType.number)
    #
    # omniMobileAppActivation = ColumnMetadata("omni_mobile_app_activation", AggregationType.sum, ColumnType.number)
    #
    # mobileAppInstall = ColumnMetadata("mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # uniqueMobileAppInstall = ColumnMetadata("unique.mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # valueMobileAppInstall = ColumnMetadata("value.mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # costMobileAppInstall = ColumnMetadata("COST.mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # costPerUniqueMobileAppInstall = ColumnMetadata("cost_per_unique.mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # omniMobileAppInstall = ColumnMetadata("omni_mobile_app_install", AggregationType.sum, ColumnType.number)
    #
    # #  ====== Custom conversions ====== #
    # # TODO: Link custom events with ids so I can extract from ColumnFacebookMetadataPool results
    #

    #  ====== Calculated metrics ====== #
    cost_per_1000_people_reached = ColumnMetadata(FacebookFieldsMetadata.cost_per_1000_people_reached.name, AggregationType.avg, ColumnType.number)

    cost_per_video_thruplay_watched_actions = ColumnMetadata(FacebookFieldsMetadata.cost_per_thruplay.name, AggregationType.avg, ColumnType.number)

    results = ColumnMetadata(FacebookFieldsMetadata.results.name, AggregationType.sum, ColumnType.number)

    cost_per_result = ColumnMetadata(FacebookFieldsMetadata.cost_per_result.name, AggregationType.avg, ColumnType.number)

    conversions = ColumnMetadata(FacebookFieldsMetadata.conversions.name, AggregationType.sum, ColumnType.number)

    cost_per_conversion = ColumnMetadata(FacebookFieldsMetadata.cost_per_conversion.name, AggregationType.sum, ColumnType.number)

