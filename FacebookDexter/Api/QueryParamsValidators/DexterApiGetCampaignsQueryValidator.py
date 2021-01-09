import json
from typing import List, Dict

from flask import Response

from Core.Dexter.Infrastructure.Domain.DexterJournalEnums import DexterEngineRunJournalEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelIdKeyEnum
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from Core.mongo_adapter import MongoRepositoryBase, MongoOperator, MongoProjectionState


def validate(request_args):
    ad_account_id = request_args.get('adAccountId', None)
    channel = request_args.get('channel', None)
    if ad_account_id is None and channel is None:
        error = json.dumps('Please provide ad account and channel')
        return Response(response=error, status=400, mimetype='application/json')
    if ad_account_id is None:
        error = json.dumps('Please provide ad account')
        return Response(response=error, status=400, mimetype='application/json')
    if channel is None:
        error = json.dumps('Please provide channel')
        return Response(response=error, status=400, mimetype='application/json')
    return {
        'ad_account_id': ad_account_id,
        'channel': channel
    }


def get_campaigns(recommendation_repository: MongoRepositoryBase, ad_account_id: str, channel: str) -> List[Dict]:

    on_metrics = [
        LevelIdKeyEnum.CAMPAIGN.value,
        FieldsMetadata.campaign_name.name,
    ]
    off_metrics = ["_id"]

    db_result = recommendation_repository.get(
        query={
            MongoOperator.AND.value: [
                {
                    LevelIdKeyEnum.ACCOUNT.value: {
                        MongoOperator.EQUALS.value: ad_account_id
                    }
                },
                {
                    DexterEngineRunJournalEnum.CHANNEL.value: {
                        MongoOperator.EQUALS.value: channel
                    }
                },
            ]
        },
        projection={
            **{m: MongoProjectionState.OFF.value for m in off_metrics},
            **{m: MongoProjectionState.ON.value for m in on_metrics},
        },
    )

    for entry in db_result:
        entry["id"] = entry.pop(FieldsMetadata.campaign_id.name)
        entry["name"] = entry.pop(FieldsMetadata.campaign_name.name)

    # Creates a set from the list of dictionaries to avoid duplicates
    return [dict(t) for t in {tuple(d.items()) for d in db_result}]
