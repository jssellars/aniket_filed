from collections.abc import Mapping

from Core.Tools.Misc.ClassGenerator import ClassGenerator
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Tools.Misc.ObjectManipulators import extract_class_attributes


class QueryBuilderColumn(ClassGenerator):
    Name = None
    Aggregator = None


class QueryBuilderDimension(ClassGenerator):
    GroupColumnName = None


class Condition(ClassGenerator):
    ColumnName = None
    Operator = None
    Value = None

    @classmethod
    def has_same_parameters(cls, other):
        if not isinstance(other, Mapping):
            return False

        return list(other.keys()) == extract_class_attributes(cls)


class FiledFacebookInsightsTableName(EnumerationBase):
    ACCOUNT = 'vAdAccountInsights'
    CAMPAIGN = 'vCampaignInsights'
    ADSET = 'vAdSetInsights'
    AD = 'vAdInsights'


class QueryBuilderRequestMapper:
    TableName = None
    Columns = None
    Dimensions = None
    Where = None

    table_name = FiledFacebookInsightsTableName

    def __init__(self, query_builder_request):
        self.TableName = query_builder_request['TableName']
        self.Columns = [QueryBuilderColumn(column) for column in query_builder_request['Columns']]
        self.Dimensions = [QueryBuilderDimension(dimension) for dimension in query_builder_request['Dimensions']]
        self.Conditions = self.find_all_where_conditions(query_builder_request['Where'])

    def get_level(self):
        return self.table_name.get_by_value(self.TableName).lower()

    @staticmethod
    def find_all_where_conditions(entry):
        is_list = lambda x: isinstance(x, list)
        is_dict = lambda x: isinstance(x, Mapping)
        is_leaf = lambda x: Condition.has_same_parameters(x)

        leaves = []

        def find_all_conditions(entry):
            if is_leaf(entry):
                leaves.append(Condition(entry))
            elif is_dict(entry):
                for key, value in entry.items():
                    if (is_list(value) or is_dict(value)) and not is_leaf(value):
                        find_all_conditions(value)
                    elif is_leaf(value):
                        leaves.append(Condition(value))
                    else:
                        continue
            elif is_list(entry):
                for element in entry:
                    if (is_list(element) or is_dict(element)) and not is_leaf(element):
                        find_all_conditions(element)
                    elif is_leaf(element):
                        leaves.append(Condition(element))
                    else:
                        continue

        find_all_conditions(entry)
        return leaves
