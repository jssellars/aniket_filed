from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="google", name="turing", kind="bt")
    mongo = core.replace_in_class(
        core.Default.mongo,
        accounts_collection_name="google_accounts",
        google_accounts_database_name="{env}_google_turing_accounts",
        google_insights_database_name="{env}_google_turing_insights",
        google_structures_database_name="{env}_google_turing_structures",
        location_data_collection_name="location_data"
    )
    rabbitmq = core.replace_in_class(
        core.Default.rabbitmq,
        exchanges=[
            core.Exchange(
                name="{env}.direct",
                type="direct",
                inbound_queue=core.Queue(
                    name="{env}.{app_domain}.{app_name}.outbound", key="{env}.{app_domain}.{app_name}.outbound.key"
                )
            )
        ]
    )
