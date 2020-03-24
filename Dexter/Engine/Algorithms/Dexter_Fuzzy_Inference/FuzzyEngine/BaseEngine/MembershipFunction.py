class MembershipFunction(object):
    _default_boolean_function_threshold = 0.5
    _default_step_function_threshold = 0.5

    def get_membership_function(self, function_type):
        return getattr(self, function_type, 'linear_function')

    def boolean_function(self, value=0.0, *args):
        if not args:
            return int(value > self._default_boolean_function_threshold)

        return int(value > args[0])

    def linear_function(self, value=None, *args):
        parameters = args[0]
        return parameters[0] * value + parameters[1]

    def step_function(self, value=None, *args):
        if not args:
            return int(value > self._default_step_function_threshold)

        return int(value > args[0])
