import typing
from dataclasses import dataclass

from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Metadata.Views import AgGridMasterView
from Core.Metadata.Views.AgGridMasterView import ACCOUNT_COLUMNS_DEFINITION
from Core.Metadata.Views.ViewBase import AgGridAccountsView, AgGridView
from Core.Tools.Misc import AgGridConstants
from Core.Tools.Misc.AgGridFilter import AgGridFilter
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum

accounts_ag_grid_view = AgGridAccountsView(
    "Accounts master table",
    id=1,
    account_structure_columns=[
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.ACCOUNT_ID],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.ACCOUNTS_NAME],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.ACCOUNT_STATUS],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.BUSINESS_ID],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.BUSINESS_MANAGER],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CURRENCY],
    ],
    account_insight_columns=[
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.AMOUNT_SPENT],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CPC],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CPM],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.PURCHASES_COST],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CTR],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.UNIQUE_CTR_ALL],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.IMPRESSIONS],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.UNIQUE_CLICKS_ALL],
    ],
)


def get_view():
    return object_to_json(
        AgGridView(
            accounts_ag_grid_view.name,
            id=accounts_ag_grid_view.id,
            is_default=True,
            is_selected=True,
            columns=get_view_columns(),
        )
    )


def get_view_columns():
    result = []
    for column in accounts_ag_grid_view.account_structure_columns + accounts_ag_grid_view.account_insight_columns:
        column_property = {
            AgGridConstants.FIELD: column.primary_value.name,
            AgGridConstants.FILTER: True,
            AgGridConstants.HEADER_NAME: column.display_name,
            AgGridConstants.COLUMN_TYPE: ViewColumnType(column.type_id).name,
        }

        if column.no_of_decimals:
            column_property[AgGridConstants.NUMBER_OF_DECIMALS] = column.no_of_decimals

        if column.is_hidden:
            column_property[AgGridConstants.SUPPRESS_COLUMNS_TOOL_PANEL] = True

        column_type = column_property[AgGridConstants.COLUMN_TYPE]
        if column_type in AgGridFilter.__members__:
            filter_property = AgGridFilter[column_type]
            column_property[AgGridConstants.FILTER] = filter_property.value

        result.append(column_property)

    return result


@dataclass
class BusinessOwnerCreatedDto:
    facebook_id: str = None
    name: str = None
    email: str = None
    requested_permissions: str = None
    filed_user_id: int = None
    businesses: typing.List[typing.Any] = None  # List[BusinessModel]


@dataclass
class BusinessOwnerUpdatedDto:
    facebook_id: str = None
    requested_permissions: str = None
    businesses: typing.List[typing.Any] = None  # List[BusinessModel]
