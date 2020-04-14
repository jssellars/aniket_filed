from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdLevel import RuleBasedOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdSetLevel import RuleBasedOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationCampaignLevel import RuleBasedOptimizationCampaignLevel
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum


class AlgorithmsFactory:

    # TODO: use defaultdict
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleBasedOptimizationCampaignLevel,
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): RuleBasedOptimizationAdSetLevel,
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleBasedOptimizationAdLevel
    }

    @classmethod
    def factory(cls,
                algorithm_type,
                level: LevelEnum = None):
        algorithm = cls.__factory[algorithm_type, level]()
        return algorithm
