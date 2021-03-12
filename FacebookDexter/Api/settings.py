from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="dexter", kind="api")
    port = 47300
    mongo = core.replace_in_class(
        core.Default.mongo,
        recommendations_collection_name="recommendations",
        recommendations_database_name="{env}_dexter_recommendations",
        structures_database="{env}_facebook_turing_structures",
    )
    rabbitmq = core.replace_in_class(
        core.Default.rabbitmq,
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
