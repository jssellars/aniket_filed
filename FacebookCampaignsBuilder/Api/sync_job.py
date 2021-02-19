from datetime import datetime, timedelta

from Core.mongo_adapter import MongoOperator, MongoRepositoryBase
from FacebookCampaignsBuilder.Api.startup import config
from FacebookCampaignsBuilder.Infrastructure.Mappings.PublishStatus import \
    PublishStatus


def clean_publish_feedback():
    feedback_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.publish_feedback_database_name,
        collection_name=config.mongo.publish_feedback_collection_name,
    )

    query = {
        "status": {MongoOperator.NOTEQUAL.value: PublishStatus.IN_PROGRESS.value},
        "start_date": {MongoOperator.LESSTHAN.value: datetime.now() - timedelta(days=1)},
    }
    feedback_repository.delete_many(query)
