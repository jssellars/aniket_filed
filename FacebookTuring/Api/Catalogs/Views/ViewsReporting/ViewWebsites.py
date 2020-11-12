from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewWebsites:
    purchases = ViewColumn(id=Autoincrement.hex_string("websites_purchases"),
                           display_name="Purchases (FB Pixel)",
                           primary_value=FieldsMetadata.purchases_total,
                           type_id=ViewColumnType.NUMBER.value,
                           group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    landing_page_views = ViewColumn(id=Autoincrement.hex_string('landing_page_views'),
                                    display_name='Landing page views',
                                    primary_value=FieldsMetadata.landing_page_views_total,
                                    type_id=ViewColumnType.NUMBER.value,
                                    group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    initiated_checkouts = ViewColumn(id=Autoincrement.hex_string('initiated_checkouts'),
                                     display_name='Initiated checkout (FB Pixel)',
                                     primary_value=FieldsMetadata.checkouts_initiated_total,
                                     type_id=ViewColumnType.NUMBER.value,
                                     group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    view_content = ViewColumn(id=Autoincrement.hex_string('view_content'),
                              display_name='View content (FB Pixel)',
                              primary_value=FieldsMetadata.content_views_total,
                              type_id=ViewColumnType.NUMBER.value,
                              group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    add_payment_info = ViewColumn(id=Autoincrement.hex_string('add_payment_info'),
                                  display_name='Add payment info (FB Pixel)',
                                  primary_value=FieldsMetadata.add_payment_info_total,
                                  type_id=ViewColumnType.NUMBER.value,
                                  group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    complete_registrations = ViewColumn(id=Autoincrement.hex_string('complete_registrations'),
                                        display_name='Complete registrations (FB Pixel)',
                                        primary_value=FieldsMetadata.registrations_completed_total,
                                        type_id=ViewColumnType.NUMBER.value,
                                        group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    add_to_wishlist = ViewColumn(id=Autoincrement.hex_string('add_to_wishlist'),
                                 display_name='Add to wishilist (FB Pixel)',
                                 primary_value=FieldsMetadata.adds_to_wish_list_total,
                                 type_id=ViewColumnType.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    add_to_cart = ViewColumn(id=Autoincrement.hex_string('add_to_cart'),
                             display_name='Add to cart (FB Pixel)',
                             primary_value=FieldsMetadata.adds_to_cart_total,
                             type_id=ViewColumnType.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    search = ViewColumn(id=Autoincrement.hex_string('search'),
                        display_name='Search (FB Pixel)',
                        primary_value=FieldsMetadata.searches_total,
                        type_id=ViewColumnType.NUMBER.value,
                        group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    leads_facebook = ViewColumn(id=Autoincrement.hex_string('leads_facebook'),
                                display_name='Leads (FB Pixel)',
                                primary_value=FieldsMetadata.leads_total,
                                type_id=ViewColumnType.NUMBER.value,
                                group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    leads_form = ViewColumn(id=Autoincrement.hex_string('leads_form'),
                            display_name='Leads (Form)',
                            primary_value=FieldsMetadata.on_facebook_leads_total,
                            type_id=ViewColumnType.NUMBER.value,
                            group_display_name=ViewColumnGroupEnum.WEBSITES.value)
    purchases_all = ViewColumn(id=Autoincrement.hex_string('purchases_all'),
                               display_name='Purchases',
                               primary_value=FieldsMetadata.purchases_all_total,
                               type_id=ViewColumnType.NUMBER.value,
                               group_display_name=ViewColumnGroupEnum.WEBSITES.value)
