from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategoryEnum import ViewColumnCategoryEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewFieldsMetricPerformanceMetadata:
    result_rate = ViewColumn(Autoincrement.hex_string('result_rate'), display_name="Results rate",
                             primary_value=FieldsMetadata.result_rate,
                             type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                             category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    reach = ViewColumn(Autoincrement.hex_string('reach'), display_name="Reach", primary_value=FieldsMetadata.reach,
                       type_id=ViewColumnTypeEnum.NUMBER.value, category_id=ViewColumnCategoryEnum.PERFORMANCE.value,
                       is_fixed=False)
    frequency = ViewColumn(Autoincrement.hex_string('frequency'), display_name="Frequency",
                           primary_value=FieldsMetadata.frequency,
                           type_id=ViewColumnTypeEnum.NUMBER.value,
                           category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    impressions = ViewColumn(Autoincrement.hex_string('impressions'), display_name="Impressions",
                             primary_value=FieldsMetadata.impressions,
                             type_id=ViewColumnTypeEnum.NUMBER.value,
                             category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    amount_spent = ViewColumn(Autoincrement.hex_string('amount_spent'), display_name="Amount spent",
                              primary_value=FieldsMetadata.amount_spent,
                              type_id=ViewColumnTypeEnum.CURRENCY.value,
                              category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    clicks_all = ViewColumn(Autoincrement.hex_string('clicks_all'), display_name="Clicks (All)",
                            primary_value=FieldsMetadata.clicks_all,
                            type_id=ViewColumnTypeEnum.NUMBER.value,
                            category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    cpc_all = ViewColumn(Autoincrement.hex_string('cpc_all'), display_name="CPC (All)",
                         primary_value=FieldsMetadata.cpc_all,
                         type_id=ViewColumnTypeEnum.CURRENCY.value,
                         category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    ctr_all = ViewColumn(Autoincrement.hex_string('ctr_all'), display_name="CTR (All)",
                         primary_value=FieldsMetadata.ctr_all,
                         type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                         category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    quality_ranking = ViewColumn(Autoincrement.hex_string('quality_ranking'), display_name="Quality ranking",
                                 primary_value=FieldsMetadata.quality_ranking,
                                 type_id=ViewColumnTypeEnum.TEXT.value,
                                 category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    engagement_rate_ranking = ViewColumn(Autoincrement.hex_string('engagement_rate_ranking'),
                                         display_name="Engagement rate ranking",
                                         primary_value=FieldsMetadata.engagement_rate_ranking,
                                         type_id=ViewColumnTypeEnum.TEXT.value,
                                         category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    conversion_rate_ranking = ViewColumn(Autoincrement.hex_string('conversion_rate_ranking'),
                                         display_name="Conversion rate ranking",
                                         primary_value=FieldsMetadata.conversion_rate_ranking,
                                         type_id=ViewColumnTypeEnum.TEXT.value,
                                         category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    cost_per_1000_people_reached = ViewColumn(Autoincrement.hex_string('cost_per_1000_people_reached'),
                                              display_name="Cost per 1000 people reached",
                                              primary_value=FieldsMetadata.cost_per_1000_people_reached,
                                              type_id=ViewColumnTypeEnum.CURRENCY.value,
                                              category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    cpm = ViewColumn(Autoincrement.hex_string('cpm'), display_name="CPM",
                     primary_value=FieldsMetadata.cpm, type_id=ViewColumnTypeEnum.CURRENCY.value,
                     category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    results = ViewColumn(Autoincrement.hex_string('results'), display_name="Results",
                         primary_value=FieldsMetadata.results, type_id=ViewColumnTypeEnum.NUMBER.value,
                         category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    cost_per_result = ViewColumn(Autoincrement.hex_string('cost_per_result'), display_name="Cost per result",
                                 primary_value=FieldsMetadata.cost_per_result,
                                 type_id=ViewColumnTypeEnum.CURRENCY.value,
                                 category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
