from typing import Dict, List

from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Metadata.Views.ViewBase import AgGridView
from Core.Tools.Misc import AgGridConstants
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list, object_to_json
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster

json_list_encoder = object_to_attribute_values_list


def format_columns(view_columns: List[ViewColumn]) -> List[Dict]:
    result = []
    for column in view_columns:
        column_property = {
            AgGridConstants.FIELD: column.primary_value.name,
            AgGridConstants.HEADER_NAME: column.display_name,
            AgGridConstants.DESCRIPTION: column.description,
            AgGridConstants.COLUMN_TYPE: ViewColumnType(column.type_id).name,
        }

        if column.no_of_decimals:
            column_property[AgGridConstants.NUMBER_OF_DECIMALS] = column.no_of_decimals

        result.append(column_property)

    return result


MASTER_VIEW = AgGridView(
    "MasterView",
    id=1,
    columns=format_columns(
        [
            ViewColumnsMaster.purchases_total,
            ViewColumnsMaster.purchases_cost,
            ViewColumnsMaster.purchase_roas,
            ViewColumnsMaster.leads_total,
            ViewColumnsMaster.leads_cost,
            ViewColumnsMaster.amount_spent,
            ViewColumnsMaster.impressions,
            ViewColumnsMaster.reach,
            ViewColumnsMaster.cpm,
            ViewColumnsMaster.cpc_all,
            ViewColumnsMaster.unique_ctr_all,
            ViewColumnsMaster.frequency,
            ViewColumnsMaster.landing_page_views_total,
            ViewColumnsMaster.landing_page_views_cost,
        ]
    ),
)

PERFORMANCE_VIEW = AgGridView(
    "Performance",
    id=2,
    is_default=True,
    columns=format_columns(
        [
            ViewColumnsMaster.cpm,
            ViewColumnsMaster.unique_ctr_all,
            ViewColumnsMaster.cpc_all,
            ViewColumnsMaster.amount_spent,
        ]
    ),
)

PURCHASES_VIEW = AgGridView(
    "Purchases",
    id=3,
    columns=format_columns(
        [
            ViewColumnsMaster.purchases_total,
            ViewColumnsMaster.purchases_cost,
            ViewColumnsMaster.purchase_roas,
            ViewColumnsMaster.amount_spent,
        ]
    ),
)

LEADS_VIEW = AgGridView(
    "Leads",
    id=4,
    columns=format_columns(
        [
            ViewColumnsMaster.leads_total,
            ViewColumnsMaster.leads_cost,
            ViewColumnsMaster.landing_page_views_total,
            ViewColumnsMaster.amount_spent,
        ]
    ),
)

WEBSITE_TRAFFIC_VIEW = AgGridView(
    "Website Traffic",
    id=5,
    columns=format_columns(
        [
            ViewColumnsMaster.impressions,
            ViewColumnsMaster.landing_page_views_total,
            ViewColumnsMaster.cpm,
            ViewColumnsMaster.unique_ctr_all,
        ]
    ),
)

ENGAGEMENT_VIEW = AgGridView(
    "Engagement",
    id=6,
    columns=format_columns(
        [
            ViewColumnsMaster.impressions,
            ViewColumnsMaster.landing_page_views_total,
            ViewColumnsMaster.cpm,
            ViewColumnsMaster.unique_ctr_all,
        ]
    ),
)

AWARENESS_VIEW = AgGridView(
    "Awareness",
    id=7,
    columns=format_columns(
        [
            ViewColumnsMaster.reach,
            ViewColumnsMaster.cpm,
            ViewColumnsMaster.unique_ctr_all,
            ViewColumnsMaster.frequency,
        ]
    ),
)

views = [
    MASTER_VIEW,
    PERFORMANCE_VIEW,
    PURCHASES_VIEW,
    LEADS_VIEW,
    WEBSITE_TRAFFIC_VIEW,
    ENGAGEMENT_VIEW,
    AWARENESS_VIEW
]


def get_card_views():
    return object_to_json(views)
