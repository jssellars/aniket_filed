from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


def extract_insights_columns():
    insights_field_types = [FieldType.INSIGHT, FieldType.ACTION_INSIGHT]
    view_columns_master = extract_class_attributes_values(ViewColumnsMaster)
    insights_columns = [column for column in view_columns_master
                        if column.primary_value.field_type in insights_field_types]
    return insights_columns


METRICS_COLUMNS = extract_insights_columns()
