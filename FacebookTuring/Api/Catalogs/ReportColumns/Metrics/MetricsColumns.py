from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster

insights_field_types = [FieldType.INSIGHT, FieldType.ACTION_INSIGHT]
excluded_metrics = [
    ViewColumnsMaster.account_id,
    ViewColumnsMaster.account_name,
    ViewColumnsMaster.campaign_name,
    ViewColumnsMaster.campaign_id,
    ViewColumnsMaster.adset_name,
    ViewColumnsMaster.adset_id,
    ViewColumnsMaster.ad_name,
    ViewColumnsMaster.ad_id
]


def extract_insights_columns(insights_field_types, excluded_metrics):
    view_columns_master = extract_class_attributes_values(ViewColumnsMaster)
    insights_columns = [column for column in view_columns_master
                        if column.primary_value.field_type in insights_field_types and column not in excluded_metrics]
    return insights_columns


METRICS_COLUMNS = extract_insights_columns(insights_field_types, excluded_metrics)
