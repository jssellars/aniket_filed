from itertools import chain
from typing import Dict, List

from Core.mongo_adapter import MongoProjectionState
from Core.settings_models import Model
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from facebook_business.adobjects.adaccount import AdAccount
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountBusinessMapping import (
    GraphAPIAdAccountBusinessMapping,
)
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


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
        business_owner_pages_repository = TuringMongoRepository(
            config=config.mongo,
            database_name=config.mongo.accounts_journal_database_name,
            collection_name=config.mongo.business_owner_pages_collection_name,
        )

        db_pages_result = business_owner_pages_repository.get(
            query={FieldsMetadata.business_id.name: business_id}, projection={"_id": MongoProjectionState.OFF.value}
        )

        # get promoted pages
        promote_pages = account.get_promote_pages()

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
