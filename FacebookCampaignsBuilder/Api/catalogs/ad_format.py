from FacebookCampaignsBuilder.Api.catalogs import objectives
from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node
from Core.Tools.Misc.FiledAdFormatEnum import FiledAdFormatEnum

image = Node(str(FiledAdFormatEnum.IMAGE.value))
video = Node(str(FiledAdFormatEnum.VIDEO.value))
carousel = Node(str(FiledAdFormatEnum.CAROUSEL.value))
existing_post = Node(str(FiledAdFormatEnum.EXISTING_POST.value))


class AdFormat(Base):
    brand_awareness = objectives.brand_awareness.with_children(image, video, carousel)
    reach = objectives.reach.with_children(image, video, carousel)
    website_traffic = objectives.website_traffic.with_children(image, video, carousel)
    page_likes = objectives.page_likes.with_children(image, video, existing_post)
    post_likes = objectives.post_likes.with_children(image, video)
    event_responses = objectives.event_responses.with_children(image, video)
    app_installs = objectives.app_installs.with_children(image, video, carousel)
    traffic_for_apps = objectives.app_traffic.with_children(image, video, carousel)
    # Existing post only works with a video post. This should be validated on FE when the post is selected I think
    video_views = objectives.video_views.with_children(video, existing_post)
    lead_generation = objectives.lead_generation.with_children(image, video, carousel)
    conversions = objectives.conversions_leaf.with_children(image, video, carousel)
    catalog_sales = objectives.catalog_sales.with_children(image, carousel)
