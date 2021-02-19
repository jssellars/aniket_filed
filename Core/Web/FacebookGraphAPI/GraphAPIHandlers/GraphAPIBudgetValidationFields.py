from Core.Tools.Misc.EnumerationBase import EnumerationBase


class GraphAPIBudgetValidationField(EnumerationBase):

    CURRENCY = "currency"
    CURRENCY_SYMBOL = "currencySymbol"
    MAX_AD_ACCOUNT_BID = "maximumAdAccountBid"
    MIN_AD_ACCOUNT_DAILY_BUDGET = "minimumAdAccountDailyBudget"
    MIN_AD_ACCOUNT_BUDGETS = "minimumAdAccountBudgets"
    IMPRESSIONS = "IMPRESSIONS"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    APP_INSTALLS = "APP_INSTALLS"
    LINK_CLICKS = "LINK_CLICK"
    PAGE_LIKES = "PAGE_LIKES"
    DEFAULT = "DEFAULT"
