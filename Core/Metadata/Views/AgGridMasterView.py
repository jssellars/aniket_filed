from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata

ACCOUNTS_NAME = "account_name"
ACCOUNT_STATUS = "account_status"
CURRENCY = "currency"
BUSINESS_ID = "business_id"
AMOUNT_SPENT = "amount_spent"
CPM = "cpm"
UNIQUE_CTR_ALL = "unique_ctr_all"
UNIQUE_LINK_CLICK_THROUGH_RATE = "unique_link_click_through_rate"
UNIQUE_CLICKS_ALL = "unique_clicks_all"
CPC = "cpc"
PURCHASES = "purchases"
LEADS_TOTAL = "leads_total"

ACCOUNT_COLUMNS_DEFINITION = {
    ACCOUNTS_NAME: ViewColumn(
        display_name="Account name",
        primary_value=FieldsMetadata.name,
        type_id=ViewColumnType.TEXT.value,
    ),
    ACCOUNT_STATUS: ViewColumn(
        display_name="Status",
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
    AMOUNT_SPENT: ViewColumn(
        display_name="Amount spent",
        primary_value=FieldsMetadata.amount_spent,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_digits=2,
    ),
    CPM: ViewColumn(
        display_name="CPM",
        primary_value=FieldsMetadata.cpm,
        type_id=ViewColumnType.CURRENCY.value,
        no_of_digits=2,
    ),
    UNIQUE_CTR_ALL: ViewColumn(
        display_name="Unique CTR (All)",
        primary_value=FieldsMetadata.unique_ctr_all,
        type_id=ViewColumnType.PERCENTAGE.value,
        no_of_digits=2,
    ),
    UNIQUE_LINK_CLICK_THROUGH_RATE: ViewColumn(
        display_name="Unique link click-through rate",
        primary_value=FieldsMetadata.unique_link_click_through_rate,
        type_id=ViewColumnType.PERCENTAGE.value,
        no_of_digits=2,
    ),
    UNIQUE_CLICKS_ALL: ViewColumn(
        display_name="Unique clicks (All)",
        primary_value=FieldsMetadata.unique_clicks_all,
        type_id=ViewColumnType.NUMBER.value,
    ),
    CPC: ViewColumn(
        display_name="CPC (All)",
        primary_value=FieldsMetadata.cpc_all,
        type_id=ViewColumnType.CURRENCY.value,
    ),
    PURCHASES: ViewColumn(
        display_name="Purchases (FB Pixel)",
        primary_value=FieldsMetadata.purchases_total,
        type_id=ViewColumnType.NUMBER.value,
    ),
    LEADS_TOTAL: ViewColumn(
        display_name="Leads",
        primary_value=FieldsMetadata.leads_total,
        type_id=ViewColumnType.NUMBER.value,
    ),
}
