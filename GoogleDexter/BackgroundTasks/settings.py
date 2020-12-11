from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="google", name="dexter", kind="bt")
    mongo = core.replace_in_class(
        core.Default.mongo,
        accounts_collection_name="google_accounts",
        accounts_database="{env}_google_turing_accounts",
        insights_database="{env}_google_turing_insights",
        journal_collection_name="dexter_journal",
        journal_database_name="{env}_google_dexter_engine_run_journal",
        logs_database="{env}_google_dexter_logs",
        recommendations_collection_name="recommendations",
        recommendations_database_name="{env}_google_dexter_fuzzy_inference_recommendations",
        structures_database="{env}_google_turing_structures"
    )
    dexter = core.Dexter(
        min_results=1,
        days_since_last_change=3,
        recommendation_days_last_updated=3,
        time_intervals=[3, 7, 14, 30],
        date_stop=None,
    )


class Prod:
    dexter = core.replace_in_class(
        Default.dexter,
        min_results=50
    )
