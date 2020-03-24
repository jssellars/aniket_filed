class MembershipFunction(object):
    _defaultBooleanFunctionThreshold = 0.5
    _defaultStepFunctionThreshold = 0.5

    def GetMembershipFunction(self, functionType):
        return getattr(self, functionType, 'LinearFunction')

    def BooleanFunction(self, value=0.0, *args):
        if not args:
            return int(value > self._defaultBooleanFunctionThreshold)
        
        return int(value > args[0])

    def LinearFunction(self, value=None, *args):
        parameters = args[0]
        return parameters[0] * value + parameters[1]

    def StepFunction(self, value=None, *args):
        if not args:
            return int(value > self._defaultStepFunctionThreshold)

        return int(value > args[0])


