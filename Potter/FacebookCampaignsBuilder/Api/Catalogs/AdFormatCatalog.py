import copy

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdPreviewBuilderHandler import \
    FiledAdFormatEnum
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import brand_awareness, reach, page_likes, \
    post_likes, event_responses, app_installs, video_views, app_traffic, lead_generation, conversions_leaf, \
    catalog_sales, website_traffic

image = CatalogNode(str(FiledAdFormatEnum.IMAGE.value), 'Single Image', 'single-image')
video = CatalogNode(str(FiledAdFormatEnum.VIDEO.value), 'Video', 'video')
carousel = CatalogNode(str(FiledAdFormatEnum.CAROUSEL.value), 'Carousel', 'carousel')
# TODO: put correct image name here once it's known
existing_post = CatalogNode(str(FiledAdFormatEnum.EXISTING_POST.value), 'Use existing post',
                            'existing-post-image-name-placeholder')

brand_awareness_ad_format = copy.deepcopy(brand_awareness)
brand_awareness_ad_format.image_name = None
brand_awareness_ad_format.description = None
brand_awareness_ad_format.children = [image, video, carousel]

reach_ad_format = copy.deepcopy(reach)
reach_ad_format.image_name = None
reach_ad_format.description = None
reach_ad_format.children = [image, video, carousel]

website_traffic_ad_format = copy.deepcopy(website_traffic)
website_traffic_ad_format.image_name = None
website_traffic_ad_format.description = None
website_traffic_ad_format.children = [image, video, carousel]

# Children for engagement
page_likes_ad_format = copy.deepcopy(page_likes)
page_likes_ad_format.image_name = None
page_likes_ad_format.description = None
page_likes_ad_format.children = [image, video, existing_post]

post_likes_ad_format = copy.deepcopy(post_likes)
post_likes_ad_format.image_name = None
post_likes_ad_format.description = None
post_likes_ad_format.children = [image, video]

event_response_ad_format = copy.deepcopy(event_responses)
event_response_ad_format.description = None
event_response_ad_format.image_name = None
event_response_ad_format.children = [image, video]

app_installs_ad_format = copy.deepcopy(app_installs)
app_installs_ad_format.description = None
app_installs_ad_format.image_name = None
app_installs_ad_format.children = [image, video, carousel]

traffic_for_apps_ad_format = copy.deepcopy(app_traffic)
traffic_for_apps_ad_format.description = None
traffic_for_apps_ad_format.image_name = None
traffic_for_apps_ad_format.children = [image, video, carousel]

video_views_ad_format = copy.deepcopy(video_views)
video_views_ad_format.image_name = None
video_views_ad_format.description = None
# Existing post only works with a video post. This should be validated on FE when the post is selected I think
video_views_ad_format.children = [video, existing_post]

lead_generation_ad_format = copy.deepcopy(lead_generation)
lead_generation_ad_format.image_name = None
lead_generation_ad_format.description = None
lead_generation_ad_format.children = [image, video, carousel]

conversions_ad_format = copy.deepcopy(conversions_leaf)
conversions_ad_format.image_name = None
conversions_ad_format.description = None
conversions_ad_format.children = [image, video, carousel]

catalog_sales_ad_format = copy.deepcopy(catalog_sales)
catalog_sales_ad_format.image_name = None
catalog_sales_ad_format.description = None
catalog_sales_ad_format.children = [image, carousel]


class AdFormatCatalog(CatalogBase):

    A_brand_awareness = brand_awareness_ad_format
    B_reach = reach_ad_format
    C_website_traffic = website_traffic_ad_format
    D_page_likes = page_likes_ad_format
    E_post_likes = post_likes_ad_format
    F_event_responses = event_response_ad_format
    G_app_installs = app_installs_ad_format
    H_traffic_for_apps = traffic_for_apps_ad_format
    I_video_views = video_views_ad_format
    J_lead_generation = lead_generation_ad_format
    K_conversions = conversions_ad_format
    L_catalog_sales = catalog_sales_ad_format

