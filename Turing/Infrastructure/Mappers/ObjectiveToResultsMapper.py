class ObjectiveToResultsMapper:
    __objective_map = {
        "app_installs": "mobile_app_install",
        "brand_awareness": "estimated_ad_recallers",
        "conversions": "offsite_conversion.custom.",
        "event_responses": "rsvp",
        "lead_generation": "onsite_conversion.lead_grouped",
        "link_clicks": "link_click",
        "messages": "onsite_conversion.messaging_conversation_started_7d",
        "page_likes": "like",
        "post_engagement": "post_engagement",
        "product_catalog_sales": "offsite_conversion.fb_pixel_purchase",
        "reach": "reach",
        "video_views": "video_thruplay_watched_actions"
    }

    source_field = "objective"

    @classmethod
    def map(cls, response):
        objective = response[cls.source_field].lower()
        if objective not in cls.__objective_map.keys():
            raise ValueError("Invalid campaign objective. Cannot calculate results for this campaign")

        results_field = cls.__objective_map[objective]

        return results_field