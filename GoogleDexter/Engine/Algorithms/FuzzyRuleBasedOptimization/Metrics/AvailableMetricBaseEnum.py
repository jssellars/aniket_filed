from enum import Enum

from GoogleDexter.Infrastructure.Domain.Metrics.Metric import MetricBase
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class AvailableMetricBaseEnum(Enum):
    RESULTS = MetricBase(GoogleFieldsMetadata.conversions.name, "Results")
    SPEND = MetricBase(GoogleFieldsMetadata.cost.name, "Amount spent")
    REACH = MetricBase(GoogleFieldsMetadata.impression_reach.name, "Reach")
    LINK_CLICKS = MetricBase(GoogleFieldsMetadata.link_clicks.name, "Link clicks")
    IMPRESSIONS = MetricBase(GoogleFieldsMetadata.impressions.name, "Impressions")
    PURCHASES = MetricBase(GoogleFieldsMetadata.purchases.name, "Purchases")
    LEADS = MetricBase(GoogleFieldsMetadata.leads.name, "Leads")
    CONVERSIONS = MetricBase(GoogleFieldsMetadata.conversions.name, "Conversions")
    PURCHASES_VALUE = MetricBase(GoogleFieldsMetadata.purchase_value.name, "Purchases value")
    CLICKS = MetricBase(GoogleFieldsMetadata.clicks.name, "Clicks")
    MULTIPLE_KEYWORDS_PER_ADGROUP = MetricBase("Multiple Keywords Per Adgroup", "Multiple Keywords Per Adgroup")

    # not used
    # PAGE_LIKES = MetricBase(FieldsMetadata.page_likes.name, "Page likes")
    # VIDEO_PLAYS = MetricBase(FieldsMetadata.video_plays.name, "Video plays")
    # RSVPS = MetricBase(FieldsMetadata.event_responses.name, "RSVPs")
    # APP_INSTALLS = MetricBase(FieldsMetadata.website_app_installs_total.name, "App installs")
    # THRUPLAYS = MetricBase(FieldsMetadata.thru_plays.name, "Thru plays")
    # UNIQUE_CLICKS = MetricBase(FieldsMetadata.unique_link_clicks.name, "Unique clicks")
    # POST_LIKES = MetricBase(FieldsMetadata.post_likes.name, "Post likes")
    # POST_COMMENTS = MetricBase(FieldsMetadata.post_comments.name, "Post comments")
    # POST_SHARES = MetricBase(FieldsMetadata.post_shares.name, "Post shares")
    # POST_VIEWS = MetricBase(FieldsMetadata.photo_views.name, "Post views")
    # POST_ENGAGEMENT = MetricBase(FieldsMetadata.post_engagement.name, "Post engagement")
    # QUALITY_RANKING = MetricBase(FieldsMetadata.quality_ranking.name, "Quality ranking")
    # OBJECTIVE = MetricBase(FieldsMetadata.objective.name, "Objective")
    # AUDIENCE_SIZE = MetricBase(FieldsMetadata.targeting.name, "Estimated audience size")
    # TEXT_OVERLAY = MetricBase("text_overlay", "Text overlay percent")
    # INTERESTS = MetricBase("interests", "Interests")
    # PIXEL = MetricBase("pixel", "Pixel")
    # PROSPECTING_CAMPAIGN = MetricBase("prospecting_campaign", "Prospecting campaign")
