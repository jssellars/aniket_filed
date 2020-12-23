from Core.Metadata.Views.ViewBase import AgGridView
from Core.Tools.Misc import AgGridConstants
from Core.Tools.Misc.AgGridFilter import AgGridFilter
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import Level

BASE_VIEW_COLUMNS = [
    ViewColumnsMaster.reach,
    ViewColumnsMaster.impressions,
    ViewColumnsMaster.ctr_all,
    ViewColumnsMaster.cpc_all,
    ViewColumnsMaster.unique_link_clicks,
]


def get_view(level):
    view_name = ""
    view_columns = []
    if level == Level.CAMPAIGN.value:
        view_name = "Campaigns Table"
        view_columns.extend([*BASE_VIEW_COLUMNS, ViewColumnsMaster.campaign_name, ViewColumnsMaster.campaign_id])
    else:
        view_name = "Adsets Table"
        view_columns.extend([*BASE_VIEW_COLUMNS, ViewColumnsMaster.adset_name, ViewColumnsMaster.ad_id])

    return object_to_json(
        AgGridView(
            name=view_name,
            id=1,
            is_default=True,
            is_selected=True,
            columns=get_view_columns(view_columns),
        )
    )


def get_view_columns(view_columns):
    result = []
    for column in view_columns:
        column_property = {
            AgGridConstants.FIELD: column.primary_value.name,
            AgGridConstants.HEADER_NAME: column.display_name,
            AgGridConstants.SORTABLE: column.is_sortable,
        }

        if column.no_of_decimals:
            column_property[AgGridConstants.NUMBER_OF_DECIMALS] = column.no_of_decimals

        column_type = FieldDataTypeEnum.get_by_value(column.primary_value.type_id)
        if column_type in AgGridFilter.__members__:
            filter_property = AgGridFilter[column_type]
            column_property[AgGridConstants.FILTER] = filter_property.value

        result.append(column_property)

    return result
