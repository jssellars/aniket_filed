class JoinCondition:
    def __init__(self, compare_field=None, equal_to=None, target_field=None):
        self.compare_field = compare_field
        self.equal_to = equal_to
        self.target_field = target_field
