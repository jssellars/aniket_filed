class LinguisticVariable(object):

    def __init__(self, name=None, levels=None, maxValue=None):
        self.name = name
        self.levels = levels
        self.maxValue = maxValue

    def GenerateMembershipFunctionsByLevel(self, levelName=None, step=0.1):
        return self.levels[levelName].GetAllLevelValues(step=step)

    def GetMembershipValue(self, levelName=None, value=None):
        return self.levels[levelName].EvaluateMembership(value)
        
            
    

