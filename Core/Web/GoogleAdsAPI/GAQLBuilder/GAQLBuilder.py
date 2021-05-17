from typing import List, Union

from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType


class WhereBuilder:
    def __init__(self, where_conditions):
        self.where_condition_queries = []
        self.field = None
        self.value = None
        self.operator = None

        self.operators = {
            "EQUAL": self.equal,
            "NOT_EQUAL": self.not_equal,
            "LESS_THAN": self.less_than,
            "LESS_THAN_OR_EQUAL": self.less_than_or_equal,
            "GREATER_THAN": self.greater_than,
            "GREATER_THAN_OR_EQUAL": self.greater_than_or_equal,
            "IN": self.in_,
            "NOT_IN": self.not_in,
            "BETWEEN": self.between,
            "DURING": self.during,
        }

        self.parse_operator(where_conditions)

    def parse_operator(self, where_conditions):
        for condition in where_conditions:
            self.field = condition.name
            self.value = condition.value
            self.operator = condition.operator.value
            operator_method = self.operators.get(condition.operator.name)
            self.where_condition_queries.append(operator_method())

    def equal(self):
        return self._parse_single_value_condition()

    def not_equal(self):
        return self._parse_single_value_condition()

    def less_than(self):
        return self._parse_single_value_condition()

    def less_than_or_equal(self):
        return self._parse_single_value_condition()

    def greater_than(self):
        return self._parse_single_value_condition()

    def greater_than_or_equal(self):
        return self._parse_single_value_condition()

    def in_(self):
        self.value = ['"%s"' % value if isinstance(value, str) else str(value) for value in self.value]
        return "%s %s (%s)" % (self.field, self.operator, ", ".join(self.value))

    def not_in(self):
        self.value = ['"%s"' % value if isinstance(value, str) else str(value) for value in self.value]
        return "%s %s (%s)" % (self.field, self.operator, ", ".join(self.value))

    def between(self):
        return f"{self.field} {self.operator} '{self.value[0]}' AND '{self.value[1]}'"

    def during(self):
        return f"{self.field} {self.operator} {self.value}"

    def _parse_single_value_condition(self):
        if isinstance(self.value, list):
            self.value = self.value[0]

        return f"{self.field} {self.operator} {self.value}"

    def _parse_multiple_value_condition(self):
        self.value = ['"%s"' % value if isinstance(value, str) else str(value) for value in self.value]
        return "%s %s [%s]" % (self.field, self.operator, ", ".join(self.value))


class _QueryBuilder:
    def __init__(self, query_builder=None):
        if query_builder is None:
            self.where_builders = []
        else:
            try:
                self.where_builders = list(query_builder.where_builders)
            except (AttributeError, TypeError):
                raise ValueError("The passed query builder should be of the QueryBuilder type.")

    def Select(self, *fields):
        raise NotImplementedError("You must subclass _QueryBuilder.")


class GAQLBuilder:
    def __init__(self):
        self.where_builders = []
        self.select_fields = []
        self.from_resource = None
        self.order = None
        self.limit = None

    @staticmethod
    def map_attribute(field_type: GoogleFieldType, resource_type: GoogleResourceType = None):
        if field_type == GoogleFieldType.ATTRIBUTE:
            if resource_type:
                return resource_type.value
            else:
                raise ValueError("resource type is not present for field with field type of attribute")
        else:
            return field_type.value

    def select_(self, google_fields: List[GoogleField]):
        for field in google_fields:
            attribute = GAQLBuilder.map_attribute(field.field_type, field.resource_type)
            self.select_fields.append(".".join([attribute, field.field_name]))

        return self

    def from_(self, resource_type: Union[GoogleResourceType, str]):
        if type(resource_type) == str:
            self.from_resource = resource_type
        else:
            self.from_resource = resource_type.value
        return self

    def where_(self, f):
        where_builder = WhereBuilder(f)
        self.where_builders.extend(where_builder.where_condition_queries)
        return self

    def order_by_(self, field, ascending=True):
        self.order = f" ORDER BY {field} {'ASC' if ascending else 'DESC'}"
        return self

    def limit_(self, limit_value):
        self.limit = f" LIMIT {limit_value}"
        return self

    def build_(self):
        parts = ["SELECT ", (", ".join(self.select_fields))]
        parts.extend([" FROM ", self.from_resource])

        if len(self.where_builders) > 0:
            parts.append(f" WHERE {' AND '.join([clause for clause in self.where_builders])}")

        if self.order:
            parts.append(self.order)
        if self.limit:
            parts.append(self.limit)

        query = "".join(parts)
        return query
