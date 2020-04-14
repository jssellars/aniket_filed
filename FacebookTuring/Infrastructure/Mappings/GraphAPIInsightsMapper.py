from functools import reduce
from itertools import repeat
from operator import itemgetter, getitem

from numpy import float

from FacebookTuring.Infrastructure.Mappings.ObjectiveToResultsMapper import ObjectiveToResultsMapper
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class GraphAPIInsightsMapper:

    action_value_mapper_factory = {
        FieldsMetadata.results.name: ObjectiveToResultsMapper,
        FieldsMetadata.cost_per_result.name: ObjectiveToResultsMapper
    }

    ids_map = [FieldsMetadata.ad_account_id.name,
               FieldsMetadata.campaign_id.name,
               FieldsMetadata.adset_id.name,
               FieldsMetadata.ad_id.name]

    @classmethod
    def mappers_factory(cls):
        mappers_factory = {
            FieldType.SIMPLE: cls.map_simple,
            FieldType.NESTED: cls.map_nested,
            FieldType.TOTAL: cls.map_total,
            FieldType.COST: cls.map_cost,
            FieldType.BREAKDOWN: cls.map_breakdown,
            FieldType.ACTION_BREAKDOWN: cls.map_simple,
            FieldType.TIME_BREAKDOWN: cls.map_time_breakdown,
            FieldType.STRUCTURE: cls.map_simple
        }

        return mappers_factory

    def map(self, requested_fields, response):
        if not response:
            return []
        return self.map_response(requested_fields, response)

    @classmethod
    def map_response(cls, requested_fields, response):
        # extract action breakdowns from each NESTED response and create 1 insights entry per action BREAKDOWN value
        action_breakdowns = [field for field in requested_fields if field.field_type == FieldType.ACTION_BREAKDOWN and field.name != FieldsMetadata.action_type.name]

        if action_breakdowns:
            nested_fields = [field for field in requested_fields if field.field_type == FieldType.NESTED]
            expanded_response = [cls.map_action_breakdown(nested_fields, action_breakdown, entry) for action_breakdown in action_breakdowns for entry in response]
            mapped_response = [r for resp in expanded_response for r in resp]
        else:
            mapped_response = response

        mapped_response = [{field.name: getitem(cls.mappers_factory(), field.field_type)(field, entry)
                            for field in requested_fields}
                           for entry in mapped_response]

        return mapped_response

    @classmethod
    def passer(cls, *args, **kwargs):
        pass

    @classmethod
    def reducer(cls, source):
        try:
            result = reduce(lambda x, y: float(x) + float(y) if x and y else None, source)
            return result
        except ValueError:
            return None
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()

    @classmethod
    def __is_convertible(cls, field):
        return field.field_name not in cls.ids_map and field.field_type not in [FieldType.BREAKDOWN, FieldType.ACTION_BREAKDOWN, FieldType.TIME_BREAKDOWN]

    @classmethod
    def map_simple(cls, field, response):

        if field.field_type != FieldType.STRUCTURE:
            try:
                return float(response[field.field_name]) if cls.__is_convertible(field) else response[field.field_name]
            except ValueError:
                return response[field.field_name]
            except KeyError:
                return response.get(field.field_name)
            except Exception as e:
                print(e)

    @classmethod
    def map_nested(cls, field, response):
        try:
            if field.name in cls.action_value_mapper_factory.keys():
                field.action_field_name_value = cls.action_value_mapper_factory[field.name].map(response)

            field_name_values = list(map(itemgetter(field.action_field_name_key), response[field.field_name]))

            fields = list(filter(lambda x: x.find(field.action_field_name_value) > -1, field_name_values))

            field_objects = list(filter(lambda x: x[field.action_field_name_key] in fields, response[field.field_name]))

            matching_fields_values = list(map(itemgetter(field.action_field_value_key), field_objects))

            return float(matching_fields_values[0]) if matching_fields_values else None
        except Exception as e:
            print(e)
            # todo: log errors

    @classmethod
    def map_total(cls, field, response):
        try:
            values = cls.map_nested(field, response)
            return reduce(lambda x, y: float(x) + float(y), values) if isinstance(values, list) else values
        except Exception as e:
            print(e)

    @classmethod
    def map_cost(cls, field, response):
        if field.name == FieldsMetadata.cost_per_1000_people_reached.name:
            return cls.map_cost_per_1000_people_reached(field, response)
        else:
            return cls.map_cost_per_action(field, response)

    @classmethod
    def map_cost_per_action(cls, field, response):
        try:
            action_field_value_total = cls.map_total(field, response)
            cost_per_action = float(response[field.spend_field_name]) / action_field_value_total if action_field_value_total else None
            return cost_per_action if action_field_value_total else None
        except Exception as e:
            print(e)

    @classmethod
    def map_cost_per_1000_people_reached(cls, field, response):
        try:
            return response[FieldsMetadata.social_spend.name] / response[FieldsMetadata.reach.name] * 1000
        except Exception as e:
            print(e)

    @classmethod
    def map_breakdown(cls, field, response):
        try:
            if isinstance(field.field_name, list):
                return ", ".join([response[field_key] for field_key in field.field_name])
            else:
                return response[field.field_name]
        except Exception as e:
            print(e)

    @classmethod
    def map_time_breakdown(cls, field, response):
        try:
            return response[field.Fields[0]] + " - " + response[field.Fields[1]]
        except Exception as e:
            print(e)

    @classmethod
    def map_action_breakdown(cls, nested_fields, action_breakdown_field, response):
        return [{**response, **action_object} for nested_field in nested_fields for action_object in cls.__extract_action_object(nested_field, action_breakdown_field, response)]

    @classmethod
    def __extract_action_object(cls, nested_field, action_breakdown_field, response):

        try:
            action_breakdowns = list(
                map(cls.__build_action_breakdown_entry,
                    response[nested_field.field_name],
                    repeat(action_breakdown_field.action_field_name_key, len(response[nested_field.field_name]))
                    )
            )

            return list({v[action_breakdown_field.action_field_name_key]: v for v in action_breakdowns}.values())
        except Exception as e:
            # todo: log errors
            print(e)
            return []

    @classmethod
    def __build_action_breakdown_entry(cls, action_object, action_breakdown_key):
        return {
            action_breakdown_key: action_object[action_breakdown_key]
        }
