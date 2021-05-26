import copy
import itertools
import json
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative

from Core import mongo_adapter
from Core.Tools.QueryBuilder.QueryBuilderFacebookRequestParser import QueryBuilderFacebookRequestParser
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import (
    add_results_to_response,
    create_facebook_filter,
    get_next_page_cursor,
    get_sdk_insights_page,
    get_sdk_structures,
)
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields, FacebookParametersStrings
from Core.Web.FacebookGraphAPI.GraphAPIDomain.StructureStatusEnum import StructureStatusEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.GraphAPIInsightsMapper import GraphAPIInsightsMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import (
    FacebookLevelPlural,
    Level,
    LevelToFacebookIdKeyMapping,
)
from Core.Web.FacebookGraphAPI.Models.Field import Field as FacebookField
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Infrastructure.Domain.BudgetMessageEnum import BudgetMessageEnum
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestInsights import GraphAPIRequestInsights
from FacebookTuring.Infrastructure.GraphAPIRequests.GraphAPIRequestStructures import GraphAPIRequestStructures
from FacebookTuring.Infrastructure.PersistenceLayer.TuringMongoRepository import TuringMongoRepository

PAGE_SIZE = 100


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
    def get_insights_base(
        cls,
        ad_account_id: str = None,
        fields: List[str] = None,
        parameters: Dict = None,
        requested_fields: List[FieldsMetadata] = None,
        level: str = None,
    ) -> List[Dict]:

        ad_account = AdAccount(ad_account_id)
        insights = ad_account.get_insights(fields=fields, params=parameters)

        if not insights:
            return []

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
            add_results_to_response(level, insights_data, ad_account_id)
        insights_response = (
            GraphAPIInsightsMapper().map(requested_fields=requested_fields, response=insights_data)
            if insights_data
            else []
        )

        if not insights_response:
            return []

        return insights_response

    @classmethod
    def get_insights_page(
        cls,
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
                add_results_to_response(level, response, ad_account_id)
            insights_response = GraphAPIInsightsMapper().map(requested_fields, response) if response else []

            if not summary and not insights_response:
                summary = {field: None for field in requested_fields}

            summary_response = GraphAPIInsightsMapper().map(requested_fields, [summary]) if summary else []

            cls._add_level_name_to_summary(summary_response, level)

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
                FacebookParametersStrings.filtering: [
                    create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, insight_ids)
                ]
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
    def get_ag_grid_insights(
        cls,
        config,
        level: str = None,
        query: QueryBuilderFacebookRequestParser = None,
    ) -> Dict:

        ad_account_id = query.facebook_id
        fields = query.fields
        parameters = query.parameters
        structure_fields = query.structure_fields
        requested_fields = query.requested_columns
        next_page_cursor = query.next_page_cursor
        page_size = query.page_size
        has_delivery = query.has_delivery
        adset_not_null = query.adset_not_null

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

            if level == FieldsMetadata.adset.name and FieldsMetadata.campaign_name.name in structure_fields:
                for data in response:
                    campaign_id = data.get("campaign_id")
                    if not campaign_id:
                        break
                    data[FieldsMetadata.campaign_name.name] = cls._get_campaign_name(campaign_id)

            if level == FieldsMetadata.ad.name:

                for data in response:
                    ad_id = data.get("ad_id")
                    if not ad_id:
                        break
                    data[FieldsMetadata.ad_image.name] = cls._get_image_url_ad(ad_id)

            return {"nextPageCursor": next_page_cursor, "data": response, "summary": summary}

        if adset_not_null:
            insights, structures, next_page_cursor, summary = cls._get_structure_master_data_adset(
                config,
                level=level,
                ad_account_id=ad_account_id,
                fields=fields,
                parameters=parameters,
                structure_fields=structure_fields,
                requested_fields=requested_fields,
                page_size=page_size,
                next_page_cursor=next_page_cursor,
                insights_actions_filtering=query.action_filtering,
            )
        else:
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
                insights_actions_filtering=query.action_filtering,
            )

        response = cls.right_join_insights_and_structures(
            level=level,
            requested_fields=requested_fields,
            insights=insights,
            structures=structures,
        )

        return {"nextPageCursor": next_page_cursor, "data": response, "summary": summary}

    @classmethod
    def _get_image_url_ad(
            cls,
            ad_id: str
    ) -> str:
        fb_ad = Ad(ad_id)
        ad_creatives = fb_ad.get_ad_creatives(fields=[AdCreative.Field.image_hash, AdCreative.Field.image_url])

        ad_creative = ad_creatives.get_one()
        return cls._get_thumbnail_url(ad_creative)

    @classmethod
    def _get_thumbnail_url(
            cls,
            ad_creative: AdCreative
    ) -> str:
        fields = [AdCreative.Field.thumbnail_url]
        params = {
            'thumbnail_width': 50,
            'thumbnail_height': 50,
        }
        ad_creative.api_get(fields=fields, params=params)
        return ad_creative[AdCreative.Field.thumbnail_url]

    @classmethod
    def _get_campaign_name(
            cls,
            campaign_id: str
    ) -> str:
        if not campaign_id:
            return ""
        fb_campaign = Campaign(campaign_id)
        fb_campaign.api_get(fields=[Campaign.Field.name])
        return fb_campaign._json[Campaign.Field.name]

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

        return insight_response, structures_response, next_page_cursor, summary

    """
    This is same as _get_structure_master_data() except
    this only returns campaigns with adsets
    """
    @classmethod
    def _get_structure_master_data_adset(
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
        insights_actions_filtering: Dict = None,
    ):
        requested_structure_fields = [
            getattr(FieldsMetadata, entry) for entry in structure_fields if hasattr(FieldsMetadata, entry)
        ]
        facebook_structure_fields = [structure_field.facebook_fields for structure_field in requested_structure_fields]
        facebook_structure_fields = list(itertools.chain(*facebook_structure_fields))
        structures_filter = {
            "after": next_page_cursor,
            "limit": page_size,
            FacebookParametersStrings.filtering: parameters.get(FacebookParametersStrings.filtering, []),
        }

        structures = get_sdk_structures(
            ad_account_id, Level[level.upper()], facebook_structure_fields, structures_filter
        )

        structures_response = []
        if level == Level.CAMPAIGN.value:
            adsets = get_sdk_structures(
                ad_account_id, Level.ADSET, [AdSet.Field.campaign_id], None
            )
            campaign_ids = set()
            for adset in adsets:
                if adset[AdSet.Field.campaign_id] not in campaign_ids:
                    campaign_ids.add(adset[AdSet.Field.campaign_id])
            while len(structures_response) < len(structures):
                current_structure = structures.next().export_all_data()
                for field in facebook_structure_fields:
                    if field not in current_structure:
                        current_structure[field] = None

                if current_structure[Campaign.Field.id] in campaign_ids:
                    structures_response.append(current_structure)
        else:
            # iterate like this to avoid swapping page on the iterator
            for i in range(0, len(structures)):
                current_structure = structures[i].export_all_data()
                for field in facebook_structure_fields:
                    if field not in current_structure:
                        current_structure[field] = None

                structures_response.append(current_structure)

        structures_response = GraphAPIInsightsMapper().map(requested_structure_fields, structures_response)

        structure_ids = [x["id"] for x in structures_response if "id" in x]
        next_page_cursor = get_next_page_cursor(structures)

        facebook_structure_key = LevelToFacebookIdKeyMapping[level.upper()].value.replace("_", ".")
        filtering = [create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, structure_ids)]
        if insights_actions_filtering:
            filtering.append(insights_actions_filtering)
        parameters[FacebookParametersStrings.filtering] = filtering

        # The after cursor is valid only for structures, not insights on this flow
        parameters.pop("after", None)

        insight_response, _, summary = cls.get_insights_page(
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            level=level,
        )

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
        insights_actions_filtering: Dict = None,
    ):
        requested_structure_fields = [
            getattr(FieldsMetadata, entry) for entry in structure_fields if hasattr(FieldsMetadata, entry)
        ]
        facebook_structure_fields = [structure_field.facebook_fields for structure_field in requested_structure_fields]
        facebook_structure_fields = list(itertools.chain(*facebook_structure_fields))
        structures_filter = {
            "after": next_page_cursor,
            "limit": page_size,
            FacebookParametersStrings.filtering: parameters.get(FacebookParametersStrings.filtering, []),
        }

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

        structures_response = GraphAPIInsightsMapper().map(requested_structure_fields, structures_response)

        structure_ids = [x["id"] for x in structures_response if "id" in x]
        next_page_cursor = get_next_page_cursor(structures)

        facebook_structure_key = LevelToFacebookIdKeyMapping[level.upper()].value.replace("_", ".")
        filtering = [create_facebook_filter(facebook_structure_key, AgGridFacebookOperator.IN, structure_ids)]
        if insights_actions_filtering:
            filtering.append(insights_actions_filtering)
        parameters[FacebookParametersStrings.filtering] = filtering

        # The after cursor is valid only for structures, not insights on this flow
        parameters.pop("after", None)

        insight_response, _, summary = cls.get_insights_page(
            ad_account_id=ad_account_id,
            fields=fields,
            parameters=parameters,
            requested_fields=requested_fields,
            level=level,
        )

        return insight_response, structures_response, next_page_cursor, summary

    @classmethod
    def right_join_insights_and_structures(
        cls,
        level: str = None,
        requested_fields: List[FieldsMetadata] = None,
        insights: List[Dict] = None,
        structures: List[Dict] = None,
    ) -> List[Dict]:
        requested_fields_names = [field.name for field in requested_fields]
        if FieldsMetadata.result_type.name not in requested_fields_names:
            requested_fields_names.append(FieldsMetadata.result_type.name)

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
                orphan_insight = {**empty_structure_dict, **insight}
                # If the id is present in insights but not in structures, that means that the structures was removed
                # since the insights API take a bit longer to remove deleted structures
                if FacebookMiscFields.status in orphan_insight:
                    orphan_insight[FacebookMiscFields.status] = StructureStatusEnum.REMOVED.name.title()

                if FacebookMiscFields.effective_status in orphan_insight:
                    orphan_insight[FacebookMiscFields.effective_status] = StructureStatusEnum.REMOVED.name.title()

                result.append(orphan_insight)
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

    @classmethod
    def _add_level_name_to_summary(self, summary: List[Dict], level: str):
        if summary and f"{level}_name" in summary[0]:
            summary[0][f"{level}_name"] = FacebookLevelPlural[level.upper()].value.capitalize()
