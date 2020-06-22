import typing

from FacebookTuring.Infrastructure.Domain.QueryBuilder.InsightsQuery import InsightsQuerySort, InsightsQuerySortEnum, \
    InsightsQuery, InsightsQueryDimension, InsightsQueryColumn, InsightsQueryCondition
from marshmallow import EXCLUDE, fields, post_load

from Core.Tools.Mapper.MapperBase import MapperBase
from FacebookTuring.Infrastructure.Domain.FiledFacebookInsightsTableEnum import \
    FiledFacebookInsightsTableEnum


def is_list(x: typing.Any) -> bool:
    return isinstance(x, list)


def is_dict(x: typing.Any) -> bool:
    return isinstance(x, dict)


def is_leaf(x: typing.Dict, leaf_keys: typing.List[typing.AnyStr] = None) -> bool:
    if not isinstance(x, dict):
        return False
    return list(x.keys()) == leaf_keys


def find_all_where_conditions(entry: typing.Dict = None) -> typing.List[InsightsQueryCondition]:
    leaves = []

    def find_all_conditions(entry):
        if is_leaf(entry):
            leaves.append(InsightsQueryCondition(**entry))
        elif is_dict(entry):
            for key, value in entry.items():
                if (is_list(value) or is_dict(value)) and not is_leaf(value):
                    find_all_conditions(value)
                elif is_leaf(value):
                    leaves.append(InsightsQueryCondition(**value))
                else:
                    continue
        elif is_list(entry):
            for element in entry:
                if (is_list(element) or is_dict(element)) and not is_leaf(element):
                    find_all_conditions(element)
                elif is_leaf(element):
                    leaves.append(InsightsQueryCondition(**element))
                else:
                    continue

    find_all_conditions(entry)
    return leaves


class AdsManagerInsightsCommandMapping(MapperBase):
    query = fields.Dict()
    page = fields.String()
    sort = fields.List(dict)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def build(self, data: typing.Any, **kwargs):
        # map query
        raw_query = data.pop('query', None)
        if raw_query:
            query = InsightsQuery()
            query.table_name = FiledFacebookInsightsTableEnum(raw_query['table_name'])
            query.columns = [InsightsQueryColumn(**entry) for entry in raw_query['columns']]
            query.dimensions = [InsightsQueryDimension(**entry) for entry in raw_query['dimensions']]
            query.conditions = find_all_where_conditions(raw_query.pop('where', {}))

        # map sort
        sort_query = data.pop('sort', None)
        if sort_query:
            data['sort'] = [InsightsQuerySort(dimension=entry['dimension'],
                                              order=InsightsQuerySortEnum(entry['order']))
                            for entry in sort_query]

        if self._target:
            return self._target(**data)
        else:
            return data
