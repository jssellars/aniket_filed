from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewCostPerStandardEvents:
    cost_per_subscription = ViewColumn(id=Autoincrement.hex_string('cost_per_subscription'),
                                       display_name='Cost per subscription',
                                       primary_value=FieldsMetadata.subscriptions_cost,
                                       type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                       group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS_COST_PER_CONVERSION.value)
    cost_per_website_subscriptions = ViewColumn(id=Autoincrement.hex_string('cost_per_website_subscriptions'),
                                                display_name='Cost per website subscriptions',
                                                primary_value=FieldsMetadata.website_subscriptions_cost,
                                                type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                                group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS_COST_PER_CONVERSION.value)
    cost_per_offline_subscriptions = ViewColumn(id=Autoincrement.hex_string('cost_per_offline_subscriptions'),
                                                display_name='Cost per offline subscriptions',
                                                primary_value=FieldsMetadata.offline_subscriptions_cost,
                                                type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                                group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS_COST_PER_CONVERSION.value)
    cost_per_instore_subscriptions = ViewColumn(id=Autoincrement.hex_string('cost_per_instore_subscriptions'),
                                                display_name='Cost per in store subscriptions',
                                                primary_value=FieldsMetadata.instore_subscriptions_cost,
                                                type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                                group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS_COST_PER_CONVERSION.value)
    cost_per_mobile_app_subscriptions = ViewColumn(id=Autoincrement.hex_string('cost_per_mobile_app_subscriptions'),
                                                   display_name='Cost per mobile app subscriptions',
                                                   primary_value=FieldsMetadata.mobile_app_subscriptions_cost,
                                                   type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                                   group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS_COST_PER_CONVERSION.value)
