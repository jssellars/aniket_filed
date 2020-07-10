from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategoryEnum import ViewColumnCategoryEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewFieldsMetricStructureMetadata:
    conversions = ViewColumn(Autoincrement.hex_string('conversions'), display_name="Conversions (All)",
                             primary_value=FieldsMetadata.conversions,
                             type_id=ViewColumnTypeEnum.NUMBER.value,
                             category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    account_id = ViewColumn(Autoincrement.hex_string('account_id'), display_name="Account ID",
                            primary_value=FieldsMetadata.account_id,
                            type_id=ViewColumnTypeEnum.TEXT.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                            is_fixed=False)
    account_name = ViewColumn(Autoincrement.hex_string('account_name'), display_name="Account name",
                              primary_value=FieldsMetadata.account_name,
                              secondary_value=FieldsMetadata.account_id, type_id=ViewColumnTypeEnum.LINK.value,
                              category_id=ViewColumnCategoryEnum.SETTINGS.value, is_fixed=False)
    ad_id = ViewColumn(Autoincrement.hex_string('ad_id'), display_name="Ad ID", primary_value=FieldsMetadata.ad_id,
                       type_id=ViewColumnTypeEnum.TEXT.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                       is_fixed=False)
    ad_name = ViewColumn(Autoincrement.hex_string('ad_name'), display_name="Ad name",
                         primary_value=FieldsMetadata.ad_name,
                         secondary_value=FieldsMetadata.ad_id, type_id=ViewColumnTypeEnum.TEXT.value,
                         category_id=ViewColumnCategoryEnum.SETTINGS.value, is_fixed=True)
    adset_id = ViewColumn(Autoincrement.hex_string('adset_id'), display_name="Ad set ID",
                          primary_value=FieldsMetadata.adset_id,
                          type_id=ViewColumnTypeEnum.TEXT.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                          is_fixed=False)
    adset_name = ViewColumn(Autoincrement.hex_string('adset_name'), display_name="Ad set name",
                            primary_value=FieldsMetadata.adset_name,
                            secondary_value=FieldsMetadata.adset_id, type_id=ViewColumnTypeEnum.LINK.value,
                            category_id=ViewColumnCategoryEnum.SETTINGS.value, is_fixed=True)
    campaign_id = ViewColumn(Autoincrement.hex_string('campaign_id'), display_name="Campaign ID",
                             primary_value=FieldsMetadata.campaign_id,
                             type_id=ViewColumnTypeEnum.TEXT.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                             is_fixed=False)
    campaign_name = ViewColumn(Autoincrement.hex_string('campaign_name'), display_name="Campaign name",
                               primary_value=FieldsMetadata.campaign_name,
                               secondary_value=FieldsMetadata.campaign_id, type_id=ViewColumnTypeEnum.LINK.value,
                               category_id=ViewColumnCategoryEnum.SETTINGS.value, is_fixed=True)
    objective = ViewColumn(Autoincrement.hex_string('objective'), display_name="Objective",
                           primary_value=FieldsMetadata.objective,
                           type_id=ViewColumnTypeEnum.TEXT.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                           is_fixed=False)
    date_start = ViewColumn(Autoincrement.hex_string('date_start'), display_name="Date start",
                            primary_value=FieldsMetadata.date_start,
                            type_id=ViewColumnTypeEnum.DATE.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                            is_fixed=False)
    date_stop = ViewColumn(Autoincrement.hex_string('date_stop'), display_name="Date stop",
                           primary_value=FieldsMetadata.date_stop,
                           type_id=ViewColumnTypeEnum.DATE.value, category_id=ViewColumnCategoryEnum.SETTINGS.value,
                           is_fixed=False)