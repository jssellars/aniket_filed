from FacebookTuring.Api.Catalogs.Views.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewCarouselEngagementBase(View):
    name = "App engagement"
    type = "Business"


class ViewCampaignCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.unique_link_clicks,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.leads_total,
        ViewColumnsMaster.mobile_content_views_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.offline_content_views_total,
        ViewColumnsMaster.content_views_unique_total,
        ViewColumnsMaster.mobile_adds_to_cart_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.offline_adds_to_cart_total,
        ViewColumnsMaster.adds_to_cart_unique,
        ViewColumnsMaster.mobile_checkouts_initiated_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.offline_checkouts_initiated_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_unique_cost,
        ViewColumnsMaster.registrations_completed_unique_cost,
        ViewColumnsMaster.adds_to_cart_unique_cost,
        ViewColumnsMaster.checkouts_initiated_unique_cost
    ]


class ViewAdSetCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.unique_link_clicks,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.leads_total,
        ViewColumnsMaster.mobile_content_views_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.offline_content_views_total,
        ViewColumnsMaster.content_views_unique_total,
        ViewColumnsMaster.mobile_adds_to_cart_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.offline_adds_to_cart_total,
        ViewColumnsMaster.adds_to_cart_unique,
        ViewColumnsMaster.mobile_checkouts_initiated_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.offline_checkouts_initiated_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_unique_cost,
        ViewColumnsMaster.registrations_completed_unique_cost,
        ViewColumnsMaster.adds_to_cart_unique_cost,
        ViewColumnsMaster.checkouts_initiated_unique_cost
    ]


class ViewAdCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_clicks,
        ViewColumnsMaster.unique_link_clicks,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.unique_ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.leads_total,
        ViewColumnsMaster.mobile_content_views_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.offline_content_views_total,
        ViewColumnsMaster.content_views_unique_total,
        ViewColumnsMaster.mobile_adds_to_cart_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.offline_adds_to_cart_total,
        ViewColumnsMaster.adds_to_cart_unique,
        ViewColumnsMaster.mobile_checkouts_initiated_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.offline_checkouts_initiated_total,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_unique_cost,
        ViewColumnsMaster.registrations_completed_unique_cost,
        ViewColumnsMaster.adds_to_cart_unique_cost,
        ViewColumnsMaster.checkouts_initiated_unique_cost
    ]
