from Core.Metadata.Columns.ViewColumns.MetricColumn import MetricColumn
from Core.Tools.Misc.Autoincrement import Autoincrement
from GoogleTuring.Api.Catalogs.Columns.GoogleMetricMetadataColumnsPool import GoogleMetricMetadataColumnsPool
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnType import ViewColumnType
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsMaster import DimensionColumnsMaster


class MetricColumnsMaster:
    __id = Autoincrement(0)
    absolute_top_impression_percentage = MetricColumn(__id.increment_as_string(),
                                                      display_name='Absolute top impression percentage',
                                                      primary_value=GoogleMetricMetadataColumnsPool.absolute_top_impression_percentage,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id,
                                                      actions=[],
                                                      not_supported_dimensions=[
                                                          DimensionColumnsMaster.conversion_adjustment])

    active_view_cpm = MetricColumn(__id.increment_as_string(), display_name='Active view cpm',
                                   primary_value=GoogleMetricMetadataColumnsPool.active_view_cpm,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    active_view_ctr = MetricColumn(__id.increment_as_string(), display_name='Active view ctr',
                                   primary_value=GoogleMetricMetadataColumnsPool.active_view_ctr,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    active_view_impressions = MetricColumn(__id.increment_as_string(), display_name='Active view impressions',
                                           primary_value=GoogleMetricMetadataColumnsPool.active_view_impressions,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    active_view_measurability = MetricColumn(__id.increment_as_string(), display_name='Active view measurability',
                                             primary_value=GoogleMetricMetadataColumnsPool.active_view_measurability,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[], not_supported_dimensions=[])

    active_view_measurable_cost = MetricColumn(__id.increment_as_string(), display_name='Active view measurable cost',
                                               primary_value=GoogleMetricMetadataColumnsPool.active_view_measurable_cost,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id,
                                               actions=[], not_supported_dimensions=[])

    active_view_measurable_impressions = MetricColumn(__id.increment_as_string(),
                                                      display_name='Active view measurable impressions',
                                                      primary_value=GoogleMetricMetadataColumnsPool.active_view_measurable_impressions,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[],
                                                      not_supported_dimensions=[])

    active_view_viewability = MetricColumn(__id.increment_as_string(), display_name='Active view viewability',
                                           primary_value=GoogleMetricMetadataColumnsPool.active_view_viewability,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    all_conversion_rate = MetricColumn(__id.increment_as_string(), display_name='All conversion rate',
                                       primary_value=GoogleMetricMetadataColumnsPool.all_conversion_rate,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[],
                                       not_supported_dimensions=[])

    all_conversions = MetricColumn(__id.increment_as_string(), display_name='All conversions',
                                   primary_value=GoogleMetricMetadataColumnsPool.all_conversions,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    all_conversion_value = MetricColumn(__id.increment_as_string(), display_name='All conversion value',
                                        primary_value=GoogleMetricMetadataColumnsPool.all_conversion_value,
                                        type_id=ViewColumnType.text.id,
                                        category_id=ViewColumnCategory.common.id, actions=[],
                                        not_supported_dimensions=[])

    average_cost = MetricColumn(__id.increment_as_string(), display_name='Average cost',
                                primary_value=GoogleMetricMetadataColumnsPool.average_cost,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_cpc = MetricColumn(__id.increment_as_string(), display_name='Cpc',
                               primary_value=GoogleMetricMetadataColumnsPool.average_cpc,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_cpe = MetricColumn(__id.increment_as_string(), display_name='Average cpe',
                               primary_value=GoogleMetricMetadataColumnsPool.average_cpe,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_cpm = MetricColumn(__id.increment_as_string(), display_name='Cpm',
                               primary_value=GoogleMetricMetadataColumnsPool.average_cpm,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_cpv = MetricColumn(__id.increment_as_string(), display_name='Average cpv',
                               primary_value=GoogleMetricMetadataColumnsPool.average_cpv,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_pageviews = MetricColumn(__id.increment_as_string(), display_name='Average pageviews',
                                     primary_value=GoogleMetricMetadataColumnsPool.average_pageviews,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_position = MetricColumn(__id.increment_as_string(), display_name='Average position',
                                    primary_value=GoogleMetricMetadataColumnsPool.average_position,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    average_time_on_site = MetricColumn(__id.increment_as_string(), display_name='Average time on site',
                                        primary_value=GoogleMetricMetadataColumnsPool.average_time_on_site,
                                        type_id=ViewColumnType.text.id,
                                        category_id=ViewColumnCategory.common.id, actions=[],
                                        not_supported_dimensions=[])

    bounce_rate = MetricColumn(__id.increment_as_string(), display_name='Bounce rate',
                               primary_value=GoogleMetricMetadataColumnsPool.bounce_rate,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    click_assisted_conversions = MetricColumn(__id.increment_as_string(), display_name='Click assisted conversions',
                                              primary_value=GoogleMetricMetadataColumnsPool.click_assisted_conversions,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[], not_supported_dimensions=[])

    click_assisted_conversions_over_last_click_conversions = MetricColumn(__id.increment_as_string(),
                                                                          display_name='Click assisted conversions over last click conversions',
                                                                          primary_value=GoogleMetricMetadataColumnsPool.click_assisted_conversions_over_last_click_conversions,
                                                                          type_id=ViewColumnType.text.id,
                                                                          category_id=ViewColumnCategory.common.id,
                                                                          actions=[], not_supported_dimensions=[])

    click_assisted_conversion_value = MetricColumn(__id.increment_as_string(),
                                                   display_name='Click assisted conversion value',
                                                   primary_value=GoogleMetricMetadataColumnsPool.click_assisted_conversion_value,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[],
                                                   not_supported_dimensions=[])

    clicks = MetricColumn(__id.increment_as_string(), display_name='Clicks',
                          primary_value=GoogleMetricMetadataColumnsPool.clicks, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    link_clicks = MetricColumn(__id.increment_as_string(), display_name='Link clicks',
                               primary_value=GoogleMetricMetadataColumnsPool.link_clicks,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    conversion_rate = MetricColumn(__id.increment_as_string(), display_name='Conversion rate',
                                   primary_value=GoogleMetricMetadataColumnsPool.conversion_rate,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    conversions = MetricColumn(__id.increment_as_string(), display_name='Conversions',
                               primary_value=GoogleMetricMetadataColumnsPool.conversions,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    leads = MetricColumn(__id.increment_as_string(), display_name='Leads',
                         primary_value=GoogleMetricMetadataColumnsPool.leads,
                         type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    conversion_value = MetricColumn(__id.increment_as_string(), display_name='Conversion value',
                                    primary_value=GoogleMetricMetadataColumnsPool.conversion_value,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    purchases = MetricColumn(__id.increment_as_string(), display_name='Purchases',
                             primary_value=GoogleMetricMetadataColumnsPool.purchases,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    purchase_value = MetricColumn(__id.increment_as_string(), display_name='Purchase value',
                                  primary_value=GoogleMetricMetadataColumnsPool.purchase_value,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    cost = MetricColumn(__id.increment_as_string(), display_name='Cost',
                        primary_value=GoogleMetricMetadataColumnsPool.cost,
                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                        actions=[], not_supported_dimensions=[])

    cost_per_all_conversion = MetricColumn(__id.increment_as_string(), display_name='Cost per all conversion',
                                           primary_value=GoogleMetricMetadataColumnsPool.cost_per_all_conversion,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    cost_per_conversion = MetricColumn(__id.increment_as_string(), display_name='Cost per conversion',
                                       primary_value=GoogleMetricMetadataColumnsPool.cost_per_conversion,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[],
                                       not_supported_dimensions=[])

    cost_per_current_model_attributed_conversion = MetricColumn(__id.increment_as_string(),
                                                                display_name='Cost per current model attributed conversion',
                                                                primary_value=GoogleMetricMetadataColumnsPool.cost_per_current_model_attributed_conversion,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[],
                                                                not_supported_dimensions=[])

    cross_device_conversions = MetricColumn(__id.increment_as_string(), display_name='Cross device conversions',
                                            primary_value=GoogleMetricMetadataColumnsPool.cross_device_conversions,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    ctr = MetricColumn(__id.increment_as_string(), display_name='Ctr',
                       primary_value=GoogleMetricMetadataColumnsPool.ctr,
                       type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                       actions=[], not_supported_dimensions=[])

    current_model_attributed_conversions = MetricColumn(__id.increment_as_string(),
                                                        display_name='Current model attributed conversions',
                                                        primary_value=GoogleMetricMetadataColumnsPool.current_model_attributed_conversions,
                                                        type_id=ViewColumnType.text.id,
                                                        category_id=ViewColumnCategory.common.id, actions=[],
                                                        not_supported_dimensions=[])

    current_model_attributed_conversion_value = MetricColumn(__id.increment_as_string(),
                                                             display_name='Current model attributed conversion value',
                                                             primary_value=GoogleMetricMetadataColumnsPool.current_model_attributed_conversion_value,
                                                             type_id=ViewColumnType.text.id,
                                                             category_id=ViewColumnCategory.common.id, actions=[],
                                                             not_supported_dimensions=[])

    engagement_rate = MetricColumn(__id.increment_as_string(), display_name='Engagement rate',
                                   primary_value=GoogleMetricMetadataColumnsPool.engagement_rate,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    engagements = MetricColumn(__id.increment_as_string(), display_name='Engagements',
                               primary_value=GoogleMetricMetadataColumnsPool.engagements,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    gmail_forwards = MetricColumn(__id.increment_as_string(), display_name='Gmail forwards',
                                  primary_value=GoogleMetricMetadataColumnsPool.gmail_forwards,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    gmail_saves = MetricColumn(__id.increment_as_string(), display_name='Gmail saves',
                               primary_value=GoogleMetricMetadataColumnsPool.gmail_saves,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    gmail_secondary_clicks = MetricColumn(__id.increment_as_string(), display_name='Gmail secondary clicks',
                                          primary_value=GoogleMetricMetadataColumnsPool.gmail_secondary_clicks,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[], not_supported_dimensions=[])

    impression_assisted_conversions = MetricColumn(__id.increment_as_string(),
                                                   display_name='Impression assisted conversions',
                                                   primary_value=GoogleMetricMetadataColumnsPool.impression_assisted_conversions,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[],
                                                   not_supported_dimensions=[])

    impression_assisted_conversions_over_last_click_conversions = MetricColumn(__id.increment_as_string(),
                                                                               display_name='Impression assisted conversions over last click conversions',
                                                                               primary_value=GoogleMetricMetadataColumnsPool.impression_assisted_conversions_over_last_click_conversions,
                                                                               type_id=ViewColumnType.text.id,
                                                                               category_id=ViewColumnCategory.common.id,
                                                                               actions=[], not_supported_dimensions=[])

    impression_assisted_conversion_value = MetricColumn(__id.increment_as_string(),
                                                        display_name='Impression assisted conversion value',
                                                        primary_value=GoogleMetricMetadataColumnsPool.impression_assisted_conversion_value,
                                                        type_id=ViewColumnType.text.id,
                                                        category_id=ViewColumnCategory.common.id, actions=[],
                                                        not_supported_dimensions=[])

    impressions = MetricColumn(__id.increment_as_string(), display_name='Impressions',
                               primary_value=GoogleMetricMetadataColumnsPool.impressions,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    interaction_rate = MetricColumn(__id.increment_as_string(), display_name='Interaction rate',
                                    primary_value=GoogleMetricMetadataColumnsPool.interaction_rate,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    interactions = MetricColumn(__id.increment_as_string(), display_name='Interactions',
                                primary_value=GoogleMetricMetadataColumnsPool.interactions,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    interaction_types = MetricColumn(__id.increment_as_string(), display_name='Interaction types',
                                     primary_value=GoogleMetricMetadataColumnsPool.interaction_types,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    percent_new_visitors = MetricColumn(__id.increment_as_string(), display_name='Percent new visitors',
                                        primary_value=GoogleMetricMetadataColumnsPool.percent_new_visitors,
                                        type_id=ViewColumnType.text.id,
                                        category_id=ViewColumnCategory.common.id, actions=[],
                                        not_supported_dimensions=[])

    top_impression_percentage = MetricColumn(__id.increment_as_string(), display_name='Top impression percentage',
                                             primary_value=GoogleMetricMetadataColumnsPool.top_impression_percentage,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[], not_supported_dimensions=[])

    value_per_all_conversion = MetricColumn(__id.increment_as_string(), display_name='Value per all conversion',
                                            primary_value=GoogleMetricMetadataColumnsPool.value_per_all_conversion,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    value_per_conversion = MetricColumn(__id.increment_as_string(), display_name='Value per conversion',
                                        primary_value=GoogleMetricMetadataColumnsPool.value_per_conversion,
                                        type_id=ViewColumnType.text.id,
                                        category_id=ViewColumnCategory.common.id, actions=[],
                                        not_supported_dimensions=[])

    value_per_current_model_attributed_conversion = MetricColumn(__id.increment_as_string(),
                                                                 display_name='Value per current model attributed conversion',
                                                                 primary_value=GoogleMetricMetadataColumnsPool.value_per_current_model_attributed_conversion,
                                                                 type_id=ViewColumnType.text.id,
                                                                 category_id=ViewColumnCategory.common.id, actions=[],
                                                                 not_supported_dimensions=[])

    video_quartile_100_rate = MetricColumn(__id.increment_as_string(), display_name='Video quartile 100 rate',
                                           primary_value=GoogleMetricMetadataColumnsPool.video_quartile_100_rate,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    video_quartile_25_rate = MetricColumn(__id.increment_as_string(), display_name='Video quartile 25 rate',
                                          primary_value=GoogleMetricMetadataColumnsPool.video_quartile_25_rate,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[], not_supported_dimensions=[])

    video_quartile_50_rate = MetricColumn(__id.increment_as_string(), display_name='Video quartile 50 rate',
                                          primary_value=GoogleMetricMetadataColumnsPool.video_quartile_50_rate,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[], not_supported_dimensions=[])

    video_quartile_75_rate = MetricColumn(__id.increment_as_string(), display_name='Video quartile 75 rate',
                                          primary_value=GoogleMetricMetadataColumnsPool.video_quartile_75_rate,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[], not_supported_dimensions=[])

    video_view_rate = MetricColumn(__id.increment_as_string(), display_name='Video view rate',
                                   primary_value=GoogleMetricMetadataColumnsPool.video_view_rate,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    video_views = MetricColumn(__id.increment_as_string(), display_name='Video views',
                               primary_value=GoogleMetricMetadataColumnsPool.video_views,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    view_through_conversions = MetricColumn(__id.increment_as_string(), display_name='View through conversions',
                                            primary_value=GoogleMetricMetadataColumnsPool.view_through_conversions,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    content_impression_share = MetricColumn(__id.increment_as_string(), display_name='Content impression share',
                                            primary_value=GoogleMetricMetadataColumnsPool.content_impression_share,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    content_rank_lost_impression_share = MetricColumn(__id.increment_as_string(),
                                                      display_name='Content rank lost impression share',
                                                      primary_value=GoogleMetricMetadataColumnsPool.content_rank_lost_impression_share,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[],
                                                      not_supported_dimensions=[])

    num_offline_impressions = MetricColumn(__id.increment_as_string(), display_name='Num offline impressions',
                                           primary_value=GoogleMetricMetadataColumnsPool.num_offline_impressions,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    num_offline_interactions = MetricColumn(__id.increment_as_string(), display_name='Num offline interactions',
                                            primary_value=GoogleMetricMetadataColumnsPool.num_offline_interactions,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    offline_interaction_rate = MetricColumn(__id.increment_as_string(), display_name='Offline interaction rate',
                                            primary_value=GoogleMetricMetadataColumnsPool.offline_interaction_rate,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    relative_ctr = MetricColumn(__id.increment_as_string(), display_name='Relative ctr',
                                primary_value=GoogleMetricMetadataColumnsPool.relative_ctr,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    search_absolute_top_impression_share = MetricColumn(__id.increment_as_string(),
                                                        display_name='Search absolute top impression share',
                                                        primary_value=GoogleMetricMetadataColumnsPool.search_absolute_top_impression_share,
                                                        type_id=ViewColumnType.text.id,
                                                        category_id=ViewColumnCategory.common.id, actions=[],
                                                        not_supported_dimensions=[])

    search_budget_lost_absolute_top_impression_share = MetricColumn(__id.increment_as_string(),
                                                                    display_name='Search budget lost absolute top impression share',
                                                                    primary_value=GoogleMetricMetadataColumnsPool.search_budget_lost_absolute_top_impression_share,
                                                                    type_id=ViewColumnType.text.id,
                                                                    category_id=ViewColumnCategory.common.id,
                                                                    actions=[], not_supported_dimensions=[])

    search_budget_lost_top_impression_share = MetricColumn(__id.increment_as_string(),
                                                           display_name='Search budget lost top impression share',
                                                           primary_value=GoogleMetricMetadataColumnsPool.search_budget_lost_top_impression_share,
                                                           type_id=ViewColumnType.text.id,
                                                           category_id=ViewColumnCategory.common.id, actions=[],
                                                           not_supported_dimensions=[])

    search_exact_match_impression_share = MetricColumn(__id.increment_as_string(),
                                                       display_name='Search exact match impression share',
                                                       primary_value=GoogleMetricMetadataColumnsPool.search_exact_match_impression_share,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[],
                                                       not_supported_dimensions=[])

    search_impression_share = MetricColumn(__id.increment_as_string(), display_name='Search impression share',
                                           primary_value=GoogleMetricMetadataColumnsPool.search_impression_share,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[], not_supported_dimensions=[])

    search_rank_lost_absolute_top_impression_share = MetricColumn(__id.increment_as_string(),
                                                                  display_name='Search rank lost absolute top impression share',
                                                                  primary_value=GoogleMetricMetadataColumnsPool.search_rank_lost_absolute_top_impression_share,
                                                                  type_id=ViewColumnType.text.id,
                                                                  category_id=ViewColumnCategory.common.id, actions=[],
                                                                  not_supported_dimensions=[])

    search_rank_lost_impression_share = MetricColumn(__id.increment_as_string(),
                                                     display_name='Search rank lost impression share',
                                                     primary_value=GoogleMetricMetadataColumnsPool.search_rank_lost_impression_share,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[],
                                                     not_supported_dimensions=[])

    search_rank_lost_top_impression_share = MetricColumn(__id.increment_as_string(),
                                                         display_name='Search rank lost top impression share',
                                                         primary_value=GoogleMetricMetadataColumnsPool.search_rank_lost_top_impression_share,
                                                         type_id=ViewColumnType.text.id,
                                                         category_id=ViewColumnCategory.common.id, actions=[],
                                                         not_supported_dimensions=[])

    search_top_impression_share = MetricColumn(__id.increment_as_string(), display_name='Search top impression share',
                                               primary_value=GoogleMetricMetadataColumnsPool.search_top_impression_share,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id,
                                               actions=[], not_supported_dimensions=[])

    average_frequency = MetricColumn(__id.increment_as_string(), display_name='Average frequency',
                                     primary_value=GoogleMetricMetadataColumnsPool.average_frequency,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    content_budget_lost_impression_share = MetricColumn(__id.increment_as_string(),
                                                        display_name='Content budget lost impression share',
                                                        primary_value=GoogleMetricMetadataColumnsPool.content_budget_lost_impression_share,
                                                        type_id=ViewColumnType.text.id,
                                                        category_id=ViewColumnCategory.common.id, actions=[],
                                                        not_supported_dimensions=[])

    impression_reach = MetricColumn(__id.increment_as_string(), display_name='Impression reach',
                                    primary_value=GoogleMetricMetadataColumnsPool.impression_reach,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    invalid_click_rate = MetricColumn(__id.increment_as_string(), display_name='Invalid click rate',
                                      primary_value=GoogleMetricMetadataColumnsPool.invalid_click_rate,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[],
                                      not_supported_dimensions=[])

    invalid_clicks = MetricColumn(__id.increment_as_string(), display_name='Invalid clicks',
                                  primary_value=GoogleMetricMetadataColumnsPool.invalid_clicks,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[], not_supported_dimensions=[])

    search_budget_lost_impression_share = MetricColumn(__id.increment_as_string(),
                                                       display_name='Search budget lost impression share',
                                                       primary_value=GoogleMetricMetadataColumnsPool.search_budget_lost_impression_share,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[],
                                                       not_supported_dimensions=[])

    search_click_share = MetricColumn(__id.increment_as_string(), display_name='Search click share',
                                      primary_value=GoogleMetricMetadataColumnsPool.search_click_share,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[],
                                      not_supported_dimensions=[])

    historical_creative_quality_score = MetricColumn(__id.increment_as_string(),
                                                     display_name='Historical creative quality score',
                                                     primary_value=GoogleMetricMetadataColumnsPool.historical_creative_quality_score,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[],
                                                     not_supported_dimensions=[])

    historical_landing_page_quality_score = MetricColumn(__id.increment_as_string(),
                                                         display_name='Historical landing page quality score',
                                                         primary_value=GoogleMetricMetadataColumnsPool.historical_landing_page_quality_score,
                                                         type_id=ViewColumnType.text.id,
                                                         category_id=ViewColumnCategory.common.id, actions=[],
                                                         not_supported_dimensions=[])

    historical_quality_score = MetricColumn(__id.increment_as_string(), display_name='Historical quality score',
                                            primary_value=GoogleMetricMetadataColumnsPool.historical_quality_score,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[], not_supported_dimensions=[])

    historical_search_predicted_ctr = MetricColumn(__id.increment_as_string(),
                                                   display_name='Historical search predicted ctr',
                                                   primary_value=GoogleMetricMetadataColumnsPool.historical_search_predicted_ctr,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[],
                                                   not_supported_dimensions=[])
