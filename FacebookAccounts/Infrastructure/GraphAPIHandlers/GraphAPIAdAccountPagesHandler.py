from itertools import chain
from typing import Dict, List

from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.mongo_adapter import MongoProjectionState, MongoRepositoryBase
from Core.settings_models import Model
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from facebook_business.adobjects.adaccount import AdAccount
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountBusinessMapping import (
    GraphAPIAdAccountBusinessMapping,
)


class GraphAPIAdAccountPagesHandler:
    @classmethod
    def handle(cls, permanent_token: str, account_id: str, config) -> List[Dict]:

        _ = GraphAPISdkBase(config.facebook, permanent_token)

        # get business_id for ad account
        business_mapping = GraphAPIAdAccountBusinessMapping(GraphAPIBusinessDto)

        account = AdAccount(account_id)
        response = account.api_get(fields=["business"])

        business = business_mapping.load(response)

        return cls.get_all_pages(config=config, account_id=account_id, business_id=business.id)

    @classmethod
    def get_all_pages(cls, config: Model, account_id: str, business_id: str):

        account = AdAccount(account_id)
        business_owner_pages_repository = MongoRepositoryBase(
            config=config.mongo,
            database_name=config.mongo.accounts_journal_database_name,
            collection_name=config.mongo.business_owner_pages_collection_name,
        )

        db_pages_result = business_owner_pages_repository.get(
            query={FieldsMetadata.business_id.name: business_id},
            projection={
                "_id": MongoProjectionState.OFF.value,
                FacebookMiscFields.id: MongoProjectionState.ON.value,
                FacebookMiscFields.name: MongoProjectionState.ON.value,
            },
        )

        # get promoted pages
        # Note: We filter valid pages if they have an associated business field
        # But the existence of business field might not necessarily be the determining factor
        raw_promote_pages = account.get_promote_pages(fields=["name", "id", "business"])
        promote_pages = [page for page in raw_promote_pages if page.pop("business", None) is not None]

        all_pages = chain(db_pages_result, promote_pages)

        # Map and remove duplicates
        ids = set()
        pages = []
        for page in all_pages:
            if not page["id"] in ids:
                ids.add(page["id"])
                page["facebook_id"] = page.pop("id")
                pages.append(page)

        return pages
