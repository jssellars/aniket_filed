from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewCostPerUniqueAction:
    cost_per_unique_app_engagement = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_app_engagement'),
                                                display_name='Cost per unique app engagement',
                                                primary_value=FieldsMetadata.app_engagement_unique_cost,
                                                type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_app_story_engagement = ViewColumn(
        id=Autoincrement.hex_string('cost_per_unique_app_story_engagement'),
        display_name='Cost per app unique story engagement',
        primary_value=FieldsMetadata.app_story_engagements_unique_cost,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_app_use = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_app_use'),
                                         display_name='Cost per unique app use',
                                         primary_value=FieldsMetadata.app_use_unique_cost,
                                         type_id=ViewColumnTypeEnum.CURRENCY.value,
                                         group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_new_messaging_conversation = ViewColumn(
        id=Autoincrement.hex_string('cost_per_unique_new_messaging_conversation'),
        display_name='Cost per unique new messaging conversation',
        primary_value=FieldsMetadata.cost_per_unique_new_messaging_connection,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_messaging_conversation_started = ViewColumn(
        id=Autoincrement.hex_string('cost_per_messaging_conversation_started'),
        display_name='Cost per messaging conversation started',
        primary_value=FieldsMetadata.cost_per_messaging_conversation_started,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_blocked_messaging_converastion = ViewColumn(id=Autoincrement.hex_string(
        'cost_per_unique_blocked_messaging_converastion'),
        display_name='Cost per unique blocked messaging conversation',
        primary_value=FieldsMetadata.cost_per_unique_blocked_messaging_conversation,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_messaging_reply = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_messaging_reply'),
                                                 display_name='Cost per unique messaging reply',
                                                 primary_value=FieldsMetadata.cost_per_unique_messaging_reply,
                                                 type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                 group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_credit_spend = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_credit_spend'),
                                              display_name='Cost per unique credit spend',
                                              primary_value=FieldsMetadata.credit_spends_unique_cost,
                                              type_id=ViewColumnTypeEnum.CURRENCY.value,
                                              group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_custom_conversion = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_custom_conversion'),
                                                   display_name='Cost per unique custom conversion',
                                                   primary_value=FieldsMetadata.unique_custom_conversion_cost,
                                                   type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                   group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_game_play = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_game_play'),
                                           display_name='Cost per unique game play',
                                           primary_value=FieldsMetadata.game_plays_unique_cost,
                                           type_id=ViewColumnTypeEnum.CURRENCY.value,
                                           group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_lead_form = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_lead_form'),
                                           display_name='Cost per unique lead form',
                                           primary_value=FieldsMetadata.on_facebook_unique_leads_cost,
                                           type_id=ViewColumnTypeEnum.CURRENCY.value,
                                           group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_add_to_cart = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_add_to_cart'),
                                             display_name='Cost per offline add to cart',
                                             primary_value=FieldsMetadata.adds_to_cart_unique_cost,
                                             type_id=ViewColumnTypeEnum.CURRENCY.value,
                                             group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_offline_other_conversion = ViewColumn(
        id=Autoincrement.hex_string('cost_per_offline_other_conversion'),
        display_name='Cost per unique offline other conversion',
        primary_value=FieldsMetadata.other_offline_conversions_unique_cost,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_offline_conversion = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_offline_conversion'),
                                                    display_name='Cost per offline conversion',
                                                    primary_value=FieldsMetadata.offline_conversion_unique_cost,
                                                    type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                    group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_registrations_completed = ViewColumn(
        id=Autoincrement.hex_string('cost_per_unique_registrations_completed'),
        display_name='Cost per unique registrations completed',
        primary_value=FieldsMetadata.registrations_completed_unique_cost,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_page_engagement = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_page_engagement'),
                                                 display_name='Cost per unique page engagement',
                                                 primary_value=FieldsMetadata.cost_per_unique_page_engagement,
                                                 type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                 group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_page_like = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_page_like'),
                                           display_name='Cost per unique page like',
                                           primary_value=FieldsMetadata.cost_per_unique_page_like,
                                           type_id=ViewColumnTypeEnum.CURRENCY.value,
                                           group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_post_engagement = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_post_engagement'),
                                                 display_name='Cost per unqiue post engagement',
                                                 primary_value=FieldsMetadata.cost_per_unique_post_engagement,
                                                 type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                 group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_rsvp = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_rsvp'),
                                      display_name='Cost per unique RSVP',
                                      primary_value=FieldsMetadata.cost_per_unique_event_response)
    cost_per_unique_thruplay = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_thruplay'),
                                          display_name='Cost per unique video view',
                                          primary_value=FieldsMetadata.cost_per_unique_thruplay,
                                          type_id=ViewColumnTypeEnum.CURRENCY.value,
                                          group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_purchase = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_purchase'),
                                          display_name='Cost per unique purchase',
                                          primary_value=FieldsMetadata.purchases_cost,
                                          type_id=ViewColumnTypeEnum.CURRENCY.value,
                                          group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_total_leads = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_total_leads'),
                                             display_name='Cost per unique total leads',
                                             primary_value=FieldsMetadata.leads_unique_costs,
                                             type_id=ViewColumnTypeEnum.CURRENCY.value,
                                             group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_total_checkouts_initiated = ViewColumn(
        id=Autoincrement.hex_string('cost_per_unique_total_checkouts_initiated'),
        display_name='Cost per unique total checkouts initiated',
        primary_value=FieldsMetadata.checkouts_initiated_unique_cost,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
    cost_per_unique_view_content = ViewColumn(id=Autoincrement.hex_string('cost_per_unique_view_content'),
                                              display_name='Cost per unique view content',
                                              primary_value=FieldsMetadata.content_views_unique_cost,
                                              type_id=ViewColumnTypeEnum.CURRENCY.value,
                                              group_display_name=ViewColumnGroupEnum.COST_PER_UNIQUE_ACTION.value)
