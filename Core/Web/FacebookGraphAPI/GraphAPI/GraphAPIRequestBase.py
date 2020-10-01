import json
from string import Template


class GraphAPIRequestBase:
    _limit = 25
    _api_version = "v7.0"

    def __init__(self, facebook_id=None, business_owner_permanent_token=None, fields=None, params=None,
                 filter_params=None, api_version=None, limit=None):
        self._facebook_id = facebook_id
        self.business_owner_permanent_token = business_owner_permanent_token
        self._fields = fields
        self._params = params
        self._filter = filter_params

        self._graph_api_base_url = ""

        if api_version is not None:
            self._api_version = api_version

        if limit is not None:
            self._limit = limit

        self._url = None

    @property
    def url(self):
        return self._build_graph_api_request_url()

    @url.setter
    def url(self, value):
        self._url = value

    @url.deleter
    def url(self):
        del self._url

    def _build_graph_api_request_url(self):
        graph_api_request = self._graph_api_base_url

        # Build fields part of the FB Graph API request
        if self._fields:
            graph_api_request += "?fields={fields}".format(fields=",".join(self._fields))

        # Build params part of the FB Graph API request
        if self._params:
            for key, value in self._params.items():
                if isinstance(value, list) or isinstance(value, dict):
                    graph_api_request += "&{key}={value}".format(key=key, value=json.dumps(value))
                else:
                    graph_api_request += "&{key}={value}".format(key=key, value=value)

        # Build filtering part of the FB Graph API request
        if self._filter:
            graph_api_request += "&filtering={value}".format(value=self._filter)

        #  Combine request components
        graph_api_request_other_params = Template(
            "&access_token=$business_owner_permanent_facebook_token&limit=$limit").safe_substitute(limit=self._limit,
                                                                                                   business_owner_permanent_facebook_token=self.business_owner_permanent_token)
        graph_api_request += graph_api_request_other_params

        # Try to replace facebook_id ( if required in the Fields Graph API URL )
        graph_api_request = Template(graph_api_request)
        graph_api_request_url = graph_api_request.safe_substitute(facebook_id=self._facebook_id)

        return graph_api_request_url

    def modify_fields_and_params(self, fields=None, params=None):
        self._fields = fields
        self._params = params
        self._url = self._build_graph_api_request_url()
