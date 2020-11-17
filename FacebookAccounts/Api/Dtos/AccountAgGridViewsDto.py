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
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.ACCOUNTS_NAME],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.ACCOUNT_STATUS],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.BUSINESS_ID],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CURRENCY],
    ],
    account_insight_columns=[
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.AMOUNT_SPENT],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CPM],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.UNIQUE_CTR_ALL],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.UNIQUE_LINK_CLICK_THROUGH_RATE],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.UNIQUE_CLICKS_ALL],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.CPC],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.PURCHASES],
        ACCOUNT_COLUMNS_DEFINITION[AgGridMasterView.LEADS_TOTAL],
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
            AgGridConstants.field: column.primary_value.name,
            AgGridConstants.editable: True,
            AgGridConstants.filter: True,
            AgGridConstants.header_name: column.display_name,
        }
        if column.no_of_digits:
            column_property[AgGridConstants.number_of_decimals] = column.no_of_digits

        column_type = FieldDataTypeEnum.get_by_value(column.primary_value.type_id)
        if column_type in AgGridFilter.__members__:
            filter_property = AgGridFilter[column_type]
            column_property[AgGridConstants.filter] = filter_property.value

        result.append(column_property)

    return result
