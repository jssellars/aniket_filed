from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewStandardEvents:
    subscriptions = ViewColumn(id=Autoincrement.hex_string('subscriptions'),
                               display_name='Subscriptions',
                               primary_value=FieldsMetadata.subscriptions_total,
                               type_id=ViewColumnTypeEnum.NUMBER.value,
                               group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS.value)
    website_subscriptions = ViewColumn(id=Autoincrement.hex_string('website_subscriptions'),
                                       display_name='Website subscriptions',
                                       primary_value=FieldsMetadata.website_subscriptions_total,
                                       type_id=ViewColumnTypeEnum.NUMBER.value,
                                       group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS.value)
    offline_subscriptions = ViewColumn(id=Autoincrement.hex_string('offline_subscriptions'),
                                       display_name='Offline subscriptions',
                                       primary_value=FieldsMetadata.offline_subscriptions_total,
                                       type_id=ViewColumnTypeEnum.NUMBER.value,
                                       group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS.value)
    instore_subscriptions = ViewColumn(id=Autoincrement.hex_string('instore_subscriptions'),
                                       display_name='In store subscriptions',
                                       primary_value=FieldsMetadata.instore_subscriptions_total,
                                       type_id=ViewColumnTypeEnum.NUMBER.value,
                                       group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS.value)
    mobile_app_subscriptions = ViewColumn(id=Autoincrement.hex_string('mobile_app_subscriptions'),
                                          display_name='Mobile app subscriptions',
                                          primary_value=FieldsMetadata.mobile_app_subscriptions_total,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.STANDARD_EVENTS.value)
