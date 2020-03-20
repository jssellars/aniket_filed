class SyncJobDefinitionBase:

    fields = []

    @classmethod
    def to_fields_list(cls):
        return [field.field_name for field in cls.fields]