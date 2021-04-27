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
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )
