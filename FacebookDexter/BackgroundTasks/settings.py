from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="dexter", kind="bt")
    mongo = core.replace_in_class(
        core.Default.mongo,
        insights_database="{env}_facebook_turing_insights",
        journal_collection_name="dexter_journal",
        journal_database_name="{env}_dexter_engine_run_journal",
        logs_database="{env}_facebook_dexter_logs",
        recommendations_collection_name="recommendations",
        recommendations_database_name="{env}_dexter_recommendations",
        structures_database="{env}_facebook_turing_structures"
    )
    dexter = core.Dexter(
        min_results=50,
        days_since_last_change=3,
        recommendation_days_last_updated=3,
        time_intervals=[7, 14, 3, 30],
        date_stop=None,
        minimum_number_of_data_points=core.MinimumNumberOfDataPoints.parse_obj({"3": 2, "7": 4, "14": 9, "30": 20}),
    )
