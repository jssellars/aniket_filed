from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata

ACCOUNT_ID = "account_id"
ACCOUNTS_NAME = "account_name"
ACCOUNT_STATUS = "account_status"
CURRENCY = "currency"
BUSINESS_ID = "business_id"
BUSINESS_MANAGER = "business_manager"
AMOUNT_SPENT = "amount_spent"
CPC = "cpc"
CPM = "cpm"
PURCHASES_COST = "purchases_cost"
UNIQUE_CTR_ALL = "unique_ctr_all"
UNIQUE_CLICKS_ALL = "unique_clicks_all"
IMPRESSIONS = "impressions"
PURCHASES = "purchases"
CTR = "ctr"

ACCOUNT_COLUMNS_DEFINITION = {
    ACCOUNT_ID: ViewColumn(
        display_name="Account ID",
        primary_value=FieldsMetadata.account_id,
        type_id=ViewColumnType.TEXT.value,
        is_hidden=True,
    ),
    ACCOUNTS_NAME: ViewColumn(
        display_name="Account Name",
        primary_value=FieldsMetadata.name,
        type_id=ViewColumnType.TEXT.value,
    ),
    ACCOUNT_STATUS: ViewColumn(
        display_name="Account Status",
        primary_value=FieldsMetadata.account_status,
        type_id=ViewColumnType.TEXT.value,
    ),
    CURRENCY: ViewColumn(
        display_name="Currency",
        primary_value=FieldsMetadata.currency,
        type_id=ViewColumnType.CURRENCY.value,
    ),
    BUSINESS_ID: ViewColumn(
        display_name="Business ID",
        primary_value=FieldsMetadata.business_id,
        type_id=ViewColumnType.TEXT.value,
    ),
    BUSINESS_MANAGER: ViewColumn(
        display_name="Business Manager",
        primary_value=FieldsMetadata.business_manager,
        type_id=ViewColumnType.TEXT.value,
    ),
    AMOUNT_SPENT: ViewColumn(
        display_name="Total Spent",
        primary_value=FieldsMetadata.amount_spent,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_decimals=2,
    ),
    CPC: ViewColumn(
        display_name="CPC",
        primary_value=FieldsMetadata.cpc_all,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_decimals=2,
    ),
    CPM: ViewColumn(
        display_name="CPM",
        primary_value=FieldsMetadata.cpm,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_decimals=2,
    ),
    PURCHASES_COST: ViewColumn(
        display_name="CPP",
        primary_value=FieldsMetadata.purchases_cost,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_decimals=2,
    ),
    CTR: ViewColumn(
        display_name="CTR",
        primary_value=FieldsMetadata.ctr_all,
        type_id=ViewColumnType.PERCENTAGE.value,
        no_of_decimals=2,
    ),
    UNIQUE_CTR_ALL: ViewColumn(
        display_name="Unique CTR (All)",
        primary_value=FieldsMetadata.unique_ctr_all,
        type_id=ViewColumnType.PERCENTAGE.value,
        no_of_decimals=2,
    ),
    IMPRESSIONS: ViewColumn(
        display_name="Impressions",
        primary_value=FieldsMetadata.impressions,
        type_id=ViewColumnType.NUMBER.value,
    ),
    UNIQUE_CLICKS_ALL: ViewColumn(
        display_name="Unique Clicks",
        primary_value=FieldsMetadata.unique_clicks_all,
        type_id=ViewColumnType.NUMBER.value,
    ),
}

