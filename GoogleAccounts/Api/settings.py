from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="google", name="accounts", kind="api")
    port = 47500
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        google_accounts_database_name="{env}_google_accounts",
        accounts_collection_name="google_accounts",
        customers_collection_name="google_account_customers",
    )
