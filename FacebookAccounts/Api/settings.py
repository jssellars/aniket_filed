from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="accounts", kind="api")
    port = 47200
    mongo = core.replace_in_class(
        core.Default.mongo,
        accounts_journal_database_name="{env}_facebook_turing_accounts_journal",
        business_owner_pages_collection_name="business_owner_pages",
    )
