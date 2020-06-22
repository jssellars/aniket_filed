from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewApps:
    app_installs = ViewColumn(id=Autoincrement.hex_string("app_installs"),
                              display_name="App Installs",
                              primary_value=FieldsMetadata.app_installs_total,
                              type_id=ViewColumnTypeEnum.NUMBER.value,
                              group_display_name=ViewColumnGroupEnum.APPS.value)
    app_engagement = ViewColumn(id=Autoincrement.hex_string('app_engagement'),
                                display_name='App engagement',
                                primary_value=FieldsMetadata.app_engagements_total,
                                type_id=ViewColumnTypeEnum.NUMBER.value,
                                group_display_name=ViewColumnGroupEnum.APPS.value)
    app_story_engagement = ViewColumn(id=Autoincrement.hex_string('app_story_engagement'),
                                      display_name='App story engagement',
                                      primary_value=FieldsMetadata.app_story_engagements_total,
                                      type_id=ViewColumnTypeEnum.NUMBER.value,
                                      group_display_name=ViewColumnGroupEnum.APPS.value)
    app_uses = ViewColumn(id=Autoincrement.hex_string('app_uses'),
                          display_name='App uses',
                          primary_value=FieldsMetadata.app_uses_total,
                          type_id=ViewColumnTypeEnum.NUMBER.value,
                          group_display_name=ViewColumnGroupEnum.APPS.value)
    credit_spends = ViewColumn(id=Autoincrement.hex_string('credit_spends'),
                               display_name='Credit spends',
                               primary_value=FieldsMetadata.mobile_credit_spends_total,
                               type_id=ViewColumnTypeEnum.NUMBER.value,
                               group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_installs = ViewColumn(id=Autoincrement.hex_string('mobile_app_installs'),
                                     display_name='Mobile app installs',
                                     primary_value=FieldsMetadata.mobile_app_installs_total,
                                     type_id=ViewColumnTypeEnum.NUMBER.value,
                                     group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_registrations = ViewColumn(id=Autoincrement.hex_string('mobile_app_registrations'),
                                          display_name='Mobile app registrations',
                                          primary_value=FieldsMetadata.mobile_app_registrations_completed_total,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_content_views = ViewColumn(id=Autoincrement.hex_string('mobile_app_content_views'),
                                          display_name='Mobile app content views',
                                          primary_value=FieldsMetadata.mobile_content_views_total,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_searches = ViewColumn(id=Autoincrement.hex_string('mobile_app_searches'),
                                     display_name='Mobile app searches',
                                     primary_value=FieldsMetadata.mobile_app_searches_total,
                                     type_id=FieldsMetadata.mobile_app_searches_total,
                                     group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_ratings = ViewColumn(id=Autoincrement.hex_string('mobile_app_ratings'),
                                    display_name='Mobile app ratings',
                                    primary_value=FieldsMetadata.mobile_app_ratings_total,
                                    type_id=ViewColumnTypeEnum.NUMBER.value,
                                    group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_tutorial_completions = ViewColumn(id=Autoincrement.hex_string('mobile_app_tutorial_completions'),
                                                 display_name='Mobile app tutorial completions',
                                                 primary_value=FieldsMetadata.mobile_app_tutorials_completed_total,
                                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                                 group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_add_to_cart = ViewColumn(id=Autoincrement.hex_string('mobile_app_add_to_cart'),
                                        display_name='Mobile app add to cart',
                                        primary_value=FieldsMetadata.mobile_adds_to_cart_total,
                                        type_id=ViewColumnTypeEnum.NUMBER.value,
                                        group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_add_to_wishlist = ViewColumn(id=Autoincrement.hex_string('mobile_app_add_to_wishlist'),
                                            display_name='Mobile app add to wishlist',
                                            primary_value=FieldsMetadata.mobile_adds_to_wish_list_total,
                                            type_id=ViewColumnTypeEnum.NUMBER.value,
                                            group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_checkouts = ViewColumn(id=Autoincrement.hex_string('mobile_app_checkouts'),
                                      display_name='Mobile app checkouts',
                                      primary_value=FieldsMetadata.mobile_checkouts_initiated_total,
                                      type_id=ViewColumnTypeEnum.NUMBER.value,
                                      group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_add_of_payment_info = ViewColumn(id=Autoincrement.hex_string('mobile_app_add_of_payment_info'),
                                                display_name='Mobile app payment details',
                                                primary_value=FieldsMetadata.mobile_app_adds_of_payment_info_total,
                                                type_id=ViewColumnTypeEnum.NUMBER.value,
                                                group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_purchases = ViewColumn(id=Autoincrement.hex_string('mobile_app_purchases'),
                                      display_name='Mobile app purchases',
                                      primary_value=FieldsMetadata.mobile_app_purchases_total,
                                      type_id=ViewColumnTypeEnum.NUMBER.value,
                                      group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_achievements = ViewColumn(id=Autoincrement.hex_string('mobile_app_achievements'),
                                         display_name='Mobile app achievements',
                                         primary_value=FieldsMetadata.mobile_app_achievements_unlocked_total,
                                         type_id=ViewColumnTypeEnum.NUMBER.value,
                                         group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_feature_unlocks = ViewColumn(id=Autoincrement.hex_string('mobile_app_feature_unlocks'),
                                            display_name='Mobile app feature unlocks',
                                            primary_value=FieldsMetadata.mobile_app_feature_unlocks,
                                            type_id=ViewColumnTypeEnum.NUMBER.value,
                                            group_display_name=ViewColumnGroupEnum.APPS.value)
    mobile_app_credit_spends = ViewColumn(id=Autoincrement.hex_string('mobile_app_credit_spends'),
                                          display_name='Mobile app credit spends',
                                          primary_value=FieldsMetadata.desktop_credit_spends_total,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.APPS.value)
