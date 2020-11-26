from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class ViewCarouselEngagementBase(View):
    name = "Carousel engagement"
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
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cpc_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_leads_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.website_registrations_completed_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.app_install_cost,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_cost,
        ViewColumnsMaster.registrations_completed_cost,
        ViewColumnsMaster.adds_to_cart_cost,
        ViewColumnsMaster.checkouts_initiated_cost,
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
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cpc_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_leads_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.website_registrations_completed_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.app_install_cost,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_cost,
        ViewColumnsMaster.registrations_completed_cost,
        ViewColumnsMaster.adds_to_cart_cost,
        ViewColumnsMaster.checkouts_initiated_cost,
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
        ViewColumnsMaster.link_click_through_rate,
        ViewColumnsMaster.clicks_all,
        ViewColumnsMaster.unique_clicks_all,
        ViewColumnsMaster.cpc_all,
        ViewColumnsMaster.cost_per_unique_click_all,
        ViewColumnsMaster.ctr_all,
        ViewColumnsMaster.amount_spent,
        ViewColumnsMaster.cpm,
        ViewColumnsMaster.cost_per_1000_people_reached,
        ViewColumnsMaster.mobile_app_installs_total,
        ViewColumnsMaster.website_leads_total,
        ViewColumnsMaster.website_content_views_total,
        ViewColumnsMaster.website_registrations_completed_total,
        ViewColumnsMaster.website_adds_to_cart_total,
        ViewColumnsMaster.website_checkouts_initiated_total,
        ViewColumnsMaster.app_install_cost,
        ViewColumnsMaster.leads_cost,
        ViewColumnsMaster.content_views_cost,
        ViewColumnsMaster.registrations_completed_cost,
        ViewColumnsMaster.adds_to_cart_cost,
        ViewColumnsMaster.checkouts_initiated_cost,
    ]
