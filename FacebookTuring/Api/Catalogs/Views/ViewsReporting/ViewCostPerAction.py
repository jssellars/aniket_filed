from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewCostPerAction:
    cost_per_1000_people_reached = ViewColumn(
        id=Autoincrement.hex_string("cost_per_1000_people_reached"),
        display_name="Cost per 1000 people reached",
        primary_value=FieldsMetadata.cost_per_1000_people_reached,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cpm = ViewColumn(
        id=Autoincrement.hex_string("cpm"),
        display_name="Average CPM",
        primary_value=FieldsMetadata.cpm,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    spend = ViewColumn(
        id=Autoincrement.hex_string("spend"),
        display_name="Spend",
        primary_value=FieldsMetadata.amount_spent,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_post_engagement = ViewColumn(
        id=Autoincrement.hex_string("cost_per_post_engagement"),
        display_name="Cost per post engagement",
        primary_value=FieldsMetadata.cost_per_post_engagement,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_page_like = ViewColumn(
        id=Autoincrement.hex_string("cost_per_page_like"),
        display_name="Cost per page like",
        primary_value=FieldsMetadata.cost_per_page_like,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_rsvp = ViewColumn(
        id=Autoincrement.hex_string("cost_per_rsvp"),
        display_name="Cost per RSVP",
        primary_value=FieldsMetadata.cost_per_event_response,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_unique_click = ViewColumn(
        id=Autoincrement.hex_string("cost_per_unique_click"),
        display_name="Cost per unique click",
        primary_value=FieldsMetadata.cost_per_unique_click_all,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_video_view = ViewColumn(
        id=Autoincrement.hex_string("cost_per_video_view"),
        display_name="Cost per video view",
        primary_value=FieldsMetadata.cost_per_thru_play,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_app_engagement = ViewColumn(
        id=Autoincrement.hex_string("cost_per_app_engagement"),
        display_name="Cost per app engagement",
        primary_value=FieldsMetadata.app_engagement_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_app_story_engagement = ViewColumn(
        id=Autoincrement.hex_string("cost_per_app_story_engagement"),
        display_name="Cost per app story engagement",
        primary_value=FieldsMetadata.app_story_engagements_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_app_use = ViewColumn(
        id=Autoincrement.hex_string("cost_per_app_use"),
        display_name="Cost per app use",
        primary_value=FieldsMetadata.app_use_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_credit_spend = ViewColumn(
        id=Autoincrement.hex_string("cost_per_credit_spend"),
        display_name="Cost per credit spend",
        primary_value=FieldsMetadata.credit_spends_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_page_engagement = ViewColumn(
        id=Autoincrement.hex_string("cost_per_page_engagement"),
        display_name="Cost per page engagement",
        primary_value=FieldsMetadata.cost_per_page_engagement,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_game_play = ViewColumn(
        id=Autoincrement.hex_string("cost_per_game_play"),
        display_name="Cost per game play",
        primary_value=FieldsMetadata.game_plays_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_facebook_and_website_lead = ViewColumn(
        id=Autoincrement.hex_string("cost_per_facebook_and_website_lead"),
        display_name="Cost per Facebook and Pixel lead",
        primary_value=FieldsMetadata.facebook_and_pixel_lead_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_new_messaging_conversation = ViewColumn(
        id=Autoincrement.hex_string("cost_per_new_messaging_conversation"),
        display_name="Cost per new messaging conversation",
        primary_value=FieldsMetadata.cost_per_new_messaging_connection,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_messaging_conversation_started = ViewColumn(
        id=Autoincrement.hex_string("cost_per_messaging_conversation_started"),
        display_name="Cost per messaging conversation started",
        primary_value=FieldsMetadata.cost_per_messaging_conversation_started,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_blocked_messaging_converastion = ViewColumn(
        id=Autoincrement.hex_string("cost_per_blocked_messaging_conversation"),
        display_name="Cost per blocked messaging conversation",
        primary_value=FieldsMetadata.cost_per_blocked_messaging_conversation,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_messaging_reply = ViewColumn(
        id=Autoincrement.hex_string("cost_per_messaging_reply"),
        display_name="Cost per messaging reply",
        primary_value=FieldsMetadata.cost_per_messaging_reply,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_offline_add_to_cart = ViewColumn(
        id=Autoincrement.hex_string("cost_per_offline_add_to_cart"),
        display_name="Cost per offline add to cart",
        primary_value=FieldsMetadata.offline_adds_to_cart_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_offline_other_conversion = ViewColumn(
        id=Autoincrement.hex_string("cost_per_offline_other_conversion"),
        display_name="Cost per offline other conversion",
        primary_value=FieldsMetadata.other_offline_conversions_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_offline_conversion = ViewColumn(
        id=Autoincrement.hex_string("cost_per_offline_conversion"),
        display_name="Cost per offline conversion",
        primary_value=FieldsMetadata.offline_conversion_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_purchase = ViewColumn(
        id=Autoincrement.hex_string("cost_per_purchase"),
        display_name="Cost per purchase",
        primary_value=FieldsMetadata.purchases_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    cost_per_add_to_cart = ViewColumn(
        id=Autoincrement.hex_string("cost_per_add_to_cart"),
        display_name="Cost per add to cart",
        primary_value=FieldsMetadata.adds_to_cart_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    cost_per_total_leads = ViewColumn(
        id=Autoincrement.hex_string("cost_per_total_leads"),
        display_name="Cost per total leads",
        primary_value=FieldsMetadata.leads_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_total_checkouts_initiated = ViewColumn(
        id=Autoincrement.hex_string("cost_per_total_checkouts_initiated"),
        display_name="Cost per total checkouts initiated",
        primary_value=FieldsMetadata.checkouts_initiated_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_view_content = ViewColumn(
        id=Autoincrement.hex_string("cost_per_view_content"),
        display_name="Cost per view content",
        primary_value=FieldsMetadata.content_views_cost,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
    cost_per_15s_video_view = ViewColumn(
        id=Autoincrement.hex_string("cost_per_15s_video_view"),
        display_name="Cost per 15s video views",
        primary_value=FieldsMetadata.cost_per_15s_video_view,
        type_id=ViewColumnType.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.COST_PER_ACTION.value,
    )
