from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Metadata.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewFieldsMetricStandardEventsMetadata:
    achievements_unlocked_total = ViewColumn(
        Autoincrement.hex_string("achievements_unlocked_total"),
        display_name="Total achievements unlocked",
        primary_value=FieldsMetadata.achievements_unlocked_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    achievements_unlocked_unique = ViewColumn(
        Autoincrement.hex_string("achievements_unlocked_unique"),
        display_name="Unique achievements unlocked",
        primary_value=FieldsMetadata.achievements_unlocked_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    achievements_unlocked_unique_cost = ViewColumn(
        Autoincrement.hex_string("achievements_unlocked_unique_cost"),
        display_name="Cost per unique achievement unlocked",
        primary_value=FieldsMetadata.achievements_unlocked_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    achievements_unlocked_cost = ViewColumn(
        Autoincrement.hex_string("achievements_unlocked_cost"),
        display_name="Cost per achievement unlocked",
        primary_value=FieldsMetadata.achievements_unlocked_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    achievements_unlocked_value = ViewColumn(
        Autoincrement.hex_string("achievements_unlocked_value"),
        display_name="Value achievements unlocked",
        primary_value=FieldsMetadata.achievements_unlocked_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_adds_of_payment_info_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_adds_of_payment_info_total"),
        display_name="Total mobile adds of payment info",
        primary_value=FieldsMetadata.mobile_app_adds_of_payment_info_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_app_adds_of_payment_info_total = ViewColumn(
        Autoincrement.hex_string("website_app_adds_of_payment_info_total"),
        display_name="Total website adds of payment info",
        primary_value=FieldsMetadata.website_app_adds_of_payment_info_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_app_adds_of_payment_info_total = ViewColumn(
        Autoincrement.hex_string("offline_app_adds_of_payment_info_total"),
        display_name="Total offline adds of payment info",
        primary_value=FieldsMetadata.offline_app_adds_of_payment_info_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_adds_of_payment_info_unique = ViewColumn(
        Autoincrement.hex_string("app_adds_of_payment_info_unique"),
        display_name="Unique adds of payment info",
        primary_value=FieldsMetadata.app_adds_of_payment_info_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_adds_of_payment_info_value = ViewColumn(
        Autoincrement.hex_string("mobile_app_adds_of_payment_info_value"),
        display_name="Mobile adds of payment info value",
        primary_value=FieldsMetadata.mobile_app_adds_of_payment_info_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_app_adds_of_payment_info_value = ViewColumn(
        Autoincrement.hex_string("website_app_adds_of_payment_info_value"),
        display_name="Website adds of payment info value",
        primary_value=FieldsMetadata.website_app_adds_of_payment_info_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_app_adds_of_payment_info_value = ViewColumn(
        Autoincrement.hex_string("offline_app_adds_of_payment_info_value"),
        display_name="Offline adds of payment info value",
        primary_value=FieldsMetadata.offline_app_adds_of_payment_info_value,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_adds_of_payment_info_cost = ViewColumn(
        Autoincrement.hex_string("app_adds_of_payment_info_cost"),
        display_name="Adds of payment info cost",
        primary_value=FieldsMetadata.app_adds_of_payment_info_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_adds_of_payment_info_unique_cost = ViewColumn(
        Autoincrement.hex_string("app_adds_of_payment_info_unique_cost"),
        display_name="Unique adds of payment info cost",
        primary_value=FieldsMetadata.app_adds_of_payment_info_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_adds_to_wish_list_total = ViewColumn(
        Autoincrement.hex_string("mobile_adds_to_wish_list_total"),
        display_name="Total mobile adds to wish list",
        primary_value=FieldsMetadata.mobile_adds_to_wish_list_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_adds_to_wish_list_total = ViewColumn(
        Autoincrement.hex_string("website_adds_to_wish_list_total"),
        display_name="Total website adds to wish list",
        primary_value=FieldsMetadata.website_adds_to_wish_list_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_adds_to_wish_list_total = ViewColumn(
        Autoincrement.hex_string("offline_adds_to_wish_list_total"),
        display_name="Total offline adds to wish list",
        primary_value=FieldsMetadata.offline_adds_to_wish_list_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    adds_to_wish_list_unique = ViewColumn(
        Autoincrement.hex_string("adds_to_wish_list_unique"),
        display_name="Unique adds to wish list",
        primary_value=FieldsMetadata.adds_to_wish_list_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_adds_to_wish_list_value = ViewColumn(
        Autoincrement.hex_string("mobile_adds_to_wish_list_value"),
        display_name="Mobile adds to wish list value",
        primary_value=FieldsMetadata.mobile_adds_to_wish_list_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_adds_to_wish_list_value = ViewColumn(
        Autoincrement.hex_string("website_adds_to_wish_list_value"),
        display_name="Website adds to wish list value",
        primary_value=FieldsMetadata.website_adds_to_wish_list_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_adds_to_wish_list_value = ViewColumn(
        Autoincrement.hex_string("offline_adds_to_wish_list_value"),
        display_name="Offline adds to wish list value",
        primary_value=FieldsMetadata.offline_adds_to_wish_list_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    adds_to_wish_list_cost = ViewColumn(
        Autoincrement.hex_string("adds_to_wish_list_cost"),
        display_name="Adds to wish list cost",
        primary_value=FieldsMetadata.adds_to_wish_list_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    adds_to_wish_list_unique_cost = ViewColumn(
        Autoincrement.hex_string("adds_to_wish_list_unique_cost"),
        display_name="Unique adds to wish list cost",
        primary_value=FieldsMetadata.adds_to_wish_list_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_adds_to_cart_total = ViewColumn(
        Autoincrement.hex_string("mobile_adds_to_cart_total"),
        display_name="Total mobile adds to cart",
        primary_value=FieldsMetadata.mobile_adds_to_cart_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    website_adds_to_cart_total = ViewColumn(
        Autoincrement.hex_string("website_adds_to_cart_total"),
        display_name="Total website adds to cart",
        primary_value=FieldsMetadata.website_adds_to_cart_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    offline_adds_to_cart_total = ViewColumn(
        Autoincrement.hex_string("offline_adds_to_cart_total"),
        display_name="Total offline adds to cart",
        primary_value=FieldsMetadata.offline_adds_to_cart_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    adds_to_cart_unique = ViewColumn(
        Autoincrement.hex_string("adds_to_cart_unique"),
        display_name="Unique adds to cart",
        primary_value=FieldsMetadata.adds_to_cart_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    mobile_adds_to_cart_value = ViewColumn(
        Autoincrement.hex_string("mobile_adds_to_cart_value"),
        display_name="Mobile adds to cart value",
        primary_value=FieldsMetadata.mobile_adds_to_cart_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_adds_to_cart_value = ViewColumn(
        Autoincrement.hex_string("website_adds_to_cart_value"),
        display_name="Website adds to cart value",
        primary_value=FieldsMetadata.website_adds_to_cart_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_adds_to_cart_value = ViewColumn(
        Autoincrement.hex_string("offline_adds_to_cart_value"),
        display_name="Offline adds to cart value",
        primary_value=FieldsMetadata.offline_adds_to_cart_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    adds_to_cart_cost = ViewColumn(
        Autoincrement.hex_string("adds_to_cart_cost"),
        display_name="Cost per add to cart",
        primary_value=FieldsMetadata.adds_to_cart_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    adds_to_cart_unique_cost = ViewColumn(
        Autoincrement.hex_string("adds_to_cart_unique_cost"),
        display_name="Cost per unique add to cart",
        primary_value=FieldsMetadata.adds_to_cart_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    app_activations_total = ViewColumn(
        Autoincrement.hex_string("app_activations_total"),
        display_name="App activations",
        primary_value=FieldsMetadata.app_activations_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_activations_unique = ViewColumn(
        Autoincrement.hex_string("app_activations_unique"),
        display_name="Unique app activations",
        primary_value=FieldsMetadata.app_activations_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_activations_value = ViewColumn(
        Autoincrement.hex_string("app_activations_value"),
        display_name="App activations value",
        primary_value=FieldsMetadata.app_activations_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_activations_cost = ViewColumn(
        Autoincrement.hex_string("app_activations_cost"),
        display_name="Cost per app activation",
        primary_value=FieldsMetadata.app_activations_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    app_activations_unique_cost = ViewColumn(
        Autoincrement.hex_string("app_activations_unique_cost"),
        display_name="Cost per unique app activation",
        primary_value=FieldsMetadata.app_activations_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_installs_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_installs_total"),
        display_name="Mobile app installs",
        primary_value=FieldsMetadata.mobile_app_installs_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    website_app_installs_total = ViewColumn(
        Autoincrement.hex_string("website_app_installs_total"),
        display_name="Website app installs",
        primary_value=FieldsMetadata.website_app_installs_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    app_install_cost = ViewColumn(
        Autoincrement.hex_string("app_install_cost"),
        display_name="Cost per app install",
        primary_value=FieldsMetadata.app_install_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
    )
    mobile_checkouts_initiated_total = ViewColumn(
        Autoincrement.hex_string("mobile_checkouts_initiated_total"),
        display_name="Mobile checkouts initiated",
        primary_value=FieldsMetadata.mobile_checkouts_initiated_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    website_checkouts_initiated_total = ViewColumn(
        Autoincrement.hex_string("website_checkouts_initiated_total"),
        display_name="Website checkouts initiated",
        primary_value=FieldsMetadata.website_checkouts_initiated_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    offline_checkouts_initiated_total = ViewColumn(
        Autoincrement.hex_string("offline_checkouts_initiated_total"),
        display_name="Offline checkouts initiated",
        primary_value=FieldsMetadata.offline_checkouts_initiated_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    mobile_checkouts_initiated_value = ViewColumn(
        Autoincrement.hex_string("mobile_checkouts_initiated_value"),
        display_name="Mobile checkouts initiated value",
        primary_value=FieldsMetadata.mobile_checkouts_initiated_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_checkouts_initiated_value = ViewColumn(
        Autoincrement.hex_string("website_checkouts_initiated_value"),
        display_name="Website checkouts initiated value",
        primary_value=FieldsMetadata.website_checkouts_initiated_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_checkouts_initiated_value = ViewColumn(
        Autoincrement.hex_string("offline_checkouts_initiated_value"),
        display_name="Offline checkouts initiated value",
        primary_value=FieldsMetadata.offline_checkouts_initiated_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    checkouts_initiated_cost = ViewColumn(
        Autoincrement.hex_string("checkouts_initiated_cost"),
        display_name="Cost per checkout initiated",
        primary_value=FieldsMetadata.checkouts_initiated_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    checkouts_initiated_unique_cost = ViewColumn(
        Autoincrement.hex_string("checkouts_initiated_unique_cost"),
        display_name="Cost per unique checkouts initiated",
        primary_value=FieldsMetadata.checkouts_initiated_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
    )
    checkouts_initiated_unique_total = ViewColumn(
        Autoincrement.hex_string("checkouts_initiated_unique_total"),
        display_name="Unique checkouts initiated",
        primary_value=FieldsMetadata.checkouts_initiated_unique_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_content_views_total = ViewColumn(
        Autoincrement.hex_string("mobile_content_views_total"),
        display_name="Mobile content views",
        primary_value=FieldsMetadata.mobile_content_views_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    website_content_views_total = ViewColumn(
        Autoincrement.hex_string("website_content_views_total"),
        display_name="Website content views",
        primary_value=FieldsMetadata.website_content_views_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    offline_content_views_total = ViewColumn(
        Autoincrement.hex_string("offline_content_views_total"),
        display_name="Offline content views",
        primary_value=FieldsMetadata.offline_content_views_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    mobile_content_views_value = ViewColumn(
        Autoincrement.hex_string("mobile_content_views_value"),
        display_name="Mobile content views value",
        primary_value=FieldsMetadata.mobile_content_views_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_content_views_value = ViewColumn(
        Autoincrement.hex_string("website_content_views_value"),
        display_name="Website content views value",
        primary_value=FieldsMetadata.website_content_views_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_content_views_value = ViewColumn(
        Autoincrement.hex_string("offline_content_views_value"),
        display_name="Offline content views value",
        primary_value=FieldsMetadata.offline_content_views_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    content_views_cost = ViewColumn(
        Autoincrement.hex_string("content_views_cost"),
        display_name="Cost per content view",
        primary_value=FieldsMetadata.content_views_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    content_views_unique_cost = ViewColumn(
        Autoincrement.hex_string("content_views_unique_cost"),
        display_name="Cost per unique content view",
        primary_value=FieldsMetadata.content_views_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    content_views_unique_total = ViewColumn(
        Autoincrement.hex_string("content_views_unique_total"),
        display_name="Unique content views",
        primary_value=FieldsMetadata.content_views_unique_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    mobile_credit_spends_total = ViewColumn(
        Autoincrement.hex_string("mobile_credit_spends_total"),
        display_name="Mobile credits spend",
        primary_value=FieldsMetadata.mobile_credit_spends_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_credit_spends_total = ViewColumn(
        Autoincrement.hex_string("desktop_credit_spends_total"),
        display_name="Desktop credit spend",
        primary_value=FieldsMetadata.desktop_credit_spends_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_credit_spends_value = ViewColumn(
        Autoincrement.hex_string("mobile_credit_spends_value"),
        display_name="Mobile credit spend value",
        primary_value=FieldsMetadata.mobile_credit_spends_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_credit_spends_value = ViewColumn(
        Autoincrement.hex_string("desktop_credit_spends_value"),
        display_name="Desktop credit spend value",
        primary_value=FieldsMetadata.desktop_credit_spends_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    credit_spends_cost = ViewColumn(
        Autoincrement.hex_string("credit_spends_cost"),
        display_name="Cost per credit spend",
        primary_value=FieldsMetadata.credit_spends_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_credit_spends_unique_cost = ViewColumn(
        Autoincrement.hex_string("mobile_credit_spends_unique_cost"),
        display_name="Cost per unique mobile credit spend",
        primary_value=FieldsMetadata.mobile_credit_spends_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_credit_spends_unique_total = ViewColumn(
        Autoincrement.hex_string("mobile_credit_spends_unique_total"),
        display_name="Unique mobile credit spend",
        primary_value=FieldsMetadata.mobile_credit_spends_unique_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    custom_events_total = ViewColumn(
        Autoincrement.hex_string("custom_events_total"),
        display_name="Custom events",
        primary_value=FieldsMetadata.custom_events_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    custom_events_cost = ViewColumn(
        Autoincrement.hex_string("custom_events_cost"),
        display_name="Cost per custom event",
        primary_value=FieldsMetadata.custom_events_total,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_engagements_total = ViewColumn(
        Autoincrement.hex_string("desktop_app_engagements_total"),
        display_name="Desktop app engagement",
        primary_value=FieldsMetadata.desktop_app_engagements_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_engagements_cost = ViewColumn(
        Autoincrement.hex_string("desktop_app_engagements_cost"),
        display_name="Cost per desktop app engagement",
        primary_value=FieldsMetadata.desktop_app_engagements_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_story_engagements_total = ViewColumn(
        Autoincrement.hex_string("desktop_app_story_engagements_total"),
        display_name="Desktop app story engagement",
        primary_value=FieldsMetadata.desktop_app_story_engagements_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_story_engagements_cost = ViewColumn(
        Autoincrement.hex_string("desktop_app_story_engagements_cost"),
        display_name="Cost per desktop app story engagement",
        primary_value=FieldsMetadata.desktop_app_story_engagements_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_uses_total = ViewColumn(
        Autoincrement.hex_string("desktop_app_uses_total"),
        display_name="Desktop app uses",
        primary_value=FieldsMetadata.desktop_app_uses_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    desktop_app_uses_cost = ViewColumn(
        Autoincrement.hex_string("desktop_app_uses_cost"),
        display_name="Cost per desktop app use",
        primary_value=FieldsMetadata.desktop_app_uses_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    game_plays_total = ViewColumn(
        Autoincrement.hex_string("game_plays_total"),
        display_name="Game plays",
        primary_value=FieldsMetadata.game_plays_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    game_plays_cost = ViewColumn(
        Autoincrement.hex_string("game_plays_cost"),
        display_name="Cost per game play",
        primary_value=FieldsMetadata.game_plays_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    landing_page_views_total = ViewColumn(
        Autoincrement.hex_string("landing_page_views_total"),
        display_name="Landing page views",
        primary_value=FieldsMetadata.landing_page_views_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        description="The number of times that a person clicked on an ad link and successfully loaded the destination"
                    " web page.",
    )
    landing_page_views_unique = ViewColumn(
        Autoincrement.hex_string("landing_page_views_unique"),
        display_name="Unique landing page views",
        primary_value=FieldsMetadata.landing_page_views_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    landing_page_views_cost = ViewColumn(
        Autoincrement.hex_string("landing_page_views_cost"),
        display_name="Cost per landing page view",
        primary_value=FieldsMetadata.landing_page_views_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
        description="The average cost for each landing page view.",
    )
    landing_page_views_unique_cost = ViewColumn(
        Autoincrement.hex_string("landing_page_views_unique_cost"),
        display_name="Cost per unique landing page view",
        primary_value=FieldsMetadata.landing_page_views_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    leads_total = ViewColumn(
        Autoincrement.hex_string("leads_total"),
        display_name="Leads",
        primary_value=FieldsMetadata.leads_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        description="The number of Lead events attributed to your ads.",
    )
    website_leads_total = ViewColumn(
        Autoincrement.hex_string("website_leads_total"),
        display_name="Website leads",
        primary_value=FieldsMetadata.website_leads_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_leads_total = ViewColumn(
        Autoincrement.hex_string("offline_leads_total"),
        display_name="Offline leads",
        primary_value=FieldsMetadata.offline_leads_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    on_facebook_leads_total = ViewColumn(
        Autoincrement.hex_string("on_facebook_leads_total"),
        display_name="On-Facebook leads",
        primary_value=FieldsMetadata.on_facebook_leads_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    leads_value = ViewColumn(
        Autoincrement.hex_string("leads_value"),
        display_name="Leads value",
        primary_value=FieldsMetadata.leads_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_leads_value = ViewColumn(
        Autoincrement.hex_string("website_leads_value"),
        display_name="Website leads value",
        primary_value=FieldsMetadata.website_leads_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_leads_value = ViewColumn(
        Autoincrement.hex_string("offline_leads_value"),
        display_name="Offline leads value",
        primary_value=FieldsMetadata.offline_leads_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    on_facebook_leads_value = ViewColumn(
        Autoincrement.hex_string("on_facebook_leads_value"),
        display_name="On-Facebook leads value",
        primary_value=FieldsMetadata.on_facebook_leads_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    leads_cost = ViewColumn(
        Autoincrement.hex_string("leads_cost"),
        display_name="Cost per lead",
        primary_value=FieldsMetadata.leads_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
        description="The average cost of each Lead.",
    )
    on_facebook_workflow_completions_total = ViewColumn(
        Autoincrement.hex_string("on_facebook_workflow_completions_total"),
        display_name="On-Facebook workflow completions",
        primary_value=FieldsMetadata.on_facebook_workflow_completions_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    on_facebook_workflow_completions_value = ViewColumn(
        Autoincrement.hex_string("on_facebook_workflow_completions_value"),
        display_name="On-Facebook workflow completions value",
        primary_value=FieldsMetadata.on_facebook_workflow_completions_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    on_facebook_workflow_completions_cost = ViewColumn(
        Autoincrement.hex_string("on_facebook_workflow_completions_cost"),
        display_name="Cost per on-Facebook workflow completion",
        primary_value=FieldsMetadata.on_facebook_workflow_completions_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    other_offline_conversions_total = ViewColumn(
        Autoincrement.hex_string("other_offline_conversions_total"),
        display_name="Other offline conversions",
        primary_value=FieldsMetadata.other_offline_conversions_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    other_offline_conversions_value = ViewColumn(
        Autoincrement.hex_string("other_offline_conversions_value"),
        display_name="Other offline conversions value",
        primary_value=FieldsMetadata.other_offline_conversions_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    other_offline_conversions_cost = ViewColumn(
        Autoincrement.hex_string("other_offline_conversions_cost"),
        display_name="Cost per other offline conversion",
        primary_value=FieldsMetadata.other_offline_conversions_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_purchase_roas = ViewColumn(
        Autoincrement.hex_string("mobile_app_purchase_roas"),
        display_name="Mobile app purchases ROAS",
        primary_value=FieldsMetadata.mobile_app_purchase_roas,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    purchases_total = ViewColumn(
        Autoincrement.hex_string("purchases_total"),
        display_name="Purchases",
        primary_value=FieldsMetadata.purchases_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        description="The number of Purchase events attributed to your ads.",
    )
    mobile_app_purchases_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_purchases_total"),
        display_name="Mobile app purchases",
        primary_value=FieldsMetadata.mobile_app_purchases_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_purchases_total = ViewColumn(
        Autoincrement.hex_string("website_purchases_total"),
        display_name="Website purchases",
        primary_value=FieldsMetadata.website_purchases_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_purchases_total = ViewColumn(
        Autoincrement.hex_string("offline_purchases_total"),
        display_name="Offline purchases total",
        primary_value=FieldsMetadata.offline_purchases_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    purchases_unique = ViewColumn(
        Autoincrement.hex_string("purchases_unique"),
        display_name="Unique purchases",
        primary_value=FieldsMetadata.purchases_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    purchases_value = ViewColumn(
        Autoincrement.hex_string("purchases_value"),
        display_name="Purchases value",
        primary_value=FieldsMetadata.purchases_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_purchases_value = ViewColumn(
        Autoincrement.hex_string("mobile_app_purchases_value"),
        display_name="Mobile app purchases value",
        primary_value=FieldsMetadata.mobile_app_purchases_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_purchases_value = ViewColumn(
        Autoincrement.hex_string("website_purchases_value"),
        display_name="Website purchases value",
        primary_value=FieldsMetadata.website_purchases_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_purchases_value = ViewColumn(
        Autoincrement.hex_string("offline_purchases_value"),
        display_name="Offline purchases value",
        primary_value=FieldsMetadata.offline_purchases_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    purchases_cost = ViewColumn(
        Autoincrement.hex_string("purchases_cost"),
        display_name="Cost per purchase",
        primary_value=FieldsMetadata.purchases_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
        description="The average cost of each purchase.",
    )
    purchases_unique_cost = ViewColumn(
        Autoincrement.hex_string("purchases_unique_cost"),
        display_name="Cost per unique purchase",
        primary_value=FieldsMetadata.purchases_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_sortable=True,
        is_filterable=True,
        no_of_decimals=2,
    )
    registrations_completed_total = ViewColumn(
        Autoincrement.hex_string("registrations_completed_total"),
        display_name="Registrations completed",
        primary_value=FieldsMetadata.registrations_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_registrations_completed_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_registrations_completed_total"),
        display_name="Mobile app registrations completed",
        primary_value=FieldsMetadata.mobile_app_registrations_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_registrations_completed_total = ViewColumn(
        Autoincrement.hex_string("website_registrations_completed_total"),
        display_name="Website registrations completed",
        primary_value=FieldsMetadata.website_registrations_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_registrations_completed_total = ViewColumn(
        Autoincrement.hex_string("offline_registrations_completed_total"),
        display_name="Offline registrations completed",
        primary_value=FieldsMetadata.offline_registrations_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    registrations_completed_unique = ViewColumn(
        Autoincrement.hex_string("registrations_completed_unique"),
        display_name="Unique registrations completed",
        primary_value=FieldsMetadata.registrations_completed_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    registrations_completed_value = ViewColumn(
        Autoincrement.hex_string("registrations_completed_value"),
        display_name="Registrations completed value",
        primary_value=FieldsMetadata.registrations_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_registrations_completed_value = ViewColumn(
        Autoincrement.hex_string("mobile_app_registrations_completed_value"),
        display_name="Mobile app registrations completed value",
        primary_value=FieldsMetadata.mobile_app_registrations_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_registrations_completed_value = ViewColumn(
        Autoincrement.hex_string("website_registrations_completed_value"),
        display_name="Website registrations completed value",
        primary_value=FieldsMetadata.website_registrations_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_registrations_completed_value = ViewColumn(
        Autoincrement.hex_string("offline_registrations_completed_value"),
        display_name="Offline registrations completed value",
        primary_value=FieldsMetadata.offline_registrations_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    registrations_completed_unique_cost = ViewColumn(
        Autoincrement.hex_string("registrations_completed_unique_cost"),
        display_name="Cost per unique registration completed",
        primary_value=FieldsMetadata.registrations_completed_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    registrations_completed_cost = ViewColumn(
        Autoincrement.hex_string("registrations_completed_cost"),
        display_name="Cost per registration completed",
        primary_value=FieldsMetadata.registrations_completed_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    searches_total = ViewColumn(
        Autoincrement.hex_string("searches_total"),
        display_name="Searches",
        primary_value=FieldsMetadata.searches_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_searches_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_searches_total"),
        display_name="Mobile app searches",
        primary_value=FieldsMetadata.mobile_app_searches_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_searches_total = ViewColumn(
        Autoincrement.hex_string("website_searches_total"),
        display_name="Website searches",
        primary_value=FieldsMetadata.website_searches_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_searches_total = ViewColumn(
        Autoincrement.hex_string("offline_searches_total"),
        display_name="Offline searches",
        primary_value=FieldsMetadata.offline_searches_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    searches_unique = ViewColumn(
        Autoincrement.hex_string("searches_unique"),
        display_name="Unique searches",
        primary_value=FieldsMetadata.searches_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    searches_value = ViewColumn(
        Autoincrement.hex_string("searches_value"),
        display_name="Searches value",
        primary_value=FieldsMetadata.searches_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_searches_value = ViewColumn(
        Autoincrement.hex_string("mobile_app_searches_value"),
        display_name="Mobile app searches value",
        primary_value=FieldsMetadata.mobile_app_searches_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    website_searches_value = ViewColumn(
        Autoincrement.hex_string("website_searches_value"),
        display_name="Website searches value",
        primary_value=FieldsMetadata.website_searches_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    offline_searches_value = ViewColumn(
        Autoincrement.hex_string("offline_searches_value"),
        display_name="Offline searches value",
        primary_value=FieldsMetadata.offline_searches_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    searches_cost = ViewColumn(
        Autoincrement.hex_string("searches_cost"),
        display_name="Cost per search",
        primary_value=FieldsMetadata.searches_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    searches_unique_cost = ViewColumn(
        Autoincrement.hex_string("searches_unique_cost"),
        display_name="Cost per unique search",
        primary_value=FieldsMetadata.searches_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    subscriptions_total = ViewColumn(
        Autoincrement.hex_string("subscriptions_total"),
        display_name="Subscriptions",
        primary_value=FieldsMetadata.subscriptions_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    subscriptions_value = ViewColumn(
        Autoincrement.hex_string("subscriptions_value"),
        display_name="Subscriptions value",
        primary_value=FieldsMetadata.subscriptions_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    subscriptions_cost = ViewColumn(
        Autoincrement.hex_string("subscriptions_cost"),
        display_name="Cost per subscription",
        primary_value=FieldsMetadata.subscriptions_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    tutorials_completed_total = ViewColumn(
        Autoincrement.hex_string("tutorials_completed_total"),
        display_name="Total tutorials completed",
        primary_value=FieldsMetadata.tutorials_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_tutorials_completed_total = ViewColumn(
        Autoincrement.hex_string("mobile_app_tutorials_completed_total"),
        display_name="Total mobile app tutorials completed",
        primary_value=FieldsMetadata.mobile_app_tutorials_completed_total,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    tutorials_completed_unique = ViewColumn(
        Autoincrement.hex_string("tutorials_completed_unique"),
        display_name="Unique tutorials completed",
        primary_value=FieldsMetadata.tutorials_completed_unique,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    tutorials_completed_value = ViewColumn(
        Autoincrement.hex_string("tutorials_completed_value"),
        display_name="Tutorials completed value",
        primary_value=FieldsMetadata.tutorials_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    mobile_app_tutorials_completed_value = ViewColumn(
        Autoincrement.hex_string("mobile_app_tutorials_completed_value"),
        display_name="Mobile app tutorials completed value",
        primary_value=FieldsMetadata.mobile_app_tutorials_completed_value,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    tutorials_completed_cost = ViewColumn(
        Autoincrement.hex_string("tutorials_completed_cost"),
        display_name="Cost per tutorial completed",
        primary_value=FieldsMetadata.tutorials_completed_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
    tutorials_completed_unique_cost = ViewColumn(
        Autoincrement.hex_string("tutorials_completed_unique_cost"),
        display_name="Cost per unique tutorial completed",
        primary_value=FieldsMetadata.tutorials_completed_unique_cost,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.CONVERSION.value,
        is_fixed=False,
    )
