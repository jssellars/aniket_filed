from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="dexter", kind="api")
    port = 47300
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        recommendations_collection_name="recommendations",
        recommendations_database_name="{env}_dexter_recommendations",
        structures_database="{env}_facebook_turing_structures",
    )
    rabbitmq = core.replace_in_class(
        get_env_model(env, "rabbitmq"),
        exchanges=[
            core.Exchange(
                name="{env}.direct",
                type="direct",
                outbound_queue=core.Queue(
                    name="{env}.{app_domain}.turing.outbound", key="{env}.{app_domain}.turing.outbound.key"
                ),
            )
        ],
    )
