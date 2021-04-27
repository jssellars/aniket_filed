import logging
import os


from Core.mongo_adapter import MongoRepositoryBase
from Core.Web.GoogleAdsAPI.AdsAPI.AdsBaseClient import AdsBaseClient
from GoogleAccounts.Api.startup import config
from Core.Web.GoogleAdsAPI.Models.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleResourceType


logger = logging.getLogger(__name__)

# Oauth2 requires SSL which is not present in local testing, so disable SSl check
# https://stackoverflow.com/questions/27785375/testing-flask-oauthlib-locally-without-https
# TODO disable check only in development configuration not in production
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class AdAccountsTreeClient(AdsBaseClient):
    accounts_tree_repository = MongoRepositoryBase(
        config=config.mongo,
        database_name=config.mongo.google_accounts_database_name,
        collection_name=config.mongo.customers_collection_name,
    )

    __ACCOUNT_FIELDS = [
        GoogleAttributeFieldsMetadata.customer_client_id,
        GoogleAttributeFieldsMetadata.client_descriptive_name,
        GoogleAttributeFieldsMetadata.client_customer,
        GoogleAttributeFieldsMetadata.level,
        GoogleAttributeFieldsMetadata.manager,
        GoogleAttributeFieldsMetadata.time_zone,
        GoogleAttributeFieldsMetadata.currency_code,
    ]

    def get_account_tree(self):
        field_names = [field.resource_type.value + "." + field.field_name for field in self.__ACCOUNT_FIELDS]

        response = list()

        googleads_service = self.get_ad_service()
        customer_service = self.get_customer_service()

        # A collection of customer IDs to handle.
        customer_ids = []

        # query to retrieve all child accounts of a manager account.
        query = f"""
                       SELECT {','.join(field for field in field_names)}
                       FROM {GoogleResourceType.CUSTOMER_CLIENT.value}
                       WHERE {GoogleAttributeFieldsMetadata.level.resource_type.value + "." +
                              GoogleAttributeFieldsMetadata.level.field_name} <= 1
                """

        customer_resource_names = customer_service.list_accessible_customers().resource_names

        for customer_resource_name in customer_resource_names:
            try:
                customer = customer_service.get_customer(resource_name=customer_resource_name)
                customer_ids.append(customer.id)
            except Exception as e:
                logger.exception(f"Customer ID is cancelled, {repr(e)}")

        customer_ids = [str(id_) for id_ in customer_ids]

        for customer_id in customer_ids:
            unprocessed_customer_ids = [customer_id]
            customer_ids_to_child_accounts = dict()
            root_customer_client = None

            while unprocessed_customer_ids:
                customer_id = unprocessed_customer_ids.pop(0)
                customers = googleads_service.search(customer_id=customer_id, query=query)

                # Iterates over all rows in all pages to get all customer
                # clients under the specified customer's hierarchy.
                for googleads_row in customers:
                    customer_client = googleads_row.customer_client

                    # The customer client that with level-0 is the specified customer.
                    if customer_client.level == 0:
                        if root_customer_client is None:
                            root_customer_client = customer_client
                        continue

                    # For all level-1 (direct child) accounts that are a
                    # manager account, the above query will be run against them
                    # to create a Dictionary of managers mapped to their child
                    # accounts for printing the hierarchy afterwards.
                    if customer_id not in customer_ids_to_child_accounts:
                        customer_ids_to_child_accounts[customer_id] = []

                    customer_ids_to_child_accounts[customer_id].append(customer_client)

                    if customer_client.manager:
                        # A customer can be managed by multiple managers, so to
                        # prevent visiting the same customer many times, we
                        # need to check if it's already in the Dictionary.
                        if customer_client.id not in customer_ids_to_child_accounts and customer_client.level == 1:
                            unprocessed_customer_ids.append(customer_client.id)

            if root_customer_client is not None:
                result = list()
                self.create_account_hierarchy(result, root_customer_client, customer_ids_to_child_accounts, 0)
                response.extend(result)
            else:
                raise UserWarning(
                    "CustomerID is likely a test account, so its customer client information cannot be retrieved."
                )

        customer_info = {"google_business_owner_id": "andrew@filed.com", "customers": response}
        try:
            AdAccountsTreeClient.accounts_tree_repository.add_one(customer_info)
        except Exception as e:
            logger.exception(f"Unable to add to database, {repr(e)}")

    def create_account_hierarchy(self, response, customer_client, customer_ids_to_child_accounts, depth):
        customer_id = str(customer_client.id)

        customer_info = {
            "customer_id": customer_client.id,
            "name": customer_client.descriptive_name,
            "currency_code": customer_client.currency_code,
            "time_zone": customer_client.time_zone,
            "is_manager": customer_client.manager,
            "children": [],
        }

        response.append(customer_info)

        # Recursively call this function for all child accounts of customer_client.
        if customer_id in customer_ids_to_child_accounts:
            for child_account in customer_ids_to_child_accounts[customer_id]:
                self.create_account_hierarchy(
                    response[-1]["children"], child_account, customer_ids_to_child_accounts, depth + 1
                )
