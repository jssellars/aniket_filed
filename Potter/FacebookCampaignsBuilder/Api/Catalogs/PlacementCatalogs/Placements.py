# Facebook Placements
from facebook_business.adobjects.contentdeliveryreport import ContentDeliveryReport
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode

facebook_feed_placement = CatalogNode(ContentDeliveryReport.Position.feed, 'Facebook News Feed', 'facebook-news-feed')
facebook_instant_article_placement = CatalogNode(ContentDeliveryReport.Position.instant_article,
                                                 'Facebook Instant Articles', 'facebook-instant-articles')
facebook_video_feeds_placement = CatalogNode(ContentDeliveryReport.Position.video_feeds, 'Facebook Video Feeds',
                                             'facebook-video-feeds')
facebook_right_column_placement = CatalogNode(ContentDeliveryReport.Position.right_hand_column, 'Facebook Right Column',
                                              'facebook-right-column')
facebook_marketplace_placement = CatalogNode(ContentDeliveryReport.Position.marketplace, 'Facebook Marketplace',
                                             'facebook-marketplace')
facebook_stories_placement = CatalogNode(ContentDeliveryReport.Position.facebook_stories, 'Facebook Stories',
                                         'facebook-stories')
facebook_search_results_placement = CatalogNode(ContentDeliveryReport.Position.search, 'Facebook Search results',
                                                'facebook-search-results')
facebook_in_stream_videos_placement = CatalogNode(ContentDeliveryReport.Position.instream_video,
                                                  'Facebook In-stream videos', 'facebook-in-stream-videos')

# Instagram Placements
instagram_feed_placement = CatalogNode(ContentDeliveryReport.Position.feed, 'Instagram Feed', 'insta-feed')
instagram_stories_placement = CatalogNode(ContentDeliveryReport.Position.instagram_stories, 'Instagram Stories',
                                          'instagram-stories')
instagram_explore_placement = CatalogNode(ContentDeliveryReport.Position.instagram_explore, 'Instagram Explore',
                                          'instagram-explore')

# Audience Network Placements
audience_network_native_placement = CatalogNode(ContentDeliveryReport.Position.an_classic, 'Audience Network Native',
                                                'audience-network-native')
audience_network_in_stream_videos_placement = CatalogNode(ContentDeliveryReport.Position.instream_video,
                                                          'Audience Network In-stream video',
                                                          'audience-network-in-stream')
audience_network_rewarded_videos_placement = CatalogNode(ContentDeliveryReport.Position.rewarded_video,
                                                         'Audience Network Rewarded Videos',
                                                         'audience-network-rewarded-videos')

