from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewClicks:
    clicks = ViewColumn(
        id=Autoincrement.hex_string("clicks"),
        display_name="Clicks",
        primary_value=FieldsMetadata.clicks_all,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    link_clicks = ViewColumn(
        id=Autoincrement.hex_string("link_clicks"),
        display_name="Link clicks",
        primary_value=FieldsMetadata.link_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_clicks = ViewColumn(
        id=Autoincrement.hex_string("unique_clicks"),
        display_name="Unique clicks",
        primary_value=FieldsMetadata.unique_clicks_all,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_link_clicks = ViewColumn(
        id=Autoincrement.hex_string("unique_link_clicks"),
        display_name="Unique link clicks",
        primary_value=FieldsMetadata.unique_link_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    ctr = ViewColumn(
        id=Autoincrement.hex_string("ctr"),
        display_name="CTR (%)",
        primary_value=FieldsMetadata.ctr_all,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_link_clicks_ctr = ViewColumn(
        id=Autoincrement.hex_string("unique_ctr"),
        display_name="Unique link CTR (%)",
        primary_value=FieldsMetadata.unique_link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    link_clicks_ctr = ViewColumn(
        id=Autoincrement.hex_string("link_clicks_ctr"),
        display_name="Link CTR (%)",
        primary_value=FieldsMetadata.link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    link_clicks_cpc = ViewColumn(
        id=Autoincrement.hex_string("link_clicks_cpc"),
        display_name="CPC (Link)",
        primary_value=FieldsMetadata.cost_per_link_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    cpc = ViewColumn(
        id=Autoincrement.hex_string("cpc"),
        display_name="CPC (All)",
        primary_value=FieldsMetadata.cpc_all,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    outbound_clicks = ViewColumn(
        id=Autoincrement.hex_string("outbound_clicks"),
        display_name="Outbound clicks",
        primary_value=FieldsMetadata.outbound_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    outbound_clicks_ctr = ViewColumn(
        id=Autoincrement.hex_string("outbound_clicks_ctr"),
        display_name="Outbound clicks CTR (%)",
        primary_value=FieldsMetadata.outbound_link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_outbound_clicks = ViewColumn(
        id=Autoincrement.hex_string("unique_outbound_clicks"),
        display_name="Unique outbound clicks",
        primary_value=FieldsMetadata.unique_outbound_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_outbound_clicks_ctr = ViewColumn(
        id=Autoincrement.hex_string("unique_outbound_clicks_ctr"),
        display_name="Unique outbound clicks CTR (%)",
        primary_value=FieldsMetadata.unique_outbound_linK_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    cost_per_outbound_clicks = ViewColumn(
        id=Autoincrement.hex_string("cost_per_outbound_click"),
        display_name="Cost per outbound click",
        primary_value=FieldsMetadata.cost_per_outbound_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    cost_per_unique_outbound_clicks = ViewColumn(
        id=Autoincrement.hex_string("cost_per_unique_outbound_clicks"),
        display_name="Cost per unique outbound clicks",
        primary_value=FieldsMetadata.cost_per_unique_outbound_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    cost_per_inline_post_engagement = ViewColumn(
        id=Autoincrement.hex_string("cost_per_inline_post_engagement"),
        display_name="Cost per post engagement",
        primary_value=FieldsMetadata.cost_per_page_engagement,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    cost_per_unique_inline_link_click = ViewColumn(
        id=Autoincrement.hex_string("cost_per_unique_inline_link_click"),
        display_name="Cost per unique inline link click",
        primary_value=FieldsMetadata.cost_per_unique_inline_link_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    inline_post_engagement = ViewColumn(
        id=Autoincrement.hex_string("inline_post_engagement"),
        display_name="Inline post engagement",
        primary_value=FieldsMetadata.post_engagement,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    social_spend = ViewColumn(
        id=Autoincrement.hex_string("social_spend"),
        display_name="Social spend",
        primary_value=FieldsMetadata.social_spend,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
    unique_inline_link_click_ctr = ViewColumn(
        id=Autoincrement.hex_string("unique_inline_link_click_ctr"),
        display_name="Unique inline link click CTR (%)",
        primary_value=FieldsMetadata.unique_inline_link_click_ctr,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        group_display_name=ViewColumnGroupEnum.CLICKS.value,
    )
