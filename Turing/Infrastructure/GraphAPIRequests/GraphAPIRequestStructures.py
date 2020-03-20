from string import Template

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIRequestBase import GraphAPIRequestBase


class GraphAPIRequestStructures(GraphAPIRequestBase):
    def __init__(self, level, *args, **kwargs):
        super(GraphAPIRequestStructures, self).__init__(*args, **kwargs)

        self._graph_api_base_url = Template("https://graph.facebook.com/$api_version/$facebook_id/$level").substitute(api_version=self._api_version,
                                                                                                                      facebook_id=self._facebook_id,
                                                                                                                      level=level)
