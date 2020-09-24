import functools
import operator


class StructureModelFieldBase:
    structure_fields = []
    insights_fields = []
    required_structure_fields = []

    @classmethod
    def get_structure_fields(cls):
        fields = [field.facebook_fields for field in cls.structure_fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return list(set(fields))

    @classmethod
    def get_insights_fields(cls):
        fields = [field.facebook_fields for field in cls.insights_fields]
        fields = functools.reduce(operator.iconcat, fields, [])
        return fields

    @classmethod
    def get_fields(cls):
        structure_fields = cls.get_structure_fields()
        insights_fields = cls.get_insights_fields()
        return [*structure_fields, *insights_fields]

    @classmethod
    def get_required_structure_fields(cls):
        fields = [field.name if hasattr(field, 'name') else field for field in cls.required_structure_fields]
        return list(set(fields))
