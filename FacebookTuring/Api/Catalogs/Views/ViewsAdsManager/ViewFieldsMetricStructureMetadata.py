from Core.Metadata.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Tools.Misc.AgGridConstants import PinnedDirection
from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn


class ViewFieldsMetricStructureMetadata:
    conversions = ViewColumn(
        Autoincrement.hex_string("conversions"),
        display_name="Conversions (All)",
        primary_value=FieldsMetadata.conversions,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_fixed=False,
    )
    account_id = ViewColumn(
        Autoincrement.hex_string("account_id"),
        display_name="Account ID",
        primary_value=FieldsMetadata.account_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    account_name = ViewColumn(
        Autoincrement.hex_string("account_name"),
        display_name="Account name",
        primary_value=FieldsMetadata.account_name,
        secondary_value=FieldsMetadata.account_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    ad_id = ViewColumn(
        Autoincrement.hex_string("ad_id"),
        display_name="Ad ID",
        primary_value=FieldsMetadata.ad_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    ad_image = ViewColumn(
        Autoincrement.hex_string("ad_image"),
        display_name="Ad Image",
        primary_value=FieldsMetadata.ad_image,
        type_id=ViewColumnType.IMAGE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    ad_name = ViewColumn(
        Autoincrement.hex_string("ad_name"),
        display_name="Ad name",
        primary_value=FieldsMetadata.ad_name,
        secondary_value=FieldsMetadata.ad_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )
    adset_id = ViewColumn(
        Autoincrement.hex_string("adset_id"),
        display_name="Ad set ID",
        primary_value=FieldsMetadata.adset_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    adset_name = ViewColumn(
        Autoincrement.hex_string("adset_name"),
        display_name="Ad set name",
        primary_value=FieldsMetadata.adset_name,
        secondary_value=FieldsMetadata.adset_id,
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
        primary_value=FieldsMetadata.campaign_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    campaign_name = ViewColumn(
        Autoincrement.hex_string("campaign_name"),
        display_name="Campaign name",
        primary_value=FieldsMetadata.campaign_name,
        secondary_value=FieldsMetadata.campaign_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        is_editable=True,
        pinned=PinnedDirection.LEFT,
        is_sortable=True,
        is_filterable=True,
    )
    objective = ViewColumn(
        Autoincrement.hex_string("objective"),
        display_name="Objective",
        primary_value=FieldsMetadata.objective,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )

    objective_structure = ViewColumn(
        Autoincrement.hex_string("objective_structure"),
        display_name="Objective structure",
        primary_value=FieldsMetadata.objective_structure,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
        hidden=True,
        objective_filtering=True,
    )

    date_start = ViewColumn(
        Autoincrement.hex_string("date_start"),
        display_name="Date start",
        primary_value=FieldsMetadata.date_start,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    date_stop = ViewColumn(
        Autoincrement.hex_string("date_stop"),
        display_name="Date stop",
        primary_value=FieldsMetadata.date_stop,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    date_time = ViewColumn(
        Autoincrement.hex_string("date_start"),
        display_name="Date",
        primary_value=FieldsMetadata.date_start,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
