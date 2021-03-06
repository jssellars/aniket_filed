from Core.Dexter.Infrastructure.Domain.Metrics.AvailableMetricEnumBase import AvailableMetricEnumBase
from Core.Dexter.Infrastructure.Domain.Metrics.Metric import MetricBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class FacebookAvailableMetricsEnum(AvailableMetricEnumBase):
    RESULTS = MetricBase(FieldsMetadata.results.name, "Results")
    SPEND = MetricBase(FieldsMetadata.amount_spent.name, "Amount spent")
    REACH = MetricBase(FieldsMetadata.reach.name, "Reach")
    LINK_CLICKS = MetricBase(FieldsMetadata.link_clicks.name, "Link clicks")
    PAGE_LIKES = MetricBase(FieldsMetadata.page_likes.name, "Page likes")
    IMPRESSIONS = MetricBase(FieldsMetadata.impressions.name, "Impressions")
    PURCHASES = MetricBase(FieldsMetadata.purchases_total.name, "Purchases")
    VIDEO_PLAYS = MetricBase(FieldsMetadata.video_plays.name, "Video plays")
    LEADS = MetricBase(FieldsMetadata.leads_total.name, "Leads")
    RSVPS = MetricBase(FieldsMetadata.event_responses.name, "RSVPs")
    APP_INSTALLS = MetricBase(FieldsMetadata.app_installs_total.name, "App installs")
    CONVERSIONS = MetricBase(FieldsMetadata.conversions.name, "Conversions")
    THRUPLAYS = MetricBase(FieldsMetadata.thru_plays.name, "Thru plays")
    UNIQUE_CLICKS = MetricBase(FieldsMetadata.unique_link_clicks.name, "Unique clicks")
    POST_LIKES = MetricBase(FieldsMetadata.post_likes.name, "Post likes")
    POST_COMMENTS = MetricBase(FieldsMetadata.post_comments.name, "Post comments")
    POST_SHARES = MetricBase(FieldsMetadata.post_shares.name, "Post shares")
    POST_VIEWS = MetricBase(FieldsMetadata.photo_views.name, "Post views")
    POST_ENGAGEMENT = MetricBase(FieldsMetadata.post_engagement.name, "Post engagement")
    PURCHASES_VALUE = MetricBase(FieldsMetadata.purchases_value.name, "Purchases value")
    CLICKS = MetricBase(FieldsMetadata.clicks_all.name, "Clicks")
    OBJECTIVE = MetricBase(FieldsMetadata.objective.name, "Objective")
    QUALITY_RANKING = MetricBase(FieldsMetadata.quality_ranking.name, "Quality ranking")
    AUDIENCE_SIZE = MetricBase(FieldsMetadata.targeting.name, "Estimated audience size")
    TEXT_OVERLAY = MetricBase("text_overlay", "Text overlay percent")
    INTERESTS = MetricBase("interests", "Interests")
    PIXEL = MetricBase("pixel", "Pixel")
    PROSPECTING_CAMPAIGN = MetricBase("prospecting_campaign", "Prospecting campaign")
    NUMBER_OF_ADS = MetricBase("number_of_ads", "Number of ads")
    DUPLICATE_AD = MetricBase("duplicate_ad", "Duplicate ad")
