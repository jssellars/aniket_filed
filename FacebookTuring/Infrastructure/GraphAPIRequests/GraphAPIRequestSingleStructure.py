from string import Template

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIRequestBase import GraphAPIRequestBase


class GraphAPIRequestSingleStructure(GraphAPIRequestBase):
    def __init__(self, *args, **kwargs):
        super(GraphAPIRequestSingleStructure, self).__init__(*args, **kwargs)

        self._graph_api_base_url = Template("https://graph.facebook.com/$api_version/$facebook_id").substitute(
            api_version=self._api_version,
            facebook_id=self._facebook_id)
