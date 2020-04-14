import copy
import typing
from collections import OrderedDict
from operator import getitem

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import GraphAPIRequestInsights
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class GraphAPIInsightsHandler:

    __ids_keymap = {
        Level.ACCOUNT.value: {
            "structure": FieldsMetadata.id.field_name,
            "insight": FieldsMetadata.ad_account_id.field_name
        },

        Level.CAMPAIGN.value: {
            "structure": FieldsMetadata.id.field_name,
            "insight": FieldsMetadata.campaign_id.field_name
        },

        Level.ADSET.value: {
            "structure": FieldsMetadata.id.field_name,
            "insight": FieldsMetadata.adset_id.field_name
        },

        Level.AD.value: {
            "structure": FieldsMetadata.id.field_name,
            "insight": FieldsMetadata.ad_id.field_name
        }
    }

    __structure_insights_keymap = {
        Level.ACCOUNT.value: {
            FieldsMetadata.name.field_name: FieldsMetadata.account_name.field_name,
            FieldsMetadata.id.field_name: FieldsMetadata.ad_account_id.field_name
        },

        Level.CAMPAIGN.value: {
            FieldsMetadata.name.field_name: FieldsMetadata.campaign_name.field_name,
            FieldsMetadata.id.field_name: FieldsMetadata.campaign_id.field_name
        },

        Level.ADSET.value: {
            FieldsMetadata.name.field_name: FieldsMetadata.adset_name.field_name,
            FieldsMetadata.id.field_name: FieldsMetadata.adset_id.field_name
        },

        Level.AD.value: {
            FieldsMetadata.name.field_name: FieldsMetadata.ad_name.field_name,
            FieldsMetadata.id.field_name: FieldsMetadata.ad_id.field_name
        }
    }

    __insights_to_structures_level_map = {
        Level.ACCOUNT.value: "accounts",
        Level.CAMPAIGN.value: "campaigns",
        Level.ADSET.value: "adsets",
        Level.AD.value: "ads"
    }

    @classmethod
    def get_insights_base(cls,
                          permanent_token: typing.AnyStr = None,
                          ad_account_id: typing.AnyStr = None,
                          fields: typing.List[typing.AnyStr] = None,
                          parameters: typing.Dict = None,
                          requested_fields: typing.List[FieldsMetadata] = None,
                          add_totals: bool = False) -> typing.Tuple[typing.List[typing.Dict], typing.List[typing.Dict]]:
        graph_api_client = GraphAPIClientBase(permanent_token)
        graph_api_client.config = cls.build_get_insights_config(permanent_token=permanent_token,
                                                                ad_account_id=ad_account_id,
                                                                fields=fields,
                                                                params=parameters,
                                                                add_totals=add_totals)

        try:
            response, summary = graph_api_client.call_facebook()
            insights_response = GraphAPIInsightsMapper().map(requested_fields, response)
            return insights_response, summary
        except Exception as e:
            raise e

    @classmethod
    def get_structures_base(cls,
                            permanent_token: typing.AnyStr = None,
                            ad_account_id: typing.AnyStr = None,
                            level: typing.AnyStr = None,
                            fields: typing.List[typing.AnyStr] = None) -> typing.Tuple[typing.List[typing.Dict], typing.List[typing.Dict]]:
        graph_api_client = GraphAPIClientBase(permanent_token)
        graph_api_client.config = cls.build_get_structure_config(permanent_token=permanent_token,
                                                                 ad_account_id=ad_account_id,
                                                                 level=level,
                                                                 fields=fields)
        try:
            structures_response, summary = graph_api_client.call_facebook()
            return structures_response, summary
        except Exception as e:
            raise e

    @classmethod
    def get_insights(cls,
                     permanent_token: str = None,
                     level: str = None,
                     ad_account_id: str = None,
                     fields: typing.List[typing.AnyStr] = None,
                     parameters: typing.Dict = None,
                     structure_fields: typing.List[typing.AnyStr] = None,
                     requested_fields: typing.List[FieldsMetadata] = None) -> typing.List[typing.Dict]:
        insights_response, _ = cls.get_insights_base(permanent_token=permanent_token,
                                                     ad_account_id=ad_account_id,
                                                     fields=fields,
                                                     parameters=parameters,
                                                     requested_fields=requested_fields)

        if not structure_fields:
            return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=insights_response)
        else:
            structures_response, _ = cls.get_structures_base(permanent_token=permanent_token,
                                                             ad_account_id=ad_account_id,
                                                             level=level,
                                                             fields=structure_fields)
            response = cls.join_insights_and_structures(level=level,
                                                        requested_fields=requested_fields,
                                                        insights=insights_response,
                                                        structures=structures_response)
            return response

    @classmethod
    def get_insights_with_totals(cls,
                                 permanent_token: typing.AnyStr = None,
                                 level: typing.AnyStr = None,
                                 ad_account_id: typing.AnyStr = None,
                                 fields: typing.List[typing.AnyStr] = None,
                                 parameters: typing.Dict = None,
                                 structure_fields: typing.List[typing.AnyStr] = None,
                                 requested_fields: typing.List[FieldsMetadata] = None) -> typing.Dict:
        # get data with breakdowns
        insights, summary = cls.get_insights_base(permanent_token=permanent_token,
                                                  ad_account_id=ad_account_id,
                                                  fields=fields,
                                                  parameters=parameters,
                                                  requested_fields=requested_fields,
                                                  add_totals=True)

        if parameters["breakdowns"]:
            # get data without breakdowns
            parameters_without_breakdowns = copy.deepcopy(parameters)
            del parameters_without_breakdowns["action_breakdowns"]
            del parameters_without_breakdowns["breakdowns"]
            insights_without_breakdowns, _ = cls.get_insights_base(permanent_token=permanent_token,
                                                                   ad_account_id=ad_account_id,
                                                                   fields=fields,
                                                                   parameters=parameters_without_breakdowns,
                                                                   requested_fields=requested_fields)
        else:
            insights_without_breakdowns = []

        # Combine insights without breakdowns with insights with breakdowns
        combined_insights = cls.join_insights(insights=insights, insights_without_breakdowns=insights_without_breakdowns)

        # Get structure information
        if not structure_fields:
            return {"data": cls.map_to_requested_fields(level=level,
                                                        requested_fields=requested_fields,
                                                        response=combined_insights),
                    "summary": summary}
        else:
            structures_response, _ = cls.get_structures_base(permanent_token=permanent_token,
                                                             ad_account_id=ad_account_id,
                                                             level=level,
                                                             fields=structure_fields)
            response = cls.join_insights_and_structures(level=level,
                                                        requested_fields=requested_fields,
                                                        insights=combined_insights,
                                                        structures=structures_response)
            return {"data": response, "summary": summary}

    @classmethod
    def join_insights(cls,
                      insights: typing.List[typing.Dict] = None,
                      insights_without_breakdowns: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        return insights + insights_without_breakdowns

    @classmethod
    def join_insights_and_structures(cls,
                                     level: typing.AnyStr = None,
                                     requested_fields: typing.List[FieldsMetadata] = None,
                                     insights: typing.List[typing.Dict] = None,
                                     structures: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        structure_id_key = cls.__ids_keymap[level]["structure"]
        insight_id_key = cls.__ids_keymap[level]["insight"]

        if not structures and not insights:
            return []
        elif structures and not insights:
            response = cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=structures)
        elif not structures and insights:
            response = cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=insights)
        else:
            requested_fields_names = [field.name for field in requested_fields]
            response = [{**insight, **structure}
                        for structure in structures
                        for insight in list(filter(lambda x: getitem(x, insight_id_key) == getitem(structure, structure_id_key), insights))] + \
                       [{**dict.fromkeys(requested_fields_names), **structure}
                        for structure in structures
                        if not list(filter(lambda x: getitem(x, insight_id_key) == getitem(structure, structure_id_key), insights))]

        return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=response)

    @classmethod
    def map_to_requested_fields(cls,
                                level: typing.AnyStr = None,
                                requested_fields: typing.List[FieldsMetadata] = None,
                                response: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        sorted_fields = sorted([field.name for field in requested_fields])

        def f(entry):
            sorted_response = {**OrderedDict.fromkeys(sorted_fields), **OrderedDict(sorted(entry.items()))}
            for structure_key, insight_key in cls.__structure_insights_keymap[level].items():
                if sorted_response.get(structure_key):
                    sorted_response[insight_key] = sorted_response.pop(structure_key)

            return sorted_response

        return list(map(f, response))

    @classmethod
    def build_get_structure_config(cls,
                                   permanent_token: typing.AnyStr = None,
                                   level: typing.AnyStr = None,
                                   ad_account_id: typing.AnyStr = None,
                                   fields: typing.List[typing.AnyStr] = None) -> GraphAPIClientBaseConfig:
        get_structure_config = GraphAPIClientBaseConfig()
        get_structure_config.try_partial_requests = True
        get_structure_config.required_field = cls.__ids_keymap[level]["structure"]
        get_structure_config.fields = fields
        get_structure_config.request = GraphAPIRequestStructures(facebook_id=ad_account_id,
                                                                 business_owner_permanent_token=permanent_token,
                                                                 level=cls.__insights_to_structures_level_map[level],
                                                                 fields=fields)

        return get_structure_config

    @classmethod
    def build_get_insights_config(cls,
                                  permanent_token: typing.AnyStr = None,
                                  ad_account_id: typing.AnyStr = None,
                                  fields: typing.List[typing.AnyStr] = None,
                                  params: typing.Dict = None,
                                  add_totals: bool = False) -> GraphAPIClientBaseConfig:
        params["default_summary"] = add_totals

        get_insights_config = GraphAPIClientBaseConfig()
        get_insights_config.try_partial_requests = True
        get_insights_config.required_field = cls.__ids_keymap[params["level"]]["insight"]
        get_insights_config.fields = fields
        get_insights_config.params = params
        get_insights_config.request = GraphAPIRequestInsights(facebook_id=ad_account_id,
                                                              business_owner_permanent_token=permanent_token,
                                                              fields=fields,
                                                              params=params)

        return get_insights_config
