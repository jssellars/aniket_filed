class LinguisticVariable(object):

    def __init__(self, name=None, levels=None, max_value=None):
        self.name = name
        self.levels = levels
        self.max_value = max_value

    def generate_membership_functions_by_level(self, level_name=None, step=0.1):
        return self.levels[level_name].get_all_level_values(step=step)

    def get_membership_value(self, level_name=None, value=None):
        return self.levels[level_name].evaluate_membership(value)
