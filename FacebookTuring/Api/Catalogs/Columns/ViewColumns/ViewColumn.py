class ViewColumn:

    def __init__(self, id=None, display_name=None, primary_value=None, secondary_value=None, type_id=None,
                 actions=None, category_id=None, width=50, is_fixed=False):
        self.id = id
        self.display_name = display_name  # string
        self.primary_value = primary_value  # ColumnMetadata
        self.secondary_value = secondary_value  # ColumnMetadata
        self.type_id = type_id  # ViewColumnTypeEnum
        self.actions = actions  # List of actions ["editName", "changeState"] ( context menu per cell )
        self.category_id = category_id  # ViewColumnCategoryEnum -> id
        self.width = width
        self.is_fixed = is_fixed
