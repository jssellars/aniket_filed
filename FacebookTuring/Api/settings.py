from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="turing", kind="api")
    port = 47350
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        insights_database_name="{env}_facebook_turing_insights",
        structures_database_name="{env}_facebook_turing_structures",
    )
