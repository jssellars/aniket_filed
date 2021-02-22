from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="turing", kind="bt")
    mongo = core.replace_in_class(
        core.Default.mongo,
        accounts_journal_collection_name="journal",
        accounts_journal_database_name="{env}_facebook_turing_accounts_journal",
        business_owner_pages_collection_name="{env}_business_owner_pages",
        accounts_journal_sync_reports_collection_name="sync_reports",
        insights_database_name="{env}_facebook_turing_insights",
        structures_database_name="{env}_facebook_turing_structures"
    )
    rabbitmq = core.replace_in_class(
        core.Default.rabbitmq,
        exchanges=[
            core.Exchange(
                name="{env}.direct",
                type="direct",
                inbound_queue=core.Queue(
                    name="{env}.{app_domain}.{app_name}.outbound", key="{env}.{app_domain}.{app_name}.outbound.key"
                ),
                outbound_queue=core.Queue(
                    name="{env}.{app_domain}.dexter.inbound", key="{env}.{app_domain}.dexter.inbound.key"
                ),
            )
        ]
    )
    port = 47351
    days_to_sync = 60
