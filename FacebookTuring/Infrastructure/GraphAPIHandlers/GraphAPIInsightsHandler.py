import copy
import typing
from collections import OrderedDict
from operator import getitem
from queue import Queue
from threading import Thread
from time import sleep

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Startup import startup
from FacebookTuring.Infrastructure.Domain.BudgetMessageEnum import BudgetMessageEnum
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import GraphAPIRequestInsights
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository


class GraphAPIInsightsHandler:
    __logger = None

    __ids_keymap = {
        Level.ACCOUNT.value: {
            "structure": FieldsMetadata.id.name,
            "insight": FieldsMetadata.account_name.name
        },

        Level.CAMPAIGN.value: {
            "structure": FieldsMetadata.id.name,
            "insight": FieldsMetadata.campaign_id.name
        },

        Level.ADSET.value: {
            "structure": FieldsMetadata.id.name,
            "insight": FieldsMetadata.adset_id.name
        },

        Level.AD.value: {
            "structure": FieldsMetadata.id.name,
            "insight": FieldsMetadata.ad_id.name
        }
    }

    __structure_insights_keymap = {
        Level.ACCOUNT.value: {
            FieldsMetadata.name.name: FieldsMetadata.account_name.name,
            FieldsMetadata.id.name: FieldsMetadata.account_name.name
        },

        Level.CAMPAIGN.value: {
            FieldsMetadata.name.name: FieldsMetadata.campaign_name.name,
            FieldsMetadata.id.name: FieldsMetadata.campaign_id.name,
            FieldsMetadata.budget.name: [FieldsMetadata.daily_budget.name, FieldsMetadata.lifetime_budget.name,
                                         BudgetMessageEnum.NO_CAMPAIGN_BUDGET.value]
        },

        Level.ADSET.value: {
            FieldsMetadata.name.name: FieldsMetadata.adset_name.name,
            FieldsMetadata.id.name: FieldsMetadata.adset_id.name,
            FieldsMetadata.budget.name: [FieldsMetadata.daily_budget.name, FieldsMetadata.lifetime_budget.name,
                                         BudgetMessageEnum.NO_ADSET_BUDGET.value]
        },

        Level.AD.value: {
            FieldsMetadata.name.name: FieldsMetadata.ad_name.name,
            FieldsMetadata.id.name: FieldsMetadata.ad_id.name
        }
    }

    __insights_to_structures_level_map = {
        Level.ACCOUNT.value: "accounts",
        Level.CAMPAIGN.value: "campaigns",
        Level.ADSET.value: "adsets",
        Level.AD.value: "ads"
    }

    @classmethod
    def set_logger(cls, logger):
        cls.__logger = logger
        return cls

    @classmethod
    def get_insights_base(cls,
                          permanent_token: typing.AnyStr = None,
                          ad_account_id: typing.AnyStr = None,
                          fields: typing.List[typing.AnyStr] = None,
                          parameters: typing.Dict = None,
                          requested_fields: typing.List[FieldsMetadata] = None,
                          add_totals: bool = False,
                          thread: typing.Union[typing.AnyStr, int] = None) -> typing.Dict:
        graph_api_client = GraphAPIClientBase(permanent_token)
        graph_api_client.config = cls.build_get_insights_config(permanent_token=permanent_token,
                                                                ad_account_id=ad_account_id,
                                                                fields=fields,
                                                                params=parameters,
                                                                add_totals=add_totals)

        try:
            response, summary = graph_api_client.call_facebook()
            insights_response = GraphAPIInsightsMapper().map(requested_fields, response) if response else []
            summary_response = GraphAPIInsightsMapper().map(requested_fields, [summary]) if summary else []

            # Warning: These mappings might need to be reactivated after extensive testing
            # It looks like it messes up the order of the items in the response
            # insights_response = list(map(dict, set(tuple(x.items()) for x in insights_response)))
            # summary_response = list(map(dict, set(tuple(x.items()) for x in summary_response)))

            return copy.deepcopy({thread: (insights_response, summary_response)})
        except Exception as e:
            raise e

    @classmethod
    def get_structures_base(cls,
                            permanent_token: typing.AnyStr = None,
                            ad_account_id: typing.AnyStr = None,
                            level: typing.AnyStr = None,
                            fields: typing.List[typing.AnyStr] = None,
                            filter_params: typing.List[typing.Dict] = None,
                            structure_fields: typing.List[FieldsMetadata] = None,
                            thread: typing.Union[typing.AnyStr, int] = None) -> typing.Dict:
        graph_api_client = GraphAPIClientBase(permanent_token)
        graph_api_client.config = cls.build_get_structure_config(permanent_token=permanent_token,
                                                                 ad_account_id=ad_account_id,
                                                                 level=level,
                                                                 fields=fields,
                                                                 filter_params=filter_params)
        try:
            # structures_response, summary = graph_api_client.call_facebook()
            repository = TuringMongoRepository(config=startup.mongo_config,
                                               database_name=startup.mongo_config.structures_database_name,
                                               logger=cls.__logger)
            summary = []
            account_id = ad_account_id.split("_")[1]
            structures = repository.get_all_structures_by_ad_account_id(level=Level(level), account_id=account_id)
            structures_response = GraphAPIInsightsMapper().map(structure_fields, structures)
            structures_response = list(map(dict, set(tuple(x.items()) for x in structures_response)))
            return copy.deepcopy({thread: (structures_response, summary)})
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
                     requested_fields: typing.List[FieldsMetadata] = None,
                     filter_params: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        insights_thread = 0
        structure_thread = 1
        queue = Queue()

        def _get_insights(cls,
                          permanent_token: str = None,
                          level: str = None,
                          ad_account_id: str = None,
                          fields: typing.List[typing.AnyStr] = None,
                          parameters: typing.Dict = None,
                          structure_fields: typing.List[typing.AnyStr] = None,
                          requested_fields: typing.List[FieldsMetadata] = None,
                          filter_params: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
            # get insights
            t1 = Thread(
                target=lambda q, arg1, arg2, arg3, arg4, arg5, arg6: q.put(cls.get_insights_base(
                    permanent_token=arg1,
                    ad_account_id=arg2,
                    fields=arg3,
                    parameters=arg4,
                    requested_fields=arg5,
                    thread=arg6)),
                args=(queue, permanent_token, ad_account_id, fields, parameters, requested_fields, insights_thread))
            t1.start()

            # get structures
            requested_structure_fields = [getattr(FieldsMetadata, entry) for entry in structure_fields]
            t2 = Thread(target=lambda q, arg1, arg2, arg3, arg4, arg5, arg6, arg7: q.put(cls.get_structures_base(
                permanent_token=arg1,
                ad_account_id=arg2,
                level=arg3,
                fields=arg4,
                filter_params=arg5,
                structure_fields=arg6,
                thread=arg7)),
                        args=(queue, permanent_token, ad_account_id, level, structure_fields, filter_params,
                              requested_structure_fields, structure_thread))
            t2.start()

            #  get responses
            responses = []
            while not len(queue.queue) == 2:
                sleep(1)
            else:
                responses += [element for element in queue.queue]
            return responses

        responses = _get_insights(cls=cls,
                                  permanent_token=permanent_token,
                                  level=level,
                                  ad_account_id=ad_account_id,
                                  fields=fields,
                                  parameters=parameters,
                                  structure_fields=structure_fields,
                                  requested_fields=requested_fields,
                                  filter_params=filter_params)

        #  combine responses
        insights = next(filter(lambda x: insights_thread in x.keys(), responses), None)
        structures = next(filter(lambda x: structure_thread in x.keys(), responses), None)

        response = cls.join_insights_and_structures(level=level,
                                                    requested_fields=requested_fields,
                                                    insights=insights[insights_thread][0],
                                                    structures=structures[structure_thread][0])
        return response

    @classmethod
    def get_insights_with_totals(cls,
                                 permanent_token: typing.AnyStr = None,
                                 level: typing.AnyStr = None,
                                 ad_account_id: typing.AnyStr = None,
                                 fields: typing.List[typing.AnyStr] = None,
                                 parameters: typing.Dict = None,
                                 structure_fields: typing.List[typing.AnyStr] = None,
                                 requested_fields: typing.List[FieldsMetadata] = None,
                                 filter_params: typing.List[typing.Dict] = None) -> typing.Dict:
        insights_thread = 0
        insights_without_breakdowns_thread = 1
        structure_thread = 2

        queue = Queue()

        def _get_insights(cls,
                          permanent_token: typing.AnyStr = None,
                          level: typing.AnyStr = None,
                          ad_account_id: typing.AnyStr = None,
                          fields: typing.List[typing.AnyStr] = None,
                          parameters: typing.Dict = None,
                          structure_fields: typing.List[typing.AnyStr] = None,
                          requested_fields: typing.List[FieldsMetadata] = None,
                          filter_params: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
            # get insights
            t1 = Thread(
                target=lambda q, arg1, arg2, arg3, arg4, arg5, arg6, arg7: q.put(cls.get_insights_base(
                    permanent_token=arg1,
                    ad_account_id=arg2,
                    fields=arg3,
                    parameters=arg4,
                    requested_fields=arg5,
                    thread=arg6,
                    add_totals=arg7)),
                args=(queue, permanent_token, ad_account_id, fields,
                      parameters, requested_fields, insights_thread, True))
            t1.start()

            # get structures
            requested_structure_fields = [getattr(FieldsMetadata, entry) for entry in structure_fields]
            t2 = Thread(target=lambda q, arg1, arg2, arg3, arg4, arg5, arg6, arg7: q.put(cls.get_structures_base(
                permanent_token=arg1,
                ad_account_id=arg2,
                level=arg3,
                fields=arg4,
                filter_params=arg5,
                structure_fields=arg6,
                thread=arg7)),
                        args=(queue, permanent_token, ad_account_id, level, structure_fields, filter_params,
                              requested_structure_fields, structure_thread))
            t2.start()

            # get insights without breakdowns
            t3 = None
            if parameters["breakdowns"]:
                # get data without breakdowns
                parameters_without_breakdowns = copy.deepcopy(parameters)
                del parameters_without_breakdowns["action_breakdowns"]
                del parameters_without_breakdowns["breakdowns"]
                requested_fields_without_breakdowns = [field for field in requested_fields
                                                       if field.field_type != FieldType.BREAKDOWN]
                t3 = Thread(
                    target=lambda q, arg1, arg2, arg3, arg4, arg5, arg6: q.put(cls.get_insights_base(
                        permanent_token=arg1,
                        ad_account_id=arg2,
                        fields=arg3,
                        parameters=arg4,
                        requested_fields=arg5,
                        thread=arg6)),
                    args=(
                        queue, permanent_token, ad_account_id, fields, parameters_without_breakdowns,
                        requested_fields_without_breakdowns, insights_without_breakdowns_thread))
                t3.start()

            t1.join()
            t2.join()
            if t3:
                t3.join()

            #  get responses
            responses = []
            if queue.not_empty:
                responses = [element for element in queue.queue]
            return responses

        responses = _get_insights(cls=cls,
                                  permanent_token=permanent_token,
                                  level=level,
                                  ad_account_id=ad_account_id,
                                  fields=fields,
                                  parameters=parameters,
                                  structure_fields=structure_fields,
                                  requested_fields=requested_fields,
                                  filter_params=filter_params)

        #  combine responses
        insights_response = next(filter(lambda x: insights_thread in x.keys(), responses), None)
        insights = insights_response[insights_thread][0]
        summary = insights_response[insights_thread][1]

        insights_without_breakdowns_response = next(filter(lambda x: insights_without_breakdowns_thread in x.keys(),
                                                           responses), None)
        if insights_without_breakdowns_response:
            insights_without_breakdowns = insights_without_breakdowns_response[insights_without_breakdowns_thread][0]
        else:
            insights_without_breakdowns = []

        structures_response = next(filter(lambda x: structure_thread in x.keys(), responses), None)
        structures = structures_response[structure_thread][0]

        # Combine insights without breakdowns with insights with breakdowns
        if insights_without_breakdowns:
            insights = insights + insights_without_breakdowns

        response = cls.join_insights_and_structures(level=level,
                                                    requested_fields=requested_fields,
                                                    insights=insights,
                                                    structures=structures)
        return {"data": response, "summary": summary}

    @classmethod
    def get_reports_insights(cls,
                             permanent_token: str = None,
                             ad_account_id: str = None,
                             fields: typing.List[typing.AnyStr] = None,
                             parameters: typing.Dict = None,
                             requested_fields: typing.List[FieldsMetadata] = None) -> typing.List[typing.Dict]:
        report_insights_thread = 1
        insights_response = cls.get_insights_base(permanent_token=permanent_token,
                                                  ad_account_id=ad_account_id,
                                                  fields=fields,
                                                  parameters=parameters,
                                                  requested_fields=requested_fields,
                                                  thread=report_insights_thread)
        return insights_response[report_insights_thread][0]

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
            return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=structures)
        elif not structures and insights:
            return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=insights)
        else:
            requested_fields_names = [field.name for field in requested_fields]
            active_structures = [{**insight, **structure}
                                 for structure in structures
                                 for insight in list(
                    filter(lambda x: getitem(x, insight_id_key) == str(getitem(structure, structure_id_key)),
                           insights))]
            empty_structure_dict = dict.fromkeys(requested_fields_names)
            inactive_structures = [{**empty_structure_dict, **structure}
                                   for structure in structures
                                   if not list(
                    filter(lambda x: getitem(x, insight_id_key) == str(getitem(structure, structure_id_key)),
                           insights))]
            response = active_structures + inactive_structures

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
                if isinstance(insight_key, list):
                    found = False
                    underscore = '_'
                    for key in insight_key:
                        if sorted_response.get(key) is not None and sorted_response.get(key) != 0:
                            value = sorted_response.pop(key)
                            if structure_key == FieldsMetadata.budget.name:
                                value = value / 100
                            answer = f'{value}({key.split(underscore)[0]})'
                            sorted_response[structure_key] = answer
                            found = True
                            break
                    if not found:
                        sorted_response[structure_key] = insight_key[-1]
                else:
                    sorted_response[insight_key] = sorted_response.pop(structure_key, None)

            return sorted_response

        return list(map(f, response))

    @classmethod
    def build_get_structure_config(cls,
                                   permanent_token: typing.AnyStr = None,
                                   level: typing.AnyStr = None,
                                   ad_account_id: typing.AnyStr = None,
                                   fields: typing.List[typing.AnyStr] = None,
                                   filter_params: typing.List[typing.Dict] = None) -> GraphAPIClientBaseConfig:
        get_structure_config = GraphAPIClientBaseConfig()
        get_structure_config.try_partial_requests = True
        get_structure_config.required_field = cls.__ids_keymap[level]["structure"]
        get_structure_config.fields = fields
        get_structure_config.request = GraphAPIRequestStructures(facebook_id=ad_account_id,
                                                                 business_owner_permanent_token=permanent_token,
                                                                 level=cls.__insights_to_structures_level_map[level],
                                                                 fields=fields,
                                                                 filter_params=filter_params)

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
