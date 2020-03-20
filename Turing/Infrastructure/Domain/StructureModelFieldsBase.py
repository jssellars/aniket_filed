class StructureModelFieldBase:

    structure_fields = []
    insights_fields = []

    @classmethod
    def get_structure_fields(cls):
        return [field.field_name for field in cls.structure_fields]

    @classmethod
    def get_insights_fields(cls):
        return [field.field_name for field in cls.insights_fields]

    @classmethod
    def get_fields(cls):
        structure_fields = cls.get_structure_fields()
        insights_fields = cls.get_insights_fields()
        return [*structure_fields, *insights_fields]