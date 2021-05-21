from Core.Metadata.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Tools.Misc.AgGridConstants import PinnedDirection
from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.GoogleAdsAPI.Models.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn


class ViewFieldsAttributeMetadata:
    ad_id = ViewColumn(
        Autoincrement.hex_string("ad_id"),
        display_name="Ad ID",
        primary_value=GoogleFieldsMetadata.ad_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    ad_name = ViewColumn(
        Autoincrement.hex_string("ad_name"),
        display_name="Ad name",
        primary_value=GoogleFieldsMetadata.ad_name,
        secondary_value=GoogleFieldsMetadata.ad_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )

    adgroup_id = ViewColumn(
        Autoincrement.hex_string("adset_id"),
        display_name="Ad Group ID",
        primary_value=GoogleFieldsMetadata.adgroup_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    adgroup_name = ViewColumn(
        Autoincrement.hex_string("adset_name"),
        display_name="Ad Group name",
        primary_value=GoogleFieldsMetadata.adgroup_name,
        secondary_value=GoogleFieldsMetadata.adgroup_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )

    campaign_id = ViewColumn(
        Autoincrement.hex_string("campaign_id"),
        display_name="Campaign ID",
        primary_value=GoogleFieldsMetadata.campaign_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    campaign_name = ViewColumn(
        Autoincrement.hex_string("campaign_name"),
        display_name="Campaign Name",
        primary_value=GoogleFieldsMetadata.campaign_name,
        secondary_value=GoogleFieldsMetadata.campaign_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )

    keyword_id = ViewColumn(
        Autoincrement.hex_string("keyword_id"),
        display_name="Keyword ID",
        primary_value=GoogleFieldsMetadata.criterion_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    keyword_match_type = ViewColumn(
        Autoincrement.hex_string("keyword_id"),
        display_name="Keyword ID",
        primary_value=GoogleFieldsMetadata.criterion_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    keyword_name = ViewColumn(
        Autoincrement.hex_string("keyword_name"),
        display_name="Keyword Name",
        primary_value=GoogleFieldsMetadata.keyword_text,
        secondary_value=GoogleFieldsMetadata.criterion_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=False,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )

    campaign_budget = ViewColumn(
        Autoincrement.hex_string("campaign_budget"),
        display_name="Campaign Name",
        primary_value=GoogleFieldsMetadata.campaign_budget,
        secondary_value=GoogleFieldsMetadata.currency_code,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )

    audience_id = ViewColumn(
        Autoincrement.hex_string("audience_id"),
        display_name="Audience ID",
        primary_value=GoogleFieldsMetadata.ad_group_criterion_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    audience = ViewColumn(
        Autoincrement.hex_string("audience"),
        display_name="Audience",
        primary_value=GoogleFieldsMetadata.audience,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        pinned=PinnedDirection.LEFT,
    )

    audience_category = ViewColumn(
        Autoincrement.hex_string("audience_category"),
        display_name="Category",
        primary_value=GoogleFieldsMetadata.audience_category,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        pinned=PinnedDirection.LEFT,
    )

    audience_type = ViewColumn(
        Autoincrement.hex_string("audience_type"),
        display_name="Type",
        primary_value=GoogleFieldsMetadata.ad_group_criterion_type,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        pinned=PinnedDirection.LEFT,
    )

    level = ViewColumn(
        Autoincrement.hex_string("level"),
        display_name="Level",
        primary_value=GoogleFieldsMetadata.level,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        pinned=PinnedDirection.LEFT,
    )
