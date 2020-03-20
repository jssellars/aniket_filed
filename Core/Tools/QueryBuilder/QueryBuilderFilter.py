from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import QueryBuilderLogicalOperator


class QueryBuilderFilter:

    def __init__(self, condition):
        self.field = condition.ColumnName
        self.operator = QueryBuilderLogicalOperator(condition.Operator)
        self.value = condition.Value

    def AsDict(self):
        filter_dict = {
            'field': self.field,
            'operator': self.operator,
            'value': self.value
        }
        return filter_dict
