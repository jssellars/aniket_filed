from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from facebook_business.adobjects.campaign import Campaign

# Conversions children
store_traffic = CatalogNode(Campaign.Objective.local_awareness, 'Store Traffic', None,
                            'Increase the number of visits to your store.')

conversions_leaf = CatalogNode(Campaign.Objective.conversions, 'Conversions', None,
                               'Grow your audience over time with quality audiences')

catalog_sales = CatalogNode(Campaign.Objective.product_catalog_sales, 'Catalog Sales', None,
                            'Get more people to buy from your catalog')

# Awareness Children
brand_awareness = CatalogNode(Campaign.Objective.brand_awareness, 'Brand Awareness', None,
                              'Reach people who are more likely to recall your ads and increase awareness of your '
                              'brand. '
                              )

reach = CatalogNode(Campaign.Objective.reach, 'Reach', None,
                    'Show your add to the maximun number of people in your audience.')

# App Activity children

traffic = CatalogNode(Campaign.Objective.link_clicks, 'Traffic', None, 'Increase the number of visits to your website.')
app_installs = CatalogNode(Campaign.Objective.app_installs, 'App Installs', None,
                           'Get more people to install your app.')


# engagement children
post_likes = CatalogNode(Campaign.Objective.post_engagement, 'Post Likes')
page_likes = CatalogNode(Campaign.Objective.page_likes, 'Page Likes')

# Consideration Children
engagement = CatalogNode('ENGAGEMENT', 'Engagement', None, 'Get more people to see and engage with your post or page',
                         [post_likes, page_likes])
video_views = CatalogNode(Campaign.Objective.video_views, 'Video Views', None,
                          'Promote videos that show behind-the-scenes footage, product launches or ??? stories to '
                          'rise brand awareness.')

lead_generation = CatalogNode(Campaign.Objective.lead_generation, 'Lead Generation', None,
                              'Collect lead information such as email address, from people interested in your business.')

messages = CatalogNode(Campaign.Objective.messages, 'Messages', None,
                       'Get more people to have conversations with your business to generate leads, '
                       'drive transactions, answer question or offer support')


class ObjectivesCatalog(CatalogBase):

    A_awareness = CatalogNode('AWARENESS', 'Awareness', 'awareness', None, [brand_awareness, reach])

    # The messages objective is also conceptually here but we do not support it yet
    B_consideration = CatalogNode('CONSIDERATION', 'Consideration', 'consideration', None, [traffic, engagement,
                                                                                            video_views, lead_generation
                                                                                            ])

    C_conversions = CatalogNode(Campaign.Objective.conversions, 'Conversions', 'conversions',
                              None, [store_traffic, catalog_sales, conversions_leaf])

    D_app_activity = CatalogNode('App Activity', 'App Activity', 'appactivity', None,
                               [traffic, app_installs, conversions_leaf])


