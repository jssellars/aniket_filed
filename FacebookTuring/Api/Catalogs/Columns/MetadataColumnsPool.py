from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ColumnMetadata import ColumnMetadata


class MetadataColumnsPool():
    #  Structure fields and parameters
    #  Object names, IDs, statuses, and dates
    ad_account_id = ColumnMetadata(FieldsMetadata.ad_account_id.name, FieldAggregationTypeEnum.null,
                                   FieldDataTypeEnum.text)

    account_name = ColumnMetadata(FieldsMetadata.account_name.name, FieldAggregationTypeEnum.null,
                                  FieldDataTypeEnum.text)

    ad_id = ColumnMetadata(FieldsMetadata.ad_id.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    ad_name = ColumnMetadata(FieldsMetadata.ad_name.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    adset_id = ColumnMetadata(FieldsMetadata.adset_id.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    adset_name = ColumnMetadata(FieldsMetadata.adset_name.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    buying_type = ColumnMetadata(FieldsMetadata.buying_type.name, FieldAggregationTypeEnum.null,
                                 FieldDataTypeEnum.text)

    campaign_id = ColumnMetadata(FieldsMetadata.campaign_id.name, FieldAggregationTypeEnum.null,
                                 FieldDataTypeEnum.text)

    campaign_name = ColumnMetadata(FieldsMetadata.campaign_name.name, FieldAggregationTypeEnum.null,
                                   FieldDataTypeEnum.text)

    effective_status = ColumnMetadata(FieldsMetadata.effective_status.name, FieldAggregationTypeEnum.null,
                                      FieldDataTypeEnum.text)

    tags = ColumnMetadata(FieldsMetadata.tags.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    objective = ColumnMetadata(FieldsMetadata.objective.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    created_at = ColumnMetadata(FieldsMetadata.created_at.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.date)

    last_significant_edit = ColumnMetadata(FieldsMetadata.last_significant_edit.name, FieldAggregationTypeEnum.null,
                                           FieldDataTypeEnum.date)

    start_date = ColumnMetadata(FieldsMetadata.start_date.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.date)

    end_date = ColumnMetadata(FieldsMetadata.end_date.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.date)

    bid_strategy = ColumnMetadata(FieldsMetadata.bid_strategy.name, FieldAggregationTypeEnum.null,
                                  FieldDataTypeEnum.text)

    amount_spent_percentage = ColumnMetadata(FieldsMetadata.amount_spent_percentage.name, FieldAggregationTypeEnum.avg,
                                             FieldDataTypeEnum.number)

    bid_cap = ColumnMetadata(FieldsMetadata.bid_cap.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    budget = ColumnMetadata(FieldsMetadata.budget.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    budget_remaining = ColumnMetadata(FieldsMetadata.budget_remaining.name, FieldAggregationTypeEnum.sum,
                                      FieldDataTypeEnum.number)

    # Targeting

    location = ColumnMetadata(FieldsMetadata.location.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    age = ColumnMetadata(FieldsMetadata.age.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    gender = ColumnMetadata(FieldsMetadata.gender.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    included_custom_audiences = ColumnMetadata(FieldsMetadata.included_custom_audiences.name,
                                               FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    excluded_custom_audiences = ColumnMetadata(FieldsMetadata.excluded_custom_audiences.name,
                                               FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    # Ad creative

    page_name = ColumnMetadata(FieldsMetadata.page_name.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    headline = ColumnMetadata(FieldsMetadata.headline.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    body = ColumnMetadata(FieldsMetadata.body.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    link = ColumnMetadata(FieldsMetadata.link.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    destination = ColumnMetadata(FieldsMetadata.destination.name, FieldAggregationTypeEnum.null,
                                 FieldDataTypeEnum.text)

    # Tracking
    url_parameters = ColumnMetadata(FieldsMetadata.url_parameters.name, FieldAggregationTypeEnum.null,
                                    FieldDataTypeEnum.text)

    pixel = ColumnMetadata(FieldsMetadata.pixel.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    app_event = ColumnMetadata(FieldsMetadata.app_event.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    offline_event = ColumnMetadata(FieldsMetadata.offline_event.name, FieldAggregationTypeEnum.null,
                                   FieldDataTypeEnum.text)

    # TODO: Split test

    # TODO: Optimization

    # Insights fields and parameters

    canvas_avg_view_percent = ColumnMetadata(FieldsMetadata.instant_experience_view_percentage.name,
                                             FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    canvas_avg_view_time = ColumnMetadata(FieldsMetadata.instant_experience_view_time.name,
                                          FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    clicks = ColumnMetadata(FieldsMetadata.all_clicks.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    conversion_rate_ranking = ColumnMetadata(FieldsMetadata.conversion_rate_ranking.name,
                                             FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    cost_per_estimated_ad_recallers = ColumnMetadata(FieldsMetadata.cost_per_estimated_ad_recall_lift.name,
                                                     FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    # costPerInlineLinkClick = ColumnMetadata(FacebookFieldsMetadata.costPerIn, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    # costPerInlinePostEngagement = ColumnMetadata("cost_per_inline_post_engagement", FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_unique_click = ColumnMetadata(FieldsMetadata.cost_per_unique_click_all.name, FieldAggregationTypeEnum.avg,
                                           FieldDataTypeEnum.number)

    # costPerUniqueInlineLinkClick = ColumnMetadata("cost_per_unique_inline_link_click", FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cpc = ColumnMetadata(FieldsMetadata.all_cpc.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cpm = ColumnMetadata(FieldsMetadata.cpm.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cpp = ColumnMetadata(FieldsMetadata.all_cpp.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    ctr = ColumnMetadata(FieldsMetadata.all_ctr.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    date_start = ColumnMetadata(FieldsMetadata.date_start.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.date)

    date_stop = ColumnMetadata(FieldsMetadata.date_stop.name, FieldAggregationTypeEnum.null, FieldDataTypeEnum.date)

    engagement_rate_ranking = ColumnMetadata(FieldsMetadata.engagement_rate_ranking.name,
                                             FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    estimated_ad_recall_rate = ColumnMetadata(FieldsMetadata.estimated_ad_recall_rate.name,
                                              FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    estimated_ad_recallers = ColumnMetadata(FieldsMetadata.estimated_ad_recall_lift.name, FieldAggregationTypeEnum.sum,
                                            FieldDataTypeEnum.number)

    frequency = ColumnMetadata(FieldsMetadata.frequency.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    full_view_impressions = ColumnMetadata(FieldsMetadata.full_view_impressions.name, FieldAggregationTypeEnum.sum,
                                           FieldDataTypeEnum.number)

    full_view_reach = ColumnMetadata(FieldsMetadata.full_view_reach.name, FieldAggregationTypeEnum.sum,
                                     FieldDataTypeEnum.number)

    impressions = ColumnMetadata(FieldsMetadata.impressions.name, FieldAggregationTypeEnum.sum,
                                 FieldDataTypeEnum.number)

    # inlineLinkClickCtr = ColumnMetadata("inline_link_click_ctr", FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    # inlineLinkClicks = ColumnMetadata("inline_link_clicks", FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    # inlinePostEngagement = ColumnMetadata("inline_post_engagement", FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    instant_experience_clicks_to_open = ColumnMetadata(FieldsMetadata.instant_experience_click_to_open.name,
                                                       FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    instant_experience_clicks_to_start = ColumnMetadata(FieldsMetadata.instant_experience_click_to_start.name,
                                                        FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    instant_experience_outbound_clicks = ColumnMetadata(FieldsMetadata.instant_experience_outbound_click.name,
                                                        FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    # placePageName = ColumnMetadata("place_page_name", FieldAggregationTypeEnum.null, FieldDataTypeEnum.text)

    quality_ranking = ColumnMetadata(FieldsMetadata.quality_ranking.name, FieldAggregationTypeEnum.null,
                                     FieldDataTypeEnum.text)

    reach = ColumnMetadata(FieldsMetadata.reach.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    social_spend = ColumnMetadata(FieldsMetadata.social_spend.name, FieldAggregationTypeEnum.sum,
                                  FieldDataTypeEnum.number)

    spend = ColumnMetadata(FieldsMetadata.amount_spent.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    unique_clicks = ColumnMetadata(FieldsMetadata.unique_click.name, FieldAggregationTypeEnum.sum,
                                   FieldDataTypeEnum.number)

    unique_ctr = ColumnMetadata(FieldsMetadata.unique_ctr.name, FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    # uniqueInlineLinkClickCtr = ColumnMetadata("unique_inline_link_click_ctr", FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)
    #
    # uniqueInlineLinkClicks = ColumnMetadata("unique_inline_link_clicks", FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    unique_link_clicks_ctr = ColumnMetadata(FieldsMetadata.unique_link_click_ctr.name, FieldAggregationTypeEnum.sum,
                                            FieldDataTypeEnum.number)

    # Page post

    page_engagement = ColumnMetadata(FieldsMetadata.page_engagement.name, FieldAggregationTypeEnum.sum,
                                     FieldDataTypeEnum.number)

    like = ColumnMetadata(FieldsMetadata.page_like.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    comment = ColumnMetadata(FieldsMetadata.post_comment.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    post_engagement = ColumnMetadata(FieldsMetadata.post_engagement.name, FieldAggregationTypeEnum.sum,
                                     FieldDataTypeEnum.number)

    post_reaction = ColumnMetadata(FieldsMetadata.post_reaction.name, FieldAggregationTypeEnum.sum,
                                   FieldDataTypeEnum.number)

    # onsiteConversion = ColumnMetadata("actions_onsite_conversion_post_save", FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    post_share = ColumnMetadata(FieldsMetadata.post_share.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    photo_view = ColumnMetadata(FieldsMetadata.post_view.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    event_responses = ColumnMetadata(FieldsMetadata.event_responses.name, FieldAggregationTypeEnum.sum,
                                     FieldDataTypeEnum.number)

    # effectShare = ColumnMetadata("effect_share", FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    cost_per_page_engagement = ColumnMetadata(FieldsMetadata.cost_per_page_engagement.name,
                                              FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_like = ColumnMetadata(FieldsMetadata.cost_per_page_like.name, FieldAggregationTypeEnum.avg,
                                   FieldDataTypeEnum.number)

    cost_per_post_engagement = ColumnMetadata(FieldsMetadata.cost_per_post_engagement.name,
                                              FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_event_response = ColumnMetadata(FieldsMetadata.cost_per_event_response.name, FieldAggregationTypeEnum.avg,
                                             FieldDataTypeEnum.number)

    # Messaging

    messaging_block = ColumnMetadata(FieldsMetadata.blocked_messaging_connections.name, FieldAggregationTypeEnum.sum,
                                     FieldDataTypeEnum.number)

    messaging_conversation_started_7d = ColumnMetadata(FieldsMetadata.messaging_conversation_started_7d.name,
                                                       FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    messaging_first_reply = ColumnMetadata(FieldsMetadata.new_messaging_connections.name, FieldAggregationTypeEnum.sum,
                                           FieldDataTypeEnum.number)

    cost_per_messaging_first_reply = ColumnMetadata(FieldsMetadata.cost_per_new_messaging_connection.name,
                                                    FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    total_video_p100_watched_actions = ColumnMetadata(FieldsMetadata.total_video_100p_watched_actions.name,
                                                      FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    total_video_p25_watched_actions = ColumnMetadata(FieldsMetadata.total_video_25p_watched_actions.name,
                                                     FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    total_video_p50_watched_actions = ColumnMetadata(FieldsMetadata.total_video_50p_watched_actions.name,
                                                     FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    total_video_p75_watched_actions = ColumnMetadata(FieldsMetadata.total_video_75p_watched_actions.name,
                                                     FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    total_video_p95_watched_actions = ColumnMetadata(FieldsMetadata.total_video_95p_watched_actions.name,
                                                     FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    video_play_actions = ColumnMetadata(FieldsMetadata.video_play.name, FieldAggregationTypeEnum.sum,
                                        FieldDataTypeEnum.number)

    video_thruplay_watched_actions = ColumnMetadata(FieldsMetadata.thruplay.name, FieldAggregationTypeEnum.sum,
                                                    FieldDataTypeEnum.number)

    link_click_website_ctr = ColumnMetadata(FieldsMetadata.link_click_ctr.name, FieldAggregationTypeEnum.sum,
                                            FieldDataTypeEnum.number)

    website_purchase_roas = ColumnMetadata(FieldsMetadata.website_purchase_roas.name, FieldAggregationTypeEnum.sum,
                                           FieldDataTypeEnum.number)

    purchase_roas = ColumnMetadata(FieldsMetadata.purchase_roas.name, FieldAggregationTypeEnum.sum,
                                   FieldDataTypeEnum.number)

    #  Clicks

    link_click = ColumnMetadata(FieldsMetadata.link_click.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    unique_link_click = ColumnMetadata(FieldsMetadata.unique_link_click.name, FieldAggregationTypeEnum.sum,
                                       FieldDataTypeEnum.number)

    outbound_click = ColumnMetadata(FieldsMetadata.outbound_click.name, FieldAggregationTypeEnum.sum,
                                    FieldDataTypeEnum.number)

    unique_outbound_click = ColumnMetadata(FieldsMetadata.unique_outbound_click.name, FieldAggregationTypeEnum.sum,
                                           FieldDataTypeEnum.number)

    outbound_link_click_ctr = ColumnMetadata(FieldsMetadata.outbound_link_click_ctr.name, FieldAggregationTypeEnum.avg,
                                             FieldDataTypeEnum.number)

    unique_outbound_link_click_ctr = ColumnMetadata(FieldsMetadata.unique_outbound_link_click_ctr.name,
                                                    FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_outbound_click = ColumnMetadata(FieldsMetadata.cost_per_outbound_link_click.name,
                                             FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_unique_outbound_click = ColumnMetadata(FieldsMetadata.click_per_unique_outbound_link_click.name,
                                                    FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    #  ====== Calculated metrics ====== #
    cost_per_1000_people_reached = ColumnMetadata(FieldsMetadata.cost_per_1000_people_reached.name,
                                                  FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    cost_per_video_thruplay_watched_actions = ColumnMetadata(FieldsMetadata.cost_per_thruplay.name,
                                                             FieldAggregationTypeEnum.avg, FieldDataTypeEnum.number)

    results = ColumnMetadata(FieldsMetadata.results.name, FieldAggregationTypeEnum.sum, FieldDataTypeEnum.number)

    cost_per_result = ColumnMetadata(FieldsMetadata.cost_per_result.name, FieldAggregationTypeEnum.avg,
                                     FieldDataTypeEnum.number)

    conversions = ColumnMetadata(FieldsMetadata.conversions.name, FieldAggregationTypeEnum.sum,
                                 FieldDataTypeEnum.number)

    cost_per_conversion = ColumnMetadata(FieldsMetadata.cost_per_conversion.name, FieldAggregationTypeEnum.sum,
                                         FieldDataTypeEnum.number)
