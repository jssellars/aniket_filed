from Core.Tools.Misc import AgGridConstants
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list, object_to_json
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum
from FacebookTuring.Api.Catalogs.BusinessViews.ViewBiddingAndOptimization import (
    ViewAdBiddingAndOptimization,
    ViewAdSetBiddingAndOptimization,
    ViewCampaignBiddingAndOptimization,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewCrossDevice import (
    ViewAdCrossDevice,
    ViewAdSetCrossDevice,
    ViewCampaignCrossDevice,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewDelivery import (
    ViewAdDelivery,
    ViewAdSetDelivery,
    ViewCampaignDelivery,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewEngagement import (
    ViewAdEngagement,
    ViewAdSetEngagement,
    ViewCampaignEngagement,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewPerformance import (
    ViewAdPerformance,
    ViewAdSetPerformance,
    ViewCampaignPerformance,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewPerformanceAndClicks import (
    ViewAdPerformanceAndClicks,
    ViewAdSetPerformanceAndClicks,
    ViewCampaignPerformanceAndClicks,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewTargetingAndCreative import (
    ViewAdSetTargetingAndCreative,
    ViewAdTargetingAndCreative,
    ViewCampaignTargetingAndCreative,
)
from FacebookTuring.Api.Catalogs.BusinessViews.ViewVideoEngagement import (
    ViewAdSetVideoEngagement,
    ViewAdVideoEngagement,
    ViewCampaignVideoEngagement,
)
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewBase import AgGridView, View
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster
from FacebookTuring.Infrastructure.Domain.AgGridFilterEnum import AgGridFilterEnum
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level


class AdsManagerCatalogsViewsAgGridDto:
    json_list_encoder = object_to_attribute_values_list

    campaign = {
        "views": [
            ViewCampaignBiddingAndOptimization(),
            ViewCampaignCrossDevice(),
            ViewCampaignDelivery(),
            ViewCampaignEngagement(),
            ViewCampaignPerformance(),
            ViewCampaignPerformanceAndClicks(),
            ViewCampaignTargetingAndCreative(),
            ViewCampaignVideoEngagement(),
        ]
    }

    adset = {
        "views": [
            ViewAdSetBiddingAndOptimization(),
            ViewAdSetCrossDevice(),
            ViewAdSetDelivery(),
            ViewAdSetEngagement(),
            ViewAdSetPerformance(),
            ViewAdSetPerformanceAndClicks(),
            ViewAdSetTargetingAndCreative(),
            ViewAdSetVideoEngagement(),
        ]
    }

    ad = {
        "views": [
            ViewAdBiddingAndOptimization(),
            ViewAdCrossDevice(),
            ViewAdDelivery(),
            ViewAdEngagement(),
            ViewAdPerformance(),
            ViewAdPerformanceAndClicks(),
            ViewAdTargetingAndCreative(),
            ViewAdVideoEngagement(),
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

        if level == Level.AD.value:
            view_columns.append(
                cls.map_column_data(
                    column=ViewColumnsMaster.adset_id,
                    field_value=ViewColumnsMaster.adset_id.primary_value,
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
    def map_column_data(cls, column: ViewColumn = None, field_value: Field = None, is_secondary_value: bool = False):
        column_mapping = {AgGridConstants.column_id: field_value.name, AgGridConstants.field: field_value.name}

        if is_secondary_value:
            column_mapping[AgGridConstants.header_name] = ""
            column_mapping[AgGridConstants.suppress_columns_tool_panel] = True
            return column_mapping

        column_mapping[AgGridConstants.header_name] = column.display_name
        column_mapping[AgGridConstants.sortable] = column.is_sortable

        if column.no_of_decimals:
            column_mapping[AgGridConstants.number_of_decimals] = column.no_of_decimals

        if column.is_filterable:
            filter_property = AgGridFilterEnum.get_enum_by_name(FieldDataTypeEnum.get_by_value(field_value.type_id))
            if filter_property:
                column_mapping[AgGridConstants.filter] = filter_property.value

        if column.pinned:
            column_mapping[AgGridConstants.pinned] = column.pinned.value

        if column.is_editable:
            column_mapping[AgGridConstants.editable] = column.is_editable

        return column_mapping
