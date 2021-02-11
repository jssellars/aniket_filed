import os
from datetime import datetime
from typing import List

import requests
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationFields import RecommendationField
from Core.mongo_adapter import MongoOperator, MongoProjectionState, MongoRepositoryBase
from FacebookDexter.BackgroundTasks.startup import config, fixtures
from FacebookDexter.Infrastructure.DexterRules.DexterOuputFormat import get_formatted_message
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import RecommendationPriority
from jinja2 import Template

EMAIL_RECIPIENTS = ["ovidiu.istrate@filed.com"]
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(CURRENT_DIR, "EmailTable.html")


def send_email(recommendations_repository: MongoRepositoryBase, account_ids: List[str]):
    recommendations = read_recommendations(recommendations_repository, account_ids)

    if not recommendations:
        return

    template = Template(open(HTML_FILE).read())
    html_body = template.render(recommendations=recommendations)

    headers = {"Authorization": f"Bearer {fixtures.technical_token_manager.get_token()}"}

    params = {
        "Recipients": ";".join(EMAIL_RECIPIENTS),
        "Subject": f"Dexter Recommendations for {datetime.now().date().isoformat()}",
        "Body": html_body,
    }

    response = requests.post(config.external_services.notification_endpoint, json=params, headers=headers)
    return response


def read_recommendations(recommendations_repository: MongoRepositoryBase, account_ids: List[str]):
    on_metrics = [
        RecommendationField.TEMPLATE.value,
        RecommendationField.ACCOUNT_ID.value,
        RecommendationField.STRUCTURE_ID.value,
        RecommendationField.STRUCTURE_NAME.value,
        RecommendationField.LEVEL.value,
        RecommendationField.TRIGGER_VARIANCE.value,
        RecommendationField.TIME_INTERVAL.value,
        RecommendationField.PRIORITY.value,
    ]

    off_metrics = ["_id"]

    result = recommendations_repository.get_sorted(
        query={RecommendationField.ACCOUNT_ID.value: {MongoOperator.IN.value: account_ids}},
        projection={
            **{m: MongoProjectionState.OFF.value for m in off_metrics},
            **{m: MongoProjectionState.ON.value for m in on_metrics},
        },
        sort_query=[(RecommendationField.PRIORITY.value, -1)],
    )

    for entry in result:
        entry.update(
            {
                RecommendationField.RECOMMENDATION.value: get_formatted_message(
                    entry[RecommendationField.TEMPLATE.value],
                    trigger_variance=entry.get("trigger_variance", None),
                    no_of_days=entry.get("time_interval", None),
                    underperforming_breakdowns=entry.get("underperforming_breakdowns", None),
                )
            }
        )
        entry[RecommendationField.TEMPLATE.value] = entry[RecommendationField.TEMPLATE.value].replace("_", " ")
        entry[RecommendationField.PRIORITY.value] = RecommendationPriority(
            entry[RecommendationField.PRIORITY.value]
        ).name.title()

        entry.pop(RecommendationField.TRIGGER_VARIANCE.value, None)
        entry.pop(RecommendationField.TIME_INTERVAL.value, None)

    return result
