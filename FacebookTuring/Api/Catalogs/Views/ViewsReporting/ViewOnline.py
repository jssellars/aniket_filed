from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewEvents:
    offline_adds_of_payment_info = ViewColumn(id=Autoincrement.hex_string("offline_adds_of_payment_info"),
                                              display_name="Offline adds of payment info",
                                              primary_value=FieldsMetadata.offline_app_adds_of_payment_info_total,
                                              type_id=ViewColumnType.NUMBER.value,
                                              group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_adds_to_cart = ViewColumn(id=Autoincrement.hex_string("offline_adds_to_cart"),
                                      display_name="Offline adds to cart",
                                      primary_value=FieldsMetadata.offline_adds_to_cart_total,
                                      type_id=ViewColumnType.NUMBER.value,
                                      group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_adds_to_wishlist = ViewColumn(id=Autoincrement.hex_string("offline_adds_to_wishlist"),
                                          display_name='Offline adds to wishlist',
                                          primary_value=FieldsMetadata.offline_adds_to_wish_list_total,
                                          type_id=ViewColumnType.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_registrations_completed = ViewColumn(id=Autoincrement.hex_string('offline_registrations_completed'),
                                                 display_name='Offline registrations completed',
                                                 primary_value=FieldsMetadata.offline_registrations_completed_total,
                                                 type_id=ViewColumnType.NUMBER.value,
                                                 group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_checkouts_initiated = ViewColumn(id=Autoincrement.hex_string('offline_checkouts_initiated'),
                                             display_name='Offline checkouts initiated',
                                             primary_value=FieldsMetadata.offline_checkouts_initiated_total,
                                             type_id=ViewColumnType.NUMBER.value,
                                             group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_leads = ViewColumn(id=Autoincrement.hex_string('offline_leads'),
                               display_name='Offline leads',
                               primary_value=FieldsMetadata.offline_leads_total,
                               type_id=ViewColumnType.NUMBER.value,
                               group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_purchases = ViewColumn(id=Autoincrement.hex_string('offline_purchases'),
                                   display_name='Offline purchases',
                                   primary_value=FieldsMetadata.offline_purchases_total,
                                   type_id=ViewColumnType.NUMBER.value,
                                   group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_searches = ViewColumn(id=Autoincrement.hex_string('offline_searches'),
                                  display_name='Offline searches',
                                  primary_value=FieldsMetadata.offline_searches_total,
                                  type_id=ViewColumnType.NUMBER.value,
                                  group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_content_views = ViewColumn(id=Autoincrement.hex_string('offline_content_views'),
                                       display_name='Offline content views',
                                       primary_value=FieldsMetadata.offline_content_views_total,
                                       type_id=ViewColumnType.NUMBER.value,
                                       group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    offline_other_conversions = ViewColumn(id=Autoincrement.hex_string('offline_other_conversions'),
                                           display_name='Offline other conversions',
                                           primary_value=FieldsMetadata.other_offline_conversions_total,
                                           type_id=ViewColumnType.NUMBER.value,
                                           group_display_name=ViewColumnGroupEnum.OFFLINE.value)
    all_offline_conversions = ViewColumn(id=Autoincrement.hex_string('all_offline_conversions'),
                                         display_name='All offline conversions',
                                         primary_value=FieldsMetadata.offline_conversions_total,
                                         type_id=ViewColumnType.NUMBER.value,
                                         group_display_name=ViewColumnGroupEnum.OFFLINE.value)
