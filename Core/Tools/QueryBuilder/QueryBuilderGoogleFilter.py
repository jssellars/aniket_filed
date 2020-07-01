from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import QueryBuilderLogicalOperator


class QueryBuilderGoogleFilter:

    def __init__(self, condition, entry):
        self.field = condition.field_name
        self.operator = QueryBuilderLogicalOperator(entry.Operator)
        self.value = entry.Value
