from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="productcatalogs", kind="bt")

    rabbitmq = core.replace_in_class(
        get_env_model(env, "rabbitmq"),
        exchanges=[
            core.Exchange(
                name="{env}.direct",
                type="direct",
                inbound_queue=core.Queue(name="{env}.{app_name}.inbound", key="{env}.{app_name}.inbound.key"),
                outbound_queue=core.Queue(name="{env}.{app_name}.outbound", key="{env}.{app_name}.outbound.key"),
            )
        ],
    )
    port = 46351
