from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Metadata.Views.ViewBase import AgGridView
from Core.Tools.Misc import AgGridConstants
from Core.Tools.Misc.AgGridFilter import AgGridFilter
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list, object_to_json
from Core.Web.GoogleAdsAPI.Mappings.LevelMapping import Level
from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField
from Core.Web.GoogleAdsAPI.Models.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Api.Catalogs.BusinessViews.ViewPerformance import (
    ViewAdGroupPerformance,
    ViewAdPerformance,
    ViewAudiencePerformance,
    ViewCampaignPerformance,
    ViewKeywordPerformance,
)
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from GoogleTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import View
from GoogleTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster


class AdsManagerCatalogsViewsAgGridDto:
    json_list_encoder = object_to_attribute_values_list

    campaign = {
        "views": [
            ViewCampaignPerformance(),
        ]
    }

    ad_group = {
        "views": [
            ViewAdGroupPerformance(),
        ]
    }

    ad = {
        "views": [
            ViewAdPerformance(),
        ]
    }

    keyword_view = {
        "views": [
            ViewKeywordPerformance(),
        ]
    }

    audience_view = {
        "views": [
            ViewAudiencePerformance(),
        ]
    }

    def __init__(self):
        super().__init__()

    @classmethod
    def get(cls, level):
        ag_grid_views = []
        views = getattr(cls, level).get("views")

        for index, view in enumerate(views):
            ag_grid_view = AgGridView(name=view.name, id=index + 1, columns=cls.get_view_columns(view, level))
            ag_grid_views.append(ag_grid_view)

        # Make the first view from the list the default one
        if ag_grid_views:
            ag_grid_views[0].is_default = True

        return object_to_json(ag_grid_views)

    @classmethod
    def get_view_columns(cls, view: View = None, level: Level = None):

        view_columns = []

        if level in [Level.AD.value, Level.KEYWORDS.value]:
            view_columns.append(
                cls.map_column_data(
                    column=ViewColumnsMaster.adgroup_id,
                    field_value=ViewColumnsMaster.adgroup_id.primary_value,
                    is_secondary_value=True,
                )
            )

        if level == Level.KEYWORDS.value:
            view_columns.append(
                cls.map_column_data(
                    column=ViewColumnsMaster.ad_id,
                    field_value=ViewColumnsMaster.ad_id.primary_value,
                    is_secondary_value=True,
                )
            )

        for column in view.columns:
            if column.secondary_value:
                view_columns.append(
                    cls.map_column_data(column=column, field_value=column.secondary_value, is_secondary_value=True)
                )
            view_columns.append(cls.map_column_data(column=column, field_value=column.primary_value))

        return view_columns

    @classmethod
    def map_column_data(
        cls, column: ViewColumn = None, field_value: GoogleField = None, is_secondary_value: bool = False
    ):
        column_mapping = {
            AgGridConstants.COLUMN_ID: field_value.name,
            AgGridConstants.FIELD: field_value.name,
            AgGridConstants.COLUMN_TYPE: ViewColumnType(column.type_id).name,
        }

        if is_secondary_value:
            column_mapping[AgGridConstants.HEADER_NAME] = ""
            column_mapping[AgGridConstants.SUPPRESS_COLUMNS_TOOL_PANEL] = True
            return column_mapping

        column_mapping[AgGridConstants.HEADER_NAME] = column.display_name
        column_mapping[AgGridConstants.SORTABLE] = column.is_sortable

        if column.no_of_decimals:
            column_mapping[AgGridConstants.NUMBER_OF_DECIMALS] = column.no_of_decimals

        if column.is_filterable:
            filter_property = AgGridFilter[ViewColumnType(column.type_id).name]
            if filter_property:
                column_mapping[AgGridConstants.FILTER] = filter_property.value

        if column.pinned:
            column_mapping[AgGridConstants.PINNED] = column.pinned.value

        if column.is_editable:
            column_mapping[AgGridConstants.EDITABLE] = column.is_editable

        if column.is_toggle:
            column_mapping[AgGridConstants.IS_TOGGLE] = column.is_toggle

        if column.primary_value.name in [
            GoogleFieldsMetadata.campaign_name.name,
            GoogleFieldsMetadata.adgroup_name.name,
        ]:
            column_mapping[AgGridConstants.IS_NAME_CLICKABLE] = True

        return column_mapping
