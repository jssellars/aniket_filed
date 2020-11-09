from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientHelper import GraphAPIGetHelper
from Core.Web.FacebookGraphAPI.GraphAPI.HTTPRequestTypeEnum import HTTPRequestTypeEnum


class GraphAPIClientBase(GraphAPIGetHelper):
    def __init__(self, business_owner_permanent_token=None, config=None):
        assert business_owner_permanent_token is not None

        self._business_owner_permanent_token = business_owner_permanent_token

        self.config = config

    #  ====== FB API requests using HTTP calls ====== #
    def call_facebook(self):
        if self.config.request.url is None:
            # TODO: Log error
            raise Exception("Missing Fields API url. Please provide an appropriate FB API url and try again.")

        if self.config.verb.lower() == HTTPRequestTypeEnum.GET.value:
            return self._get()
        elif self.config.verb.lower() == HTTPRequestTypeEnum.POST.value:
            return self._post()
        elif self.config.verb.lower() == HTTPRequestTypeEnum.PUT.value:
            return self._put()
        elif self.config.verb.lower() == HTTPRequestTypeEnum.DELETE.value:
            return self._delete()

    def get_page_from_facebook(self, cursor_link=None):
        if self.config.request.url is None:
            # TODO: Log error
            raise Exception('Missing Fields API url. Please provide an appropriate FB API url and try again.')

        if self.config.verb.lower() != HTTPRequestTypeEnum.GET.value:
            raise Exception('Unexpected request verb.')

        return self._get_insights_page(self.config, cursor_link)

    def _get(self):
        if not self.config.async_trials and not self.config.try_partial_requests:
            return self._get_graph_api_base(self.config)

        if self.config.async_trials:
            return self._get_graph_api_base_async(self.config)

        if self.config.try_partial_requests:
            return self._get_partial_graph_api_base(self.config)

    def _post(self):
        try:
            response = self.post(self.config.request.url, self.config.params)
        except Exception as e:
            # TODO: Log error
            raise Exception(e)

        return response

    def _put(self):
        try:
            response = self.put(self.config.request.url, self.config.params)
        except Exception as e:
            # TODO: Log error
            raise Exception(e)

        return response

    def _delete(self):
        if self.config.request.url is None:
            # TODO: Log error
            raise Exception("Missing Fields API url. Please provide an appropriate FB API url and try again.")

        try:
            response = self.delete(self.config.request.url)
        except Exception as e:
            # TODO: Log error
            raise Exception(e)

        return response

    def _check_rate_limits(self):
        # todo: implement
        """Check FB API rate limits. If requests > 75% rate limit, cool down for 5 minutes and start again"""
        pass
