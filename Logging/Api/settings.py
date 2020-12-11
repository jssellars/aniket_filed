from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="", name="logging", kind="bt")
    port = 40666
    mongo = core.replace_in_class(
        core.Default.mongo,
        logging_database_name="{env}_logs",
        logging_collection_name="logs",
        logs_database="{env}_logger_api_logs"
    )
