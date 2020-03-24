import copy
import json

import requests


class ColumnAggregator:
    sum = 1
    max = 2
    min = 3
    avg = 4


class LogicalOperator:
    and_ = 0
    or_ = 1


class WhereOperator:
    equals = 0
    greater_than = 1
    greater_than_or_equals = 2
    less_than = 3
    less_than_or_equal_with = 4
    not_equals = 5


class QueryBuilderHelper:
    _query_builder_endpoint = 'metadatas/query'

    @staticmethod
    def link_filter_blocks(parent_block, child_block):
        # Returns a new block where the two blocks are linked
        new_block = copy.deepcopy(parent_block)
        if 'ChildConditions' in new_block:
            new_block['ChildConditions'].append(child_block)
        else:
            new_block['ChildConditions'] = [child_block]
        return new_block

    @staticmethod
    def get_columns(dummy_object, aggregator=ColumnAggregator.max):
        # Gets columns based on the keys in the dummy object. To be implemented to also use properties potentially

        columns = []
        for attr in dummy_object.keys():
            columns.append({
                'name': attr,
                'Aggregator': aggregator
            })
        return columns

    def __init__(self, base_endpoint, table_name, authorization_token, table_schema='dbo'):
        self.table_name = table_name
        self._base_endpoint = base_endpoint
        self.table_schema = table_schema
        self._authorization_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authorization_token
        }

    def get_filter_block(self, filter_values, filter_column_name, operator=LogicalOperator.or_):
        # Creates a filter block to be used as a main whereCondition block or as a childConditionBlock
        return {
            'LogicalOperator': operator,
            'Conditions': list(map(lambda x: {
                'ColumnName': filter_column_name,
                'Operator': WhereOperator.equals,
                'Value': x
            }, filter_values))
        }

    def get_time_block(self, from_date, until_date, time_column_name):
        # Returns a WhereConditionBlock that filters based on the provided dates. DateFormat = DbDate = YYYY-MM-DD
        date_start_condition = {
            'ColumnName': time_column_name,
            'Operator': WhereOperator.greater_than,
            'Value': from_date
        }

        date_end_condition = {
            'ColumnName': time_column_name,
            'Operator': WhereOperator.less_than_or_equal_with,
            'Value': until_date
        }

        conditions = [date_start_condition, date_end_condition]
        return {
            'LogicalOperator': LogicalOperator.and_,
            'Conditions': conditions
        }

    def send_query(self, columns, dimensions, filter_block):
        query = self._build_query(columns, dimensions, filter_block)
        url = self._base_endpoint + self._query_builder_endpoint
        json_query = json.dumps(query)
        result = requests.post(url, data=json_query, headers=self._authorization_headers)
        return result

    def _build_query(self, columns, dimensions, filter_block):
        return {
            'TableSchema': self.table_schema,
            'TableName': self.table_name,
            'Columns': columns,
            'Dimensions': dimensions,
            'Where': filter_block
        }
