from string import Template

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIRequestBase import GraphAPIRequestBase


class GraphAPIRequestInsights(GraphAPIRequestBase):
    def __init__(self, **kwargs):
        super(GraphAPIRequestInsights, self).__init__(**kwargs)

        self._graph_api_base_url = Template("https://graph.facebook.com/$api_version/$facebook_id/insights").substitute(api_version=self._api_version,
                                                                                                                        facebook_id='$facebook_id')
