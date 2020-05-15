from GoogleTuring.Api.Startup import startup
from GoogleTuring.Infrastructure.AdWordsAPIHandlers.AdWordsAPIBaseHandler import AdWordsAPIBaseHandler
from GoogleTuring.Infrastructure.GoogleAdWordsAPI.AdWordsStructuresClient import AdWordsStructuresClient


class AdWordsAPIStructuresHandler(AdWordsAPIBaseHandler):
    @classmethod
    def _build_client(cls, client_customer_id, permanent_token):
        adwords_client = AdWordsStructuresClient(startup.google_config, refresh_token=permanent_token)
        adwords_client.set_client_customer_id(client_customer_id)
        return adwords_client

    @classmethod
    def delete_structure(cls, permanent_token, client_customer_id, level, structure_id):
        adwords_client = cls._build_client(client_customer_id, permanent_token)
        adwords_client.delete_structure(structure_id=structure_id, level=level)

    @classmethod
    def update_structure(cls, permanent_token, client_customer_id, level, structure_id, details, data_source_name, additional_info):
        adwords_client = cls._build_client(client_customer_id, permanent_token)
        return adwords_client.update_structure(structure_id=structure_id, level=level, details=details, data_source_name=data_source_name, additional_info=additional_info)
