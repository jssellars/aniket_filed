class BreakdownsEnumeration:

    def __init__(self, id=None, column_name=None, display_name=None):
        self.id = id
        self.column_name = column_name
        self.display_name = display_name

    def to_string(self):
        return self.column_name

