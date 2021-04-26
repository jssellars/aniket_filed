from enum import Enum


class FacebookMiscFields:
    business_owner_id = "business_owner_id"
    business_owner_facebook_id = "business_owner_facebook_id"
    business_facebook_id = "business_facebook_id"
    account_id = "account_id"
    status = "status"
    sync_status = "sync_status"
    insights_sync_status = "insights_sync_status"
    structures_sync_status = "structures_sync_status"
    sync_start_date = "last_sync_start_date"
    structures_sync_start_date = "structures_last_sync_start_date"
    insights_sync_start_date = "insights_last_sync_start_date"
    sync_end_date = "last_sync_end_date"
    structures_sync_end_date = "structures_last_sync_end_date"
    insights_sync_end_date = "insights_last_sync_end_date"
    last_synced_on = "last_synced_on"
    previous_last_synced_on = "previous_last_synced_on"
    last_three_months = 90
    last_one_months = 30
    last_two_weeks = 14
    id = "id"
    name = "name"
    facebook_id = "facebook_id"
    actions = "actions"
    last_updated_at = "last_updated_at"
    details = "details"
    effective_status = "effective_status"
    end_time = "end_time"
    created_time = "created_time"
    created_at = "created_at"
    report = "sync_report"
    date_added = "date_added"
    level = "level"
    structure_id = "structure_id"
    targeting = "targeting"
    age_min = "age_min"
    age_max = "age_max"
    genders = "genders"
    copied_adset_id = "copied_adset_id"
    business = "business"


class FacebookParametersStrings:
    level = "level"
    breakdowns = "breakdowns"
    action_breakdowns = "action_breakdowns"
    time_increment = "time_increment"
    time_range = "time_range"
    since = "since"
    until = "until"
    limit = "limit"
    filtering = "filtering"
    sort = "sort"
    default_summary = "default_summary"
    average = "average"


class Gender(Enum):
    ALL = 0
    WOMEN = 1
    MEN = 2


class FacebookGender(Enum):
    MEN = 1
    WOMEN = 2


class FacebookBreakdownGender(Enum):
    MALE = 1
    FEMALE = 2
