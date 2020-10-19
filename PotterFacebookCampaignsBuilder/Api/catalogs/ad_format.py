from PotterFacebookCampaignsBuilder.Api.catalogs import objectives
from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node
from PotterFacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIAdPreviewBuilderHandler import (
    FiledAdFormatEnum,
)

image = Node(str(FiledAdFormatEnum.IMAGE.value))
video = Node(str(FiledAdFormatEnum.VIDEO.value))
carousel = Node(str(FiledAdFormatEnum.CAROUSEL.value))
existing_post = Node(str(FiledAdFormatEnum.EXISTING_POST.value))


class AdFormat(Base):
    A_brand_awareness = objectives.brand_awareness.with_children(image, video, carousel)
    B_reach = objectives.reach.with_children(image, video, carousel)
    C_website_traffic = objectives.website_traffic.with_children(image, video, carousel)
    D_page_likes = objectives.page_likes.with_children(image, video, existing_post)
    E_post_likes = objectives.post_likes.with_children(image, video)
    F_event_responses = objectives.event_responses.with_children(image, video)
    G_app_installs = objectives.app_installs.with_children(image, video, carousel)
    H_traffic_for_apps = objectives.app_traffic.with_children(image, video, carousel)
    # Existing post only works with a video post. This should be validated on FE when the post is selected I think
    I_video_views = objectives.video_views.with_children(video, existing_post)
    J_lead_generation = objectives.lead_generation.with_children(image, video, carousel)
    K_conversions = objectives.conversions_leaf.with_children(image, video, carousel)
    L_catalog_sales = objectives.catalog_sales.with_children(image, carousel)
