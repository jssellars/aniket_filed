class GoogleField:
    def __init__(self, name=None, field_name=None, fields=None, field_type=None, conversion_function=None, required_fields=None):
        self.name = name
        self.field_name = field_name
        self.fields = fields
        self.field_type = field_type
        self.conversion_function = conversion_function
        self.required_fields = required_fields
