from Core.Tools.Misc.AgGridConstants import PinnedDirection
from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Metadata.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewFieldsStructureMetadata:
    buying_type = ViewColumn(
        Autoincrement.hex_string("buying_type"),
        display_name="Buying type",
        primary_value=FieldsMetadata.buying_type,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    status = ViewColumn(
        Autoincrement.hex_string("status"),
        display_name="Status",
        primary_value=FieldsMetadata.status,
        type_id=ViewColumnType.BUTTON.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=True,
        pinned=PinnedDirection.LEFT,
        is_toggle=True,
    )
    account_status = ViewColumn(
        Autoincrement.hex_string("status"),
        display_name="Status",
        primary_value=FieldsMetadata.account_status,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
    )
    effective_status = ViewColumn(
        Autoincrement.hex_string("effective_status"),
        display_name="Effective status",
        primary_value=FieldsMetadata.effective_status,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    created_at = ViewColumn(
        Autoincrement.hex_string("created_at"),
        display_name="Created at",
        primary_value=FieldsMetadata.created_at,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    last_significant_edit = ViewColumn(
        Autoincrement.hex_string("last_significant_edit"),
        display_name="Last significant edit",
        primary_value=FieldsMetadata.last_significant_edit,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    start_date = ViewColumn(
        Autoincrement.hex_string("start_date"),
        display_name="Start date",
        primary_value=FieldsMetadata.start_date,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    stop_time = ViewColumn(
        Autoincrement.hex_string("stop_time"),
        display_name="End date",
        primary_value=FieldsMetadata.stop_time,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_strategy = ViewColumn(
        Autoincrement.hex_string("bid_strategy"),
        display_name="Bid strategy",
        primary_value=FieldsMetadata.bid_strategy,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    amount_spent_percentage = ViewColumn(
        Autoincrement.hex_string("amount_spent_percentage"),
        display_name="Amount spent percentage",
        primary_value=FieldsMetadata.amount_spent_percentage,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_cap = ViewColumn(
        Autoincrement.hex_string("bid_cap"),
        display_name="Bid cap",
        primary_value=FieldsMetadata.bid_cap,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    budget = ViewColumn(
        Autoincrement.hex_string("budget"),
        display_name="Budget",
        primary_value=FieldsMetadata.budget,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
        no_of_digits=2,
    )
    daily_min_adset_budget = ViewColumn(
        Autoincrement.hex_string("daily_min_adset_budget"),
        display_name="Daily mininum adset budget",
        primary_value=FieldsMetadata.daily_min_adset_budget,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    daily_max_adset_budget = ViewColumn(
        Autoincrement.hex_string("daily_max_adset_budget"),
        display_name="Daily maximum adset budget",
        primary_value=FieldsMetadata.daily_max_adset_budget,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    lifetime_min_adset_budget = ViewColumn(
        Autoincrement.hex_string("lifetime_min_adset_budget"),
        display_name="Lifetime minimum adset budget",
        primary_value=FieldsMetadata.lifetime_min_adset_budget,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    lifetime_max_adset_budget = ViewColumn(
        Autoincrement.hex_string("lifetime_max_adset_budget"),
        display_name="Lifetime maximum adset budget",
        primary_value=FieldsMetadata.lifetime_max_adset_budget,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    budget_remaining = ViewColumn(
        Autoincrement.hex_string("budget_remaining"),
        display_name="Budget remaining",
        primary_value=FieldsMetadata.budget_remaining,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    daily_budget = ViewColumn(
        Autoincrement.hex_string("daily_budget"),
        display_name="Daily budget",
        primary_value=FieldsMetadata.daily_budget,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    lifetime_budget = ViewColumn(
        Autoincrement.hex_string("lifetime_budget"),
        display_name="Lifetime budget",
        primary_value=FieldsMetadata.lifetime_budget,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    special_ad_category = ViewColumn(
        Autoincrement.hex_string("special_ad_category"),
        display_name="Special ad category",
        primary_value=FieldsMetadata.special_ad_category,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    source_campaign_id = ViewColumn(
        Autoincrement.hex_string("source_campaign_id"),
        display_name="Source campaign ID",
        primary_value=FieldsMetadata.source_campaign_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    spend_cap = ViewColumn(
        Autoincrement.hex_string("spend_cap"),
        display_name="Spend cap",
        primary_value=FieldsMetadata.spend_cap,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    updated_time = ViewColumn(
        Autoincrement.hex_string("updated_time"),
        display_name="Last updated time",
        primary_value=FieldsMetadata.updated_time,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    adset_schedule = ViewColumn(
        Autoincrement.hex_string("adset_schedule"),
        display_name="Ad set schedule",
        primary_value=FieldsMetadata.adset_schedule,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    attribution_spec = ViewColumn(
        Autoincrement.hex_string("attribution_spec"),
        display_name="Attribution spec",
        primary_value=FieldsMetadata.attribution_spec,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_adjustments = ViewColumn(
        Autoincrement.hex_string("bid_adjustments"),
        display_name="Bid adjustments",
        primary_value=FieldsMetadata.bid_adjustments,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_constraints = ViewColumn(
        Autoincrement.hex_string("bid_constraints"),
        display_name="Bid constraints",
        primary_value=FieldsMetadata.bid_constraints,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_amount = ViewColumn(
        Autoincrement.hex_string("bid_amount"),
        display_name="Bid amount",
        primary_value=FieldsMetadata.bid_amount,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    bid_info = ViewColumn(
        Autoincrement.hex_string("bid_info"),
        display_name="Bid info",
        primary_value=FieldsMetadata.bid_info,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    billing_event = ViewColumn(
        Autoincrement.hex_string("billing_event"),
        display_name="Billing event",
        primary_value=FieldsMetadata.billing_event,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    daily_min_spend_target = ViewColumn(
        Autoincrement.hex_string("daily_min_spend_target"),
        display_name="Daily min budget",
        primary_value=FieldsMetadata.daily_min_spend_target,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    destination_type = ViewColumn(
        Autoincrement.hex_string("destination_type"),
        display_name="Destination type",
        primary_value=FieldsMetadata.destination_type,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    end_time = ViewColumn(
        Autoincrement.hex_string("end_time"),
        display_name="End time",
        primary_value=FieldsMetadata.end_time,
        type_id=ViewColumnType.DATE.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    instagram_actor_id = ViewColumn(
        Autoincrement.hex_string("instagram_actor_id"),
        display_name="Instagram actor ID",
        primary_value=FieldsMetadata.instagram_actor_id,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    optimization_goal = ViewColumn(
        Autoincrement.hex_string("optimization_goal"),
        display_name="Optimization goal",
        primary_value=FieldsMetadata.optimization_goal,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    optimization_sub_event = ViewColumn(
        Autoincrement.hex_string("optimization_sub_event"),
        display_name="Optimization sub event",
        primary_value=FieldsMetadata.optimization_sub_event,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    source_adset_id = ViewColumn(
        Autoincrement.hex_string("source_adset_id"),
        display_name="Source ad set ID",
        primary_value=FieldsMetadata.source_adset_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    lifetime_min_spend_target = ViewColumn(
        Autoincrement.hex_string("lifetime_min_spend_target"),
        display_name="Minimum lifetime budget",
        primary_value=FieldsMetadata.lifetime_min_spend_target,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    daily_spend_cap = ViewColumn(
        Autoincrement.hex_string("daily_spend_cap"),
        display_name="Daily spend cap",
        primary_value=FieldsMetadata.daily_spend_cap,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    source_ad_id = ViewColumn(
        Autoincrement.hex_string("source_ad_id"),
        display_name="Source ad ID",
        primary_value=FieldsMetadata.source_ad_id,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    delivery = ViewColumn(
        Autoincrement.hex_string("delivery"),
        display_name="Delivery",
        primary_value=FieldsMetadata.delivery,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    adset_delivery = ViewColumn(
        Autoincrement.hex_string("adset_delivery"),
        display_name="Ad set delivery",
        primary_value=FieldsMetadata.adset_delivery,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    lifetime_spent = ViewColumn(
        Autoincrement.hex_string("lifetime_spent"),
        display_name="Lifetime spent",
        primary_value=FieldsMetadata.lifetime_spent,
        type_id=ViewColumnType.CURRENCY.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    location = ViewColumn(
        Autoincrement.hex_string("location"),
        display_name="Location",
        primary_value=FieldsMetadata.location,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    age = ViewColumn(
        Autoincrement.hex_string("age"),
        display_name="Age",
        primary_value=FieldsMetadata.age,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    gender = ViewColumn(
        Autoincrement.hex_string("gender"),
        display_name="Gender",
        primary_value=FieldsMetadata.gender,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    included_custom_audiences = ViewColumn(
        Autoincrement.hex_string("included_custom_audiences"),
        display_name="Included custom audiences",
        primary_value=FieldsMetadata.included_custom_audiences,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    excluded_custom_audiences = ViewColumn(
        Autoincrement.hex_string("excluded_custom_audiences"),
        display_name="Excluded custom audiences",
        primary_value=FieldsMetadata.excluded_custom_audiences,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    page_name = ViewColumn(
        Autoincrement.hex_string("page_name"),
        display_name="Page name",
        primary_value=FieldsMetadata.page_name,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    headline = ViewColumn(
        Autoincrement.hex_string("headline"),
        display_name="Headline",
        primary_value=FieldsMetadata.headline,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    body = ViewColumn(
        Autoincrement.hex_string("body"),
        display_name="Body",
        primary_value=FieldsMetadata.body,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    link = ViewColumn(
        Autoincrement.hex_string("link"),
        display_name="Link",
        primary_value=FieldsMetadata.link,
        type_id=ViewColumnType.LINK.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    destination = ViewColumn(
        Autoincrement.hex_string("destination"),
        display_name="Destination",
        primary_value=FieldsMetadata.destination,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    url_parameters = ViewColumn(
        Autoincrement.hex_string("url_parameters"),
        display_name="URL parameters",
        primary_value=FieldsMetadata.url_parameters,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    pixel = ViewColumn(
        Autoincrement.hex_string("pixel"),
        display_name="Pixel",
        primary_value=FieldsMetadata.pixel,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
    app_event = ViewColumn(
        Autoincrement.hex_string("app_event"),
        display_name="App event",
        primary_value=FieldsMetadata.app_event,
        type_id=ViewColumnType.TEXT.value,
        category_id=ViewColumnCategory.SETTINGS.value,
        is_fixed=False,
    )
