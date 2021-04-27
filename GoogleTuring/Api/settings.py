from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="google", name="turing", kind="api")
    port = 47550
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        accounts_collection_name="google_accounts",
        google_accounts_database_name="{env}_google_accounts",
        google_insights_database_name="{env}_google_turing_insights",
        google_structures_database_name="{env}_google_turing_structures",
    )
