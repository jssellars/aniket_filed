class AdWordsAPIBaseHandler:
    @classmethod
    def _build_client(cls, config, client_customer_id, permanent_token):
        raise NotImplementedError
