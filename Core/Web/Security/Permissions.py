from enum import Flag, auto, Enum


class PermissionModule(Enum):
    NONE = 0
    ACCOUNTS = 1
    ADS_MANAGER = 2
    AUDIENCE = 3
    BACK_OFFICE = 20
    CAMPAIGN_BUILDER = 30
    CREATIVE_BUILDER = 31
    MISCELLANEOUS = 130
    OPTIMIZE = 150
    PIXEL = 160
    PRODUCT_CATALOG = 161
    REPORTS = 180
    SETTINGS = 190


class AccountsPermissions(Flag):
    CAN_ACCESS_ACCOUNTS = auto()

    ACCOUNTS_CAN_ACCESS_REPORTS_DATA = auto()

    @property
    def module(self):
        return PermissionModule.ACCOUNTS


class AdsManagerPermissions(Flag):
    CAN_ACCESS_ADS_MANAGER = auto()

    ADS_MANAGER_EDIT = auto()
    ADS_MANAGER_DELETE = auto()

    ADS_MANAGER_CAN_ACCESS_REPORTS_DATA = auto()

    @property
    def module(self):
        return PermissionModule.ADS_MANAGER


class AudiencePermissions(Flag):
    CAN_ACCESS_AUDIENCE = auto()

    AUDIENCE_CREATE = auto()
    AUDIENCE_EDIT = auto()
    AUDIENCE_DELETE = auto()

    @property
    def module(self):
        return PermissionModule.AUDIENCE


class BackOfficePermissions(Flag):
    CAN_ACCESS_BACK_OFFICE = auto()

    BILLING_AND_PAYMENT_DECREASE_INVOICE_ONE_MONTH = auto()
    BILLING_AND_PAYMENT_DOWNLOAD_INVOICE = auto()
    BILLING_AND_PAYMENT_VIEW = auto()

    OFFERS_CREATE = auto()
    OFFERS_EDIT = auto()
    OFFERS_DELETE = auto()
    OFFERS_MAKE_PUBLIC_PRIVATE = auto()
    OFFERS_VIEW = auto()

    ROLES_AND_PERMISSIONS_ROLES_CREATE = auto()
    ROLES_AND_PERMISSIONS_ROLES_DELETE = auto()
    ROLES_AND_PERMISSIONS_ROLES_EDIT = auto()
    ROLES_AND_PERMISSIONS_ROLES_VIEW = auto()

    @property
    def module(self):
        return PermissionModule.BACK_OFFICE


class CampaignBuilderPermissions(Flag):
    CAN_ACCESS_CAMPAIGN_BUILDER = auto()

    SMART_CREATE_VIEW = auto()

    @property
    def module(self):
        return PermissionModule.CAMPAIGN_BUILDER


class CreativeBuilderPermissions(Flag):
    CAN_ACCESS_CREATIVE_BUILDER = auto()

    CBBRAND_GUARDIAN_CREATE = auto()
    CBBRAND_GUARDIAN_EDIT = auto()

    CBCREATE_NEW_CREATE = auto()
    CBCREATE_NEW_EDIT = auto()

    CBMY_LIBRARY_DELETE = auto()
    CBMY_LIBRARY_EDIT = auto()
    CBMY_LIBRARY_VIEW = auto()

    CBVIEW = auto()

    @property
    def module(self):
        return PermissionModule.CREATIVE_BUILDER


class MiscellaneousPermissions(Flag):
    IS_TECHNICAL_ACCOUNT = auto()

    IS_BUSINESS_OWNER = auto()
    IS_CLIENT_EMPLOYEE = auto()
    IS_FREEMIUM = auto()

    FLAG_BIT_3 = auto()

    IS_ACCOUNT_MANAGER_ADMIN = auto()
    IS_ACCOUNT_MANAGER = auto()
    IS_SALES = auto()
    IS_SALES_ADMIN = auto()
    IS_ADMIN = auto()

    MISCELLANEOUS_FILED_SMART_TABLE_ACCESS = auto()
    MISCELLANEOUS_FILED_SMART_TABLE_EXPORT = auto()
    MISCELLANEOUS_CONNECT_TO_FACEBOOK = auto()
    MISCELLANEOUS_CONNECT_TO_GOOGLE = auto()
    MISCELLANEOUS_CONNECT_TO_SHOPIFY = auto()

    @property
    def module(self):
        return PermissionModule.MISCELLANEOUS


class OptimizePermissions(Flag):
    CAN_ACCESS_OPTIMIZE = auto()

    OPTIMIZE_DELETE = auto()

    @property
    def module(self):
        return PermissionModule.OPTIMIZE


class PixelPermissions(Flag):
    CAN_ACCESS_PIXELS = auto()

    @property
    def module(self):
        return PermissionModule.PIXEL


class ProductCatalogPermissions(Flag):
    CAN_ACCESS_PRODUCT_CATALOG = auto()

    PCCATALOGS_PRODUCT_SETS_PRODUCTS_VARIANTS_VIEW = auto()
    PCCATALOGS_PRODUCT_SETS_PRODUCTS_VARIANTS_EDIT = auto()
    PCCATALOGS_PRODUCT_SETS_PRODUCTS_VARIANTS_DELETE = auto()
    PCCATALOGS_PRODUCT_SETS_PRODUCTS_VARIANTS_CREATE = auto()

    PCDIAGNOSTICS_VIEW = auto()
    PCDIAGNOSTICS_EDIT = auto()

    PCFACEBOOK_AND_SHOPIFY_IMPORT = auto()
    PCFACEBOOK_AND_SHOPIFY_EXPORT = auto()

    @property
    def module(self):
        return PermissionModule.PRODUCT_CATALOG


class ReportsPermissions(Flag):
    CAN_ACCESS_REPORTS = auto()

    REPORT_CHART_TEMPLATES_CREATE = auto()
    REPORT_CHART_TEMPLATES_DELETE = auto()
    REPORT_CHART_TEMPLATES_EDIT = auto()
    REPORT_CHART_TEMPLATES_VIEW = auto()

    REPORT_DASHBOARDS_DELETE = auto()
    REPORT_DASHBOARDS_CREATE = auto()
    REPORT_DASHBOARDS_EDIT = auto()
    REPORT_DASHBOARDS_VIEW = auto()

    REPORT_MY_CHARTS_CREATE = auto()
    REPORT_MY_CHARTS_DELETE = auto()
    REPORT_MY_CHARTS_EDIT = auto()
    REPORT_MY_CHARTS_VIEW = auto()

    REPORT_OVERVIEW_VIEW = auto()

    REPORT_SCHEDULES_CREATE = auto()
    REPORT_SCHEDULES_DELETE = auto()
    REPORT_SCHEDULES_EDIT = auto()
    REPORT_SCHEDULES_VIEW = auto()

    REPORT_TEMPLATES_CREATE = auto()
    REPORT_TEMPLATES_DELETE = auto()
    REPORT_TEMPLATES_EDIT = auto()
    REPORT_TEMPLATES_VIEW = auto()

    REPORT_CAN_ACCESS_REPORTS_DATA = auto()

    FILTERED_STRUCTURES_PERMISSION = (
            REPORT_CHART_TEMPLATES_EDIT
            | REPORT_DASHBOARDS_EDIT
            | REPORT_TEMPLATES_EDIT
            | REPORT_MY_CHARTS_EDIT
            | REPORT_CHART_TEMPLATES_CREATE
            | REPORT_DASHBOARDS_CREATE
            | REPORT_TEMPLATES_CREATE
            | REPORT_MY_CHARTS_CREATE
    )

    @property
    def module(self):
        return PermissionModule.REPORTS


class SettingsPermissions(Flag):
    SETTINGS_BILLING_AND_PAYMENT_VIEW = auto()
    SETTINGS_CHANGE_PASSWORD_VIEW = auto()
    SETTINGS_MANAGE_PERMISSIONS_VIEW = auto()
    SETTINGS_MANAGE_PERMISSIONS_EDIT = auto()
    SETTINGS_MY_ACCOUNT_VIEW = auto()
    SETTINGS_MY_ACCOUNT_EDIT = auto()
    SETTINGS_MY_SUBSCRIPTION_VIEW = auto()
    SETTINGS_USER_MANAGEMENT_FULL = auto()
    SETTINGS_USER_MANAGEMENT_VIEW = auto()
    SETTINGS_USER_MANAGEMENT_EDIT = auto()

    @property
    def module(self):
        return PermissionModule.SETTINGS


PERMISSION_TO_MODULE = {
    AccountsPermissions: PermissionModule.ACCOUNTS,
    AdsManagerPermissions: PermissionModule.ADS_MANAGER,
    AudiencePermissions: PermissionModule.AUDIENCE,
    BackOfficePermissions: PermissionModule.BACK_OFFICE,
    CampaignBuilderPermissions: PermissionModule.CAMPAIGN_BUILDER,
    CreativeBuilderPermissions: PermissionModule.CREATIVE_BUILDER,
    MiscellaneousPermissions: PermissionModule.MISCELLANEOUS,
    OptimizePermissions: PermissionModule.OPTIMIZE,
    PixelPermissions: PermissionModule.PIXEL,
    ProductCatalogPermissions: PermissionModule.PRODUCT_CATALOG,
    ReportsPermissions: PermissionModule.REPORTS,
    SettingsPermissions: PermissionModule.SETTINGS
}
