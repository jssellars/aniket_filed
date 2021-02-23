import copy
import itertools
import json
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union

from Core import mongo_adapter
from Core.settings_models import Model
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import (
    create_facebook_filter,
    get_next_page_cursor,
    get_sdk_insights_page,
    get_sdk_structures,
)
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    FacebookLevelPlural,
    Level,
    LevelToFacebookIdKeyMapping,
)
from Core.Web.FacebookGraphAPI.Models.Field import Field as FacebookField
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from FacebookTuring.Infrastructure.Domain.BudgetMessageEnum import BudgetMessageEnum
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import GraphAPIRequestInsights
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.Mappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

PAGE_SIZE = 200


class GraphAPIInsightsHandler:
    __ids_keymap = {
        Level.ACCOUNT.value: {"structure": FieldsMetadata.id.name, "insight": FieldsMetadata.account_name.name},
        Level.CAMPAIGN.value: {"structure": FieldsMetadata.id.name, "insight": FieldsMetadata.campaign_id.name},
        Level.ADSET.value: {"structure": FieldsMetadata.id.name, "insight": FieldsMetadata.adset_id.name},
        Level.AD.value: {"structure": FieldsMetadata.id.name, "insight": FieldsMetadata.ad_id.name},
    }

    __structure_insights_keymap = {
        Level.ACCOUNT.value: {
            FieldsMetadata.name.name: FieldsMetadata.account_name.name,
            FieldsMetadata.id.name: FieldsMetadata.account_name.name,
        },
        Level.CAMPAIGN.value: {
            FieldsMetadata.name.name: FieldsMetadata.campaign_name.name,
            FieldsMetadata.id.name: FieldsMetadata.campaign_id.name,
            FieldsMetadata.budget.name: [
                FieldsMetadata.daily_budget.name,
                FieldsMetadata.lifetime_budget.name,
                BudgetMessageEnum.NO_CAMPAIGN_BUDGET.value,
            ],
        },
        Level.ADSET.value: {
            FieldsMetadata.name.name: FieldsMetadata.adset_name.name,
            FieldsMetadata.id.name: FieldsMetadata.adset_id.name,
            FieldsMetadata.budget.name: [
                FieldsMetadata.daily_budget.name,
                FieldsMetadata.lifetime_budget.name,
                BudgetMessageEnum.NO_ADSET_BUDGET.value,
            ],
        },
        Level.AD.value: {
            FieldsMetadata.name.name: FieldsMetadata.ad_name.name,
            FieldsMetadata.id.name: FieldsMetadata.ad_id.name,
        },
    }

    __insights_to_structures_level_map = {
        Level.ACCOUNT.value: "accounts",
        Level.CAMPAIGN.value: "campaigns",
        Level.ADSET.value: "adsets",
        Level.AD.value: "ads",
    }

    @classmethod
    def process_async_report(
            cls,
            ad_report_run: AdReportRun,
            ad_account_id: str,
            requested_fields: List[FieldsMetadata],
            mongo_repository: TuringMongoRepository,
            level: Optional[str] = None,
    ):

        insights = ad_report_run.get_insights()
        if not insights:
            return {}

        results_requested = any(
            [
                FieldsMetadata.results.name == x.name or FieldsMetadata.cost_per_result.name == x.name
                for x in requested_fields
            ]
        )

        insights_slice = []
        for insight in insights:
            insights_slice.append(insight.export_all_data())

            if len(insights_slice) == PAGE_SIZE:
                cls.insert_insights_into_db(
                    results_requested,
                    level,
                    insights_slice,
                    ad_account_id,
                    requested_fields,
                    mongo_repository,
                )
                insights_slice = []

        cls.insert_insights_into_db(
            results_requested,
            level,
            insights_slice,
            ad_account_id,
            requested_fields,
            mongo_repository,
        )

        return

    @classmethod
    def insert_insights_into_db(
            cls,
            results_requested: bool,
            level: str,
            insights_data: List[Dict],
            ad_account_id: str,
            requested_fields: List[FieldsMetadata],
            mongo_repository: TuringMongoRepository,
    ):

        if results_requested:
            cls.add_results_to_response(level, insights_data, ad_account_id)
        insights_response = (
            GraphAPIInsightsMapper().map(requested_fields=requested_fields, response=insights_data)
            if insights_data
            else []
        )

        response = mongo_adapter.filter_null_values_from_documents(insights_response)
        mongo_repository.add_many(response)

    @classmethod
    def get_insights_base(
            cls,
            permanent_token: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            parameters: Dict = None,
            requested_fields: List[FieldsMetadata] = None,
            add_totals: bool = False,
            thread: Union[str, int] = None,
            level: str = None,
    ) -> Dict:

        try:
            graph_api_client = GraphAPIClientBase(permanent_token)
            graph_api_client.config = cls.build_get_insights_config(
                permanent_token=permanent_token,
                ad_account_id=ad_account_id,
                fields=fields,
                params=parameters,
                add_totals=add_totals,
            )
            ad_account = AdAccount(ad_account_id)
            insights = ad_account.get_insights(fields=fields, params=parameters)

            if not insights:
                return {}

            summary = insights.summary() if parameters["default_summary"] else None

            results_requested = any(
                [
                    FieldsMetadata.results.name == x.name or FieldsMetadata.cost_per_result.name == x.name
                    for x in requested_fields
                ]
            )

            insights_data = []
            for insight in insights:
                insights_data.append(insight.export_all_data())
                insights.params = parameters

            if results_requested:
                cls.add_results_to_response(level, insights_data, ad_account_id)
            insights_response = (
                GraphAPIInsightsMapper().map(requested_fields=requested_fields, response=insights_data)
                if insights_data
                else []
            )
            summary_response = (
                GraphAPIInsightsMapper().map(requested_fields, [json.loads(summary[10:])]) if summary else []
            )

            # Warning: These mappings might need to be reactivated after extensive testing
            # It looks like it messes up the order of the items in the response
            # insights_response = list(map(dict, set(tuple(x.items()) for x in insights_response)))
            # summary_response = list(map(dict, set(tuple(x.items()) for x in summary_response)))

            return copy.deepcopy({thread: (insights_response, summary_response)})
        except Exception as e:
            raise e

    @classmethod
    def get_insights_page(
            cls,
            config,
            ad_account_id: str = None,
            fields: List[str] = None,
            parameters: Dict = None,
            requested_fields: List[FieldsMetadata] = None,
            level: str = None,
    ) -> Tuple:

        try:
            response, next_page_cursor, summary = get_sdk_insights_page(
                ad_account_id, fields, parameters, Level[level.upper()]
            )
            results_requested = any(
                [
                    FieldsMetadata.results.name == x.name or FieldsMetadata.cost_per_result.name == x.name
                    for x in requested_fields
                ]
            )
            if results_requested:
                cls.add_results_to_response(level, response, ad_account_id)
            insights_response = GraphAPIInsightsMapper().map(requested_fields, response) if response else []
            summary_response = GraphAPIInsightsMapper().map(requested_fields, [summary]) if summary else []

            # Warning: These mappings might need to be reactivated after extensive testing
            # It looks like it messes up the order of the items in the response
            # insights_response = list(map(dict, set(tuple(x.items()) for x in insights_response)))
            # summary_response = list(map(dict, set(tuple(x.items()) for x in summary_response)))

            return insights_response, next_page_cursor, summary_response
        except Exception as e:
            raise e

    @classmethod
    def get_structures_for_insights(
            cls,
            ad_account_id: str,
            level: str,
            insight_ids: List[str],
            structure_fields: List[FacebookField],
    ) -> List:
        try:

            facebook_structure_fields = [structure_field.facebook_fields for structure_field in structure_fields]
            facebook_structure_fields = list(itertools.chain(*facebook_structure_fields))

            facebook_structure_key = LevelToFacebookIdKeyMapping[level.upper()].value.replace("_", ".")

            structures_filter = {
                "filtering": [create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, insight_ids)]
            }
            structures = get_sdk_structures(
                ad_account_id, Level[level.upper()], facebook_structure_fields, structures_filter
            )

            structures_response = GraphAPIInsightsMapper().map(structure_fields, structures)
            structures_response = list(map(dict, set(tuple(x.items()) for x in structures_response)))
            return structures_response
        except Exception as e:
            raise e

    @classmethod
    def __join_insights_and_structure_results(
            cls,
            structure_key: str = None,
            insight_response: List = None,
            structure_results: List = None,
    ) -> List:
        for insight in insight_response:
            possible_objective = []
            for structure in structure_results:
                if insight[structure_key] == structure[structure_key]:
                    if (
                            GraphAPIInsightsFields.custom_event_type in structure
                            and structure[GraphAPIInsightsFields.custom_event_type]
                    ):
                        if structure[GraphAPIInsightsFields.custom_event_type] not in possible_objective:
                            possible_objective.append(structure[GraphAPIInsightsFields.custom_event_type])
                    elif (
                            GraphAPIInsightsFields.optimization_goal in structure
                            and structure[GraphAPIInsightsFields.optimization_goal]
                    ):
                        if structure[GraphAPIInsightsFields.optimization_goal] not in possible_objective:
                            possible_objective.append(structure[GraphAPIInsightsFields.optimization_goal])
                    if len(possible_objective) > 1:
                        insight.update({FieldsMetadata.result_type.name: "multiple_conversion_types"})
                        break
                    insight.update(structure)
        return insight_response

    @classmethod
    def get_structures_base(
            cls,
            config,
            permanent_token: str = None,
            ad_account_id: str = None,
            level: str = None,
            fields: List[str] = None,
            filter_params: List[Dict] = None,
            structure_fields: List[FieldsMetadata] = None,
            thread: Union[str, int] = None,
    ) -> Dict:
        graph_api_client = GraphAPIClientBase(permanent_token)
        graph_api_client.config = cls.build_get_structure_config(
            permanent_token=permanent_token,
            ad_account_id=ad_account_id,
            level=level,
            fields=fields,
            filter_params=filter_params,
        )
        try:
            # structures_response, summary = graph_api_client.call_facebook()
            repository = TuringMongoRepository(
                config=config.mongo,
                database_name=config.mongo.structures_database_name,
            )
            summary = []
            account_id = ad_account_id.split("_")[1]
            structures = repository.get_all_structures_by_ad_account_id(level=Level(level), account_id=account_id)
            structures_response = GraphAPIInsightsMapper().map(structure_fields, structures)
            structures_response = list(map(dict, set(tuple(x.items()) for x in structures_response)))
            return copy.deepcopy({thread: (structures_response, summary)})
        except Exception as e:
            raise e

    @classmethod
    def get_structures_page(
            cls,
            config,
            ad_account_id: str,
            structure_fields: List[FieldsMetadata],
            level: str,
            parameter: Dict = None,
            start_row: int = 0,
            end_row: int = 200,
    ) -> List:
        try:
            repository = TuringMongoRepository(
                config=config.mongo,
                database_name=config.mongo.structures_database_name,
            )
            if parameter["value"]:
                structure_ids = parameter["value"]
            else:
                structure_ids = None
            structure_key = parameter["field"].replace(".", "_")
            if structure_key not in [enum.value for enum in LevelToFacebookIdKeyMapping]:
                return []
            structures = repository.get_ad_account_slice(
                level=Level(level),
                account_id=ad_account_id,
                structure_key=structure_key,
                structure_ids=structure_ids,
                start_row=start_row,
                end_row=end_row,
            )
            structures_response = GraphAPIInsightsMapper().map(structure_fields, structures)
            structures_response = list(map(dict, set(tuple(x.items()) for x in structures_response)))
            return structures_response

        except Exception as e:
            raise e

    @classmethod
    def add_results_to_response(cls, level: str, response: List, account_id: str):
        if not response:
            return

        structure_key = ""
        if level == Level.CAMPAIGN.value or level == Level.ADSET.value:
            structure_key = LevelToFacebookIdKeyMapping.get_enum_by_name(level.upper()).value
        elif level == Level.AD.value:
            structure_key = LevelToFacebookIdKeyMapping.get_enum_by_name(Level.ADSET.value.upper()).value
        structure_ids = list({x[structure_key] for x in response if structure_key in x})

        params = {
            "filtering": [
                json.dumps(
                    create_facebook_filter(structure_key.replace("_", "."), AgGridFacebookOperator.IN, structure_ids)
                )
            ]
        }
        fields = [GraphAPIInsightsFields.promoted_object, structure_key, GraphAPIInsightsFields.optimization_goal]
        structure_results = AdAccount(account_id).get_ad_sets(fields=fields, params=params)

        mapped_structures = []
        for structure in structure_results:
            structure[structure_key] = structure.pop("id")

            promoted_event = structure.pop(GraphAPIInsightsFields.promoted_object, None)
            if promoted_event:
                if "pixel_id" in promoted_event:
                    structure[GraphAPIInsightsFields.custom_event_type] = promoted_event.get(
                        GraphAPIInsightsFields.custom_event_type, None
                    )
            mapped_structures.append(structure)

        cls.__join_insights_and_structure_results(
            structure_key=structure_key, insight_response=response, structure_results=mapped_structures
        )

    @classmethod
    def get_ag_grid_insights(
            cls,
            config,
            permanent_token: str = None,
            level: str = None,
            query: QueryBuilderFacebookRequestParser = None,
    ) -> Dict:

        _ = GraphAPISdkBase(config.facebook, permanent_token)

        ad_account_id = query.facebook_id
        fields = query.fields
        parameters = query.parameters
        structure_fields = query.structure_fields
        requested_fields = query.requested_columns
        next_page_cursor = query.next_page_cursor
        page_size = query.page_size
        has_delivery = query.has_delivery

        if has_delivery:
            insights, structures, next_page_cursor, summary = cls._get_insights_master_data(
                config,
                level=level,
                ad_account_id=ad_account_id,
                fields=fields,
                parameters=parameters,
                structure_fields=structure_fields,
                requested_fields=requested_fields,
            )

            response = cls.left_join_insights_and_structures(
                level=level,
                requested_fields=requested_fields,
                insights=insights,
                structures=structures,
                structure_fields=structure_fields,
            )

            return {"nextPageCursor": next_page_cursor, "data": response, "summary": summary}

        insights, structures, next_page_cursor, summary = cls._get_structure_master_data(
            config,
            level=level,
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            structure_fields=structure_fields,
            requested_fields=requested_fields,
            page_size=page_size,
            next_page_cursor=next_page_cursor,
        )

        response = cls.right_join_insights_and_structures(
            level=level,
            requested_fields=requested_fields,
            insights=insights,
            structures=structures,
        )

        return {"nextPageCursor": next_page_cursor, "data": response, "summary": summary}

    @classmethod
    def _get_insights_master_data(
            cls,
            config,
            level: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            parameters: Dict = None,
            structure_fields: List[str] = None,
            requested_fields: List[FieldsMetadata] = None,
    ) -> Tuple:

        insight_response, next_page_cursor, summary = cls.get_insights_page(
            config,
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            level=level,
        )

        structure_key = LevelToFacebookIdKeyMapping[level.upper()].value
        insight_ids = [x[structure_key] for x in insight_response if structure_key in x]

        # get structures
        requested_structure_fields = [
            getattr(FieldsMetadata, entry) for entry in structure_fields if hasattr(FieldsMetadata, entry)
        ]
        structures_response = cls.get_structures_for_insights(
            ad_account_id,
            level,
            insight_ids,
            requested_structure_fields,
        )

        if summary and f"{level}_name" in summary[0]:
            summary[0][f"{level}_name"] = FacebookLevelPlural[level.upper()].value.capitalize()

        return insight_response, structures_response, next_page_cursor, summary

    @classmethod
    def _get_structure_master_data(
            cls,
            config,
            level: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            parameters: Dict = None,
            structure_fields: List[str] = None,
            requested_fields: List[FieldsMetadata] = None,
            page_size: int = 200,
            next_page_cursor: str = None,
    ):
        requested_structure_fields = [
            getattr(FieldsMetadata, entry) for entry in structure_fields if hasattr(FieldsMetadata, entry)
        ]
        facebook_structure_fields = [structure_field.facebook_fields for structure_field in requested_structure_fields]
        facebook_structure_fields = list(itertools.chain(*facebook_structure_fields))
        structures_filter = {"after": next_page_cursor, "limit": page_size, "filtering": parameters.get("filtering")}

        structures = get_sdk_structures(
            ad_account_id, Level[level.upper()], facebook_structure_fields, structures_filter
        )

        # iterate like this to avoid swapping page on the iterator
        structures_response = []
        for i in range(0, len(structures)):
            current_structure = structures[i].export_all_data()
            for field in facebook_structure_fields:
                if field not in current_structure:
                    current_structure[field] = None

            structures_response.append(current_structure)

        structure_ids = [x["id"] for x in structures_response if "id" in x]
        next_page_cursor = get_next_page_cursor(structures)

        if not parameters.get("filtering"):
            facebook_structure_key = LevelToFacebookIdKeyMapping[level.upper()].value.replace("_", ".")
            parameters["filtering"] = [
                json.dumps(create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, structure_ids))
            ]

        insight_response, _, _ = cls.get_insights_page(
            config,
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            level=level,
        )

        # Get collective summary (without filtering)
        _, _, summary = cls.get_insights_page(
            config,
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            level=Level.CAMPAIGN.value,
        )

        return insight_response, structures_response, next_page_cursor, summary

    @classmethod
    def get_reports_insights(
            cls,
            config,
            permanent_token: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            parameters: Dict = None,
            requested_fields: List[FieldsMetadata] = None,
            level: str = None,
    ) -> List[Dict]:
        report_insights_thread = 1
        insights_response = cls.get_insights_base(
            permanent_token=permanent_token,
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            thread=report_insights_thread,
            level=level,
        )

        if not insights_response:
            return []

        return insights_response[report_insights_thread][0]

    @classmethod
    def right_join_insights_and_structures(
            cls,
            level: str = None,
            requested_fields: List[FieldsMetadata] = None,
            insights: List[Dict] = None,
            structures: List[Dict] = None,
    ) -> List[Dict]:
        requested_fields_names = [field.name for field in requested_fields]
        structure_id_key = cls.__ids_keymap[level]["structure"]
        insight_id_key = cls.__ids_keymap[level]["insight"]

        structure_ids = {str(i[structure_id_key]) for i in structures}
        insights_ids = {i[insight_id_key] for i in insights}
        structures_only_ids = structure_ids - insights_ids

        active_structures = [
            {**insight, **structure}
            for structure in structures
            for insight in insights
            if str(structure[structure_id_key]) == insight[insight_id_key]
        ]

        empty_structure_dict = dict.fromkeys(requested_fields_names)
        inactive_structures = [
            {**empty_structure_dict, **structure}
            for structure in structures
            if str(structure[structure_id_key]) in structures_only_ids
        ]

        response = active_structures + inactive_structures

        return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=response)

    @classmethod
    def left_join_insights_and_structures(
            cls,
            level: str = None,
            requested_fields: List[FieldsMetadata] = None,
            structure_fields: List[str] = None,
            insights: List[Dict] = None,
            structures: List[Dict] = None,
    ) -> List[Dict]:
        structure_id_key = cls.__ids_keymap[level]["structure"]
        insight_id_key = cls.__ids_keymap[level]["insight"]
        requested_fields_names = [field.name for field in requested_fields]
        requested_fields_names = set(requested_fields_names + structure_fields)

        structure_ids = {str(i[structure_id_key]) for i in structures}
        insights_ids = {i[insight_id_key] for i in insights if insight_id_key in i}

        if not insights_ids:
            return insights

        insights_only_ids = insights_ids - structure_ids
        result = []
        empty_structure_dict = dict.fromkeys(requested_fields_names)

        for insight in insights:
            if insight[insight_id_key] in insights_only_ids:
                result.append({**empty_structure_dict, **insight})
                continue

            for structure in structures:
                if str(structure[structure_id_key]) == insight[insight_id_key]:
                    result.append({**insight, **structure})

        return cls.map_to_requested_fields(level=level, requested_fields=requested_fields, response=result)

    @classmethod
    def map_to_requested_fields(
            cls,
            level: str = None,
            requested_fields: List[FieldsMetadata] = None,
            response: List[Dict] = None,
    ) -> List[Dict]:
        sorted_fields = sorted([field.name for field in requested_fields])

        def f(entry):
            sorted_response = {**OrderedDict.fromkeys(sorted_fields), **OrderedDict(sorted(entry.items()))}
            for structure_key, insight_key in cls.__structure_insights_keymap[level].items():
                if isinstance(insight_key, list):
                    found = False
                    underscore = "_"
                    for key in insight_key:
                        if sorted_response.get(key) is not None and sorted_response.get(key) != 0:
                            value = sorted_response.pop(key)
                            if structure_key == FieldsMetadata.budget.name:
                                value = int(value) / 100
                            answer = f"{value} {key.split(underscore)[0]}"
                            sorted_response[structure_key] = answer
                            found = True
                            break
                    if not found:
                        sorted_response[structure_key] = insight_key[-1]
                elif sorted_response[structure_key]:
                    # TODO we need to change the id in the database to be strings
                    sorted_response[insight_key] = str(sorted_response.pop(structure_key, None))

            return sorted_response

        return list(map(f, response))

    @classmethod
    def build_get_structure_config(
            cls,
            permanent_token: str = None,
            level: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            filter_params: List[Dict] = None,
    ) -> GraphAPIClientBaseConfig:
        api_config = GraphAPIClientBaseConfig()
        api_config.try_partial_requests = True
        api_config.required_field = cls.__ids_keymap[level]["structure"]
        api_config.fields = fields
        api_config.request = GraphAPIRequestStructures(
            facebook_id=ad_account_id,
            business_owner_permanent_token=permanent_token,
            level=cls.__insights_to_structures_level_map[level],
            fields=fields,
            filter_params=filter_params,
        )

        return api_config

    @classmethod
    def build_get_insights_config(
            cls,
            permanent_token: str = None,
            ad_account_id: str = None,
            fields: List[str] = None,
            params: Dict = None,
            add_totals: bool = False,
            next_page_cursor: str = None,
            page_size: int = 200,
    ) -> GraphAPIClientBaseConfig:
        params["default_summary"] = add_totals

        api_config = GraphAPIClientBaseConfig()
        api_config.try_partial_requests = True
        api_config.required_field = cls.__ids_keymap[params["level"]]["insight"]
        api_config.fields = fields
        api_config.params = params
        api_config.request = GraphAPIRequestInsights(
            facebook_id=ad_account_id,
            business_owner_permanent_token=permanent_token,
            fields=fields,
            params=params,
            next_page_cursor=next_page_cursor,
        )
        api_config.page_size = page_size

        return api_config
