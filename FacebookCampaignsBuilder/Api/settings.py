from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="campaignsbuilder", kind="api")
    port = 47220
    rabbitmq = core.replace_in_class(
        core.Default.rabbitmq,
        exchanges=[
            core.Exchange(
                name="{env}.direct",
                type="direct",
                outbound_queue=core.Queue(
                    name="{env}.{app_domain}.{app_name}.outbound", key="{env}.{app_domain}.{app_name}.outbound.key"
                ),
            )
        ]
    )
